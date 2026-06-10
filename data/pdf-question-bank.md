# SnowPro Core - PDF Question Bank (SnowProQBaat2026)

> Extracted from `pdf/SnowProQBaat2026.pdf` and converted to multiple-choice format
> consistent with `snowpro_core_questions.json` (IDs 501-598).
> A few source answers that were factually inaccurate were corrected against the
> official Snowflake documentation (periodic rekeying = Enterprise, highest edition = VPS,
> CHARACTER(25) displays as VARCHAR(25), NULL_COUNT measures completeness).

## 501. Which statement correctly removes the stored procedure SALES_REPORT(MONTH INT, YEAR INT)?

*Domain: Data Transformations | Difficulty: intermediate*

- A. DROP PROCEDURE SALES_REPORT(INT, INT);
- B. DROP PROCEDURE SALES_REPORT;
- C. DROP PROCEDURE SALES_REPORT(MONTH, YEAR);
- D. DELETE PROCEDURE SALES_REPORT(INT, INT);

**Answer:** A - Dropping a procedure requires the name plus the argument data types (not the parameter names): DROP PROCEDURE SALES_REPORT(INT, INT). The signature disambiguates overloaded procedures.

## 502. Which sampling form returns a fixed number of rows rather than a percentage of the table?

*Domain: Data Transformations | Difficulty: intermediate*

- A. SAMPLE / TABLESAMPLE using the ROWS form, e.g., SAMPLE (10 ROWS)
- B. SAMPLE using a percentage, e.g., SAMPLE (10)
- C. BERNOULLI probability sampling
- D. SYSTEM/BLOCK percentage sampling

**Answer:** A - Fixed-size sampling uses the row-count form SAMPLE (n ROWS), returning exactly n rows. The percentage forms (BERNOULLI/SYSTEM) return an approximate fraction of rows.

## 503. Which Snowflake mechanism lets you override a table's natural clustering to improve pruning?

*Domain: Performance and Cost Optimization Concepts | Difficulty: basic*

- A. Clustering keys
- B. Materialized views
- C. Result cache
- D. Search Optimization Service

**Answer:** A - Defining a clustering key reorganizes data by chosen columns, overriding the natural (load-order) clustering and improving pruning for queries filtering on those columns.

## 504. What is the effect on existing micro-partitions when a column is dropped from a table?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. Existing micro-partitions are not rewritten; the column is removed via metadata
- B. All micro-partitions are immediately rewritten
- C. The entire table is recreated
- D. Adjacent micro-partitions are merged

**Answer:** A - Dropping a column is a metadata-only operation. Existing micro-partitions are left unchanged and the column is simply no longer exposed.

## 505. When does Snowflake perform micro-partitioning of table data?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: basic*

- A. Automatically as data is loaded into the table
- B. Only when a clustering key is defined
- C. When the user runs a manual PARTITION command
- D. During the Fail-safe period

**Answer:** A - Snowflake automatically divides data into micro-partitions as it is loaded; there is no manual partitioning step.

## 506. What happens when a single row in a table is updated?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. The micro-partition containing the row is replaced by a new one
- B. Only the single row's bytes are edited in place
- C. The entire table is rewritten
- D. Nothing changes on disk until Fail-safe

**Answer:** A - Micro-partitions are immutable, so an update writes a new micro-partition with the changed data and supersedes the old one, which also enables Time Travel.

## 507. Which table type has no Fail-safe period?

*Domain: Data Protection and Data Sharing | Difficulty: basic*

- A. Transient table
- B. Permanent table
- C. Standard table
- D. Managed table

**Answer:** A - Transient (and temporary) tables have no Fail-safe, lowering storage cost. Permanent tables include a 7-day Fail-safe.

## 508. Which table type is visible only within the session that created it?

*Domain: Data Protection and Data Sharing | Difficulty: basic*

- A. Temporary table
- B. Transient table
- C. Permanent table
- D. External table

**Answer:** A - A temporary table exists only for its creating session and is automatically dropped when that session ends.

## 509. Which Snowflake table type is optimized for transactional (OLTP-style) workloads?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. Hybrid table (Unistore)
- B. Transient table
- C. External table
- D. Temporary table

**Answer:** A - Hybrid tables (Unistore) add primary keys and row-level indexes for fast single-row reads/writes, supporting transactional workloads alongside analytics.

## 510. What is the maximum data recovery window for a transient table using Time Travel?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. 0 to 1 day
- B. Up to 7 days
- C. Up to 90 days
- D. 0 days only

**Answer:** A - Transient tables support Time Travel of 0 or 1 day and have no Fail-safe, so the maximum recovery window is 1 day.

## 511. What is the default Time Travel retention period for a table?

*Domain: Data Protection and Data Sharing | Difficulty: basic*

- A. 1 day
- B. 0 days
- C. 7 days
- D. 90 days

