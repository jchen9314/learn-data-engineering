# dbx_de_prof_exam_prep

## Security

### Cluster access-control

- 2 types of permissions
  - allow cluster creation: admin controls who can create clusters 
  - cluster-level permission
    - view Spark UI, cluster metrics, driver logs -> min permission: Can Attach To
    - terminate, start, restart cluster -> min permission: Can Restart
    - Others -> min permission: Can Manage
    <br>
    
    | Ability                                     | No Permissions | Can Attach To | Can Restart | Can Manage |
    |:---------------------------------------------|:----------------:|:---------------:|:-------------:|:------------:|
    | Attach notebook to cluster                  |                | x             | x           | x          |
    | View Spark UI, cluster metrics, driver logs |                | x             | x           | x          |
    | Terminate, start, restart cluster           |                |               | x           | x          |
    | Edit cluster                                |                |               |             | x          |
    | Attach library to cluster                   |                |               |             | x          |
    | Resize cluster                              |                |               |             | x          |
    | Modify permissions                          |                |               |             | x          |

### Set Operators
- INTERSECT, UNION, EXCEPT
- When chaining set operations INTERSECT has a higher precedence than UNION and EXCEPT.

#### EXCEPT ALL/DISTINCT
- Returns the rows in subquery1 which are not in subquery2.
  - If ALL is specified, each row in subquery2 will remove exactly one of possibly multiple matches from subquery1.
  - DISTINCT is the default option, duplicate rows are removed from subquery1 before applying the operation
- You can specify MINUS as a syntax alternative for EXCEPT.

## Testing and Deployment

### Magic command

- %sh: it executes shell code only on the local driver machine which leads to significant performance overhead; it runs only on the Apache Spark driver, not on the worker nodes.

## Improving performance

### Data skipping

- Delta transaction logs capture stats for each data file of the table
- Each transaction log file:
  - total number of records
  - min, max value in each column of the first 32 columns of the table
  - null value counts in each column of the first 32 columns of the table
 
## Modeling data management solution

### Upsert from streaming queries using foreachBatch

```py
# Function to upsert microBatchOutputDF into Delta table using merge
def upsertToDelta(microBatchOutputDF, batchId):
  # Set the dataframe to view name
  microBatchOutputDF.createOrReplaceTempView("updates")

  # Use the view name to apply MERGE
  # NOTE: You have to use the SparkSession that has been used to define the `updates` dataframe

  # In Databricks Runtime 10.5 and below, you must use the following:
  # microBatchOutputDF._jdf.sparkSession().sql("""
  microBatchOutputDF.sparkSession.sql("""
    MERGE INTO aggregates t
    USING updates s
    ON s.key = t.key
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
  """)

# Write the output of a streaming aggregation query into Delta table
(streamingAggregatesDF.writeStream
  .format("delta")
  .foreachBatch(upsertToDelta)
  .outputMode("update")
  .start()
)
```

