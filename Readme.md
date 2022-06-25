# Web server for image classification


## Download the repository

Use git to clone the repository:

```bash
git clone https://github.com/unica-isde/flask-classification-2021-projects-G
```

And install the requirements with 

```bash
pip install -r requirements.txt
```

Additional requirements:
* Redis
* Docker

## Configuration

Configure the service by editing the file `config.py`.

## Prepare the resources

It is recommended to pre-download images and models before running 
the server. This is to avoid unnecessary waits for users.

Run `prepare_images.py` and `prepare_models.py`. Models will 
be stored in your PyTorch cache directory, while the path for 
the image directory can be found in the `config.py` file. 

## Usage

### Run locally

To run the code without containers, it is sufficient to run 
separately the `runserver.py` script, the `worker.py` and
`worker_histogram.py` scripts.
The workers will process the jobs stored in the queues. 
In order for the queues to work, you should have `redis`  
installed and running (specify port in `config.py`). 

### Run inside Docker 

To run the service with docker, we will use docker-compose:

```bash
docker-compose build
docker-compose up
```

You can run multiple workers with:

```bash 
docker-compose up --scale worker=2
```
