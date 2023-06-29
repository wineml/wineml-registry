FROM python:3.9-alpine

ENV PYTHONPATH="/usr/src:$PATH"

WORKDIR /usr

COPY docker/aws/requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src /usr/src

EXPOSE 8081

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8081" ]
