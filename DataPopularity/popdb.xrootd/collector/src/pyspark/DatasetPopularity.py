from pyspark import (HiveContext,SparkConf,SparkContext)
import sys

filename = sys.argv[1]
saveto = sys.argv[2]
jobName = sys.argv[3]
allMVs = sys.argv[4]

print "=> filename %s" % filename
print "=> saveto %s" % saveto
print "=> jobName %s" % jobName
print "=> allMVs %s" % allMVs

conf = SparkConf().setAppName(jobName)
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")
sqlc = HiveContext(sc)

T_XRD_HDFS = sqlc.read.format("json").load(filename)
T_XRD_HDFS.registerTempTable("T_XRD_HDFS")
print "=> rowsCounter T_XRD_HDFS: %d" % T_XRD_HDFS.count()
# T_XRD_HDFS.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/T_XRD_HDFS")

T_XRD_RAW_FILE = sqlc.sql("SELECT from_unixtime(end_time, 'yyyy/MM/dd') as TDay, start_time as ots, end_time as cts, file_lfn, client_host, if(server_username = '', 'unknown', server_username) as server_username, (end_time - start_time) as proctime, read_bytes_at_close as readbytes FROM T_XRD_HDFS WHERE (end_time - start_time) > 0 AND read_bytes_at_close > 0 AND `_corrupt_record` IS NULL")
T_XRD_RAW_FILE.registerTempTable("T_XRD_RAW_FILE")
print "=> rowsCounter T_XRD_RAW_FILE: %d" % T_XRD_RAW_FILE.count()
if allMVs == 1:
    T_XRD_RAW_FILE.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/T_XRD_RAW_FILE")
 
T_XRD_LFC = sqlc.read.format("com.databricks.spark.csv").load("/project/awg/cms/phedex/catalog/csv/merged/").toDF("dataset_name", "dataset_id", "dataset_is_open", "dataset_time_create", "block_name", "block_id", "block_time_create", "block_is_open", "file_lfn", "file_id", "filesize", "usernameXX", "checksum", "file_time_create")
T_XRD_LFC.registerTempTable("T_XRD_LFC")
print "=> rowsCounter T_XRD_LFC: %d" % T_XRD_LFC.count()
if allMVs == 1:
    T_XRD_LFC.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/T_XRD_LFC")
 
V_XRD_LFC_aggr1 = sqlc.sql("SELECT distinct block_name, dataset_name FROM T_XRD_LFC")
V_XRD_LFC_aggr1.registerTempTable("V_XRD_LFC_aggr1")
print "=> rowsCounter V_XRD_LFC_aggr1: %d" % V_XRD_LFC_aggr1.count()
if allMVs == 1:
    V_XRD_LFC_aggr1.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/V_XRD_LFC_aggr1")

MV_XRD_stat0_pre = sqlc.sql("SELECT raw.TDay, raw.client_host, raw.server_username, lfc.block_name, count(raw.client_host) as numaccesses, sum(raw.proctime) as proctime, sum(raw.readbytes) as readbytes FROM T_XRD_RAW_FILE raw, T_XRD_LFC lfc WHERE raw.file_lfn = lfc.file_lfn GROUP BY raw.TDay, raw.client_host, raw.server_username, lfc.block_name")
MV_XRD_stat0_pre.registerTempTable("MV_XRD_stat0_pre")
print "=> rowsCounter MV_XRD_stat0_pre: %d" % MV_XRD_stat0_pre.count()
if allMVs == 1:
    MV_XRD_stat0_pre.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_XRD_stat0_pre")
 
MV_XRD_stat0 = sqlc.sql("SELECT TDay, client_host, server_username, aggr1.dataset_name, sum(numaccesses) as numaccesses, sum(proctime) as proctime, sum(readbytes) as readbytes from MV_XRD_stat0_pre pre, V_XRD_LFC_aggr1 aggr1 WHERE pre.block_name = aggr1.block_name GROUP BY TDay, client_host, server_username, aggr1.dataset_name")
MV_XRD_stat0.registerTempTable("MV_XRD_stat0")
print "=> rowsCounter MV_XRD_stat0: %d" % MV_XRD_stat0.count()
if allMVs == 1:
    MV_XRD_stat0.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_XRD_stat0")
 
