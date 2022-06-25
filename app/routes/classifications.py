import redis
from flask import render_template
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration

import os
import re
import torchvision.transforms as Transforms
from PIL import Image

config = Configuration()


@app.route('/classifications', methods=['GET', 'POST'])
def classifications():
    """API for selecting a model and an image and running a 
    classification job. Returns the output scores from the 
    model."""
    form = ClassificationForm()

    #  get output path and remove already modified files from that path
    output_path = get_output_path()
    remove_modified_files(output_path)

    if form.validate_on_submit():  # POST

        #  get transform values from the forms and cast them to float type
        brightness = float(form.brightness.data)
        contrast = float(form.contrast.data)
        saturation = float(form.saturation.data)
        hue = float(form.hue.data)

        image_id = form.image.data
        model_id = form.model.data

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)

        #  check if the transform values are choosen by the user and if so then apply them
        if some_properties_are_modified(0, brightness, contrast, saturation, hue):
            #  build the transform object
            transform = Transforms.ColorJitter(brightness=(brightness), contrast=(contrast), saturation=(saturation), hue=(hue))
            #  transform image and then update its id
            new_image_id = transform_image(transform, image_id, output_path)
            image_id = new_image_id

        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": image_id
            })
            task = q.enqueue_job(job)

        # returns the image classification output from the specified model
        # return render_template('classification_output.html', image_id=image_id, results=result_dict)
        return render_template("classification_output_queue.html", image_id=image_id, jobID=task.get_id())

    # otherwise, it is a get request and should return the
    # image and model selector
    return render_template('classification_select.html', form=form)


#  remove already modified images from an input path
def remove_modified_files(path):
    for f in os.listdir(path):
        if re.search('modified_', f):
            os.remove(os.path.join(path, f))

#  check if the input properties are different from the reference value, returns the result
def some_properties_are_modified(reference_value, *properties):
    properties_modified = False
    for p in properties:
        if p != reference_value:
            properties_modified = True

    return properties_modified

#  get the path where the images are saved to, returns that path
def get_output_path():
    project_root = os.path.dirname(os.path.dirname(__file__))
    output_path = os.path.join(project_root, 'static/imagenet_subset/')
    return output_path

#  apply a transformation to an image in a certain path, returns the new image id after the transformation
def transform_image(transform, image_id, path):
    img = Image.open(path + image_id)
    img = transform(img)
    img.save(path + 'modified_' + image_id)
    return ('modified_' + image_id)
