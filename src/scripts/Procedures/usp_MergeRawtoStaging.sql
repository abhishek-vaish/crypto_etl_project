create or replace procedure dbo.mergerawtostaging()
returns varchar
execute as owner
as
$$
begin
create or replace temporary table transform as
select c.id as coinid,
    cr.marketcap,
    cr.price,
    cr.circulatingsupply,
    cr.totalsupply,
    cr.maxsupply,
    cr.volume,
    cr.percentchangesixmin,
    cr.percentchangeweek,
    cr.percentchangeday,
    cr.percentchangemonth,
    to_number(cr.dayhigh, 10, 2) as dayhigh,
    to_number(cr.daylow, 10, 2) as daylow,
    cr.lastupdated,
    to_date(cr.lastupdated) as filedate,
    cr.createdat
from wh_crypto.raw.coinranking cr
join wh_crypto.dim.coins c
on cr.name = c.name and cr.symbol = c.symbol
join wh_crypto.dim.categories cat
on c.categoryid = cat.id
join wh_crypto.dim.types t
on c.typeid = t.id;

insert into wh_crypto.dbo.cryptoranking
(   coinid,
    marketcap,
    price,
    circulatingsupply,
    totalsupply,
    maxsupply,
    volume,
    percentchangesixmin,
    percentchangeweek,
    percentchangeday,
    percentchangemonth,
    dayhigh,
    daylow,
    lastupdated,
    filedate,
    createdat
)
select * from transform;

truncate table wh_crypto.raw.coinranking;

return 'Data Loaded Sucessfully';
end;
$$;