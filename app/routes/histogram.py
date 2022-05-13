import redis
from rq import Connection, Queue
from rq.job import Job

from app import app
from config import Configuration
from flask import render_template

from app.forms.histogram_form import HistogramForm
import image_histogram


@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    """! Handles selection of image to analyze\
            and serves output page.
    """
    form = HistogramForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)

        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE_HIST)
            job = Job.create(image_histogram.generate, kwargs={
                "img_id": image_id
            })
            task = q.enqueue_job(job)

        return render_template("histogram_output.html", image_id=image_id, jobID=task.get_id())
    
    #serve form if method is GET
    return render_template('histogram_select.html', form=form)
