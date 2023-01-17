# AWS Glue

## Serverless discovery and generation of table definitions and schema

- glue crawler: crawl metadata from different data sources, write all metadata (columns, datatypes, table names, etc.) to glue catalog
- glue catalog: serve as a central metadata repo
- ready for analytics: athena, emr, redshift spectrum

![](https://media.licdn.com/dms/image/C5112AQHyoE5kBlyr3g/article-cover_image-shrink_720_1280/0/1537235967978?e=1679529600&v=beta&t=6_r2tsFs7wQkX9OTvNJSM4J2zYf0tfw7vdxJZvnMoSg)

## Custom ETL jobs

- trigger-driven, scheduled, or on demand
- automatic code generation (python, scala)
- can provision additional DPU to increase performance of spark jobs (enable job metrics to find out)
- error report to Cloudwatch (could tie to SNS notification)
- target: s3, JDBC (RDS, Redshift, etc.), data catalog
- DynamicFrame
  - smiliar to spark DataFrame
  - but each record is self-describing, so no schema is required initially. AWS Glue computes a schema on-the-fly when required, and explicitly encodes schema inconsistencies using a choice (or union) type. You can resolve these inconsistencies to make your datasets compatible with data stores that require a fixed schema.
  - `ResolveChoice`: deal with ambiguity and return a new one, eg. two fields has the same name (4 ways to deal with this case)
    - make_cols: create a new column for each type
    - cast: casts all values to specified type
    - make_struct: create a structure that contains each data type
    - project: projects every type to a given type, eg. project:string
- Modify data catalog
  - etl script to update schema/partitons
    - add new partitions: use enableUpdateCatalog and partitionKeys in script
    - update schema:use enableUpdateCatalog or updateBehavior from script
    - create new tables: enableUpdateCatalog or updateBehavior with setCatalogInfo
  - restrictions:
    - s3 only
    - json, csv, avro, parquet only; parquet requires special code
    - nested schema not supported

- Transformation
  - Bundled transformation: DropFields, DropNullFields, Filter, Join, Map (delete, add, lookups)
  - ML transformation:
    - FindMatchesML: identify duplicates or matching records if no common unique id or no fields match exactly
  - Format conversion
  - Spark transformtion

## Run glue jobs

- time-based schedule (cron style)
- job bookmarks:
  - prevent reprocessing old data
  - persists state from the job run
  - works with s3 in multiple formats
  - works with relational db via JDBC (if PK in sequential order)
    - only handles new rows (not updated rows)
- cloudwatch events
  - trigger lambda/SNS when fails
  - invoke EC2 run, send event to Kinesis, activate a Step Function

## Important features

- elastic views:
  - combine, replicate data across multiple data stores with SQL
  - materialized view
- databrew: clean and normalize data using pre-built transformation
- studio: GUI to create, run, monitor ETL jobs
- streaming ETL: built on spark structured streaming, compatible with Kinesis data streaming, MSK, Kafka...

## Reference

1. https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html