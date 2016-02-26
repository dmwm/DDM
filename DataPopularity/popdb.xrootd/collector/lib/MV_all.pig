------------------- T_XRD_RAW_FILE ------------------- 
-- Test input: /user/wdtmon/xrootd/cms/2015/03/11/eos
T_XRD_RAW_FILE_0 = LOAD '$input' using JsonLoader('unique_id:chararray,file_lfn:chararray,file_size:chararray,start_time:chararray,end_time:chararray,read_bytes:chararray,read_operations:chararray,read_min:chararray,read_max:chararray,read_average:chararray,read_sigma:chararray,read_single_bytes:chararray,read_single_operations:chararray,read_single_min:chararray,read_single_max:chararray,read_single_average:chararray,read_single_sigma:chararray,read_vector_bytes:chararray,read_vector_operations:chararray,read_vector_min:chararray,read_vector_max:chararray,read_vector_average:chararray,read_vector_sigma:chararray,read_vector_count_min:chararray,read_vector_count_max:chararray,read_vector_count_average:chararray,read_vector_count_sigma:chararray,write_bytes:chararray,write_operations:chararray,write_min:chararray,write_max:chararray,write_average:chararray,write_sigma:chararray,read_bytes_at_close:chararray,write_bytes_at_close:chararray,user_dn:chararray,user_vo:chararray,user_role:chararray,user_fqan:chararray,client_domain:chararray,client_host:chararray,server_username:chararray,user_protocol:chararray,app_info:chararray,server_domain:chararray,server_host:chararray,server_site:chararray');
T_XRD_RAW_FILE_1 = FOREACH T_XRD_RAW_FILE_0 GENERATE (((long) start_time - 3600) * 1000) as ots, (((long) end_time - 3600) * 1000) as cts, (LAST_INDEX_OF(file_lfn, '/store/') == -1 ? file_lfn : SUBSTRING(file_lfn, LAST_INDEX_OF(file_lfn, '/store/'), 999)) as file_lfn, client_host, (server_username == '' ? 'unknown' : server_username) AS server_username, ((long)end_time - (long)start_time) as procTime, (long)read_bytes_at_close as readBytes;
T_XRD_RAW_FILE_2 = FOREACH T_XRD_RAW_FILE_1 GENERATE ToString(ToDate(ToString(ToDate(cts),'yyyy/MM/dd'),'yyyy/MM/dd','UTC'),'yyyy/MM/dd') as TDay, ots, cts, file_lfn, client_host, server_username, procTime, readBytes;
T_XRD_RAW_FILE = FILTER T_XRD_RAW_FILE_2 BY procTime > 0 and readBytes > 0;

------------------- T_XRD_LFC -------------------
T_XRD_LFC = LOAD '/project/awg/cms/phedex/catalog/csv/merged/*' using PigStorage(',') as (dsname:chararray,foo1:chararray,foo2:chararray,foo3:chararray, blockname:chararray,foo4:chararray,foo5:chararray,foo6:chararray, lfn:chararray,foo7:chararray,foo8:chararray,foo9:chararray,foo10:chararray,foo11:chararray);

------------------- MV_xrdmon_rates_x_H -------------------
MV_xrdmon_rates_x_H_0 = FOREACH T_XRD_RAW_FILE GENERATE ToString(ToDate(ToString(ToDate(ots),'yyyy/MM/dd HH:mm'),'yyyy/MM/dd HH:mm','UTC'),'yyyy/MM/dd/HH') as sTime, ToString(ToDate(ToString(ToDate(cts),'yyyy/MM/dd HH:mm'),'yyyy/MM/dd HH:mm','UTC'),'yyyy/MM/dd/HH') as eTime, ToString(ToDate(ToString(ToDate(cts),'yyyy/MM/dd HH:mm'),'yyyy/MM/dd HH:mm','UTC'),'yyyy/MM/dd/HH') as iTime, (INDEXOF(file_lfn, '/replicate') + 1) as replica;
MV_xrdmon_rates_x_H_1 = GROUP MV_xrdmon_rates_x_H_0 BY (sTime, eTime, iTime, replica);
MV_xrdmon_rates_x_H = FOREACH MV_xrdmon_rates_x_H_1 GENERATE FLATTEN(group), COUNT(MV_xrdmon_rates_x_H_0.replica) as yValue;

------------------- V_XRD_LFC_aggr1 -------------------
V_XRD_LFC_aggr1_0 = FOREACH T_XRD_LFC GENERATE blockname, dsname;
V_XRD_LFC_aggr1_1 = DISTINCT V_XRD_LFC_aggr1_0;
V_XRD_LFC_aggr1 = ORDER V_XRD_LFC_aggr1_1 BY blockname, dsname;

