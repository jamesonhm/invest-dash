FROM python:3.11

RUN apt-get update && apt-get -y install cron

WORKDIR /app

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab && crontab /etc/cron.d/crontab

COPY ./requirements.txt /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron", "-f"]