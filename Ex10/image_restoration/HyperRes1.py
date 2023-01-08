"""
Asaf Keler, Ariel Yifee
https://arxiv.org/pdf/2206.05970.pdf
Shai Aharon, Gil Ben-Artzi
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from parallel_utils1 import ModuleParallel, convParallel
from torch.nn.common_types import _size_2_t
import logging

# create and configure logger
LOG_FORMAT = "%(levelname)s, Time: %(asctime)s, line: %(lineno)d- %(message)s"
logging.basicConfig(filename='logger.log', level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()

class HyperConv(nn.Module):
    """
    is a custom implementation of a 2D convolutional layer that can use different weights at different resolutions.
    It has a forward method that takes in a list of tensors x and returns a list of convolved tensors.
    It does this by creating a linear layer that takes in a single scalar value representing the resolution and outputs the weights for each convolution at that resolution.
    These weights are then used to compute the convolutions for each input tensor in x.
    """
    def __init__(self,
                 levels,
                 in_channels: int,
                 out_channels: int,
                 kernel_size: _size_2_t,
                 stride: _size_2_t = 1,
                 padding: _size_2_t = 0,
                 dilation: _size_2_t = 1,
                 groups: int = 1,
                 bias: bool = True,
                 padding_mode: str = 'zeros',
                 device='cpu'):
        logger.info('initialize HyperConv')
        super(HyperConv, self).__init__()

        self.levels = levels
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.groups = groups
        self.bias = bias
        self.padding_mode = padding_mode
        self.device = device

        self.fc = nn.Linear(1, self.out_channels *
                            (self.in_channels * (kernel_size * kernel_size) + int(self.bias)))
        self.w_len = self.in_channels * \
                     (self.out_channels * (self.kernel_size * self.kernel_size))
        logger.debug('finish initialize HyperConv')

    def forward(self, x):
        out = [None for _ in range(len(self.levels))]
        scale = [torch.tensor([l]).type(torch.float32).to(
            self.device) for l in self.levels]

        for i in range(len(scale)):
            tot_weights = self.fc(scale[i])
            weights = tot_weights[:self.w_len].reshape(
                self.out_channels, self.in_channels, self.kernel_size, self.kernel_size)
            bias = tot_weights[self.w_len:]
            bias = bias if self.bias else None
            out[i] = F.conv2d(x[i], weights, bias,
                              stride=self.stride,
                              padding=self.padding,
                              dilation=self.dilation
                              )

        return out

class ResBlockMeta(nn.Module):
    """
    represents a residual block with a meta network.
    """
    def __init__(self, levels, ker_n, inplanes, deivce='cpu', bias=True):
        logger.info('initialize ResBlockMeta')
        super(ResBlockMeta, self).__init__()
        # meta network
        self.bias = bias
        self.device = deivce
        self.levels = levels
        self.inplanes = inplanes
        self.ker_n = ker_n

        self.hy_conv1 = HyperConv(self.levels, ker_n, inplanes, kernel_size=3, stride=1, padding=1, device=self.device)
        self.hy_conv2 = HyperConv(self.levels, ker_n, ker_n, kernel_size=3, stride=1, padding=1, device=self.device)

        self.relu = ModuleParallel(nn.ReLU(inplace=True)) #allows running a PyTorch module in parallel over a list of inputs.
        logger.debug('finish initialize ResBlockMeta')

    def forward(self, x):
        identity = x
        out = self.hy_conv1(x)
        out = self.relu(out)
        out = self.hy_conv2(out)

        out = [out_i + in_i for out_i, in_i in zip(out, identity)]
        return out

class HyperRes(nn.Module):
    _doc_ = r"""a hyper network that learns to generate the filter weights of an image restoration network conditionally based on the required
    restoration level, given as an input parameter.
    To ensure an efficient representation at inference time, we constrain the kernels corresponding to the different levels to be identical
    up to a scaling factor and learn only the weights basis vectors.
    In order to achieve the desired accuracy and continuity over any predefined range we train our model to generate multiple restoration networks
    simultaneously; each is optimized to a different degradation level.
    """ + r"""

    Args:
        meta_blocks (int): Number of Meta Blocks
        level (int, optional): A list of corruptions levels to train on. Default: None
        device (str, optional): Device to run on,[cpu,cuda,cuda:0..]. Default: 'cpu'
        bias (bool, optional): If True, adds a learnable bias to the output. Default: True
        gray (bool, optional): Number of channels in the input image. Default: False
        norm_factor (bool, optional): The normalization factor for the distortion levels. Default: 255
    """ + r"""

    Output : Tensor
    """ + r"""

    Examples:

        >>> model = HyperRes(meta_blocks=16, level=[15], device='cpu', bias=True, gray=False, norm_factor=255)

    .. _Hyper-Res:
        https://arxiv.org/pdf/2206.05970.pdf
    """
    def __init__(self, meta_blocks, level=None, device='cpu', bias=True, gray=False, norm_factor=255):
        logger.info('initialize HyperRes')
        super(HyperRes, self).__init__()

        self.level =  level
        if min(self.level) >= 1:
            self.level = [x / norm_factor for x in self.level]

        self.device = device
        self.inplanes = 64
        self.outplanes = 64
        self.dilation = 1
        self.num_parallel = len(self.level)

        self.channels = 1 if gray else 3
        #performs a 2D convolution over a list of tensors.
        self.conv1 = convParallel(self.channels, self.inplanes, kernel_size=3, stride=2, groups=1, padding=1, bias=True)

        self.res_blocks_meta = []
        self.res_blocks_meta.append(ModuleParallel(nn.Identity()))
        for idx in range(meta_blocks):
            self.res_blocks_meta.append(
                ResBlockMeta(self.level, self.inplanes, self.outplanes, deivce=self.device, bias=bias))
        self.res_blocks_meta = nn.Sequential(*self.res_blocks_meta)

        self.conv2 = convParallel(self.inplanes, self.inplanes, kernel_size=3, stride=1, groups=1, padding=1, bias=True)
        self.conv3 = convParallel(self.inplanes, self.inplanes * (2 ** 2), kernel_size=3, stride=1, groups=1, padding=1,
                                  bias=True)

        self.pix_shuff = ModuleParallel(nn.PixelShuffle(2))
        self.relu3 = ModuleParallel(nn.ReLU(inplace=True))

        self.conv4 = convParallel(self.inplanes, self.inplanes, kernel_size=3, stride=1, groups=1, padding=1, bias=True)
        self.relu4 = ModuleParallel(nn.ReLU(inplace=True))
        self.conv5 = convParallel(self.inplanes, self.channels, kernel_size=3, stride=1, groups=1, padding=1, bias=True)
        logger.debug('finish initialize HyperRes')

    def forward(self, x):
        conv1_out = self.conv1(x)

        x = self.res_blocks_meta(conv1_out)

        x = self.conv2(x)
        x = [c_out + res_out for c_out, res_out in zip(conv1_out, x)]  # Skip connection
        x = self.conv3(x)
        x = self.pix_shuff(x)
        x = self.relu3(x)

        x = self.conv4(x)
        x = self.relu4(x)
        out = self.conv5(x)

        return out

    def setLevel(self, level):
        if not isinstance(level, list):
            level = [level]
        if max(level) >= 1:
            level = [x / 255 for x in level]

        self.level = level
        for k, v in self.res_blocks_meta._modules.items():
            if isinstance(v,ResBlockMeta):
                for k1, v1 in v._modules.items():
                    if hasattr(v1, 'levels'):
                        v1.levels = level
