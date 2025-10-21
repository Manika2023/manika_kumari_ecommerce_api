### Getting started

## Create a new Python virtual environment
python -m venv .env

## Activate the virtual environment
source .env/scripts/activate

## Install required packages
python -m pip install -r requirements.txt

## Run Django server
python manage.py runserver -> deprecated after adding web socket 
## use to run server
uvicorn e_commerce.asgi:application --reload