from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SparkSession

import urllib3
import urllib
import json

conf = SparkConf().setAppName("api_temperatura").setMaster("local")
sc = SparkContext(conf=conf)
url = "http://144.202.34.148:3018/Minip/api"
args = {"Tipo":"Completa","NoCo":"05590693"}
post_params = {"Tipo":"Completa","NoCo":"05590693"}
params = urllib.urlencode(post_params)
response = urllib3.urlopen(url, params)
json_response = json.loads(response.read())
datos = json_response

Temperatura = []
for d in datos["D"]:
    Temperatura.append(float(d['Temp']))

Data1 = sc.parallelize(Temperatura).sum()
Data2 = sc.parallelize(Temperatura).count()

promedio = Data1 / Data2
print("El promedio es: ",promedio)