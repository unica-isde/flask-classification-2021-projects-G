import json
from app import app
from flask import Response, abort

from app.utils import json_data, custom_plot


@app.route('/plot/<string:job_id>', methods=['GET'])
def get_plot(job_id):

    content = json_data.fetch(job_id)
   
    if content is None:
        abort(418)

    else:
        data_dict = json.loads(content)
        labels, values = zip(*data_dict.items())

        img = custom_plot.generate(labels, values)

        return Response(img,
                mimetype='image/png',
                headers={'Content-Disposition':'attachment;filename=plot.png'})

