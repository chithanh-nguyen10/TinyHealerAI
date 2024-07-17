FROM python:3.9.19
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . .
CMD ["fastapi", "run", "main.py", "--port", "80"]
