CREATE OR REPLACE TASK WH_CRYPTO.DBO.MERGECOINSFROMRAWTABLE
WAREHOUSE=COMPUTE_WH
AFTER WH_CRYPTO.DBO.MERGETYPEFROMRAWTABLE, WH_CRYPTO.DBO.MERGECATEGORYFROMRAWTABLE
AS
CALL WH_CRYPTO.DBO.USP_MERGECOINSFROMRAWTABLE();