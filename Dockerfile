FROM python:3.11

WORKDIR /app

COPY crontab /etc/cron.d/crontab

COPY ./requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENV PYTHONPATH "${PYTHONPATH}:/app/src"

RUN crontab /etc/cron.d/crontab

CMD ["crond", "-f"]