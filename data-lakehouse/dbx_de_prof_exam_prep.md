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

### Job permission
- Groups cannot be owners of jobs, must be an individual user

### Secret access permission

- MANAGE: allow to change ACLs, and read and write to this secret scope
- WRITE: allow to read and write to this secret scope
- READ: allow to read this secret scope and list what secrets are available

### Set Operators
- INTERSECT, UNION, EXCEPT
- When chaining set operations INTERSECT has a higher precedence than UNION and EXCEPT.

#### EXCEPT ALL/DISTINCT
- Returns the rows in subquery1 which are not in subquery2.
  - If ALL is specified, each row in subquery2 will remove exactly one of possibly multiple matches from subquery1.
  - DISTINCT is the default option, duplicate rows are removed from subquery1 before applying the operation
- You can specify MINUS as a syntax alternative for EXCEPT.

### Table deletion

- deleting data does not delete the data files from the table directory. Instead, it creates a copy of the affected files without these deleted records. So, to fully commit these deletes, you need to run VACUUM commands on the customers table.

### Dynamic view
#### column control

- only admin can see values in the email column

```sql
CREATE OR REPLACE VIEW customers_vw AS
SELECT
  customer_id,
  CASE
    WHEN IS_MEMBER('admin') THEN email
    ELSE 'REDACTED'
  END AS email
FROM customers_silver
```

#### row control

- admin can view all the data whereas others can only view a subset of the data

```sql
CREATE OR REPLACE VIEW customers_fr_vw AS
SELECT * FROM customers_vw
WHERE
  CASE
    WHEN is_member('admin') THEN TRUE
    ELSE country = 'China' and row_time >= '2023-06-23'
  END
```

## Testing and Deployment

### Magic command

- %sh: it executes shell code only on the local driver machine which leads to significant performance overhead; it runs only on the Apache Spark driver, not on the worker nodes.

### Job API

- 2 POST requests (same job) to the endpoint ‘api/2.1/jobs/create’: 2 jobs with the same name created in the workspace but has different job_id
- For each run, it has a unique run_id, and for each task, there is also a unique run_id

## Improving performance

### Partitioning

- Choosing partitioning columns: it's good to consider the fact that records with a given value (the activities of a given user) will continue to arrive indefinitely. In such a case, we use a datetime column for partitioning.
- Data that is over-partitioned or incorrectly partitioned will suffer greatly. Files cannot be combined or compacted across partition boundaries, so partitioned small tables increase storage costs and total number of files to scan. This leads to slowdowns for most general queries. Such an issue requires a full rewrite of all data files to remedy.

### Data skipping

- Delta transaction logs capture stats for each data file of the table
- Each transaction log file:
  - total number of records
  - min, max value in each column of the first 32 columns of the table
  - null value counts in each column of the first 32 columns of the table
  - Nested fields count when determining the first 32 columns (4 struct fields with 8 nested fields will total to the 32 columns)
- transaction logs: json files + parquet checkpoint files every 10 commits to accelerate the resolution of the current table state
- Statistics are generally uninformative for string fields with very high cardinality (such as free text fields), you need to omit these fields from statistics collection by setting them later in the schema after the first 32 columns

### Auto Optimize (2 complementary operations)

