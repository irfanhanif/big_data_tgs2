
# coding: utf-8

# In[7]:

sc


# In[2]:

# Konfigurasi Spark
import os
import sys

# 1. Mengeset variabel yang menyimpan lokasi di mana Spark diinstal
spark_path = "D:/spark"

# 2. Menentukan environment variable SPARK_HOME
os.environ['SPARK_HOME'] = spark_path

# 3. Simpan lokasi winutils.exe sebagai environment variable HADOOP_HOME
os.environ['HADOOP_HOME'] = spark_path

# 4. Lokasi Python yang dijalankan --> punya Anaconda
#    Apabila Python yang diinstall hanya Anaconda, maka tidak perlu menjalankan baris ini.
os.environ['PYSPARK_PYTHON'] = sys.executable

# 5. Konfigurasi path library PySpark
sys.path.append(spark_path + "/bin")
sys.path.append(spark_path + "/python")
sys.path.append(spark_path + "/python/pyspark/")
sys.path.append(spark_path + "/python/lib")
sys.path.append(spark_path + "/python/lib/pyspark.zip")
sys.path.append(spark_path + "/python/lib/py4j-0.10.4-src.zip")

# 6. Import library Spark
#    Dua library yang WAJIB di-import adalah **SparkContext** dan **SparkConf**.
from pyspark import SparkContext
from pyspark import SparkConf

# Setting konfigurasi (opsional)
conf = SparkConf()
conf.set("spark.executor.memory", "2g")
conf.set("spark.cores.max", "4")

sc = SparkContext("local", conf=conf)
#    Apabila berhasil, maka ketika sc di-print akan mengeluarkan nilai <pyspark.context.SparkContext object>


# In[3]:

sc


# In[5]:

sc


# In[6]:

print sc


# In[29]:

airlinesPath="C:\\Users\\ifirf\Documents\\BigData\\airlines.csv"
airportsPath="C:\\Users\ifirf\\Documents\\BigData\\airport.csv"
flightsPath="C:\\Users\\ifirf\\Documents\\BigData\\flights.csv"


# In[30]:

airlines=sc.textFile(airlinesPath)


# In[31]:

print airlines


# In[33]:

airlines.collect()


# In[34]:

airlines.first()


# In[36]:

airlines.take(10)


# In[37]:

airlines.count()


# In[39]:

# here is how to filter the header out
airlinesWoHeader = airlines.filter(lambda x: "Description" not in x)


# In[40]:

print airlinesWoHeader


# In[41]:

airlinesWoHeader.take(10)


# In[42]:

airlinesParsed=airlinesWoHeader.map(lambda x:x.split(",")).take(10)


# In[44]:

airlinesParsed


# In[45]:

airlines.map(len).take(10)


# In[47]:

def notHeader(row):
    return "Description" not in row
airlines.filter(notHeader).take(10)


# In[50]:

airlines.filter(notHeader)     .map(lambda x: x.split(','))     .take(10)


# In[53]:

# use python libraries
import csv
from StringIO import StringIO

def split(line):
    reader = csv.reader(StringIO(line))
    return reader.next()

airlines.filter(notHeader).map(split).take(10)


# In[ ]:



