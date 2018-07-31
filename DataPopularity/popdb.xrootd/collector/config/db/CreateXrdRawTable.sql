CREATE TABLE "T_XRD_RAW_FILE"
(
user_dn   		VARCHAR2(128 BYTE) DEFAULT 'unknown' ,
user_vo   		VARCHAR2(128 BYTE) DEFAULT 'unknown' ,
file_lfn  		VARCHAR2(4000 BYTE) DEFAULT 'unknown' ,
client_host   		VARCHAR2(128 BYTE) DEFAULT 'unknown' ,
client_domain 		VARCHAR2(128 BYTE) DEFAULT 'unknown' ,
server_host   		VARCHAR2(128 BYTE) DEFAULT 'unknown' ,
server_domain     	VARCHAR2(128 BYTE) DEFAULT 'unknown' ,
server_username   	VARCHAR2(128 BYTE) DEFAULT 'unknown' ,
unique_id 		NUMBER(16,0)  DEFAULT 0 , 
start_time		NUMBER(16,0)  DEFAULT 0 , 
end_time   		NUMBER(16,0)  DEFAULT 0 ,
write_bytes_at_close 	NUMBER(16,0)  DEFAULT 0 , 
read_bytes_at_close  	NUMBER(16,0)  DEFAULT 0 , 

--file_size             NUMBER(16,0)  DEFAULT 0 , 

--read_vector_bytes                NUMBER(16,0) DEFAULT 0,
--read_single_average              NUMBER(16,0) DEFAULT 0,
--read_vector_count_average                NUMBER(16,0) DEFAULT 0,
--read_vector_min          NUMBER(16,0) DEFAULT 0,
--read_vector_count_max            NUMBER(16,0) DEFAULT 0,
--read_min                 NUMBER(16,0) DEFAULT 0,
--read_bytes               NUMBER(16,0) DEFAULT 0,
--read_vector_count_min            NUMBER(16,0) DEFAULT 0,
--read_vector_average              NUMBER(16,0) DEFAULT 0,
--read_vector_sigma                NUMBER(16,0) DEFAULT 0,
--read_max                 NUMBER(16,0) DEFAULT 0,
--read_vector_operations           NUMBER(16,0) DEFAULT 0,
--read_operations          NUMBER(16,0) DEFAULT 0,
--read_single_min          NUMBER(16,0) DEFAULT 0,
--read_single_bytes                NUMBER(16,0) DEFAULT 0,
--read_single_max          NUMBER(16,0) DEFAULT 0,
--read_average             NUMBER(16,0) DEFAULT 0,
--read_sigma               NUMBER(16,0) DEFAULT 0,
--read_vector_count_sigma          NUMBER(16,0) DEFAULT 0,
--read_single_sigma                NUMBER(16,0) DEFAULT 0,
--read_single_operations           NUMBER(16,0) DEFAULT 0,
--read_vector_max          NUMBER(16,0) DEFAULT 0,

starttimestamp date DEFAULT( to_date('19700101','YYYYMMDD') ) NOT NULL ,
endtimestamp date DEFAULT( to_date('19700101','YYYYMMDD') ) NOT NULL ,
inserttimestamp date DEFAULT( to_date('19700101','YYYYMMDD') ) NOT NULL, 
CONSTRAINT "PK_XRD_RAW_FILE" PRIMARY KEY (unique_id,start_time,file_lfn)   
)
COMPRESS
PARTITION BY RANGE(endtimestamp)
(
PARTITION xrd_files_01_01_2012 VALUES LESS THAN(TO_DATE('01/01/2012','DD/MM/YYYY')) tablespace CMS_POPULARITY_SYSTEM_DATA2012
)
;


ALTER TABLE T_XRD_RAW_FILE SET INTERVAL(NUMTODSINTERVAL(1, 'day'));
ALTER TABLE T_XRD_RAW_FILE SET STORE IN (CMS_POPULARITY_SYSTEM_DATA2012);

