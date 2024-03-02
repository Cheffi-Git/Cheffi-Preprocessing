FROM python:3.10

RUN pip install pandas openpyxl pyproj pymysql sqlalchemy geoalchemy2

COPY source.csv .

COPY main.py .

COPY preprocess.py .

CMD ["python", "main.py"]
