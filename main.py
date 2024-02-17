import findspark

findspark.init()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql import functions as F

# from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.ml.feature import VectorAssembler
from pyspark import SparkConf, SparkContext
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType,
)


app = FastAPI()


@app.get("/")
def hello():

    spark = SparkSession.builder.appName("SparkMLPredict").getOrCreate()
#    model = PipelineModel.load("s3a://fraudstop/artifacts/tree_md7/sparkml")
    model = PipelineModel.load("./models/tree/sparkml")
    struct = StructType(
        [
            StructField("transaction_id", IntegerType(), nullable=True),
            StructField("tx_datetime", StringType(), nullable=True),
            StructField("customer_id", IntegerType(), nullable=True),
            StructField("terminal_id", IntegerType(), nullable=True),
            StructField("tx_amount", DoubleType(), nullable=True),
        ]
    )
    data = [(1510422180, "2022-04-12 13:34:27", 209997, 894, 13.01)]
    df = spark.createDataFrame(data, struct)
    df = df.withColumn("tx_datetime", col("tx_datetime").cast("timestamp"))
    df = df.withColumn(
        "tx_time",
        F.unix_timestamp(col("tx_datetime"))
        - F.unix_timestamp(F.to_date(col("tx_datetime"))),
    )
    df = df.select(
        "transaction_id", "tx_time", "customer_id", "terminal_id", "tx_amount"
    )

    predictions = model.transform(df)
    tx_id = predictions.select("transaction_id").first()[0]
    is_fraud = predictions.select("prediction").first()[0]
    spark.stop()
    return {"tx_id": tx_id, "is_fraud": is_fraud}
