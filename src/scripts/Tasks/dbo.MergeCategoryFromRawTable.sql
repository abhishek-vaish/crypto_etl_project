CREATE OR REPLACE TASK WH_CRYPTO.DBO.MERGECATEGORYFROMRAWTABLE
WAREHOUSE=COMPUTE_WH
AFTER WH_CRYPTO.DBO.MERGEFILETORAWTABLE
AS
CALL WH_CRYPTO.DBO.MERGECATEGORYFROMRAWTABLE();