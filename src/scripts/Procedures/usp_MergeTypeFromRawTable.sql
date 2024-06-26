CREATE OR REPLACE PROCEDURE WH_CRYPTO.DBO.MERGETYPESFROMRAWTABLE()
RETURNS VARCHAR
EXECUTE AS OWNER
AS
$$
BEGIN
MERGE INTO WH_CRYPTO.DIM.TYPES AS TGT
USING (SELECT DISTINCT TYPE FROM WH_CRYPTO.RAW.COINRANKING WHERE TYPE IS NOT NULL) AS SRC
ON TGT.TYPE = SRC.TYPE
WHEN NOT MATCHED THEN
	INSERT (TYPE, CREATEDAT)
	VALUES (SRC.TYPE, GETDATE());
RETURN 'Data Loaded successfully';
END;
$$;