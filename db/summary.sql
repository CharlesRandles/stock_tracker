select symbol, 
       sum(holding), 
       sum(holding * purchase_price) as paid,
       sum(offer * holding) as value
from cache
group by symbol
order by symbol;
