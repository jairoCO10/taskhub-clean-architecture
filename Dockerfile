FROM python:3.9

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . /code

# CMD ["uvicorn", "app.entrypoints.api.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
CMD ["python", "run.py"]