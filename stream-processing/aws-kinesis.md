# Kinesis

- Kinesis data streams
- kinesis data analytics
- kinesis firehose
- kinesis video stream

## Kinesis data streams (KDS)

![](https://d1tlzifd8jdoy4.cloudfront.net/wp-content/uploads/2022/08/shard1-1536x648.jpg)

- retention: 1 - 365 day -> able to reprocess data
- immutable, inserted data cannot be deleted
- data that shares the same partition goes to the same shard (ordering)
- producers
  - AWS SDK
    - PutRecord: one record
    - PutRecords: many records
      - batching, increase throughput -> less HTTP requests
    - **ProvisionedThroughputExceeded exception**:
      - make sure you don't have a hot shard (partition key)
      - increase shards
      - retry with backoff
    - use case: low throughput, higher latency, simple API, lambda
  - kinesis producer library (KPL)
    - c++/java library
    - used for building high performance, long-running producers
    - auto, configurable **retry** mech
    - sync or async API (better performance for **async**)
    - batching
      - collect records and write to multiple shards in the same PutRecords API call
      - aggregate: store multiple records on one record, increase latency, increase payload size and improve throughput
      - can influence efficiency by introducing some delay with RecordMaxBufferedTime (default: 100ms)
    - **application that cannot tolerate additional delay may need to use SDK directly**
      - eg. IoT device to send latest data after offline, use SDK PutRecords API call
    - manual compression
    - KPL records must be decoded with KCL or special helper library
  - kinesis agent
    - java based, build on top of KPL
    - monitor logfiles, send to KDS
    - install in linux server
    - features:
      - write from multi dir and write to multi streams
      - routing feature based on dir/log file
      - preprocess data before sending to streams (csv to json, etc)
      - handle file rotation, checkpointing, retry on failures
      - emit metrics to CloudWatch for monitoring
  - 3rd party libraries: spark, log4j, kafka connect, etc.
- consumers:
  - own (run on EC2 etc.):
    - kinesis client libray (KCL)
      - java-first library but exists for others
      - read data from KPL
      - share multi shards with multi consumers in 1 group, shard discovery
      - **checkpointing** feature to resume progress
        - use DynamoDB for coordination and checkpointing (one row per shard)
          - make sure have enough WCU/RCU (read/write capacity unit)
          - or use on-demond for DynamoDB, otherwise may slow down KCL
      - **ExpiredIteratorException -> increase WCU**
    - AWS SDK:
      - GetRecords:
        - each shard 2MB total aggregate throughput
        - returns up to 10 MB of data (then wait for 5 s) or up to 10k records
        - max of 5 GetRecords API calls per shard per second = 200ms latency
        - **if 5 consumer app consume from the same shard, means every consumer can poll once a second and receive less than 400KB/s**
    - kinesis connector library (legacy)
      - older java library (2016), leverages kcl
      - write data to s3, dynamoDB, redshift, elasticsearch
      - kinesis firehose replace it for a few (s3, redshift), lambda for other targets
  - managed: lambda, kinesis firehose, kinesis data analtyics
- Enhanced fan out
  - Consumers subscribeToShard() and kinesis pushes data to consumers over HTTP/2 (reduce latency: ~70ms)
    - each consumer get 2MB/s of provisioned throughput per shard
      - 20 consumers -> 40 MB/s per shard aggregated, no more 2MB/s
- Enhanced fan out vs standard consumers

  | Standard consumers | Enhanced fan out consumers |
  |:---|:---|
  | Low # of consuming apps (1,2,3, ...) | Multi consumer apps for the same stream |
  | can tolerate ~200 ms latency | low latency ~70 ms |
  | min cost | higher cost; default limit 20 consumers using EFO per data stream |

- capacity modes:
  - provisioned (pay per shard provisioned per hour)
    - choose # shards, manual scale or API
    - each shard:
      - in: 1MB/s (or 1000 records/s)
      - out: 2MB/s (or 2000 records/s)
  - on-demand (pay per stream per hr, data in/our per GB)
    - default capacity provisioned (4MB/s or 4000 records/s)
    - auto-scaling based on observed throughput peak (last 30 days)

- kinesis operation
  - adding shards (shard splitting)
    - can be used to increase capacity
    - use to divide "hot shard"

  ![](https://miro.medium.com/max/1400/1*nds9c4TFs1eHSXHxxves7g.webp)

  - merging shards
    - decrease stream capacity, save costs
    - use to group 2 shards with low traffic

  - out-of-order records after resharding

    - eg. IoT send data 1, 2 to kinesis stream (parent shard) -> split shards -> IoT send data 3, 4 to new/child shard then consumer apps -> out-of-order since 3, 4 may be sent before 1, 2
    - solution: read entirely from parent until you don't have new records, then read from child shards (KCL has this logic built-in)

    ![](../img/out-of-order-resharding-kinesis.png)

- Handle duplicates
  - producer: embed unique id in the data to deduplicate from consumer side
    - eg. network timeout such that no ACK from data streams, producer retries/reloads the data
    ![](../img/aws-kinesis-producer-duplicates.png)
  - consumer:
    - retries can make app read the same data twice
    - retries happen when record processors restart:
      1. work terminate unexpectedly
      2. work added/removed
      3. reshard
      4. deploy the app
    - fix:
      - make consumer app idempotent
      - if final destination can handle duplicates, it is recommended to do it there

  - security
  - IAM to control access
  - encryption in flight: HTTPS endpoints
  - encryption at rest: KMS
  - vpc endpoints available
  - monitor api calls using CloudTrail

## Reference

1. https://www.udemy.com/course/aws-data-analytics/