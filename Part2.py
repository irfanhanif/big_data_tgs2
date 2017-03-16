
# coding: utf-8

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
print sc


# In[3]:

airlinesPath="C:\\Users\\ifirf\Documents\\BigData\\airlines.csv"
airportsPath="C:\\Users\ifirf\\Documents\\BigData\\airport.csv"
flightsPath="C:\\Users\\ifirf\\Documents\\BigData\\flights.csv"


# In[4]:

flights = sc.textFile(flightsPath)


# In[5]:

flights.count()


# In[6]:

flights.take(10)


# In[7]:

flightsParsed=flights.map(lambda x:x.split(","))


# In[8]:

from datetime import datetime
from collections import namedtuple

fields = ('date', 'airline', 'flightnum', 'origin', 'dest', 'dep', 
          'dep_delay', 'arv', 'arv_delay', 'airtime', 'distance')
Flight = namedtuple('Flight', fields, verbose=True)

DATE_FMT ="%Y-%m-%d"
TIME_FMT = "%H%M"

def parse(row):
    row[0] = datetime.strptime(row[0], DATE_FMT).date()
    row[5] = datetime.strptime(row[5], TIME_FMT).time()
    row[6] = float(row[6])
    row[7] = datetime.strptime(row[7], TIME_FMT).time()
    row[8] = float(row[8])
    row[9] = float(row[9])
    row[10] = float(row[10])
    return Flight(*row[:11])


# In[9]:


flightsParsed=flights.map(lambda x:x.split(",")).map(parse)


# In[10]:

flightsParsed.first()


# In[17]:

#lets find the average distance traveled by a flight

totalDistance=flightsParsed.map(lambda x:x.distance).reduce(lambda x,y:x+y)


# In[18]:

avgDistance=totalDistance/flightsParsed.count()


# In[19]:

avgDistance


# In[20]:

#find the % of flights wi9th delays
flightsParsed.filter(lambda x:x.dep_delay>0).count()/float(flightsParsed.count())


# In[15]:

flightsParsed.persist()


# In[22]:

sumCount=flightsParsed.map(lambda x:x.dep_delay).aggregate((0,0),
                                                          (lambda acc,value: (acc[0]+value, acc[1]+1)),
                                                          (lambda acc1,acc2:(acc1[0]+acc2[0],acc1[1]+acc2[1])))


# In[24]:

print "The average delay is " + str (sumCount[0]/float(sumCount[1]))


# In[25]:

flightsParsed.map(lambda x:int(x.dep_delay/60)).countByValue()


# In[ ]:



