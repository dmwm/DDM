--
-- Instruction creation for T_RAW_EOS
-- An local index is first built for (unique_id, end_date)
-- and then used as primary key index (allows a partitioned PK)
--
CREATE TABLE T_RAW_CMSSW(
    UNIQUE_ID                 VARCHAR2(1000 BYTE) NOT NULL ENABLE,
    FILE_LFN                  VARCHAR2(1000 BYTE),
    FILE_SIZE                 NUMBER,
    CLIENT_DOMAIN             VARCHAR2(1000 BYTE),
    CLIENT_HOST               VARCHAR2(1000 BYTE),
    SERVER_DOMAIN             VARCHAR2(1000 BYTE),
    SERVER_HOST               VARCHAR2(1000 BYTE),
    SITE_NAME                 VARCHAR2(1000 BYTE),
    READ_BYTES_AT_CLOSE       NUMBER,
    READ_BYTES                NUMBER,
    READ_SINGLE_BYTES         NUMBER,
    READ_SINGLE_OPERATIONS    NUMBER,
    READ_SINGLE_AVERAGE       NUMBER,
    READ_SINGLE_SIGMA         NUMBER,
    READ_VECTOR_BYTES         NUMBER,
    READ_VECTOR_OPERATIONS    NUMBER,
    READ_VECTOR_AVERAGE       NUMBER,
    READ_VECTOR_SIGMA         NUMBER,
    READ_VECTOR_COUNT_AVERAGE NUMBER,
    READ_VECTOR_COUNT_SIGMA   NUMBER,
    FALLBACK                  CHAR(1 BYTE),
    USER_DN                   VARCHAR2(1000 BYTE),
    APP_INFO                  VARCHAR2(1000 BYTE),
    START_TIME                NUMBER,
    END_TIME                  NUMBER,
    START_DATE                DATE,
    END_DATE                  DATE NOT NULL,
    INSERT_DATE               DATE DEFAULT CAST(SYS_EXTRACT_UTC(SYSTIMESTAMP) AS DATE),
    CONSTRAINT T_RAW_CMSSW_PK PRIMARY KEY (UNIQUE_ID, END_DATE) 
  ) 
PARTITION BY RANGE(end_date) INTERVAL (NUMTODSINTERVAL(1,'DAY'))
(
  PARTITION part_01 VALUES LESS THAN (to_date('2012-01-01', 'YYYY-MM-DD') )
);

CREATE INDEX t_raw_cmssw_pk_idx ON t_raw_eos(unique_id, end_date) LOCAL;
CREATE INDEX t_raw_cmssw_start_date  ON t_raw_cmssw (start_date) LOCAL;
CREATE INDEX t_raw_cmssw_end_date    ON t_raw_cmssw (end_date) LOCAL;
CREATE INDEX t_raw_cmssw_insert_date ON t_raw_cmssw (insert_date) LOCAL;

--
-- Instruction creation for T_RAW_REJ
-- An local index is first built for (unique_id, end_date)
-- and then used as primary key index (allows a partitioned PK)
--
CREATE TABLE T_RAW_REJ(
    UNIQUE_ID                 VARCHAR2(1000 BYTE) NOT NULL ENABLE,
    FILE_LFN                  VARCHAR2(1000 BYTE),
    FILE_SIZE                 NUMBER,
    CLIENT_DOMAIN             VARCHAR2(1000 BYTE),
    CLIENT_HOST               VARCHAR2(1000 BYTE),
    SERVER_DOMAIN             VARCHAR2(1000 BYTE),
    SERVER_HOST               VARCHAR2(1000 BYTE),
    SITE_NAME                 VARCHAR2(1000 BYTE),
    READ_BYTES_AT_CLOSE       NUMBER,
    READ_BYTES                NUMBER,
    READ_SINGLE_BYTES         NUMBER,
    READ_SINGLE_OPERATIONS    NUMBER,
    READ_SINGLE_AVERAGE       NUMBER,
    READ_SINGLE_SIGMA         NUMBER,
    READ_VECTOR_BYTES         NUMBER,
    READ_VECTOR_OPERATIONS    NUMBER,
    READ_VECTOR_AVERAGE       NUMBER,
    READ_VECTOR_SIGMA         NUMBER,
    READ_VECTOR_COUNT_AVERAGE NUMBER,
    READ_VECTOR_COUNT_SIGMA   NUMBER,
    FALLBACK                  CHAR(1 BYTE),
    USER_DN                   VARCHAR2(1000 BYTE),
    APP_INFO                  VARCHAR2(1000 BYTE),
    START_TIME                NUMBER,
    END_TIME                  NUMBER,
    START_DATE                DATE,
    END_DATE                  DATE NOT NULL,
    INSERT_DATE               DATE DEFAULT CAST(SYS_EXTRACT_UTC(SYSTIMESTAMP) AS DATE),
    exception VARCHAR2(1000)
)
PARTITION BY RANGE(end_date) INTERVAL (NUMTODSINTERVAL(1,'DAY'))
(
  PARTITION part_01 VALUES LESS THAN (to_date('2012-01-01', 'YYYY-MM-DD') )
);

CREATE INDEX t_raw_rej_start_date  ON t_raw_rej (start_date) LOCAL;
CREATE INDEX t_raw_rej_end_date    ON t_raw_rej (end_date) LOCAL;
CREATE INDEX t_raw_rej_insert_date ON t_raw_rej (insert_date) LOCAL;
