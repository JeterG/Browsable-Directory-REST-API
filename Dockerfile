FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 8000:8000
COPY ./app /code/app
COPY ./data/home /home
COPY ./test_directory /code/test_directory
COPY ./test /code/test
RUN ["pytest","-vv"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]