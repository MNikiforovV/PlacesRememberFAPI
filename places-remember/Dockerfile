FROM python:3.11

WORKDIR /places-remember

COPY ./requirements.txt /places-remember/requirements.txt

COPY ./.env /places-remember/.env

RUN pip install --no-cache-dir --upgrade -r /places-remember/requirements.txt

COPY ./app /places-remember/app

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]