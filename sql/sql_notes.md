# SQL

## DBMS vs RDBMS

- database: structured collection of data
- DBMS: allow user to interact with database
- two types:
  - RDBMS: data stores in relations (tables)
    - stores data in row-based table structure (header: column names)
    - use ACID
      - A (atomicity): transaction that are completely done or failed
      - C (consistency): ensure that the data must meet all the validation rules
      - I (isolation): concurrency control
      - D (durability): if a transaction has been committed, it will occur whatever may come in between such as power loss, crash or any sorrt oof error
    - can be normalized
  - Non-RDBMS: key-value, columnar, graph based, ...
- sql: the core of relational database which is used for accessing and managing database

## SQL language

![SQL Command](https://media.geeksforgeeks.org/wp-content/uploads/sql-commands.jpg)

- DDL: definition; perform operations on the database/table level (CREATE, ALTER, DROP, TRUNCATE)
- DML: data manipulation; SELECT, INSERT, DELETE ...
- DCL: control access; GRANT, REVOKE
- TCL: transaction control; COMMIT, ROLLBACK...

### SELECT

- get 0 or more rows from one or more db tables or views
- most frequent DML
- SELECT queries define a result set, but not how to calculate it, because SQL is a declarative programming language
- common clause:
  - WHERE: filter records based on certain criteria (cannot filter aggregated records)
  - HAVING: filter records after applying group by. (filter aggregated records)
  - ORDER BY: sort data base on specified field(s)
  - GROUP BY: group entries with identical data and may be used with aggregation methods to obtain summarised database results

### UNION, UNION ALL, MINUS, INTERSECT

- `UNION`: combine the results of two tables while `removing duplicate entries`
- `UNION ALL`: combine the results without removing duplicates
- `MINUS`: return rows from the first query but not from the second one
- `INTERSECT`: fetch common records from both of the SELECT statements
- edge case check: num of columns, column data types, columns in the same order

### NVL(), IFNULL(), ISNULL()

- replace null values with a default value
- NVL() used in Oracle
- IFNULL() used in MySQL
- ISNULL(NULL, 500) used in SQL Server
  - if the expression is NULL, then return 500

### Character-manipulation functions

- CONCAT(s1, s2, ..., sn): add two or more strings together
- SUBSTRING(string, start_idx, length): return string[start_idx:start_idx+length]
- LENGTH()
- INSTR(string1, string2): MySQL statement, return the first index of string2 in string1
- LPAD(string, total_length, padding_string): MySQL statement, left pad string with padding_string to reach the total_length
- RPAD(): MySQL statement
- TRIM(char FROM string): removes the space(default)/specified chars from the start or end of a string
- REPLACE(string, old_string, new_string): replace all occurrences of old_string with new_string

### RANK() vs. DENSE_RANK()

- RANK() OVER (PARTITION BY partition_col ORDER BY orderby_col)
  - the rank of each row within the ordered partition
  - if rows have the same rank, `the next number = current rank + number of duplicates`
- DENSE_RANK()
  - rank without gap
  - consecutive ranking

### CASE WHEN in SQL Server

- used to construct logic that one column's value is determined by the values of other columns

```sql
CASE
  WHEN condition1 THEN result1
  WHEN condition2 THEN result2
  WHEN conditionN THEN resultN
  ELSE result
END;
```

### Date functions

- return datatime parts
  - DATENAME(date_part, input_date): return a string type
  - DATEPART(date_part, input_date): return an integer
  - DAY(input_date), MONTH(input_date), YEAR(input_date)
- return system datetime
  - CURRENT_TIMESTAMP: return the current timestamp w/o time zone offset
  - GETUTCDATE()
  - GETDATE(): return datetime type
  - SYSDATETIME(): return the current system datetime with more precison, datetime2 type
  - SYSUTCDATETIME()
  - SYSDATETIMEOFFSET(): return system datetime with tz offset

|Function|Return|
|:--|:--|
|GETDATE()|2021-10-28 09:52:20.477|
|GETUTCDATE()|2021-10-28 16:52:20.473|
|SYSDATETIME()|2021-10-28 09:52:20.4845997|
|SYSUTCDATETIME()|2021-10-28 16:52:20.4845997|
|SYSDATETIMEOFFSET()|2021-10-28 09:52:20.4845997 -07:00|

- return datetime difference
  - DATEDIFF(date_part, start_date, end_date)
  - DATEDIFF_BIG: return a bigint type
- construct datetime
  - DATEFROMPARTS(year:int, month:int, day:int) -> DATE type
    - return null if some of inputs are null
    - return error if negative, invalid inputs (like month is 20)
  - DATETIME2FROMPARTS(year, month, day, hour, minute, seconds, fractions, precision) -> datetime2 type
    - fraction: the input number after demical point
    - precision is the number of digits required after demical point
  - DATTIMEOFFSETFROMPARTS( year, month, day, hour, minute, seconds, fractions, hour_offset, minute_offset, precision) -> datetimeoffset type
  - TIMEFROMPARTS (hour, minute, seconds, fractions, precision) -> time type
- validate datetime
  - ISDATE(string/int): return 1 if date 0 otherwise
- modify datetime
  - DATEADD(date_part:str, value:int, input_date:str)
  - EOMONTH(start_date, [, offset])
    - offset: number of months to add to the start_date
  - SWITCHOFFSET(expression:datetimeoffest, tz)
  - TODATETIMEOFFSET(expression:datetime, tz)

- convert datetime to date
  - CONVERT(data_type, expression [, style]):
    - style: can be used for datetime (datetime, string type) convertion
  - CAST(expression AS data_type)

```sql
CONVERT(DATE, GETDATE())
CAST(GETDATE() AS DATE)
-- return 30 days before the current date
DATEADD(day, -30, GETDATE())
```

### SQL Join

- inner join: return records that have matching values in both tables
- left join: return all records from the left table, and matched records from the right table
- right join: return all records from the right table, and matched records from the left table
- full join: return all records when there is a match in either left or right table

### CHAR vs VARCHAR datatype

- CHAR: fix length strings
- VARCHAR(n): variable length strings, max length is n

### DELETE, TRUNCATE, DROP

- DELETE
  - DML, can apply WHERE
  - remove certain data from table row by row
  - slower that TRUNCATE, log all deleted rows in transcation logs
  - can rollback after using DELETE statement
- TRUNCATE
  - DDL; cannot apply WHERE
  - remove all the data from table
  - faster than DELETE
  - cannot rollback data
- DROP
  - DDL
  - remove table definition and its contents

### COALESCE

- returns the first non-null value in a list

```sql
SELECT COALESCE(NULL, 1, 2, 'W3Schools.com');
-- return 1
```

### LIKE

- `%`: zero or more chars
- `_`: exactly one char

### VIEW

- virtual table which consists of a subset fo data contained in a table
- take less space to store (view are not permanent table)
- restrict access to data
- make complex queries simple
- ensure data independence
- provide different views of the same data

### STUFF and REPLACE function

- STUFF(string, start_idx, length, replacement_chars): overwrite existing char or insert a string into another string
- REPLACE(string, search_string, replacement_string): replace the existing char of all the occurrences

### Cursor

- opening a cursor on a result set allows `processing the data one row at a time`
- can assign a cursor to a variable or parameter with a cursor data type
- steps:
  - after variable declaration, `DECLARE` a cursor, SELECT statement must always be coupled with the cursor def
  - to start the result set, move the cursor over it
  - before obtaining rows from the data, `OPEN` must be executed
  - to retreive and go to the next row, use `FETCH`
  - to disable the cursor, use `CLOSE`
  - use `DEALLOCATE` to remove the cursor definition and free up the resources connected to it

## Reference

1. https://www.edureka.co/blog/interview-questions/sql-interview-questions