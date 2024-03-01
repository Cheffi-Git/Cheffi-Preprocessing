FROM python:3.10

RUN pip install pandas, openpyxl, pyproj

COPY source.xlsx .

COPY main.py .

CMD ["python", "main.py"]
