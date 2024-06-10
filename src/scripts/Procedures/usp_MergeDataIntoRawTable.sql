CREATE OR REPLACE PROCEDURE wh_crypto.dbo.usp_MergeDataIntoRawTable()
RETURNS VARCHAR
EXECUTE AS OWNER
AS
$$
BEGIN
create or replace temporary table jsonfileData as
WITH CTE AS(
select $1:data
from @WH_CRYPTO.RAW.STG_CRYPTORANKING/Cryptoranking/Data/FilesForProcessing/
(PATTERN=>".*Cryptoranking.*.json.gz",
FILE_FORMAT=>WH_CRYPTO.RAW.JSON_FILE_FORMAT)
) SELECT
    value:rank::varchar as rank,
    value:name::varchar as name,
    value:symbol::varchar as symbol,
    value:type::varchar as type,
    value:category::varchar as category,
    value:images:"60x60"::varchar as images,
    value:values:USD:marketCap::varchar as marketcap,
    value:values:USD:price::varchar as price,
    value:circulatingSupply::varchar as circulatingsupply,
    value:totalSupply::varchar as totalsupply,
    value:maxSupply::varchar as maxsupply,
    value:values:USD:"volume24h"::varchar as volume,
    value:values:USD:"percentChange6m"::varchar as percentagechangesixmin,
    value:values:USD:"percentChange7d"::varchar as percentagechangeweek,
    value:values:USD:"percentChange24h"::varchar as percentagechangeday,
    value:values:USD:"percentChange30d"::varchar as percentagechangemonth,
    value:values:USD:"high24h"::varchar as dayhigh,
    value:values:USD:"low24h"::varchar as daylow,
    value:lastUpdated::varchar as lastupdated
FROM TABLE(FLATTEN(input => SELECT * FROM CTE));

INSERT INTO WH_CRYPTO.RAW.COINRANKING (
    RANK,
    NAME,
    SYMBOL,
    TYPE,
    CATEGORY,
    IMAGE,
    MARKETCAP,
    PRICE,
    CIRCULATINGSUPPLY,
    TOTALSUPPLY,
    MAXSUPPLY,
    VOLUME,
    PERCENTCHANGESIXMIN,
    PERCENTCHANGEWEEK,
    PERCENTCHANGEDAY,
    PERCENTCHANGEMONTH,
    DAYHIGH,
    DAYLOW,
    LASTUPDATED
)
SELECT * FROM jsonfileData;

RETURN 'Data Loaded';
END;
$$;