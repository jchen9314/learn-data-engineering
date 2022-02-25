# Data Warehouse(DW)

## OLTP/OLAP

|  | OLTP | OLAP |
|:---|:---|:---|
| Purpose | Transaction; control and run essential operations in real-time | Analytics; reporting, discover insights, support decisions |
| Data updates | Short, fast updates, ACID | Refreshes periodically, scheduled batch processing |
| DB design | Normalized DB for efficiency | Denormalized DB for downstream analysis (dimensional model) |
| Space requirements | Generally small if historical data is archived | Generally large due to aggregating large data |

## Data Normalization

- normalization
  - organize data in database and part of modelling process
  - splits large tables into smaller ones and joins them together using relationships
  - reduce data anomalies and redundancies, improve data integrtiy
- functional dependency
  - each table only represents one area
  - each other columns depends on PK
  - composite keys can also create functional dependency
- 1st normal form
  - must have a PK
  - should only hold single valued attribute
  - must be atomic (value cannot be subdivided): (name -> first_name, last_name)
  - no repeating groups
- 2nd normal form
  - should be in 1NF
  - all non-key columns depends on PK
  - should not contain partial dependencies
    - pd: an attribute depends only part of a PK
    - order_date, shipping details depends only on order_id

      ![](../img/dw-2nf.png)

- 3rd normal form (OLTP)
  - must be in 2NF
  - eliminate columns not dependent on PK
  - should not have transitive dependency
    - non-prime attibute depends on other non-prime attributes

## Pros/cons of Normalized Model

- Pros
  - reduce data redundancy
  - reduce size in storage
  - no data duplications
  - easy to maintain and make changes
- Cons
  - slow performance due to multiple joins
  - not for analytical purposes

## Denormalization

- optimization tech to speed up data retrieval
- requires adding redundancy to various tables
- techniques
  - add redundant columns
    - used for frequently accessed columns with large joins (avoid joins)
  - store derived columns (may need to have frequent update)
  - pre-joining tables
  
## Pros/cons of Denormalized Model

- pros
  - improve performance
  - less compute required
  - accelerate reporting
  - good for analytics
- cons
  - large storage size
  - less flexible
  - insert/updates can be complicated & expensive

## Normalization vs Denormalization

| Normalization | Denormalization |
|:---|:---|
| OLTP | OLAP |
| remove redundancy | add redundancy |
| reduce inconsistency | potential inconsistency |
| require more joins | less joins |
| complex data model | simpler data model |
| **faster data write** | **faster data read** |

## Characteristic of DW

- subject-oriented
  - focus on a subject
  - not on operational day to day
- integrated
  - data from different sources
  - data is uniformly transformed
  - well-defined schema
- time-variant
  - data is organized in time periods
  - contains element of time eitther implicitly or explicitly
- non-volatile
  - only loading and accessing data is allowed
  - daat is refreshed att scheduled time

## DW Architecture

- single-tier
  
  ![](../img/dw-single-tier.png)

  - all of source data is stored directly inside data warehouse layer
  - pro: save data storage and reduce redundancies
  - con: query data directly from dw that make BI tools slow down returning results
- two-tier
  
  ![](../img/dw-two-tier.png)

  - separate between sources and dw
  - add data lake and staging layer before dw layer
    - prevent dw being the main area of stored raw data
    - data lake: single storage area for all source data
    - staging layer: can do any transformation/cleaning before storing data in dw

- three-tier
  
  ![](../img/dw-three-tier.png)

  - add data mart layer
    - enable BI insight through data mart layer
    - model data to serve specific business purpose
  - three-tier
    - bottom tier: data source, data lake, staging
    - middle tier: data warehouse layer, data mart layer
    - top tier: BI tools/dashboards

## Data Lake

- single store of raw data, cost-effective storage
- data can be structured, unstructed, images, log, etc.
- data is in raw format
- give us better data governance

## 5V in Big Data

- volume: large amount of data
- velocity: speed of data processing
- variety: different types of data
- veracity: the level of trust in the data
- value: the value within the data

## DL vs DW

