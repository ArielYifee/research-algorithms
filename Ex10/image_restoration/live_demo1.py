import os

import cv2
import argparse

import torch
import numpy as np
from HyperRes1 import HyperRes
from NoiseNet import NoiseNet
from CommonTools import modcrop, ToTensor, calculate_psnr, postProcessForStats

###### --input test\Set5 --checkpoint pre_trained\noise_net_latest.pth
##### --input test\Set5 --checkpoint pre_trained\Dej\model_best.pth

# Global variables
alpha_slider_max = 150  # Maximum value for the slider controlling noise level
title_window = 'MoNet LiveDemo' # Title for the window displaying the image
min_v = 15 # Minimum value for random noise level
max_v = 75  # Maximum value for random noise level

device = "cuda"


# Function to add noise to an image
def addNoise(src1, noise=None):
    global title_window
    sig = np.random.randint(0, 100) # Generate random noise level

    # If a specific noise level is specified, use it
    if noise:
        sig = noise

    # Update window title with noise level
    title_window = "Noise Sigma {}".format(sig)

    # Add noise to image and return it
    ret_img = src1 + np.random.normal(0, sig / 255, src1.shape)
    return np.clip(ret_img, 0, 1), sig


# Function to add super-resolution to an image
def addSR(src1, lvl=None):
    global title_window

    # If no specific SR factor is specified, generate a random one
    if not lvl:
        lvl = np.random.randint(2, 6)

    # Update window title with SR factor
    title_window = "SR Factor {}".format(lvl)
    ret_img = cv2.resize(src1, (0, 0), fx=1 / lvl, fy=1 / lvl, interpolation=cv2.INTER_CUBIC)
    ret_img = cv2.resize(ret_img, tuple(src1.shape[-2::-1]), interpolation=cv2.INTER_CUBIC)
    # Return image and SR factor
    return np.clip(ret_img, 0, 1), lvl * 10


# Function to add deblocking to an image
def addDeJPEG(src1, lvl=None):
    global title_window

    # If no specific deblocking level is specified, generate a random one
    if not lvl:
        lvl = np.random.randint(10, 100)
    # Update window title with deblocking level
    title_window = "SR Factor {}".format(lvl)

    # Write image to JPEG file with specified deblocking level, then read it back in
    cv2.imwrite('tmp.jpg', src1 * 255, [int(cv2.IMWRITE_JPEG_QUALITY), lvl])
    # ret_img = cv2.imread('tmp.jpg', 0) / 255
    ret_img = cv2.imread('tmp.jpg') / 255
    # Delete temporary file
    os.remove('tmp.jpg')
    # Return image and deblocking level
    return np.clip(ret_img, 0, 1), lvl

# Load NoiseNet model
def loadNoiseNet(device):
    if not os.path.exists('pre_trained/noise_net_latest.pth'):
        print("No weights for NoiseNet")
        return None

    noise_model = NoiseNet().to(device) # Create NoiseNet model
    noise_model.load_state_dict(torch.load('pre_trained/noise_net_latest.pth', map_location=device), strict=False) # Load weights
    return noise_model


