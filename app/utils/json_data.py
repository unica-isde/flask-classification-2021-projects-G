import requests
import json
from flask import url_for


def fetch(job_id, url=None):
    
    if url is None:
        url = 'http://localhost:5000'+\
                url_for('classifications_id', job_id=job_id)

    try:
        result = requests.get(url)
        result.raise_for_status()

        tmp = result.json()
        status = tmp.get('task_status')

        if status != 'finished':
            raise Exception("The classification data is not available")

        content = json.dumps( dict(tmp.get('data')) )
        return content


    except Exception as e:

        print(repr(e))
        return None
