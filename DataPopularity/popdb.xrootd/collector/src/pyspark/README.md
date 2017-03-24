Command to run:

```
spark-submit --packages com.databricks:spark-csv_2.10:1.5.0 --conf spark.yarn.access.namenodes=hdfs://p01001532067275.cern.ch:8020,hdfs://p01001532965510.cern.ch:9000 --packages com.databricks:spark-csv_2.10:1.5.0 DatasetPopularity.py hdfs://hadalytic/user/wdtmon/xrootd/cms/2015/03/13/eos xrootd-MV/2015 DatasetPopularity 1
```