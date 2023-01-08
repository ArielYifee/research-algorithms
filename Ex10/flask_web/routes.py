from flask import render_template, url_for, redirect
from flask_web import app
from flask_web.forms import DataForm
from image_restoration.live_demo1 import main

@app.route('/')
def myhome():
    return render_template('home.html', 
        )

@app.route("/data", methods=['GET', 'POST'])
def data():
    picture=data.picture_filename
    form = DataForm()
    if not form.validate_on_submit():
        return render_template('data.html', title='Free try', form=form)
    else:
        if form.picture.data:
            data.picture_filename = save_picture(form.picture.data)
            return render_template('data.html', title='Free try', form=form, submitted = False, picture = data.picture_filename)
        else:
            data.submitted = True
            return render_template('data.html', title='Free try', form=form, submitted = True)

data.picture_filename = None

import os, pathlib
def save_picture(form_picture):
    picture_filename = form_picture.filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics')
    pathlib.Path(picture_path).mkdir(parents=True, exist_ok=True)  # create all folders in the given path.
    form_picture.save(os.path.join(picture_path, picture_filename))
    picture_path = os.path.join(picture_path, picture_filename)
    # call main

    return picture_filename