**Answer:** A - The default DATA_RETENTION_TIME_IN_DAYS is 1 day for all editions; Enterprise+ can extend permanent objects up to 90 days.

## 512. What is the key characteristic of Time Travel?

*Domain: Data Protection and Data Sharing | Difficulty: basic*

- A. It lets you access or restore historical data within the retention period
- B. It permanently archives data forever
- C. It replicates data across regions
- D. It encrypts data at rest

**Answer:** A - Time Travel enables querying, cloning, and restoring data as it existed at points within the configured retention window.

## 513. When the account MIN_DATA_RETENTION_TIME_IN_DAYS and an object's DATA_RETENTION_TIME_IN_DAYS differ, which value applies?

*Domain: Data Protection and Data Sharing | Difficulty: advanced*

- A. The greater of the two values
- B. The lesser of the two values
- C. Always the account-level value
- D. Always the object-level value

**Answer:** A - MIN_DATA_RETENTION_TIME_IN_DAYS sets a floor; the effective retention is the greater of the account minimum and the object's own setting.

## 514. Which of the following consume storage that Snowflake bills?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. All of these: permanent tables, materialized views, transient tables, and Fail-safe
- B. Only permanent tables
- C. Only materialized views
- D. Only Fail-safe data

**Answer:** A - Permanent/transient tables, materialized views, and Time Travel/Fail-safe data all occupy billable storage.

## 515. Which warehouse setting enables horizontal scaling (scale-out) for concurrency?

*Domain: Performance and Cost Optimization Concepts | Difficulty: intermediate*

- A. MAX_CLUSTER_COUNT
- B. WAREHOUSE_SIZE
- C. AUTO_SUSPEND
- D. STATEMENT_TIMEOUT_IN_SECONDS

**Answer:** A - Setting MAX_CLUSTER_COUNT greater than 1 creates a multi-cluster warehouse that scales out additional clusters to absorb concurrency.

## 516. Which feature temporarily adds serverless compute to accelerate occasional heavy queries without resizing the warehouse?

*Domain: Performance and Cost Optimization Concepts | Difficulty: intermediate*

- A. Query Acceleration Service
- B. Search Optimization Service
- C. Result cache
- D. Automatic Clustering

**Answer:** A - QAS offloads portions of eligible large scan/filter queries onto shared serverless compute, accelerating outliers without permanently scaling the warehouse.

## 517. Which privilege allows a role to start, stop, and resume a virtual warehouse?

*Domain: Account Access and Security | Difficulty: basic*

- A. OPERATE
- B. USAGE
- C. MONITOR
- D. MODIFY

**Answer:** A - OPERATE permits starting/stopping/suspending/resuming a warehouse; USAGE only allows running queries on it.

## 518. Which multi-cluster scaling policy minimizes credits by being conservative about starting clusters?

*Domain: Performance and Cost Optimization Concepts | Difficulty: intermediate*

- A. ECONOMY
- B. STANDARD
- C. MAXIMIZED
- D. AGGRESSIVE

**Answer:** A - The ECONOMY scaling policy favors credit conservation, starting another cluster only when there is enough load to keep it busy for about 6 minutes.

## 519. What is the recommended way to optimize a mixed workload of continuous loading and reporting?

*Domain: Performance and Cost Optimization Concepts | Difficulty: intermediate*

- A. Use separate, dedicated warehouses for each workload
- B. Run both on one extra-small warehouse
- C. Disable auto-suspend
- D. Rely solely on the result cache

**Answer:** A - Isolating loading and reporting on separate warehouses prevents resource contention and allows independent sizing, scaling, and cost attribution.

## 520. Which SQL command does Snowpipe use under the hood to load data?

*Domain: Data Loading and Unloading | Difficulty: basic*

- A. COPY INTO
- B. INSERT
- C. PUT
- D. MERGE

**Answer:** A - A pipe wraps a COPY INTO <table> statement that Snowpipe runs automatically as new files arrive.

## 521. Which COPY INTO ON_ERROR option prevents a partial load by failing the whole statement on any error?

*Domain: Data Loading and Unloading | Difficulty: intermediate*

- A. ON_ERROR = ABORT_STATEMENT
- B. ON_ERROR = CONTINUE
- C. ON_ERROR = SKIP_FILE
- D. ON_ERROR = SKIP_FILE_10

**Answer:** A - ABORT_STATEMENT stops and rolls back the load on the first error, avoiding partially loaded data. It is the default for bulk COPY.

## 522. Which COPY option validates files and returns errors without loading any data?

*Domain: Data Loading and Unloading | Difficulty: intermediate*

- A. VALIDATION_MODE = RETURN_ERRORS
- B. ON_ERROR = CONTINUE
- C. FORCE = TRUE
- D. PURGE = TRUE