MV_XRD_DS_stat0_aggr1 = sqlc.sql("SELECT TDay, dataset_name, instr(server_username,'cms') AS isusercms, sum(readbytes) as readbytes, sum(numaccesses) as numaccesses, sum(proctime) as totCPU, count(distinct server_username) as numusers FROM MV_XRD_stat0 GROUP BY TDay, dataset_name, instr(server_username,'cms')")
MV_XRD_DS_stat0_aggr1.registerTempTable("MV_XRD_DS_stat0_aggr1")
print "=> rowsCounter MV_XRD_DS_stat0_aggr1: %d" % MV_XRD_DS_stat0_aggr1.count()
if allMVs == 1:
    MV_XRD_DS_stat0_aggr1.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_XRD_DS_stat0_aggr1")
 
MV_DS = sqlc.sql("select distinct(dataset_name) as dataset_name from MV_XRD_DS_stat0_aggr1 order by dataset_name")
MV_DS.registerTempTable("MV_DS")
print "=> rowsCounter MV_DS: %d" % MV_DS.count()
MV_DS.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_DS")

MV_XRD_DS_stat0_aggr2 = sqlc.sql("select TDay, regexp_extract(dataset_name, '([^/]+)$') as datatier, INSTR(server_username, 'cms') as isusercms, sum(readbytes) as readbytes, sum(numaccesses) as numaccesses, sum(proctime) as totCPU, count (distinct server_username) as numusers from MV_XRD_stat0 group by TDay, regexp_extract(dataset_name, '([^/]+)$'), INSTR(server_username, 'cms')")
MV_XRD_DS_stat0_aggr2.registerTempTable("MV_XRD_DS_stat0_aggr2")
print "=> rowsCounter MV_XRD_DS_stat0_aggr2: %d" % MV_XRD_DS_stat0_aggr2.count()
if allMVs == 1:
    MV_XRD_DS_stat0_aggr2.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_XRD_DS_stat0_aggr2")
 
MV_DataTier = sqlc.sql("select distinct(datatier) as datatier from MV_XRD_DS_stat0_aggr2 order by datatier")
MV_DataTier.registerTempTable("MV_DataTier")
print "=> rowsCounter MV_DataTier: %d" % MV_DataTier.count()
MV_DataTier.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_DataTier")

MV_XRD_DS_stat0_aggr3 = sqlc.sql("SELECT TDay, server_username, regexp_extract(dataset_name, '([^/]+)$') as datatier, sum(readbytes) as readbytes, sum(numaccesses) as numaccesses, sum(proctime) as totCPU FROM MV_XRD_stat0 GROUP BY TDay, server_username, regexp_extract(dataset_name, '([^/]+)$')")
MV_XRD_DS_stat0_aggr3.registerTempTable("MV_XRD_DS_stat0_aggr3")
print "=> rowsCounter MV_XRD_DS_stat0_aggr3: %d" % MV_XRD_DS_stat0_aggr3.count()
if allMVs == 1:
    MV_XRD_DS_stat0_aggr3.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_XRD_DS_stat0_aggr3")

MV_XRD_DS_stat0_aggr4 = sqlc.sql("select TDay, split(dataset_name,'/')[2] as namespace, INSTR(server_username,'cms') as isusercms, sum(readBytes) as readBytes, sum(numAccesses) as numAccesses, sum(procTime) as totCPU, count (distinct server_username) as numUsers from MV_XRD_stat0 WHERE regexp_extract(dataset_name, '([^/]+)$') NOT LIKE 'USER' AND dataset_name NOT LIKE 'unknown' GROUP BY TDay, split(dataset_name,'/')[2], INSTR(server_username,'cms')")
MV_XRD_DS_stat0_aggr4.registerTempTable("MV_XRD_DS_stat0_aggr4")
print "=> rowsCounter MV_XRD_DS_stat0_aggr4: %d" % MV_XRD_DS_stat0_aggr4.count()
if allMVs == 1:
    MV_XRD_DS_stat0_aggr4.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_XRD_DS_stat0_aggr4")

MV_DSName = sqlc.sql("select distinct(namespace) as namespace from MV_XRD_DS_stat0_aggr4 order by namespace")
MV_DSName.registerTempTable("MV_DSName")
print "=> rowsCounter MV_DSName: %d" % MV_DSName.count()
MV_DSName.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_DSName")

