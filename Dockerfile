FROM python:3.11

WORKDIR /invest_dash

COPY ./requirements.txt /invest_dash

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /invest_dash

ENV PYTHONPATH "${PYTHONPATH}:/invest_dash"

#VOLUME /invest_dash

EXPOSE 9090

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090"]
