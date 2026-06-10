# Snowflake SnowPro Core Practice Questions (100)

> These are original practice questions aligned to SnowPro Core topics, not copied exam items.

## 1. What is Snowflake’s architecture model?
**Answer:** Multi-cluster shared data architecture (separate storage, compute, and cloud services).

## 2. What are the three main Snowflake layers?
**Answer:** Database storage, query processing (virtual warehouses), and cloud services.

## 3. What is a virtual warehouse in Snowflake?
**Answer:** A compute cluster used to run SQL queries and DML operations.

## 4. Does resizing a warehouse affect stored data?
**Answer:** No, resizing only changes compute resources.

## 5. What does auto-suspend do for a warehouse?
**Answer:** It stops the warehouse after inactivity to reduce compute cost.

## 6. What does auto-resume do for a warehouse?
**Answer:** It automatically starts the warehouse when a new query is submitted.

## 7. What is a multi-cluster warehouse used for?
**Answer:** Handling concurrency by automatically adding/removing clusters.

## 8. Which Snowflake edition supports failover/failback across regions?
**Answer:** Business Critical (and above) with replication/failover features.

## 9. What is Time Travel in Snowflake?
**Answer:** A feature to access historical table, schema, and database data.

## 10. What is Fail-safe in Snowflake?
**Answer:** A 7-day recovery period after Time Travel expires, managed by Snowflake.

## 11. Can users directly query Fail-safe data?
**Answer:** No, Snowflake Support must perform Fail-safe recovery.

## 12. What is zero-copy cloning?
**Answer:** Creating a clone without copying physical data at creation time.

## 13. What is data sharing in Snowflake?
**Answer:** Securely sharing live data without copying it.

## 14. What object is used to share data with another account?
**Answer:** A share object.

## 15. What is a reader account?
**Answer:** A Snowflake-managed account for data consumers without their own account.

## 16. What are micro-partitions?
**Answer:** Automatic, immutable storage units used internally by Snowflake.

## 17. Why are micro-partitions important for performance?
**Answer:** They enable pruning, so fewer data blocks are scanned.

## 18. What is partition pruning?
**Answer:** Skipping irrelevant micro-partitions during query execution.

## 19. What is clustering in Snowflake?
**Answer:** Organizing table data to improve pruning for specific query patterns.

## 20. What is a clustering key?
**Answer:** Columns/expression used to co-locate related rows in micro-partitions.

## 21. Does Snowflake automatically collect statistics for optimization?
**Answer:** Yes, metadata/statistics are automatically maintained.

## 22. What is result cache?
**Answer:** Reuse of a previous query result when underlying data and query conditions match.

## 23. Does result cache require warehouse compute for retrieval?
**Answer:** No, returning a cached result does not require warehouse compute.

## 24. What is the default data type for VARIANT storage?
**Answer:** Semi-structured data (JSON, Avro, ORC, Parquet, XML) in VARIANT.

## 25. Which function parses JSON text into VARIANT?
**Answer:** `PARSE_JSON`.

## 26. Which notation is used to access fields inside VARIANT?
**Answer:** Dot notation and bracket notation.

## 27. What does `FLATTEN` do?
**Answer:** Expands nested arrays/objects into rows.

## 28. What is an internal stage?
**Answer:** Snowflake-managed staging location for files.

## 29. What is an external stage?
**Answer:** Stage pointing to cloud storage like S3, Azure Blob, or GCS.

## 30. What command loads data from stage files into a table?
**Answer:** `COPY INTO <table>`.

## 31. What command unloads query/table data into files?
**Answer:** `COPY INTO <location>`.

## 32. What is a file format object?
**Answer:** A reusable object defining how staged files are parsed or written.

## 33. What does `ON_ERROR = CONTINUE` in COPY do?
**Answer:** Loads valid rows and skips rows with errors.

## 34. What does `VALIDATION_MODE` in COPY help with?
**Answer:** Testing/validating data load without fully loading data.

## 35. What is Snowpipe used for?
**Answer:** Continuous, automated file ingestion from stages.

## 36. Is Snowpipe serverless?
**Answer:** Yes, Snowpipe uses serverless compute billing.

## 37. What object tracks changed rows for CDC patterns?
**Answer:** A stream.

## 38. What object schedules SQL operations in Snowflake?
**Answer:** A task.

## 39. Can tasks depend on other tasks?
**Answer:** Yes, tasks can form task graphs.

## 40. What is the main use of streams + tasks together?
**Answer:** Incremental ELT pipelines.

## 41. What is RBAC in Snowflake?
**Answer:** Role-Based Access Control for privileges and object access.

## 42. What is the difference between account roles and database roles?
**Answer:** Account roles are global; database roles are scoped to a database.

## 43. Which role has full account-level administrative control?
**Answer:** `ACCOUNTADMIN`.

## 44. Which role manages users and roles typically?
**Answer:** `USERADMIN` for users/roles, `SECURITYADMIN` for grants/security.

## 45. Which role manages warehouses and compute resources?
**Answer:** `SYSADMIN` (commonly owns objects) and can manage warehouses with proper grants.

## 46. What is least privilege in Snowflake security?
**Answer:** Grant only the minimum permissions required.

## 47. What privilege allows selecting rows from a table?
**Answer:** `SELECT` on the table (and required parent grants).

## 48. What command changes the active role?
**Answer:** `USE ROLE <role_name>`.

## 49. What command changes active warehouse?
**Answer:** `USE WAREHOUSE <warehouse_name>`.

