create or replace TABLE WH_CRYPTO.DBO.CRYPTORANKING (
	ID NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	COINID NUMBER(38,0),
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
	FILEDATE TIMESTAMP_NTZ(9),
	CREATEDAT TIMESTAMP_NTZ(9),
	primary key (ID),
	foreign key (COINID) references WH_CRYPTO.DIM.COINS(ID)
);