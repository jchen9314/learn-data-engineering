# Azure Data Factory

## Intro

- cloud-based ETL/data integration service
- allow you to create data workflows that orchestrate and automate data movement and transformation

## Core concepts

- pipeline
  - logical grouping of activities
  - schedule, monitor, manage
- activity: steps in a pipeline, perform tasks
  - 3 types: data movement, transformation, control
- dataset:
  - where the data you need for inputs or outputs lives
  - represents data items (tables/notebook paths) stored in linked services
- linked service:
  - connection configuration that tells ADF to connect to data source
- integration runtime
  - provide computer env that runs activities
  - bridge between activities and linked service objects
  - 3 types: Azure, self-hosted, azure-SSIS
- trigger
  - schedule
  - event
  - tumbling window: run historical data

## Architecture

![adf-architecture](https://learn.microsoft.com/en-us/azure/data-factory/v1/media/data-factory-introduction/data-integration-service-key-concepts.png)

## Data Flow

- no code, visual soln to implement transformation logic in ADF
- for simple **transformations**
- an activity inside pipeline, you can chain with other activities

## Execute a pipeline

- 3 ways:
  - debug mode
  - trigger now
  - trigger with added trigger (3 options)

## CICD

- arm template: json file that define the infras and configuration for your pipeline
- deploy code to higher env:
  - create feature branch
  - create PR to merge code to dev branch
  - publish the code from dev to generate ARM template under `adf_publish` branch (artifact)

## Activities

- Copy
- ForEach (loop)
  - cannot do another ForEach activtiy inside ForEach activity
- GetMetadata
  - itemName, itemType (folder/file), size (file only), lastModified, childItems (folder only, eg. how many files in folder), structure, exists, columnCount, contentMD5 (file only)
- LookUp
  - return the results of executing queries or stored procedures
- Validation
  - verify presence of file in storage
  - ensure the pipeline only continue execution once it has validated the attached dataset reference exists
- Notebook
  - notebookPath
  - use baseParameters property to pass param to notebooks

## Incremental loading

- delta data loading from database using a watermark (eg. date, time column)
  - watermark table that contains all the watermark metadata of each source table
  - pass a list of tables to pipeline as parameters, for each table (ForEach Activity) do the following:

    ![](https://learn.microsoft.com/en-us/azure/data-factory/media/tutorial-incremental-copy-portal/incrementally-load.png)

- delta data loading from sql db with changing tracking technology (`sys.change_tracking_tables`)
  
  ![](https://learn.microsoft.com/en-us/azure/data-factory/media/tutorial-incremental-copy-change-tracking-feature-powershell/incremental-load-flow-diagram.png)

- loading new and changed files with LastModifiedDate
  - if you let ADF scan huge amount of files but only process few of them, will take long time due to file scanning process

- loading new files by time partitioned folder or file names

## Send notification about pipeline failure

- use Logic Apps with Web/WebHook Activity
- use Alerts/Metrics