------------------- MV_XRD_stat0_pre -------------------
MV_XRD_stat0_pre_0 = JOIN T_XRD_RAW_FILE BY file_lfn, T_XRD_LFC BY lfn;
MV_XRD_stat0_pre_1 = GROUP MV_XRD_stat0_pre_0 BY (TDay, client_host, server_username, blockname);
MV_XRD_stat0_pre = FOREACH MV_XRD_stat0_pre_1 GENERATE FLATTEN(group), COUNT(MV_XRD_stat0_pre_0.client_host) as numAccesses, SUM(MV_XRD_stat0_pre_0.procTime) as procTime, SUM(MV_XRD_stat0_pre_0.readBytes) as readBytes;

------------------- MV_XRD_stat0 -------------------
MV_XRD_stat0_0 = JOIN MV_XRD_stat0_pre BY blockname, V_XRD_LFC_aggr1 BY blockname;
MV_XRD_stat0_1 = GROUP MV_XRD_stat0_0 BY (TDay, client_host, server_username, dsname);
MV_XRD_stat0 = FOREACH MV_XRD_stat0_1 GENERATE FLATTEN(group), SUM(MV_XRD_stat0_0.numAccesses) as numAccesses, SUM(MV_XRD_stat0_0.procTime) as procTime, SUM(MV_XRD_stat0_0.readBytes) as readBytes;

------------------- MV_XRD_DS_stat0_aggr1 -------------------
--TODO: looks like there are no '^cms' servers... anyway, PIG doesnt write '0' using (REGEX_EXTRACT(server_username, '^cms', 0) == '' ? 0 : 1) as isUSERCMS, used INDEXOF instead
MV_XRD_DS_stat0_aggr1_0 = FOREACH MV_XRD_stat0 GENERATE TDay, dsname as collName, (INDEXOF(server_username, 'cms', 0) == 0 ? 1 : 0) as isUSERCMS, readBytes, numAccesses, procTime, server_username;
MV_XRD_DS_stat0_aggr1_1 = GROUP MV_XRD_DS_stat0_aggr1_0 BY (TDay, collName, isUSERCMS);
MV_XRD_DS_stat0_aggr1 = FOREACH MV_XRD_DS_stat0_aggr1_1 { 
   aggr1_server_username_distinct = DISTINCT MV_XRD_DS_stat0_aggr1_0.server_username; 
   GENERATE FLATTEN(group), SUM(MV_XRD_DS_stat0_aggr1_0.readBytes) as readBytes, SUM(MV_XRD_DS_stat0_aggr1_0.numAccesses) as numAccesses, SUM(MV_XRD_DS_stat0_aggr1_0.procTime) as totCPU, COUNT(aggr1_server_username_distinct) as numUsers; 
};

------------------- MV_XRD_DS_stat0_aggr2 -------------------
MV_XRD_DS_stat0_aggr2_0 = FOREACH MV_XRD_stat0 GENERATE TDay, SUBSTRING(dsname, LAST_INDEX_OF(dsname, '/') + 1, 999) as collName, (INDEXOF(server_username, 'cms', 0) == 0 ? 1 : 0) as isUSERCMS, readBytes, numAccesses, procTime, server_username;
MV_XRD_DS_stat0_aggr2_1 = GROUP MV_XRD_DS_stat0_aggr2_0 BY (TDay, collName, isUSERCMS);
MV_XRD_DS_stat0_aggr2 = FOREACH MV_XRD_DS_stat0_aggr2_1 {
   aggr2_server_username_distinct = DISTINCT MV_XRD_DS_stat0_aggr2_0.server_username;
   GENERATE FLATTEN(group), SUM(MV_XRD_DS_stat0_aggr2_0.readBytes) as readBytes, SUM(MV_XRD_DS_stat0_aggr2_0.numAccesses) as numAccesses, SUM(MV_XRD_DS_stat0_aggr2_0.procTime) as totCPU, COUNT(aggr2_server_username_distinct) as numUsers;
};

------------------- MV_XRD_DS_stat0_aggr3 -------------------
MV_XRD_DS_stat0_aggr3_0 = FOREACH MV_XRD_stat0 GENERATE TDay, server_username, SUBSTRING(dsname, LAST_INDEX_OF(dsname, '/') + 1, 999) as collName, readBytes, numAccesses, procTime;
MV_XRD_DS_stat0_aggr3_1 = GROUP MV_XRD_DS_stat0_aggr3_0 BY (TDay, server_username, collName);
MV_XRD_DS_stat0_aggr3 = FOREACH MV_XRD_DS_stat0_aggr3_1 GENERATE FLATTEN(group), SUM(MV_XRD_DS_stat0_aggr3_0.readBytes) as readBytes, SUM(MV_XRD_DS_stat0_aggr3_0.numAccesses) as numAccesses, SUM(MV_XRD_DS_stat0_aggr3_0.procTime) as totCPU;

