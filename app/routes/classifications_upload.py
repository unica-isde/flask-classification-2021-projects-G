import redis
from flask import render_template, request
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()


@app.route('/classifications_upload', methods=['GET', 'POST'])
def classifications_upload():
    """API for selecting and uploading an image from
    the user computer and running a classification job.
    Returns the output score from the model"""
    form = ClassificationForm()
    if request.method == 'POST':
        #TO IMPLEMENT
        return render_template("classification_output_upload_queue.html")


    return render_template('classification_upload_select.html', form=form)