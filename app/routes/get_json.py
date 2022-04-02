from app import app
from flask import Response, abort

from app.utils import json_data


@app.route('/json/<string:job_id>', methods=['GET'])
def get_json(job_id):

    data = json_data.fetch(job_id)
   
    if data is None:
        abort(418)

    else:
        return Response(data, 
                mimetype='application/json',
                headers={'Content-Disposition':'attachment;filename=data.json'})