**Answer:** A - VALIDATION_MODE (e.g., RETURN_ERRORS / RETURN_ALL_ERRORS) checks staged files and reports issues without inserting any rows.

## 523. What happens if you run the same COPY INTO command again on files that were already loaded?

*Domain: Data Loading and Unloading | Difficulty: advanced*

- A. The data loads only once; already-loaded files are skipped (idempotent)
- B. The data is duplicated on each run
- C. The statement errors out
- D. Only the most recent run is kept

**Answer:** A - COPY tracks load history (64 days) and skips files already loaded, so repeated runs are idempotent unless FORCE = TRUE is specified.

## 524. What is the role of the COMPRESSION parameter in a file format?

*Domain: Data Loading and Unloading | Difficulty: basic*

- A. It specifies the compression algorithm used for the files
- B. It sets the virtual warehouse size
- C. It enables Time Travel
- D. It defines the column delimiter

**Answer:** A - COMPRESSION tells Snowflake which algorithm (e.g., GZIP, AUTO, NONE) applies to the data files being loaded or unloaded.

## 525. Where does the command COPY INTO @my_stage write data?

*Domain: Data Loading and Unloading | Difficulty: intermediate*

- A. To the named internal stage (it unloads data)
- B. Into a table
- C. To the local client disk
- D. To the result cache

**Answer:** A - COPY INTO <location> unloads table/query data to the specified stage; here, a named internal stage.

## 526. Which file format best preserves large floating-point values precisely during load?

*Domain: Data Loading and Unloading | Difficulty: intermediate*

- A. PARQUET
- B. CSV
- C. Plain text
- D. Fixed-width text

**Answer:** A - Parquet is a typed, binary columnar format that preserves numeric precision better than text formats such as CSV.

## 527. Which practice helps optimize loading of files from external storage?

*Domain: Data Loading and Unloading | Difficulty: intermediate*

- A. Use appropriately sized, compressed (e.g., GZIP) files
- B. Use one very large uncompressed file
- C. Use thousands of tiny files
- D. Disable file formats

**Answer:** A - Compressed, right-sized files (about 100-250 MB) reduce transfer overhead and enable parallel loading across warehouse threads.

## 528. Which function/view retrieves errors and details about past COPY loads?

*Domain: Data Loading and Unloading | Difficulty: intermediate*

- A. COPY_HISTORY (and the VALIDATE function)
- B. QUERY_HISTORY only
- C. LOGIN_HISTORY
- D. TABLE_STORAGE_METRICS

**Answer:** A - COPY_HISTORY (Information Schema/Account Usage) and the VALIDATE function expose load results and rejected-row errors.

## 529. Which object lets you catalog and process unstructured files held in a stage?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. Directory table
- B. External table
- C. Stream
- D. Sequence

**Answer:** A - A directory table layered on a stage exposes queryable file metadata, enabling cataloging and processing of unstructured data.

## 530. What is the purpose of a directory table?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: basic*

- A. To store file-level metadata (path, size, last modified) for a stage
- B. To store table rows
- C. To cache query results
- D. To mask sensitive columns

**Answer:** A - Directory tables provide a queryable index of files in a stage, including each file's path, size, and timestamps.

## 531. Which mechanism provides temporary, direct access to a specific staged file?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. A pre-signed URL
- B. A network policy
- C. A resource monitor
- D. A masking policy

**Answer:** A - GET_PRESIGNED_URL generates a time-limited URL that grants direct access to a staged file for the duration of its expiration window.

## 532. How can an external (non-Snowflake) application consume an individual unstructured file from a stage?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. Via a pre-signed URL
- B. Via COPY INTO
- C. Via a stream
- D. Via a sequence

**Answer:** A - Pre-signed URLs let external tools or browsers download a staged file directly over HTTPS during the token's lifetime.

## 533. What is the authorization behavior of a pre-signed URL?

*Domain: Account Access and Security | Difficulty: advanced*

- A. Anyone holding the URL can access the file until the token expires
- B. Only the issuing user can ever use it
- C. It requires a Snowflake login on each access
- D. It never expires

**Answer:** A - A pre-signed URL embeds time-limited credentials, so anyone with the URL can access the file until it expires; share it carefully.

## 534. Which service powers Snowflake's built-in multi-factor authentication?

*Domain: Account Access and Security | Difficulty: basic*

- A. Duo Security
- B. Google Authenticator
- C. RSA SecurID
- D. Okta Verify

**Answer:** A - Snowflake's native MFA is provided by Duo Security; users self-enroll with no additional licensing required.

## 535. What is the default authenticator for the Snowflake JDBC driver?

*Domain: Account Access and Security | Difficulty: intermediate*

- A. snowflake
- B. externalbrowser
- C. oauth
- D. snowflake_jwt

