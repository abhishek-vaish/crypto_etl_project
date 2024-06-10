create or replace TABLE WH_CRYPTO.RAW.COINRANKING (
	ID NUMBER(38,0) NOT NULL IDENTITY(1, 1),
	RANK NUMBER(38,0),
	NAME VARCHAR(255),
	SYMBOL VARCHAR(50),
	TYPE VARCHAR(255),
	CATEGORY VARCHAR(255),
	IMAGE VARCHAR(255),
	MARKETCAP VARCHAR(255),
	PRICE VARCHAR(255),
	CIRCULATINGSUPPLY VARCHAR(255),
	TOTALSUPPLY VARCHAR(255),
	MAXSUPPLY VARCHAR(255),
	VOLUME VARCHAR(255),
	PERCENTCHANGESIXMIN VARCHAR(50),
	PERCENTCHANGEWEEK VARCHAR(50),
	PERCENTCHANGEDAY VARCHAR(50),
	PERCENTCHANGEMONTH VARCHAR(50),
	DAYHIGH VARCHAR(50),
	DAYLOW VARCHAR(50),
	LASTUPDATED TIMESTAMP_NTZ(9),
	CREATEDAT TIMESTAMP_NTZ(9) DEFAULT GETDATE(),
	primary key (ID)
);