MV_block_stat0_aggr_180_days = sqlc.sql("select WeekofYear(regexp_replace(Tday, '/', '-')) as week, 'T2_CH_CERN' as sitename, block_name, datediff(from_unixtime(unix_timestamp(), 'yyyy-MM-dd'), regexp_replace(Tday, '/', '-')) as days, sum(numAccesses) as numAccesses, sum(procTime) as totCPU, sum(readBytes) as readBytes FROM MV_XRD_stat0_pre WHERE datediff(from_unixtime(unix_timestamp(), 'yyyy-MM-dd'), regexp_replace(Tday, '/', '-')) < 180 GROUP BY WeekofYear(regexp_replace(Tday, '/', '-')), 'T2_CH_CERN', block_name, datediff(from_unixtime(unix_timestamp(), 'yyyy-MM-dd'), regexp_replace(Tday, '/', '-')) ORDER BY week, block_name")
MV_block_stat0_aggr_180_days.registerTempTable("MV_block_stat0_aggr_180_days")
print "=> rowsCounter MV_block_stat0_aggr_180_days: %d" % MV_block_stat0_aggr_180_days.count()
MV_block_stat0_aggr_180_days.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_block_stat0_aggr_180_days")

MV_block_stat0_aggr_12_months = sqlc.sql("select WeekofYear(regexp_replace(Tday, '/', '-')) as week, 'T2_CH_CERN' as sitename, block_name, datediff(from_unixtime(unix_timestamp(), 'yyyy-MM-dd'), regexp_replace(Tday, '/', '-')) as days, sum(numAccesses) as numAccesses, sum(procTime) as totCPU, sum(readBytes) as readBytes FROM MV_XRD_stat0_pre WHERE datediff(from_unixtime(unix_timestamp(), 'yyyy-MM-dd'), regexp_replace(Tday, '/', '-')) < 365 GROUP BY WeekofYear(regexp_replace(Tday, '/', '-')), 'T2_CH_CERN', block_name, datediff(from_unixtime(unix_timestamp(), 'yyyy-MM-dd'), regexp_replace(Tday, '/', '-')) ORDER BY week, block_name")
MV_block_stat0_aggr_12_months.registerTempTable("MV_block_stat0_aggr_12_months")
print "=> rowsCounter MV_block_stat0_aggr_12_months: %d" % MV_block_stat0_aggr_12_months.count()
MV_block_stat0_aggr_12_months.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_block_stat0_aggr_12_months")

MV_block_stat0_last_access = sqlc.sql("select MAX(WeekofYear(regexp_replace(Tday, '/', '-'))) as weekmax, 'T2_CH_CERN' as sitename, block_name FROM MV_XRD_stat0_pre GROUP BY 'T2_CH_CERN', block_name")
MV_block_stat0_last_access.registerTempTable("MV_block_stat0_last_access")
print "=> rowsCounter MV_block_stat0_last_access: %d" % MV_block_stat0_last_access.count()
MV_block_stat0_last_access.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_block_stat0_last_access")

MV_XRD_stat2 = sqlc.sql("select TDay, SUM(readBytes) as readBytes, SUM(1) as Nentries, SUBSTR(file_lfn, 1, INSTR(file_lfn, regexp_extract(file_lfn, '([^/]+)$')) - 1) AS dirName FROM T_XRD_RAW_FILE WHERE file_lfn NOT LIKE '/replicate%' GROUP BY TDay, SUBSTR(file_lfn, 1, INSTR(file_lfn, regexp_extract(file_lfn, '([^/]+)$')) - 1)") 
MV_XRD_stat2.registerTempTable("MV_XRD_stat2")
print "=> rowsCounter MV_XRD_stat2: %d" % MV_XRD_stat2.count()
if allMVs == 1:
    MV_XRD_stat2.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/MV_XRD_stat2")

V_XRD_stat2_aggr1 = sqlc.sql("select dirname as path, min(tday) as min_tday, max(tday) as max_tday, sum(readbytes)/1000/1000 as read_bytes, sum(nentries) as read_acc from MV_XRD_stat2 GROUP BY dirname ORDER BY MAX(tday) DESC")
V_XRD_stat2_aggr1.registerTempTable("V_XRD_stat2_aggr1")
print "=> rowsCounter V_XRD_stat2_aggr1: %d" % V_XRD_stat2_aggr1.count()    
V_XRD_stat2_aggr1.write.format("com.databricks.spark.csv").option("header", "false").save(saveto + "/V_XRD_stat2_aggr1")