- delta.autoOptimize.optimizeWrite
  - most effective for partitioned tables, as they reduce the number of small files written to each partition.
  - attempts to write 128 MB files

  ![](https://docs.databricks.com/_images/optimized-writes.png)

- delta.autoOptimize.autoCompact
  - after the write completes, it checks if files can be further compacted
  - if yes, it runs OPTIMIZE job toward a file size of 128 MB

### Autotune file size based on workload

- having many small files is not always a problem
  - it can lead to better data skipping, and help minimize rewrites during MERGE and DELETE

- databricks can auto-tune the file size of delta tables, based on workloads operating on the table
  - for frequent MERGE, Optimized Writes and Auto Compaction will generate data files < 128 MB. It helps in reducing the duration of further MERGE.

## Modeling data management solution

### Streaming dedup

To perform streaming deduplication, we use dropDuplicates() function to eliminate duplicate records within each new micro batch. In addition, we need to ensure that records to be inserted are not already in the target table. We can achieve this using insert-only merge.

### Streaming ignore updates and deletes

Suppose you have a table user_events with date, user_email, and action columns that is partitioned by date. You stream out of the user_events table and you need to delete data from it due to GDPR.

if you are using this table as a streaming source, deleting data breaks the append-only requirement of streaming sources, which makes the table no more streamable. To avoid this

When you **delete at partition boundaries** (that is, the WHERE is on a partition column): 

```py
spark.readStream.format("delta")
  .option("ignoreDeletes", "true")
  .load("/tmp/delta/user_events")
```

if you have to delete data in multiple partitions (in this example, filtering on user_email):

```py
spark.readStream.format("delta")
  .option("ignoreChanges", "true")
  .load("/tmp/delta/user_events")
```

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
```

### Window functions on streaming dataframe

#### Time-based window

```py
window("order_timestamp", windowDuration="5 minutes", slideDuration=None)
```

- If the `slideDuration` is not provided, the windows will be tumbling windows (non-overlapping windows)

#### Non-time-based window

- Non-time-based window operations are not supported on streaming DataFrames, such window operations need to be implemented inside a foreachBatch logic.

```py
from pyspark.sql.window import Window

def batch_upsert(microBatchDF, batchId):
  window = Window.partitionBy("customer_id").orderBy(F.col("row_time").desc())

  (microBatchDF.filter(F.col("row_status").isin(["insert", "update"]))
               .withColumn("rank", F.rank().over(window))
               .filter("rank == 1")
               .drop("rank")
               .createOrReplaceTempView("ranked_updates"))

  query = """
    MERGE INTO customer_silver c
    USING ranked_updates r
    ON c.customer_id = r.customer_id
      WHEN MATCHED AND c.row_time < r.row_time
        THEN UPDATE SET *
      WHEN NOT MATCHED
        THEN INSERT *
  """

  microBatchDF.sparkSession.sql(query)

query = (spark.readStream
               .table("bronze")
             .writeStream
               .foreachBatch(batch_upsert)
               .option("checkpointLocation", "")
               .trigger(availableNow=True)
               .start())
query.awaitTermination()
```

## Data Processing

### CDF

```py
# Newly updated records will be appeneded to the target table
spark.readStream
        .option("readChangeFeed", "true")
        .option("startingVersion", 0)
        .table ("customers")
        .filter (col("_change_type").isin(["update_postimage"]))
    .writeStream
        .option ("checkpointLocation", "dbfs:/checkpoints")
        .trigger (availableNow=True)
        .table("customers_updates")

# Entire history of updated records will overwrite the target table at each execution
spark.read
        .option("readChangeFeed", "true")
        .option("startingVersion", 0)
        .table ("customers")
        .filter(col("_change_type").isin(["update_postimage"]))
    .write
        .mode(“overwrite”)
        .table("customers_updates")
```

- when to use CDF

| Yes                                                  | No                                              |
|:------------------------------------------------------|:-------------------------------------------------|
| Delta changes include updates and/or deletes         | Delta changes are append only                   |
| Small fraction of records updated in each batch      | Most records in the table updated in each batch |
| Data received from external sources is in CDC format | Data received comprises destructive load        |
| Send data changes to downstream application          | Find and ingest data outside of the Lakehouse   |

### Stream-stream join

- Spark buffers past inputs as a streaming state for both input streams so that it can match every future input with past inputs. This state can be limited by using watermarks.

![](https://www.databricks.com/wp-content/uploads/2018/03/image4.png)

### Stream-static join

- the latest version of the static delta table is returned each time it is queried in a join operation with a data stream.

### Materialized gold tables

- Consider using a view when:
  - Your **query is not complex**. Because views are computed on demand, the view is re-computed every time the view is queried. So, frequently querying complex queries with joins and subqueries increases compute costs
  - You want to reduce storage costs. Views do not require additional storage resources.

- Consider using a gold table when:
  - Multiple downstream queries consume the table, so you want to avoid re-computing complex ad-hoc queries every time.
  - Query results should be computed incrementally from a data source that is continuously or incrementally growing.

### Cloning

- Shallow clone: does not copy the data files to the clone target, only copy the metadata
- Deep clone
  - copies the source table data to the clone target in addition to the metadata of the existing table
  - stream metadata is also cloned such that a stream that writes to the Delta table can be stopped on a source table and continued on the target of a clone from where it left off
  - can sync changes
- Any changes made to either deep or shallow clones affect only the clones themselves and not the source table.

## Monitoring and logging

### driver log -> Ganglia UI

- Cluster load, memory, CPU, network

### Spark UI summary metric

- Usually, if your computation was completely symmetric across tasks, you would see all of the statistics clustered tightly around the 50th percentile value.
- if we have a bunch of “Min” values near zero. This suggests that we have almost empty partitions