------------------- MV_XRD_DS_stat0_aggr4 -------------------
MV_XRD_DS_stat0_aggr4_0 = FOREACH MV_XRD_stat0 GENERATE TDay, SUBSTRING(dsname, 0, LAST_INDEX_OF(dsname, '/')) as collName, server_username, numAccesses, procTime, readBytes;
MV_XRD_DS_stat0_aggr4_1 = FOREACH MV_XRD_DS_stat0_aggr4_0 GENERATE TDay, SUBSTRING(collName, LAST_INDEX_OF(collName, '/') + 1, 999) as collName, server_username, numAccesses, procTime, readBytes, (INDEXOF(server_username, 'cms', 0) == 0 ? 1 : 0) as isUSERCMS;
MV_XRD_DS_stat0_aggr4_2 = GROUP MV_XRD_DS_stat0_aggr4_1 BY (TDay, collName, isUSERCMS);
MV_XRD_DS_stat0_aggr4 = FOREACH MV_XRD_DS_stat0_aggr4_2 {
   aggr4_server_username_distinct = DISTINCT MV_XRD_DS_stat0_aggr4_1.server_username;
   GENERATE FLATTEN(group), SUM(MV_XRD_DS_stat0_aggr4_1.readBytes) as readBytes, SUM(MV_XRD_DS_stat0_aggr4_1.numAccesses) as numAccesses, SUM(MV_XRD_DS_stat0_aggr4_1.procTime) as totCPU, COUNT(aggr4_server_username_distinct) as numUsers;
};

------------------- MV_DS -------------------
MV_DS_0 = FOREACH MV_XRD_DS_stat0_aggr1 GENERATE collName;
MV_DS_1 = GROUP MV_DS_0 BY (collName);
MV_DS_2 = FOREACH MV_DS_1 GENERATE FLATTEN(group);
MV_DS = ORDER MV_DS_2 BY $0 ASC;

------------------- MV_DataTier -------------------
MV_DataTier_0 = FOREACH MV_XRD_DS_stat0_aggr2 GENERATE collName;
MV_DataTier_1 = GROUP MV_DataTier_0 BY (collName);
MV_DataTier_2 = FOREACH MV_DataTier_1 GENERATE FLATTEN(group);
MV_DataTier = ORDER MV_DataTier_2 BY $0 ASC;

------------------- MV_DSName -------------------
MV_DSName_0 = FOREACH MV_XRD_DS_stat0_aggr4 GENERATE collName;
MV_DSName_1 = GROUP MV_DSName_0 BY (collName);
MV_DSName_2 = FOREACH MV_DSName_1 GENERATE FLATTEN(group);
MV_DSName = ORDER MV_DSName_2 BY $0 ASC;

------------------- MV_block_stat0_aggr_180_days -------------------
MV_block_stat0_aggr_180_days_0 = FILTER MV_XRD_stat0_pre BY DaysBetween(CurrentTime(), ToDate(TDay, 'yyyy/MM/dd')) < 180;
MV_block_stat0_aggr_180_days_1 = FOREACH MV_block_stat0_aggr_180_days_0 GENERATE GetWeek(ToDate(TDay, 'yyyy/MM/dd')) as week, 'T2_CH_CERN' as sitename, blockname as collName, numAccesses, procTime, readBytes;
MV_block_stat0_aggr_180_days_2 = GROUP MV_block_stat0_aggr_180_days_1 BY (week, sitename, collName);
MV_block_stat0_aggr_180_days = FOREACH MV_block_stat0_aggr_180_days_2 GENERATE FLATTEN(group), SUM(MV_block_stat0_aggr_180_days_1.numAccesses) as numAccesses, SUM(MV_block_stat0_aggr_180_days_1.procTime) as totCPU, SUM(MV_block_stat0_aggr_180_days_1.readBytes) as readBytes;

------------------- MV_block_stat0_aggr_12_months -------------------
MV_block_stat0_aggr_12_months_0 = FILTER MV_XRD_stat0_pre BY DaysBetween(CurrentTime(), ToDate(TDay, 'yyyy/MM/dd')) < 365;
MV_block_stat0_aggr_12_months_1 = FOREACH MV_block_stat0_aggr_12_months_0 GENERATE GetWeek(ToDate(TDay, 'yyyy/MM/dd')) as week, 'T2_CH_CERN' as sitename, blockname as collName, numAccesses, procTime, readBytes;
MV_block_stat0_aggr_12_months_2 = GROUP MV_block_stat0_aggr_12_months_1 BY (week, sitename, collName);
MV_block_stat0_aggr_12_months = FOREACH MV_block_stat0_aggr_12_months_2 GENERATE FLATTEN(group), SUM(MV_block_stat0_aggr_12_months_1.numAccesses) as numAccesses, SUM(MV_block_stat0_aggr_12_months_1.procTime) as totCPU, SUM(MV_block_stat0_aggr_12_months_1.readBytes) as readBytes;

