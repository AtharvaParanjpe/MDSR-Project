import findspark
# findspark.init('/usr/local/Cellar/apache-spark/3.0.1/libexec')
import pyspark
from pyspark import SparkContext	
from pyspark.sql import SparkSession 

import numpy as np
import os
import time
from pyspark.sql.types import *
import time
import os 

def parseTrain(lp):
    vec = lp.split('\t')
    return vec

def collect_data(file_name, sc, spark):
    f = open("temp.txt", "w")
    cSchema = StructType([StructField("source", StringType(), True), StructField("destination", StringType(), True)])
    mainDF = spark.createDataFrame([],schema=cSchema)
    
    with open(file_name) as datafile:
        count = 1
        for line in datafile:
            count+=1
            if count == 30000000:
                print (mainDF.count())
                f.close()
                count = 1
                data = sc.textFile("temp.txt").map(parseTrain)
                dataset = data.collect()
                df = spark.createDataFrame(dataset,schema=cSchema)
                mainDF = mainDF.union(df)
                os.remove("temp.txt")
                f = open("temp.txt", "w")
            f.write(line)
    f.close()
    
    data = sc.textFile("temp.txt").map(parseTrain)
    dataset = data.collect()
    df = spark.createDataFrame(dataset,schema=cSchema) 
    mainDF = mainDF.union(df)
    os.remove("temp.txt")
    
    return mainDF

def get_nodes_with_count_k(data, k, sc, spark):
    counts = data.groupBy('source').count()
    print ("Got counts")
    result = counts.where(counts["count"] < k).select("source")
    print ("Got result")
    return result

def remove_nodes(data, node_to_be_removed, sc, spark):
    node_to_be_removed_list = node_to_be_removed.select('source').collect()
    print ("node_to_be_removed_list")
    node_to_be_removed_array = [str(row.source) for row in node_to_be_removed_list]
    print ("node_to_be_removed_array")
    node_to_be_removed_set = set(node_to_be_removed_array)
    print ("node_to_be_removed_set")
    data = data.filter(~data["source"].isin(node_to_be_removed_set))
    print ("first filter")
    data = data.filter(~data["destination"].isin(node_to_be_removed_set))
    print ("second filter")
    # return data
    # node_to_be_removed_list = node_to_be_removed.select('source').rdd.map(lambda row : str(row.source)).collect()
    # print ("node_to_be_removed_list")
    # data = data.filter(~data["source"].isin(node_to_be_removed_list))
    # print ("first filter")
    # data = data.filter(~data["destination"].isin(node_to_be_removed_list))
    # print ("second filter")
    return data

 
def do_one_iteration(data, k, sc, spark):
    node_to_be_removed = get_nodes_with_count_k(data, k, sc, spark)
    print ("node_to_be_removed")
#     print (node_to_be_removed.count())
#     print (node_to_be_removed.show())
    remove_count = node_to_be_removed.count()
    print ("remove_count")
    print (remove_count)
    data = remove_nodes(data, node_to_be_removed, sc, spark)
    print ("Done interation")
    return remove_count > 0, data, remove_count

def do_peeling(k, file_name, sc, spark):
	
	data = collect_data(file_name, sc, spark)

	
	nextReqd = True
	counter = 1
	out = []
	while nextReqd:
	#     print (data.count())
	    print (counter)
	    start_time = time.time()
	    nextReqd, data, remove_count = do_one_iteration(data, k, sc, spark)
	    out.append([counter, remove_count, time.time() - start_time])
	    print("--- %s seconds ---" % (time.time() - start_time))
	    counter += 1

	print (data.count())    
	print (data.show())
	print ("----Done----")
	print("--- %s seconds ---" % (time.time() - start_time))
	return out