|  | DL | DW |
|:---|:---|:---|
| Data Structure | Structured, unstructured, raw from all the available sources | Structured, processed data after applying transformation/clean up |
| Users | DE, DS | BI developer, Analyst |
| Schema-position | Schema-on-read | Schema-on-write |
| Purpose | Location to store all raw data | Defined purpose for BI, reporting |
| Storage | Low cost storage for large amount of data | Can be expensive to store large amounts of data |

## Staging Layer

- between data lake and dw
- mutliple data source aggregated at staging layer
- perform data cleaning, transformation, validations
- storing data in this layer makes processing easier

## DW Layer

- transformed data from staging layer
- data modelling (dimensional model, OBT, Data Vault)
- data masking, PII data
- optimization strategies
- metadata info is also stored for data lineage

## Data Mart

- subset of DW
- data is organized in small managable chunks
- source data for BI

## ETL

- Extract
  - extract data from the source
  - data goes into a temporary or persistent storage area
  - batch or streaming data
  - data validation checks (format, null values, new columns etc.)
- Transform: improve quality
  - cleansing: solve and clean any inconsistency
  - standardization: apply formatting rules
  - deduplication: remove duplicates and redundancies
  - verfication: flag anomalies and remove unusable data
  - sorting: organize by type
  - other tasks: other rules applied to improve data quality
- Load
  - load the transformed data into dw
  - conduct data quality check during load
  - recovery mechanism to handle load failure
  - types
    - full refresh load: load all data as fresh
    - incremental load: scheduled at intervals

## ETL vs ELT

|  | ETL | ELT |
|:---|:---|:---|
| volume | small/medium data volume | large data volume |
| load time | slow as transformation before loading to DW | fast loading as transformation happens later |
| data type | structured data | structured & unstructured data |
| complexity | compute-intensive & complex | less complex due to transformation within SQL |
| cost | high | low |
| availability | only required for reporting/analysis | everything can be accessed from DL |
| maintenance | high-maintenance due to on-premise solutions | low-maintenance due to cloud solution |
| data governance & security | removes PII before load | option to remove PII before load but require more work; PII is removed after load |

## Data Model and Data Modeling

- data model: act as a blueprint, specify business requirements and data structures, provide visual way to communicatee with business at various level
- data modeling: structured approach to develop a data model by identifying and analyzing all the requirements
- data modeling workflow:
  1. identify business requirements
  2. collaborate with business: interviews, meetings, review existing processes
  3. define ERD notation, define data model type
  4. define data modeling method
  5. develop and deploy

## ERD Notation

- create a visual representation of entities and attributes
- provides preview of how tables should connect
- 3 components
  - Entity: the object from where data is collected (table)
  - Attribute: entity properties that can be identifiers or descriptor (column)
  - Relationship: the connection between entities
- styles (IE, Chen, Barker, UML)
  - IE:
    - most widely used
    - use lines with symbils to indicate relationships
    - use crow foot notation to represent cardinality

    ![IE data model](https://conceptdraw.com/a1003c4/p1/preview/640/pict--erd-data-model-in-ie)

  - Chen:
    - not widely used
    - use different shapes and text values to explain the relationships

    ![chen notation data model](https://vertabelo.com/blog/chen-erd-notation/chen-notation-book-and-chapter-schema-3.png)

- IE vs Chen
  - entity:
    - IE: no weak entity representation
    - chen: have weak entity represented by double rectangle, whcih means it cannot be identified by its attributes

    ![IE vs Chen entity](https://images.slideplayer.com/20/5952332/slides/slide_5.jpg)

  - cardinality:
    - one-to-one
      - one-and-only-one: `||` instead of `|`
    - one-to-many
    - many-to-one
    - many-to-many
      - better convert to either one-to-many/many-to-one (bridge tables)

    ![IE vs Chen Relationship cardinality](https://i.stack.imgur.com/thblX.jpg)

- create an ERD
  1. identify entity
  2. relationship
  3. cardinality
  4. attributes
  
## Reference

1. [Analytics-engineering-bootcamp](https://www.udemy.com/course/analytics-engineering-bootcamp/)
2. [DE-zoomcamp](https://www.youtube.com/watch?v=jrHljAoD6nM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=26&ab_channel=DataTalksClub)