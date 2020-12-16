import requests
import json
from pyspark.sql import SparkSession
#from pyspark.sql import Row
#from pyspark.sql.types import StringType, StructType, StructField
from pyspark.sql import functions as F


if __name__ == "__main__":

    spark = SparkSession \
        .builder \
        .appName("Python Spark ") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    def getDataFromApi():
        url = "http://144.202.34.148:3018/Minip/api/"
        response = requests.get(url)
        return response.text


    data = getDataFromApi()
    data = data[11:]
    data = data[:-1] 
    print(data)
    json_rdd = spark.sparkContext.parallelize([data])
    df = spark.read.json(json_rdd)
    df.printSchema()
    result = df.select("temp").agg(F.min(df["temp"]), F.max(df["temp"]), F.avg(df["temp"]))
    result.show()
    spark.stop()
