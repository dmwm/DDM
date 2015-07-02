-- define procedures
-- MVREFRESH: refresh materialized views
-- arguments: mvlist: list of MVs to refresh; mvarg: refresh mode ('F' for fast, etc.)
CREATE OR REPLACE PROCEDURE MVREFRESH (mvlist IN VARCHAR2, mvarg IN VARCHAR2:= NULL ) IS
BEGIN
  DBMS_MVIEW.REFRESH(mvlist, mvarg);
END MVREFRESH;
/
