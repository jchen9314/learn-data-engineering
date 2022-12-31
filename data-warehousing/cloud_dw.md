# DW Cloud Services

## Cloud Services

- Google BigQuery
  - cost: 1 TB data processed for $5 (on-demand pricing)
- AWS Redshift
- Azure Synapse Analytics

## Azure Synapse Dedicated SQL Pool

### MPP: Massively Parellel Processing

- want to do as much work in parallel as possible (run in multiple distributions)

![](https://social.technet.microsoft.com/wiki/resized-image.ashx/__size/400x500/__key/communityserver-wikis-components-files/00-00-00-00-05/0844.AAEAAQAAAAAAAAkwAAAAJDhmMWMyOTU2LTI1NGMtNGFhYy1hZDJhLTFhYTkyMzMwYzhkNQ.png)

- data is stored in blob storage (separate data from compute power)
- compute node: provide the compute power for analytis, run queries in parallel
- control node: brain of dw, the front end that interacts with applications and connections
  - host mpp engine: optimize and coordinate parallel queries
- DMS (data movement service): internal service that moves data across multiple nodes
  - when sql dw runs a query, the work is divided into 60 smaller queries that run in parallel

### Azure storage and distribution

- distribution: basic unit of storage and processing for parallel queries
- rows are stored across 60 distributions that are run in parallel
- each compute node manages 1 or more of the 60 distribution
- 3 distribution pattern
  - hash (highest performance, large fact table, size > 2 GB, used with clustered columnstore index)
    - hash key: -> make data distributed evenly (no data skewness)
      - same value -> same distribution
      - have many unique values
      - not date, not in WHERE
      - used in __JOIN, GROUP BY, DISTINCT, OVER, and HAVING__
        - if none of columns selected, can create a col that combines multiple cols

    ```sql
    -- partition (id range left for values (10, 20, 30, 40)): <= 10, >10 and <= 20, ...
    WITH (
        CLUSTERED COLUMNSTORE INDEX
        DISTRIBUTION = HASH([column_name])
        PARTITION (partition_column_name RANGE [LEFT | RIGHT] FOR VALUES ([boundary_value [,...n]]))
    )

    ```

    ```sql
    -- check data skewness
    DBCC PDW_SHOWSPACEUSED('table_name')
    ```

  - round-robin (fast loading, staging tables, used with heap index, no key)
    - distribute data evenly across the table without additional optimization
    - join will be slow (it requires to reshuffle data)
  
     ```sql
      WITH (
          CLUSTERED COLUMNSTORE INDEX
          DISTRIBUTION = ROUND ROBIN
      )
      ```

  - replicated (small dim tables, < 2GB after compression)
    - full copy on each node

    ```sql
    WITH (
        CLUSTERED COLUMNSTORE INDEX
        DISTRIBUTION = REPLICATE
    )
    ```

### Data types

- use the smallest data type which supports the data
- avoid defining all character columns to a large default length
- define columns as VARCHAR rather than NVARCHAR if you don't need unicode (takes two as much as space as regular worker column)
- goal: save space, move data as efficiently as possible

### Table types

- synapse:
  - clustered columnstore: large tbls, great for read-only, highly compressed
    - __minimum 1M rows per partition is needed__. before partition, dedicated sql pool already divides each table into 60 distributed databases.
  - heap (staging tables, fast load, non-index)
  - clustered index (index is physically stored, fast single or very few row lookup)
- traditional sql db:
  - unique index:
    - not allow the field to have duplicate values
    - for PK, a unique index applied automatically
  - clustered index:
    - alters the way records are stored in a database as it sorts out rows by the column which is set to be clustered index
    - each table `can only have one index`
  - non-clustered index:
    - not alter the physical order of the table
    - creates a separate object within a table which points back to the original table rows after searching
    - each table can have many indexes

### Partitioning

- enable us to divide the data into smaller groups of data
- improve the efficiency and performance of loading data by use of partition deletion, switching, and merging
- usually date column/WHERE clause, depends on the query requirement
- lower granularity (week, month) can perform better depending on how much data you have

## BigQuery

### [Paritioning & Clustering](https://www.youtube.com/watch?v=-CqXf7vhhDs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=27&ab_channel=DataTalksClub)

- BigQuery

  Choosing partition key:

  - time-unit column
  - ingestion time (_PARTITIONTIME)
  - integer range partitioning
  - when using time unit or ingestion tim
    - daily
    - hourly
    - monthly/yearly
  - number of partitions limit is 4000

  Choosing clustering key:

  - columns you specify are used to **colocate** related data
  - order of the column is important
  - the order of the specified columns determines the sort order of the data
  - clustering improves:
    - filter queries
    - aggregate queries
  - table with data size < 1 GB, don't show significant improvement with partitioning/clustering
  - you can specify up to 4 cluster columns

- Paritioning vs. clustering
  
|clustering|partitioning|
|:--|:--|
|You need more granularity than partitioning alone allows| you need partition-level management|
|Your queries commonly use filters or aggregation against multiple particular columns| Filter or aggregate on single column|
|The cardinality of the number of values in a column/group is large||