**Answer:** A - The default authenticator is 'snowflake' (username/password). Others such as externalbrowser, oauth, and snowflake_jwt must be set explicitly.

## 536. Which authentication method requires a securely stored local private key file?

*Domain: Account Access and Security | Difficulty: intermediate*

- A. Key-pair authentication
- B. Password authentication
- C. Duo MFA
- D. SAML SSO

**Answer:** A - Key-pair auth uses an RSA private key stored on the client; the matching public key is registered on the Snowflake user.

## 537. Which system role manages grants across the account by default?

*Domain: Account Access and Security | Difficulty: intermediate*

- A. SECURITYADMIN
- B. SYSADMIN
- C. USERADMIN
- D. PUBLIC

**Answer:** A - SECURITYADMIN holds MANAGE GRANTS and can grant/revoke privileges globally; it also inherits USERADMIN's user and role management.

## 538. What does a role minimally need to query a secure materialized view it does not own?

*Domain: Account Access and Security | Difficulty: advanced*

- A. USAGE on the database/schema plus SELECT on the view
- B. OWNERSHIP of the view
- C. The ACCOUNTADMIN role
- D. The MANAGE GRANTS privilege

**Answer:** A - Following least privilege, a role needs only USAGE to traverse the containers and SELECT on the secure materialized view, not ownership or an admin role.

## 539. Which feature reduces exposure of PII by transforming column values at query time based on the querying role?

*Domain: Account Access and Security | Difficulty: intermediate*

- A. Dynamic Data Masking
- B. Resource monitors
- C. Result cache
- D. Sequences

**Answer:** A - Dynamic Data Masking applies masking policies so non-privileged roles see masked values while the stored data is unchanged. (Secure views also help limit exposure.)

## 540. Which combination best supports classifying and auditing access to sensitive data?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. Object tagging with tag-based masking policies
- B. Result cache and sequences
- C. Network policies only
- D. Fail-safe

**Answer:** A - Object tags classify sensitive columns, tag-based masking policies enforce protection consistently, and ACCESS_HISTORY audits column-level access.

## 541. What is required for a user to begin using Snowflake MFA?

*Domain: Account Access and Security | Difficulty: intermediate*

- A. The user must enroll themselves in MFA
- B. It is enabled automatically for everyone
- C. A separate third-party license must be purchased
- D. Only SSO users can enroll

**Answer:** A - Snowflake MFA (Duo) requires each user to self-enroll; administrators can strongly encourage or require it, especially for privileged roles.

## 542. Which key-pair practice lets you replace keys without an authentication outage?

*Domain: Account Access and Security | Difficulty: intermediate*

- A. Key rotation using a second registered public key
- B. Disabling encryption temporarily
- C. Sharing the private key with the client team
- D. Switching to a password instead

**Answer:** A - Snowflake supports two public keys (RSA_PUBLIC_KEY and RSA_PUBLIC_KEY_2) so you can rotate keys seamlessly with no downtime.

## 543. Why might an account configure multiple identity providers (IdPs)?

*Domain: Account Access and Security | Difficulty: advanced*

- A. To provide different authentication for different user groups
- B. To disable RBAC
- C. To increase storage capacity
- D. To bypass MFA

**Answer:** A - Multiple IdPs let an organization authenticate distinct user populations (for example employees vs. partners) through their respective providers.

## 544. What is the minimum Snowflake edition required for periodic rekeying of data?

*Domain: Account Access and Security | Difficulty: advanced*

- A. Enterprise
- B. Standard
- C. Business Critical
- D. Virtual Private Snowflake

**Answer:** A - Annual periodic rekeying of older data is available in Enterprise Edition and above. (Tri-Secret Secure, by contrast, requires Business Critical.)

## 545. What is the minimum edition required to use Object Tagging?

*Domain: Account Access and Security | Difficulty: intermediate*

- A. Enterprise
- B. Standard
- C. Business Critical
- D. Virtual Private Snowflake

**Answer:** A - Object tagging, like other governance features such as masking and row access policies, requires Enterprise Edition or higher.

## 546. At which levels can network policies be applied?

*Domain: Account Access and Security | Difficulty: intermediate*

- A. Both the account level and the individual user level
- B. Account level only
- C. User level only
- D. Warehouse level only

**Answer:** A - Network policies can be set account-wide and overridden per user, enabling tailored IP allow/block lists for specific users or service accounts.

## 547. Where does data accessed through a share physically reside?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. In the provider account's micro-partitions
- B. Copied into the consumer's storage
- C. In a Snowflake-managed neutral region
- D. On the consumer's local disk

**Answer:** A - Secure Data Sharing exposes the provider's live data in place; no copy is made, so consumers query the provider's micro-partitions.

## 548. Which privilege does a consumer need to access an inbound share?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. IMPORT SHARE
- B. EXPORT SHARE
- C. OWNERSHIP
- D. MANAGE GRANTS

