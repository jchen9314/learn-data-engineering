# Spark Streaming

## Micro-batch approach

- auto looping between micro-batches
- batch start/end position management
- intermediate state management
- combine results to the prev batch results
- fault tolerance and restart management

## APIs

|Spark Streaming (DStream)| Structured Streaming|
|:--|:--|
|RDD based| Dataframe based|
|Lack spark sql engine optimization|sql engine optimization|
|No support for event time semantics|support event time semantics|
|No future upgrades and enhancements expected|Expected further enhancements and new features|

## DataStreamReader

- file options
  - `maxFilesPerTrigger`: limit number of files per micro-batch
  - `.option("cleanSource", "delete")`
  - `.option("sourceArchiveDir", "path_to_archive")`

## DataStreamWriter

- trigger:
  - unspecified
  - time interval
  - one time
  - continuous

- output modes:
  - append: insert only
  - update: upsert
  - complete: overwrite

```py
# checkpoint location: store progress information
# start(): action
# processing time: 1 minute for each micro-batch
spark.config.set('spark.streaming.stopGracefullyOnShutdown', 'true')

writer_query = df.writeStream.format('<format>').option('checkpointLocation','chk-point-dir').outputMode('complete').trigger(processingTime='1 minute').start()

writer_query.awaitTermination()
```

## Restart and failure tolerance

- exactly once:
  - don't miss any input records
  - don't create duplicate output records
- checkpoint
  - read position
    - represent start and end of the data range (current micro-batch)
    - once complete, spark creates a commit to indicate that the data range is successfully processed
  - state information (intermediate data)
- structured streaming maintain all the necessary info to restart the unfinished micro-batch but restart the failed micro-batch doesn't guarantee exactly-once unless:
  - restart with same checkpoint
  - use a replayable source
  - use deterministic computation
  - use an idempotent sink

## Transformation

- stateless:
  - select, filter, map, flatMap, explode
  - complete output mode not supported
- stateful:
  - group, aggregation, windowing, joins
  - excessive state causes out of memory (state is stored inside executor memory)
  - **unmanaged operation**
    - can define own custom state cleanup logic, used in cases where spark doesn't know when to cleanup the state (eg. continuous aggregation)
    - only available in Scala, Java
  - **managed operation** (eg. time-bounded aggregation)
- windowing aggregations (never based on trigger time)

  ![](https://cms.databricks.com/sites/default/files/2021/10/native-support-blog-og.png)

  - tumbling time window: a series of fixed-sized non-overlapping time intervals
  - sliding time window
  - session window
- watermark (**state store cleanup**)
  - expiry date for a window: don't need to keep older windows in state store
  - determine the watermark limit:
    - how long do you wanto to wait for late-arriving records?
    - when late records are not relevant?
  - **withWatermark should be placed before groupby**
  - `watermark boundary = max(event_time) - watermark`
    - if the current event_time is within watermark boundary, it will be found in state store and update the aggrgegation
    - time windows that are outside the boundary will not be deleted from state store if exists
    - outputMode:
      - complete: w/ watermark, the complete mode **will not remove** any states from state store
      - update: most useful/efficient mode for streaming queriese with streaming aggregates
        - should not be used in file storage sink, will create duplicated records
      - append:
        - allow only when spark knows the record will not update or change in the future
        - will suppress the output of the windowing aggregates until they cross the watermark boundary
        - the result will be delayed at least by the watermark duration

## Join

- stream to static: stateless
- stream to stream: stateful, must retain records in state store based on watermark configuration
- outer joins
  - left outer:
    - conditionally allowed, left side must be stream
    - watermark on the right-side stream
    - max time range constraint between the left and right-side events (eg. a click event can happeen in a max of 15 mins from the impression event)
    - if no matching found from right side, the records in left side will output the results after it passes the watermark boundary

    ```py
    join_condition = """
                     ImpressionID == ClickID
                     AND
                     ClickTime BETWEEN ImpressionTime AND ImpressionTime + interval 15 minute
                     """
    ```

  - right outer:
    - conditional allowed, right must be stream
    - watermark on the left-side stream
    - max time range constraint between the left and right-side events
  - full outer: NOT allowed

## Write to sink

- sink type: file, kafka, foreach, foreachBatch, console, memory
  - `foreachBatch`: write df to arbitrary data sinks
    - specify a function that is executed on the output data of every micro-batch of the streaming query
    - 2 params: a DataFrame/Dataset, micro-batch id
  - `forEach`: allow custom write logic on every row

  ```py
  # write data to azure synapse table
  # adapt from https://docs.databricks.com/structured-streaming/examples.html#foreachbatch-sqldw-example

  def writeToSQLWarehouse(df, epochId):
    df.write \
      .format("com.databricks.spark.sqldw") \
      .mode('overwrite') \
      .option("url", "jdbc:sqlserver://<the-rest-of-the-connection-string>") \
      .option("forward_spark_azure_storage_credentials", "true") \
      .option("dbtable", "my_table_in_dw_copy") \
      .option("tempdir", "wasbs://<your-container-name>@<your-storage-account-name>.blob.core.windows.net/<your-directory-name>") \
      .save()

  query = (
    df.writeStream
      .foreachBatch(writeToSQLWarehouse)
      .outputMode("update")
      .start()
      )
  ```

## Reference

1. https://www.udemy.com/course/spark-streaming-using-python
2. https://cms.databricks.com/sites/default/files/2021/10/native-support-blog-og.png