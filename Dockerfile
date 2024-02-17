FROM jupyter/pyspark-notebook:latest

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY main.py /app/main.py 
COPY models/ /app/models/
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