**Answer:** A - The IMPORT SHARE privilege lets a consumer create a database from a share and access the shared, read-only objects.

## 549. Which option lets a provider manage data sharing across a curated group of accounts?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. Data Exchange
- B. Reader account
- C. Resource monitor
- D. Directory table

**Answer:** A - A Data Exchange provides a private hub to share data among a managed group of provider and consumer accounts.

## 550. Setting SECURE_OBJECTS_ONLY = FALSE on a share allows sharing which additional objects?

*Domain: Data Protection and Data Sharing | Difficulty: advanced*

- A. Regular (non-secure) views
- B. Warehouses
- C. Roles
- D. Resource monitors

**Answer:** A - By default a share allows only secure objects; SECURE_OBJECTS_ONLY = FALSE relaxes this so standard (non-secure) views can also be shared.

## 551. Which statements correctly describe Secure Data Sharing?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. Data is not transferred/copied, and the consumer pays for the compute used to query it
- B. Data is copied to the consumer and the provider pays the compute
- C. Both parties pay to store the data twice
- D. Snowflake covers all storage and compute costs

**Answer:** A - Sharing provides live, read-only access without copying data; the provider stores one copy and the consumer uses its own warehouse (compute) to query it.

## 552. What is the minimum edition required to use Secure Data Sharing?

*Domain: Data Protection and Data Sharing | Difficulty: basic*

- A. Standard
- B. Enterprise
- C. Business Critical
- D. Virtual Private Snowflake

**Answer:** A - Secure Data Sharing is available beginning with Standard Edition.

## 553. Which feature protects data availability during a regional outage?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. Cross-region replication (with failover)
- B. Result cache
- C. Time Travel
- D. Search Optimization Service

**Answer:** A - Replicating databases to another region, combined with failover groups, provides business continuity if a region becomes unavailable.

## 554. What is true about database replication refresh behavior?

*Domain: Data Protection and Data Sharing | Difficulty: advanced*

- A. Only one refresh runs at a time for a given secondary
- B. Refreshes run continuously in parallel
- C. Refreshes are synchronous and block writes on the primary
- D. Refreshes only ever run manually

**Answer:** A - Replication refreshes are asynchronous and serialized: only one refresh runs at a time per secondary, which reflects the primary as of the last completed refresh.

## 555. Predicate pruning on a large table primarily relies on what?

*Domain: Performance and Cost Optimization Concepts | Difficulty: basic*

- A. Micro-partition metadata (such as min/max values)
- B. The result cache
- C. Row-level B-tree indexes
- D. The warehouse size

**Answer:** A - Snowflake prunes by consulting per-micro-partition metadata to skip partitions that cannot contain rows matching the query predicates.

## 556. Excessive query spillage (to local or remote storage) usually indicates what?

*Domain: Performance and Cost Optimization Concepts | Difficulty: intermediate*

- A. The virtual warehouse is undersized for the query
- B. The result cache is disabled
- C. There are too many micro-partitions
- D. Storage is full

**Answer:** A - Spilling means the working set exceeded available memory; scaling up to a larger warehouse with more memory typically resolves it.

## 557. Which feature helps scale performance of occasional costly queries without permanently enlarging the warehouse?

*Domain: Performance and Cost Optimization Concepts | Difficulty: intermediate*

- A. Query Acceleration Service
- B. Auto-suspend
- C. The Economy scaling policy
- D. Result cache

**Answer:** A - QAS leases extra serverless compute for eligible heavy scan/filter queries, improving performance for outliers on demand.

## 558. Which feature can improve repeated query performance over an external table?

*Domain: Performance and Cost Optimization Concepts | Difficulty: advanced*

- A. A materialized view defined on the external table
- B. Auto-suspend
- C. A resource monitor
- D. A network policy

**Answer:** A - A materialized view pre-computes and stores results from the external table inside Snowflake, accelerating repeated queries over slower external files.

## 559. Which Query Profile signal indicates a full table scan with poor pruning?

*Domain: Performance and Cost Optimization Concepts | Difficulty: intermediate*

- A. Partitions scanned is close to partitions total
- B. Bytes sent over the network
- C. The number of joins
- D. A result cache hit

**Answer:** A - When partitions scanned approaches partitions total, little pruning occurred, often because the table is not clustered on the filtered columns.

## 560. Which Query Profile operator reports partition pruning information?

*Domain: Performance and Cost Optimization Concepts | Difficulty: intermediate*

- A. TableScan
- B. Sort
- C. Aggregate
- D. Result

**Answer:** A - The TableScan operator reports partitions scanned versus total, showing how effectively pruning eliminated micro-partitions.

## 561. Which object schedules recurring SQL transformations?

*Domain: Data Transformations | Difficulty: basic*

- A. Task
- B. Stream
- C. Sequence
- D. Stage

