import sys
import requests

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import BooleanType
from dateutil import parser

fecha1 = ''
fecha2 = ''

if __name__ == "__main__":
    """
        Usage: ejercicio1 [fecha1][fecha2]
    """

    spark = SparkSession \
        .builder \
        .appName("PySparkejercisio1") \
        .getOrCreate()

    if len(sys.argv) > 2:
        fecha1 = parser.parse(sys.argv[1]).strftime('%Y-%m-%d')
        fecha2 = parser.parse(sys.argv[2]).strftime('%Y-%m-%d')
    else:
        sys.exit("Faltan argumentos, deben de ser 2 Fechas")


    def getDataFromApi():
        url = "http://144.202.34.148:3018/Minip/api/"
        response = requests.get(url)
        return response


    @F.udf(returnType=BooleanType())
    def my_fil(fec):
        fechav = parser.parse(fec).strftime('%Y-%m-%d')
        return fecha1 <= fechav <= fecha2


    data = getDataFromApi()
    json_rdd = spark.sparkContext.parallelize([data.text])
    df = spark.read.json(json_rdd)
    filtro = df.select("temp").filter(my_fil(df["temp"]))
    result = filtro.agg(F.min(df["temp"]), F.max(df["temp"]), F.avg(df["temp"]))
    print(filtro.show(truncate=False))
    print(result.show(truncate=False))
    print("Fin de del Proceso")
    spark.stop()
