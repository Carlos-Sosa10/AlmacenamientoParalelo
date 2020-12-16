import requests

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

if __name__ == "__main__":
    """
        Usage: ejercicio2
    """

    spark = SparkSession \
        .builder \
        .appName("PySparkejercisio2") \
        .getOrCreate()

    def getDataFromApi():
        url = http://144.202.34.148:3018/Minip/api/
        response = requests.get(url)
        return response

    data = getDataFromApi()
    json_rdd = spark.sparkContext.parallelize([data.text])
    df = spark.read.json(json_rdd)
    result = df.select("temp").agg(F.min(df["temp"]), F.max(df["temp"]), F.avg(df["temp"]))
    print(result.show(truncate=False))

    spark.stop()