**Answer:** A - Tasks schedule SQL statements or stored procedures (via CRON or interval) and can be chained into DAGs to build pipelines.

## 562. Which stream metadata column identifies a changed row?

*Domain: Data Transformations | Difficulty: intermediate*

- A. METADATA$ROW_ID
- B. METADATA$FILENAME
- C. METADATA$STAGE
- D. METADATA$SIZE

**Answer:** A - Streams expose METADATA$ROW_ID (row identity) along with METADATA$ACTION and METADATA$ISUPDATE to describe captured changes.

## 563. Which actions can make a table stream stale or unusable?

*Domain: Data Transformations | Difficulty: advanced*

- A. Dropping or renaming the underlying source table
- B. Querying the stream with SELECT
- C. Resizing the warehouse
- D. Running a SELECT on the source table

**Answer:** A - A stream depends on its source table; dropping or renaming that table makes the stream stale because its offset can no longer be resolved.

## 564. Which notations can be used to access fields in a semi-structured (VARIANT) column?

*Domain: Data Transformations | Difficulty: basic*

- A. Both dot/colon notation and bracket notation
- B. Only dot notation
- C. Only bracket notation
- D. Neither; you must flatten first

**Answer:** A - You can navigate VARIANT data with path/dot notation (col:key) and bracket notation (col['key']).

## 565. How can you extract the value of key 'k' from a VARIANT column c?

*Domain: Data Transformations | Difficulty: basic*

- A. Using either c:k (path) or c['k'] (bracket) notation
- B. Only c.k
- C. Only c['k']
- D. GET_KEY(c, 'k')

**Answer:** A - Both the path form (c:k) and the bracket form (c['k']) return the key's value as a VARIANT, which you can then cast to a target type.

## 566. Which functions build an ARRAY from values?

*Domain: Data Transformations | Difficulty: intermediate*

- A. ARRAY_AGG (across rows) and ARRAY_CONSTRUCT (from arguments)
- B. LISTAGG only
- C. OBJECT_CONSTRUCT only
- D. FLATTEN only

**Answer:** A - ARRAY_AGG aggregates grouped row values into an array, while ARRAY_CONSTRUCT builds an array from explicit arguments.

## 567. What is a key difference between loading JSON and CSV?

*Domain: Data Loading and Unloading | Difficulty: intermediate*

- A. CSV is flat/tabular, while JSON is hierarchical and loads into a VARIANT column
- B. JSON must be flattened before loading
- C. CSV loads into a VARIANT column
- D. JSON cannot be queried with SQL

**Answer:** A - CSV maps to flat columns, whereas JSON's nested structure is stored in a VARIANT and queried with path notation and FLATTEN.

## 568. Why load JSON into a VARIANT column?

*Domain: Data Transformations | Difficulty: intermediate*

- A. It preserves the nested structure and supports hierarchical querying
- B. It compresses better than every other format
- C. It disables schema-on-read
- D. It converts JSON to CSV

**Answer:** A - VARIANT retains the nested JSON structure so you can query it directly with path access and FLATTEN (schema-on-read).

## 569. By default, how does the FLATTEN function handle nested arrays?

*Domain: Data Transformations | Difficulty: advanced*

- A. It flattens only the top level (RECURSIVE = FALSE by default)
- B. It recursively flattens all levels automatically
- C. It ignores arrays entirely
- D. It raises an error on nested arrays

**Answer:** A - FLATTEN expands one level by default; set RECURSIVE => TRUE to expand nested structures at all levels.

## 570. Which function efficiently estimates the number of distinct values?

*Domain: Data Transformations | Difficulty: intermediate*

- A. APPROX_COUNT_DISTINCT
- B. COUNT(DISTINCT ...)
- C. ARRAY_SIZE
- D. TYPEOF

**Answer:** A - APPROX_COUNT_DISTINCT uses HyperLogLog to estimate distinct cardinality quickly and cheaply on large datasets.

## 571. Which function returns the URL/location of an external stage?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. GET_STAGE_LOCATION
- B. GET_PRESIGNED_URL
- C. BUILD_SCOPED_FILE_URL
- D. LIST

**Answer:** A - GET_STAGE_LOCATION returns the external storage location (URL) configured for a stage.

## 572. How is the validity period of a pre-signed URL controlled?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. By the expiration argument passed to GET_PRESIGNED_URL
- B. It is fixed at 24 hours
- C. By the virtual warehouse size
- D. It never expires

**Answer:** A - GET_PRESIGNED_URL accepts an expiration (in seconds) argument that sets how long the generated URL remains valid.

## 573. Which CLI tool is commonly used to script and automate Snowflake deployments?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. SnowSQL
- B. Snowsight
- C. Snowpark
- D. SnowCD

**Answer:** A - SnowSQL is the command-line client used to run scripts and automate queries and deployments against Snowflake.

