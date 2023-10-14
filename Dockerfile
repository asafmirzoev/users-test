FROM python:3.10-slim

# setup environment variable
ENV DockerHOME=/code

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy whole project to your docker home directory.
COPY . $DockerHOME

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# apply alembic migrations
RUN alembic upgrade head

# run tests
RUN pytest

# port where the FastAPI app runs
EXPOSE 8000

# run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
