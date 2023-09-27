FROM python:3.10

RUN pip install pandas

COPY source.csv .

COPY main.py .

CMD ["python", "main.py"]
