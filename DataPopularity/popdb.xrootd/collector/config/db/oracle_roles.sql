set serveroutput on size 100000

DECLARE
  role_name VARCHAR2 (100) := 'CMS_EOS_POPULARITY_MV_READER';
BEGIN
  execute immediate 'CREATE ROLE ' || role_name;
  FOR o IN (SELECT object_name name FROM user_objects where object_type = 'MATERIALIZED VIEW') LOOP
    dbms_output.put_line ('Granting SELECT on materialized view ' || o.name || ' to role ' || role_name);
    execute immediate 'GRANT SELECT ON ' || o.name || ' TO ' || role_name;
  END LOOP;
END;
/
