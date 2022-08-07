SELECT startDate, endDate, 
  DATEDIFF( endDate, startDate ) AS diff_days,
  CAST( months_between( endDate, startDate ) AS INT ) AS diff_months      
from yourTable
ORDER BY 1;