## 50. What object controls network-level access to Snowflake?
**Answer:** Network policy.

## 51. What is MFA in Snowflake context?
**Answer:** Multi-factor authentication for stronger login security.

## 52. What is Tri-Secret Secure?
**Answer:** Encryption model combining customer-managed key with Snowflake keys.

## 53. Is data encrypted at rest in Snowflake?
**Answer:** Yes, by default.

## 54. Is data encrypted in transit in Snowflake?
**Answer:** Yes, TLS is used for data in transit.

## 55. What are masking policies used for?
**Answer:** Dynamic data masking based on role/context.

## 56. What are row access policies used for?
**Answer:** Row-level security filtering.

## 57. What are tags in Snowflake?
**Answer:** Metadata labels for governance/classification and policy automation.

## 58. What is object ownership in Snowflake?
**Answer:** The owning role controls object management and grant authority.

## 59. What does `GRANT OWNERSHIP` do?
**Answer:** Transfers object ownership to another role.

## 60. What is the `PUBLIC` role?
**Answer:** A built-in role granted to all users and roles.

## 61. What is a resource monitor?
**Answer:** An object that tracks credit usage and can trigger actions at thresholds.

## 62. Can a resource monitor suspend warehouses?
**Answer:** Yes, based on configured usage thresholds/actions.

## 63. What billing unit is used for warehouse compute?
**Answer:** Credits.

## 64. What generally increases compute cost more: larger warehouse or longer runtime?
**Answer:** Both increase cost; total credits depend on size and runtime.

## 65. What is Query Profile used for?
**Answer:** Analyzing query execution steps and bottlenecks.

## 66. What is `QUERY_HISTORY` used for?
**Answer:** Reviewing executed queries, duration, status, and resource usage.

## 67. What does `WAREHOUSE_LOAD_HISTORY` help analyze?
**Answer:** Warehouse concurrency/load over time.

## 68. What does `COPY_HISTORY` show?
**Answer:** Historical file load activity and status.

## 69. What is the purpose of the Information Schema?
**Answer:** SQL-standard metadata views per database.

## 70. What are ACCOUNT_USAGE views?
**Answer:** Snowflake-provided account-level usage and governance views.

## 71. What is data retention period in Snowflake?
**Answer:** The Time Travel duration configured for an object/account.

## 72. Can temporary tables be recovered after session ends?
**Answer:** No, temporary tables are dropped at session end.

## 73. What is a transient table?
**Answer:** A table without Fail-safe, typically for lower-cost transient data.

## 74. What is a temporary table?
**Answer:** Session-scoped table visible only within the creating session.

## 75. What happens if table and view share a name in same schema?
**Answer:** Not allowed for same object type namespace rules.

## 76. What does `CREATE OR REPLACE` do?
**Answer:** Recreates an object, replacing existing definition.

## 77. What does `UNDROP` do?
**Answer:** Restores a dropped object within retention window.

## 78. What are secure views for?
**Answer:** Preventing exposure of underlying logic/metadata beyond intended access.

## 79. What is a materialized view?
**Answer:** A precomputed, maintained result set to speed certain queries.

## 80. Are materialized views free to maintain?
**Answer:** No, maintenance consumes compute/credits.

## 81. What is a sequence used for?
**Answer:** Generating unique numeric values.

## 82. What is a Snowflake stage used for?
**Answer:** Storing pointers/locations for loading or unloading files.

## 83. What is the difference between `PUT` and `GET`?
**Answer:** `PUT` uploads to internal stage; `GET` downloads from internal stage.

## 84. Can `PUT` upload directly to external stages?
**Answer:** No, `PUT` is for internal stages.

## 85. What does `MERGE` do?
**Answer:** Combines insert/update/delete logic in one statement.

## 86. Which command removes all rows but keeps table structure?
**Answer:** `TRUNCATE TABLE`.

## 87. Does `DELETE` keep deleted data available via Time Travel?
**Answer:** Yes, until retention expires.

## 88. What is Snowpark?
**Answer:** Developer framework to process data in Snowflake using languages like Python/Scala/Java.

## 89. What is a user-defined function (UDF)?
**Answer:** Custom function callable in SQL expressions.

## 90. What is a stored procedure in Snowflake?
**Answer:** Procedural logic that can execute SQL and control flow.

## 91. What is the difference between authentication and authorization?
**Answer:** Authentication verifies identity; authorization controls permissions.

## 92. What is SSO in Snowflake?
**Answer:** Single Sign-On via identity providers (typically SAML/OAuth integrations).

## 93. What is key pair authentication?
**Answer:** RSA key-based authentication often used for service users.

## 94. What is data replication in Snowflake?
**Answer:** Copying database/account objects across regions/accounts for DR and sharing scenarios.

## 95. What is failover group used for?
**Answer:** Managing replicated objects and orchestrating account failover.

## 96. What is the purpose of warehouses with different sizes?
**Answer:** Match compute power to workload performance/concurrency needs.

## 97. What is query concurrency scaling in Snowflake context?
**Answer:** Automatic addition of clusters in multi-cluster warehouses for concurrent load.

## 98. What is a common reason to use separate warehouses for BI and ELT?
**Answer:** Isolate workloads for stable performance and cost control.

## 99. What does `USE DATABASE` do?
**Answer:** Sets the current database context for the session.

## 100. What does `USE SCHEMA` do?
**Answer:** Sets the current schema context for the session.
