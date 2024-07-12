FROM python:3.12.2

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ /app/

CMD ["python", "main.py"]