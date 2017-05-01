## XrootD Data Popularity

Python version of the Scala Spark program: https://github.com/dmwm/DDM/tree/master/DataPopularity/popdb.xrootd/collector/src/spark

Author: Marco Meoni (Python conversion Luca Menichetti)

Goal: reproduce materialized views from Oracle database in Hadoop. Process Xrootd popularity aggregations using Spark. 

Input: phedex catalogue and xrootd data transfer monitoring. The first is "Sqooped" daily in the CERN IT *analytix* cluster, the second are stored in the *hadalytic* cluster with streamings by the [wdtmon account](https://twiki.cern.ch/twiki/bin/view/LCG/WLCGMonDataAnalytics#WLCG_Data_Analytics_platform).

Output: one folder per MVs in CSV format.

Example command:

```
spark-submit --packages com.databricks:spark-csv_2.10:1.5.0 \
  --conf spark.yarn.access.namenodes=hdfs://analytix,hdfs://hadalytic \
  DatasetPopularity.py \
  hdfs://hadalytic/user/wdtmon/xrootd/cms/2015/03/*/eos \
  xrootd-MV/2015-03 \
  DatasetPopularity \
  1
```