def main():
    global args

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code for Adding a Trackbar to our applications tutorial.')
    parser.add_argument('--input',
                        help='Path to example image, if it\'s a folder, a random image will be chosen from that folder',
                        required=True)
    parser.add_argument('--checkpoint', help='Path to the model weighs.', required=True)
    parser.add_argument('--no_bn', dest='bn', default=True, action='store_false',
                        help='Add Batch Normalization int the meta blocks')
    parser.add_argument('--no_bias', dest='bias', default=True, action='store_false',
                        help='Add Bias in the ResBlocks')
    parser.add_argument('--meta_blocks', type=int, default=16, help='Number of Meta Blocks')
    parser.add_argument('-y', '-Y', '--gray', dest='y_channel', default=False, action='store_true',
                        help='Train on Grayscale only')
    parser.add_argument('--data_type', type=str, default='n', choices=['n', 'sr', 'j'],
                        help='Defines the task data, de(n)oise, super-resolution(sr), de(j)peg.')
    #
    parser.add_argument('--lvls', type=int, nargs='+', default=[15], help='A list of corruptions levels to train on')
    parser.add_argument('--device', type=str, default='cpu', help='Device to run on,[cpu,cuda,cuda:0..]')
    parser.add_argument('--norm_f', type=float, default=255, help='The normalization factor for the distortion levels.')
    #
    args = parser.parse_args()
    device = args.device
    img_path = args.input
    # curr_dict = {"sr": addSR, "n": addNoise, "j": addDeJPEG}
    curr_dict = {"j": addDeJPEG}
    # Load specified image(s)
    if os.path.isdir(args.input):
        img_path = os.path.join(args.input, np.random.choice(os.listdir(args.input)))
    print(img_path)
    assert(os.path.exists(img_path))
    if False and args.data_type == "j":
        gt = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    else:
        gt = cv2.imread(img_path)

    # Modify the image by cropping by a factor of 2
    gt = modcrop(gt, 2)

    # Set the maximum value for the alpha trackbar based on data type
    alpha_slider_max = 150
    if args.data_type == "sr":
        alpha_slider_max = 6 * 10
    if args.data_type == "j":
        alpha_slider_max = 100

    # Select a function to corrupt the image based on the data type
    corrupt_fun = curr_dict[args.data_type]
    # Corrupt the image and store the noise level
    src1, rnd_noise = corrupt_fun(gt / 255,20)

    # Get the height and width of the image
    h, w = gt.shape[:2]
    # Create a canvas for displaying the original and processed images side by side
    canvas = np.zeros((h, 2 * w, 3)).astype(np.uint8)
    if False and args.data_type == "j":
        canvas = np.zeros((h, 2 * w)).astype(np.uint8)
    # Display the corrupted image on the left side of the canvas
    disp_src = src1

    # If data type is super resolution, resize the image back to its original size for display
    if args.data_type == 'sr':
        disp_src = cv2.resize(src1, (0, 0), fx=10 / rnd_noise, fy=10 / rnd_noise)
    d_h, d_w = disp_src.shape[:2]
    canvas[:d_h, :d_w] = disp_src * 255

    # Convert the corrupted image to a tensor and move it to the designated device
    src1 = ToTensor()(src1).to(device)

    # Create model
    checkpoint = torch.load(args.checkpoint, map_location=device)
    # model = HyperRes(meta_blocks=args.meta_blocks,
    #                  sigmas=[0], device=device, bn=False, bias=True,
    #                  gray=args.data_type == 'j').to(device)

    # Load model weights from checkpoint
    model = HyperRes(meta_blocks=args.meta_blocks, level=args.lvls, device=device,
                     bias=args.bias,
                     gray=args.y_channel,
                     norm_factor=args.norm_f)
    # Load the model weights
    model.load_state_dict(checkpoint['state_dict'],strict=False)
    model.to(device)

    noise_net = loadNoiseNet(device)

    init_noise = 45
    if noise_net:
        init_noise = noise_net(src1.unsqueeze(0))
        print("Noise in image:\t{}\nPredicted Noise:\t{:.2f}".format(rnd_noise, init_noise.item()))
        print("==================================\n")


    # Define a function for updating the processed image and PSNR when the trackbar is moved
    def on_trackbar(alpha):
        # If data type is super resolution, divide the trackbar value by 10
        alpha = alpha / 10 if args.data_type == 'sr' else alpha
        # Set the model's level to the trackbar value
        model.setLevel(alpha)
        # Process the image
        with torch.no_grad():
            dst = model([src1.unsqueeze(0)])[0]
        # Post-process the image and get the PSNR
        dst = postProcessForStats(dst)[0]
        print("{} : {:.2f}".format(alpha, calculate_psnr(dst, gt)))
        # Display the processed image on the right side of the canvas
        canvas[:, w:] = dst
        cv2.imshow(title_window, canvas)

    # Create a window for displaying the images and trackbars
    cv2.namedWindow(title_window)
    # Display the original and processed images
    cv2.imshow(title_window, canvas)
    # Create a trackbar for adjusting the model's level
    trackbar_name = "Alpha"
    cv2.createTrackbar(trackbar_name,
                       title_window,
                       init_noise[0,0].detach().cpu().numpy().astype(int),
                       alpha_slider_max, on_trackbar)
    # on_trackbar(init_noise)
    # Wait until user press some key
    cv2.waitKey()


if __name__ == '__main__':

    main()