## 574. In Snowpark, which type of method triggers execution of a lazily-built DataFrame?

*Domain: Data Transformations | Difficulty: intermediate*

- A. An action such as collect()
- B. select()
- C. filter()
- D. with_column()

**Answer:** A - Snowpark DataFrames are lazy; transformations build a plan and an action like collect() (or show/count) triggers execution in Snowflake.

## 575. What is the purpose of Snowflake Cortex?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. Serverless AI/ML and LLM functions callable from SQL or Python
- B. A CLI for deployments
- C. A storage compression engine
- D. A network security feature

**Answer:** A - Cortex provides managed AI/ML and LLM functions (summarize, translate, sentiment, complete, and more) directly inside Snowflake.

## 576. Which service enables multi-language (Python/Java/Scala) data processing inside Snowflake?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. Snowpark
- B. SnowSQL
- C. Snowsight
- D. Snowpipe

**Answer:** A - Snowpark offers DataFrame APIs and UDFs/procedures in Python, Java, and Scala that execute within Snowflake's compute.

## 577. Which of the following are supported Snowflake clients/drivers?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: basic*

- A. Both the Go driver and the Python connector (among others)
- B. Only ODBC
- C. Only JDBC
- D. Only the web UI

**Answer:** A - Snowflake provides many connectors and drivers, including Python, Go, JDBC, ODBC, .NET, and Node.js.

## 578. MFA token caching is supported by which connectors/drivers?

*Domain: Account Access and Security | Difficulty: advanced*

- A. JDBC and the Python connector (among supported clients)
- B. Only the web UI
- C. Only SnowSQL
- D. No connectors support it

**Answer:** A - MFA token caching reduces repeated prompts and is supported by drivers such as JDBC, ODBC, and the Python connector.

## 579. Which view shows historical query performance details?

*Domain: Performance and Cost Optimization Concepts | Difficulty: basic*

- A. QUERY_HISTORY
- B. LOGIN_HISTORY
- C. TABLE_STORAGE_METRICS
- D. GRANTS_TO_ROLES

**Answer:** A - QUERY_HISTORY records executed queries with duration, bytes scanned, and warehouse, supporting performance analysis.

## 580. Which Information Schema table function lists the files referenced by external tables?

*Domain: Data Loading and Unloading | Difficulty: intermediate*

- A. EXTERNAL_TABLE_FILES
- B. COPY_HISTORY
- C. QUERY_HISTORY
- D. STAGE_DIRECTORY

**Answer:** A - EXTERNAL_TABLE_FILES returns the staged files associated with an external table, useful for auditing external data.

## 581. Which view provides the most detailed per-table storage metrics?

*Domain: Performance and Cost Optimization Concepts | Difficulty: advanced*

- A. ACCOUNT_USAGE.TABLE_STORAGE_METRICS
- B. ACCOUNT_USAGE.QUERY_HISTORY
- C. INFORMATION_SCHEMA.COLUMNS
- D. ACCOUNT_USAGE.LOGIN_HISTORY

**Answer:** A - TABLE_STORAGE_METRICS breaks down active, Time Travel, and Fail-safe bytes per table for detailed storage analysis.

## 582. What does the NULL_COUNT data metric function (DMF) measure?

*Domain: Data Transformations | Difficulty: intermediate*

- A. The number of NULL values in a column (a data-completeness metric)
- B. The number of distinct values
- C. The accuracy of numeric values
- D. The row size in bytes

**Answer:** A - The system DMF NULL_COUNT returns how many NULLs a column contains, helping monitor data completeness and quality.

## 583. How is a column defined as CHARACTER(25) reported by DESCRIBE TABLE?

*Domain: Data Transformations | Difficulty: intermediate*

- A. VARCHAR(25)
- B. STRING(25)
- C. CHAR(25)
- D. TEXT(25)

**Answer:** A - CHAR, CHARACTER, STRING, and TEXT are synonyms for VARCHAR in Snowflake, so the type is reported as VARCHAR(25).

## 584. Which feature lets Snowflake call out to an external SaaS/API for processing?

*Domain: Data Transformations | Difficulty: intermediate*

- A. External functions
- B. External tables
- C. Streams
- D. Sequences

**Answer:** A - External functions invoke remote services (through an API integration/gateway) to process data outside Snowflake and return results.

## 585. Which command adds consumer accounts to an existing share?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. ALTER SHARE ... ADD ACCOUNTS
- B. CREATE SHARE
- C. GRANT IMPORT SHARE
- D. ALTER DATABASE

**Answer:** A - After creating a share and granting objects to it, ALTER SHARE ... ADD ACCOUNTS grants the listed consumer accounts access.

## 586. Which constructs does Snowflake support for recursive/hierarchical queries?

*Domain: Data Transformations | Difficulty: advanced*

