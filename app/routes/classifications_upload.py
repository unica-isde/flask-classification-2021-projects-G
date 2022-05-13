import redis
from flask import render_template, request, redirect, flash
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration
import os
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and filename and filename.rsplit('.', 1)[1].lower() in Configuration.ALLOWED_EXTENSIONS

@app.route('/classifications_upload', methods=['GET', 'POST'])
def classifications_upload():
    """API for selecting and uploading an image from
    the user computer and running a classification job.
    Returns the output score from the model"""
    form = ClassificationForm()
    config = Configuration()
    image_path = config.UPLOAD_FOLDER

    if not os.path.exists(image_path):
        os.mkdir(image_path)

    if request.method == 'POST':
        if 'upload_image' not in request.files:
            flash(" no one file is uploaded \n please select a file")
            return redirect(request.url)

        upload_image = request.files['upload_image']
        filename = upload_image.filename

        if filename == '':
            flash(" no selected file")
            return redirect(request.url)

        if upload_image and allowed_file(filename):
            filename = secure_filename(filename)
            upload_image.save(os.path.join(image_path, filename))
        else:
            flash("the image selected is not valid")
            return redirect(request.url)

        model_id = form.model.data

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={"model_id": model_id,
                                                     "img_id": filename})
            task = q.enqueue_job(job)
        return render_template("classification_output_upload_queue.html", image_id = filename, jobID=task.get_id())


    return render_template('classification_upload_select.html', form=form)