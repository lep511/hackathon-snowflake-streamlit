class SQLExamples():
  def __init__(self):
    self.sql_example = """-- Replace this text with your code:
SELECT
  CASE
    WHEN salary <= 750000 THEN 'low'
    WHEN salary > 750000 AND salary <= 100000 THEN 'medium'
    WHEN salary > 100000 THEN 'high'
  END AS salary_category,
  COUNT(*) AS number_of_employees
FROM    employee
GROUP BY
  CASE
    WHEN salary <= 750000 THEN 'low'
    WHEN salary > 750000 AND salary <= 100000 THEN 'medium'
    WHEN salary > 100000 THEN 'high'
END
"""
    self.sql_postgres = """- Replace this text with your code:
SELECT
  product,
  grp_name,
  price,
  RANK() OVER (
    PARTITION BY grp_name
    ORDER BY price
  ) AS ranking
FROM
  substances
INNER JOIN products USING (productid);
"""
    self.sql_mysql = """-- Replace this text with your code:
SELECT Department,
       CASE
           WHEN COUNT(*) % 2 = 0 THEN AVG(Salary)
           ELSE
               (SELECT Salary
                FROM Employees e2
                WHERE e1.Department = e2.Department
                ORDER BY Salary
                LIMIT 1 OFFSET COUNT(*) / 2)
       END AS MedianSalary
FROM Employees e1
GROUP BY Department;
"""
    self.sql_bigquery = """-- Replace this text with your code:
SELECT
  product,
  grp_name,
  price,
  RANK() OVER (
    PARTITION BY grp_name
    ORDER BY price
  ) AS ranking
FROM
  substances
INNER JOIN products USING (productid);
"""
    self.sql_sqlserver = """-- Replace this text with your code:
DECLARE @emp_id INT = 9;
SELECT orderyear, COUNT(DISTINCT custid) AS cust_count
FROM (    
    SELECT YEAR(orderdate) AS orderyear, custid
    FROM Sales.Orders
    WHERE empid=@emp_id
) AS derived_year
GROUP BY orderyear;
GO
"""

    self.sql_athena = """-- Replace this text with your code:
WITH dataset AS (
  SELECT ARRAY[
    CAST(
      ROW('aws.amazon.com', ROW(true)) AS ROW(hostname VARCHAR, flaggedActivity ROW(isNew BOOLEAN))
    ),
    CAST(
      ROW('news.cnn.com', ROW(false)) AS ROW(hostname VARCHAR, flaggedActivity ROW(isNew BOOLEAN))
    ),
    CAST(
      ROW('netflix.com', ROW(false)) AS ROW(hostname VARCHAR, flaggedActivity ROW(isNew BOOLEAN))
    )
  ] as items
)
SELECT sites.hostname, sites.flaggedActivity.isNew
FROM dataset, UNNEST(items) t(sites)
WHERE sites.flaggedActivity.isNew = true
"""

    self.sql_redshift = """-- Replace this text with your code:
SELECT "table" tablename, skew_rows,
  ROUND(CAST(max_blocks_per_slice AS FLOAT) /
  GREATEST(NVL(min_blocks_per_slice,0)::int,1)::FLOAT,5) storage_skew,
  ROUND(CAST(100*dist_slice AS FLOAT) /
  (SELECT COUNT(DISTINCT slice) FROM stv_slices),2) pct_populated
FROM svv_table_info ti
  JOIN (SELECT tbl, MIN(c) min_blocks_per_slice,
          MAX(c) max_blocks_per_slice,
          COUNT(DISTINCT slice) dist_slice
        FROM (SELECT b.tbl, b.slice, COUNT(*) AS c
              FROM STV_BLOCKLIST b
              GROUP BY b.tbl, b.slice)
        WHERE tbl = 240791 GROUP BY tbl) iq ON iq.tbl = ti.table_id;
"""


  def get_sql_example(self, sql_engine):
    if sql_engine == "MySQL":
      return self.sql_mysql
    elif sql_engine == "PostgreSQL":
      return self.sql_postgres
    elif sql_engine == "GCP BigQuery":
      return self.sql_bigquery
    elif sql_engine == "Azure SQL Server":
      return self.sql_sqlserver
    elif sql_engine == "Amazon Athena":
      return self.sql_athena
    elif sql_engine == "Amazon Redshift":
      return self.sql_redshift
    else:
      return self.sql_example