create index IN_XRD_RAW_FILE_A on T_XRD_RAW_FILE ( endtimestamp );
create index IN_XRD_RAW_FILE_B on T_XRD_RAW_FILE ( inserttimestamp );




---drop table T_XRD_LAST_UID;

CREATE TABLE "T_XRD_LAST_UID"
(
last_inserttime    DATE DEFAULT  to_date('19700101','YYYYMMDD') NOT NULL ,   
updatetime    DATE DEFAULT  to_date('19700101','YYYYMMDD') NOT NULL  
)
;


--drop table T_XRD_LFC;
CREATE TABLE "T_XRD_LFC"
(
lfn  	    	VARCHAR2(4000 BYTE) DEFAULT 'unknown' ,
blockname   VARCHAR2(4000 BYTE) DEFAULT 'unknown' ,
dsname  		VARCHAR2(4000 BYTE) DEFAULT 'unknown' ,
fullName  	VARCHAR2(4000 BYTE) DEFAULT 'unknown' ,
CONSTRAINT "PK_XRD_LFC" PRIMARY KEY (fullName) 
)
;

commit;

create index IN_XRD_LFC_dsname on T_XRD_LFC ( dsname );
create index IN_XRD_LFC_lfn    on T_XRD_LFC ( lfn    );
commit;

CREATE TABLE "T_XRD_USERFILE"
(
lfn  	    	VARCHAR2(4000 BYTE) DEFAULT 'unknown' ,
username    VARCHAR2(256 BYTE) DEFAULT 'unknown' ,
CONSTRAINT "UC_XRD_USERFILE_1" UNIQUE (lfn,username) 
)
;

ALTER TABLE T_XRD_USERFILE
ADD CONSTRAINT "PK_XRD_USERFILE_1" PRIMARY KEY (lfn);

create index IN_XRD_USERFILE_username on T_XRD_USERFILE ( username );

insert into  T_XRD_LAST_UID (LAST_INSERTTIME, updatetime)  values(to_date('19700101','YYYYMMDD'), to_date('19700101','YYYYMMDD') );
insert into  T_XRD_LAST_UID (LAST_INSERTTIME, updatetime)  values(to_date('20120131','YYYYMMDD'), to_date('19700101','YYYYMMDD') );

 ---update T_XRD_LAST_UID set unique_id=1323912186000000;
select * from T_XRD_LAST_UID;


-- To create the table for operation of fileToDSAssociation
CREATE TABLE "T_XRD_SELECT_FILES_TMP"
  (
    "FILE_LFN" VARCHAR2(4000 BYTE)
  );
  
  
    
--drop table T_MVREFRESH_LOG;
CREATE TABLE "T_MVREFRESH_LOG"
(
unique_id 		NUMBER(16,0)  DEFAULT 0 , 
mvName       VARCHAR2(4000 BYTE) DEFAULT 'unknown' ,
starttime    DATE DEFAULT  to_date('19700101','YYYYMMDD') NOT NULL ,   
endtime      DATE DEFAULT  to_date('19700101','YYYYMMDD') NOT NULL  
)
;

CREATE SEQUENCE supplier_seq
    MINVALUE 1
    START WITH 1
    INCREMENT BY 1;


insert into  T_MVREFRESH_LOG (unique_id, mvName, starttime, endtime)  values(1,'test',to_date('19700101','YYYYMMDD'), to_date('19700101','YYYYMMDD') );
update T_MVREFRESH_LOG set starttime=sysdate;
update T_MVREFRESH_LOG set endtime=sysdate;

select max(unique_id) from T_MVREFRESH_LOG;

-- Add parallelism to tables to speed up refresh of materialized views
ALTER TABLE T_XRD_LFC PARALLEL (DEGREE 4); 
ALTER TABLE T_XRD_RAW_FILE PARALLEL (DEGREE 4); 
ALTER TABLE T_XRD_USERFILE PARALLEL (DEGREE 4); 