------------------- MV_block_stat0_last_access -------------------
MV_block_stat0_last_access_0 = FOREACH MV_XRD_stat0_pre GENERATE GetWeek(ToDate(TDay, 'yyyy/MM/dd')) as week, 'T2_CH_CERN' as sitename, blockname as collName;
MV_block_stat0_last_access_1 = GROUP MV_block_stat0_last_access_0 BY (sitename, collName);
MV_block_stat0_last_access = FOREACH MV_block_stat0_last_access_1 GENERATE MAX(MV_block_stat0_last_access_0.week) as TDAY, FLATTEN(group);

------------------- MV_XRD_stat2 -------------------
MV_XRD_stat2_0 = FILTER T_XRD_RAW_FILE BY INDEXOF(file_lfn, '/replicate') == -1;
MV_XRD_stat2_1 = FOREACH MV_XRD_stat2_0 GENERATE TDay, readBytes, SUBSTRING(file_lfn, 0, LAST_INDEX_OF(file_lfn, '/') + 1) as dirName;
--MV_XRD_stat2_1 = FOREACH MV_XRD_stat2_0 GENERATE TDay, readBytes, (INDEXOF(file_lfn, '/eos/cms/') == 0 and INDEXOF(file_lfn, '/eos/cms/opstest/') == -1 ? SUBSTRING(file_lfn, 8, LAST_INDEX_OF(file_lfn, '/') + 1) :  SUBSTRING(file_lfn, 0, LAST_INDEX_OF(file_lfn, '/') + 1) ) as dirName;
MV_XRD_stat2_2 = GROUP MV_XRD_stat2_1 BY (TDay, dirName);
MV_XRD_stat2 = FOREACH MV_XRD_stat2_2 GENERATE FLATTEN(group), SUM(MV_XRD_stat2_1.readBytes) as readBytes, COUNT(MV_XRD_stat2_1.dirName) as nEntries;

------------------- V_XRD_stat2_aggr1 -------------------
V_XRD_stat2_aggr1_0 = GROUP MV_XRD_stat2 BY (dirName);
V_XRD_stat2_aggr1_1 = FOREACH V_XRD_stat2_aggr1_0 GENERATE MIN(MV_XRD_stat2.TDay) as min_tday, MAX(MV_XRD_stat2.TDay) as max_tday, FLATTEN(group), SUM(MV_XRD_stat2.readBytes)/1000/1000 as readBytes, COUNT(MV_XRD_stat2.nEntries) as read_acc;
V_XRD_stat2_aggr1 = ORDER V_XRD_stat2_aggr1_1 BY $2 ASC;

------------------- STORE OUTPUT DATA -------------------
STORE MV_xrdmon_rates_x_H into '$output/MV_xrdmon_rates_x_H' USING PigStorage(',');
--STORE MV_XRD_stat0_pre into '$output/MV_XRD_stat0_pre' USING PigStorage(',');
--STORE V_XRD_LFC_aggr1 into '$output/V_XRD_LFC_aggr1' USING PigStorage(',');
--STORE MV_XRD_stat0 into '$output/MV_XRD_stat0' USING PigStorage(',');
--STORE MV_XRD_DS_stat0_aggr1 into '$output/MV_XRD_DS_stat0_aggr1' USING PigStorage(',');
--STORE MV_XRD_DS_stat0_aggr2 into '$output/MV_XRD_DS_stat0_aggr2' USING PigStorage(',');
--STORE MV_XRD_DS_stat0_aggr3 into '$output/MV_XRD_DS_stat0_aggr3' USING PigStorage(',');
--STORE MV_XRD_DS_stat0_aggr4 into '$output/MV_XRD_DS_stat0_aggr4' USING PigStorage(',');
--STORE MV_DS into '$output/MV_DS' USING PigStorage(',');
--STORE MV_DataTier into '$output/MV_DataTier' USING PigStorage(',');
--STORE MV_DSName into '$output/MV_DSName' USING PigStorage(',');
--STORE MV_block_stat0_aggr_12_months into '$output/MV_block_stat0_aggr_12_months' USING PigStorage(',');
--STORE MV_block_stat0_last_access into '$output/MV_block_stat0_last_access' USING PigStorage(',');
--STORE MV_XRD_stat2 into '$output/MV_XRD_stat2' USING PigStorage(',');
--STORE V_XRD_stat2_aggr1 into '$output/V_XRD_stat2_aggr1' USING PigStorage(',');
