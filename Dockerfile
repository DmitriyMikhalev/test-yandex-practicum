FROM python:3.11-slim

WORKDIR /bot

COPY . .

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r infra/requirements.txt --no-cache-dir

CMD ["python", "main.py"]