- A. CONNECT BY and recursive CTEs (WITH RECURSIVE)
- B. PIVOT only
- C. FLATTEN only
- D. MERGE only

**Answer:** A - Snowflake supports hierarchical queries via CONNECT BY ... START WITH and via recursive common table expressions.

## 587. Which built-in function checks whether a role is active or inherited in the current session?

*Domain: Account Access and Security | Difficulty: intermediate*

- A. IS_ROLE_IN_SESSION
- B. CURRENT_ROLE
- C. IS_GRANTED
- D. ROLE_EXISTS

**Answer:** A - IS_ROLE_IN_SESSION tests whether a given role is in the active role hierarchy of the session, which is useful inside policies.

## 588. What is the recommended way to give a non-production account access to production data?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. Create a data share and grant it to the non-prod account
- B. Copy the data via nightly exports
- C. Grant ACCOUNTADMIN across accounts
- D. Email CSV extracts

**Answer:** A - Secure Data Sharing gives the non-prod account live, read-only access without copying data or duplicating storage.

## 589. Which Snowflake feature provides governed sharing among a curated group of accounts?

*Domain: Data Protection and Data Sharing | Difficulty: advanced*

- A. Data Exchange
- B. Reader account
- C. Result cache
- D. Resource monitor

**Answer:** A - A Data Exchange is a private, governed hub where an organization invites and manages members to share data securely.

## 590. Which protocol does Snowflake use for federated single sign-on with an identity provider?

*Domain: Account Access and Security | Difficulty: basic*

- A. SAML 2.0
- B. FTP
- C. SMTP
- D. LDAP only

**Answer:** A - Federated SSO uses SAML 2.0 with providers such as Okta, ADFS, or Azure AD to authenticate users into Snowflake.

## 591. Which of these are Python-based ways to interact with Snowflake?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. Snowpark API and Streamlit in Snowflake
- B. SnowSQL only
- C. JDBC only
- D. ODBC only

**Answer:** A - Snowpark (Python DataFrames/UDFs) and Streamlit in Snowflake let developers build Python apps and pipelines natively.

## 592. Which role is granted to every user and role by default?

*Domain: Account Access and Security | Difficulty: basic*

- A. PUBLIC
- B. SYSADMIN
- C. ACCOUNTADMIN
- D. ORGADMIN

**Answer:** A - PUBLIC is automatically held by all users and roles; any object granted to PUBLIC is accessible to everyone in the account.

## 593. Which system role can access the SNOWFLAKE database ACCOUNT_USAGE views by default?

*Domain: Account Access and Security | Difficulty: intermediate*

- A. ACCOUNTADMIN
- B. PUBLIC
- C. USERADMIN
- D. SYSADMIN

**Answer:** A - By default ACCOUNTADMIN has access to the shared SNOWFLAKE database (ACCOUNT_USAGE); this access can be delegated via grants/IMPORTED PRIVILEGES.

## 594. Which feature classifies and manages data using metadata labels?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. Object tagging
- B. Result cache
- C. Resource monitor
- D. Sequence

**Answer:** A - Object tags attach metadata labels to objects and columns for classification, governance, and cost attribution, and can drive tag-based policies.

## 595. What does AUTO_SUSPEND = 0 mean for a virtual warehouse?

*Domain: Performance and Cost Optimization Concepts | Difficulty: basic*

- A. The warehouse never auto-suspends
- B. It suspends immediately after every query
- C. It suspends after 1 second
- D. It permanently disables the warehouse

**Answer:** A - Setting AUTO_SUSPEND = 0 (or NULL) disables automatic suspension, so the warehouse keeps running (and billing) until manually suspended.

## 596. Which objects can deliver fast, pre-computed aggregate results?

*Domain: Performance and Cost Optimization Concepts | Difficulty: intermediate*

- A. Materialized views and dynamic tables
- B. Sequences and stages
- C. Streams and tasks
- D. Resource monitors

**Answer:** A - Materialized views store pre-computed results, and dynamic tables automatically maintain declaratively-defined transformed/aggregated data.

## 597. Which is the highest Snowflake edition?

*Domain: Snowflake AI Data Cloud Features and Architecture | Difficulty: intermediate*

- A. Virtual Private Snowflake (VPS)
- B. Business Critical
- C. Enterprise
- D. Standard

**Answer:** A - Editions ascend Standard, Enterprise, Business Critical, and Virtual Private Snowflake; VPS is the highest, offering a fully isolated environment.

## 598. Which feature keeps data available if an entire account or region becomes inaccessible?

*Domain: Data Protection and Data Sharing | Difficulty: intermediate*

- A. Cross-region replication (with failover)
- B. Time Travel
- C. Result cache
- D. Search Optimization Service

**Answer:** A - Replicating to another region/account and using failover groups maintains availability during a regional or account-level outage.
