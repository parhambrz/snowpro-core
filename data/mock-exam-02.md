# SnowPro Core Mock Exam 02 (100 Questions)

## 1. A team wants to scale BI queries without impacting ETL jobs. What should they do?
**Answer:** Use separate virtual warehouses for BI and ETL workloads.

## 2. A warehouse is idle most of the day. Which setting reduces cost most directly?
**Answer:** Enable auto-suspend with a short inactivity timeout.

## 3. Users report long queue times during peak dashboards. Which warehouse feature helps first?
**Answer:** Multi-cluster warehouse for concurrency scaling.

## 4. Which Snowflake layer manages authentication and metadata?
**Answer:** Cloud services layer.

## 5. Does increasing warehouse size change storage cost?
**Answer:** No, it changes compute cost only.

## 6. Which command sets the active compute cluster?
**Answer:** USE WAREHOUSE.

## 7. What is the primary purpose of micro-partition metadata?
**Answer:** It supports pruning and optimization.

## 8. Which object should be used to automate continuous file ingestion?
**Answer:** Snowpipe.

## 9. A company wants near-real-time ingestion from cloud storage events. Best fit?
**Answer:** Snowpipe with auto-ingest.

## 10. Which command loads staged files into a target table?
**Answer:** COPY INTO table.

## 11. Which COPY option skips bad rows and continues loading?
**Answer:** ON_ERROR = CONTINUE.

## 12. Which COPY option is used to test load validity before full load?
**Answer:** VALIDATION_MODE.

## 13. A table was accidentally dropped today. Which feature likely enables restore?
**Answer:** Time Travel with UNDROP.

## 14. After Time Travel expires, what recovery option remains?
**Answer:** Fail-safe recovery by Snowflake Support.

## 15. Can users query Fail-safe data directly with SQL?
**Answer:** No.

## 16. What is the benefit of zero-copy cloning for dev/test?
**Answer:** Fast environment creation without initial data copy.

## 17. A clone is created, then source table changes. Does clone auto-sync?
**Answer:** No, clone diverges after creation.

## 18. Which object captures table row changes for downstream processing?
**Answer:** Stream.

## 19. Which object schedules SQL pipelines in Snowflake?
**Answer:** Task.

## 20. Best pattern for incremental ELT in Snowflake?
**Answer:** Streams plus tasks.

## 21. Which role model does Snowflake use for access control?
**Answer:** Role-based access control (RBAC).

## 22. Which built-in role has highest account privileges?
**Answer:** ACCOUNTADMIN.

## 23. Which role typically handles user and role management?
**Answer:** USERADMIN.

## 24. Which role typically handles grants and security policy administration?
**Answer:** SECURITYADMIN.

## 25. What principle reduces security risk in Snowflake grants?
**Answer:** Least privilege.

## 26. A consumer has no Snowflake account but needs shared data. What can provider use?
**Answer:** Reader account.

## 27. Does secure data sharing copy provider data into consumer account?
**Answer:** No, it shares live data without copying.

## 28. Which object is required to expose data for secure sharing?
**Answer:** Share object.

## 29. Where are stage files stored for an internal named stage?
**Answer:** Snowflake-managed internal storage.

## 30. Which command uploads local files to an internal stage?
**Answer:** PUT.

## 31. Which command downloads files from internal stage to local environment?
**Answer:** GET.

## 32. Can PUT upload files directly to external cloud storage stages?
**Answer:** No.

## 33. Which data type stores semi-structured JSON efficiently?
**Answer:** VARIANT.

## 34. Which function converts JSON text into VARIANT?
**Answer:** PARSE_JSON.

## 35. Which table function expands nested JSON arrays into rows?
**Answer:** FLATTEN.

## 36. Which policy type hides sensitive column values by role/context?
**Answer:** Masking policy.

## 37. Which policy type filters records based on row-level conditions?
**Answer:** Row access policy.

## 38. What are tags commonly used for in governance?
**Answer:** Data classification and policy automation.

## 39. Which network control restricts client connectivity by IP rules?
**Answer:** Network policy.

## 40. Is encryption at rest enabled by default in Snowflake?
**Answer:** Yes.

## 41. Is TLS used for data in transit in Snowflake?
**Answer:** Yes.

## 42. What does Tri-Secret Secure add?
**Answer:** Customer-managed key participation in encryption hierarchy.

## 43. Which view family is most used for account-level usage monitoring?
**Answer:** ACCOUNT_USAGE views.

## 44. Which history view helps diagnose warehouse queuing and load?
**Answer:** WAREHOUSE_LOAD_HISTORY.

## 45. Which view is used to inspect executed SQL statements?
**Answer:** QUERY_HISTORY.

## 46. Which view tracks COPY load operations?
**Answer:** COPY_HISTORY.

## 47. A query runs repeatedly with same text and unchanged data. Why can it return instantly?
**Answer:** Result cache reuse.

## 48. Does returning result cache consume warehouse compute credits?
**Answer:** No.

## 49. What is a transient table mainly used for?
**Answer:** Data that does not need Fail-safe.

## 50. What is a temporary table lifecycle?
**Answer:** Exists only for the session.

## 51. Can another session read your temporary table?
**Answer:** No.

## 52. Which command restores a dropped table within retention window?
**Answer:** UNDROP TABLE.

## 53. Which command removes all rows but keeps table definition?
**Answer:** TRUNCATE TABLE.

## 54. DELETE vs TRUNCATE for logging removed rows in query history: which removes selectively?
**Answer:** DELETE.

## 55. Which statement supports matched update and unmatched insert in one operation?
**Answer:** MERGE.

## 56. Which object stores reusable parsing options for CSV/JSON/Parquet?
**Answer:** File format object.

## 57. Which Snowflake feature enables historical access to changed/deleted rows?
**Answer:** Time Travel.

## 58. If retention is 1 day, can you restore data from 10 days ago?
**Answer:** No.

## 59. Which role should own business tables in common enterprise practice?
**Answer:** SYSADMIN-owned functional roles.

## 60. Why avoid using ACCOUNTADMIN for daily queries?
**Answer:** It violates least privilege and increases risk.

## 61. Which command sets active database context?
**Answer:** USE DATABASE.

## 62. Which command sets active schema context?
**Answer:** USE SCHEMA.

## 63. Which object can enforce spending thresholds and suspend warehouses?
**Answer:** Resource monitor.

## 64. What is Snowflake billing unit for compute?
**Answer:** Credits.

## 65. Which factor affects compute credits most directly?
**Answer:** Warehouse size and runtime duration.

## 66. If concurrency is low but single query is slow, scale which way first?
**Answer:** Scale up warehouse size.

## 67. If many queries queue but each is light, scale which way first?
**Answer:** Enable or increase multi-cluster/concurrency.

## 68. What is the main purpose of Query Profile?
**Answer:** Identify scan, join, and execution bottlenecks.

## 69. What does secure view primarily protect?
**Answer:** Underlying logic/metadata exposure.

## 70. Does materialized view maintenance consume credits?
**Answer:** Yes.

## 71. When is a materialized view useful?
**Answer:** Repeated expensive queries on relatively stable data patterns.

## 72. Which object generates sequential unique numbers?
**Answer:** Sequence.

## 73. Can Snowflake auto-manage clustering depth for large tables with keys?
**Answer:** Yes, via automatic clustering when enabled.

## 74. What is pruning effectiveness tied to?
**Answer:** Data organization and predicate selectivity.

## 75. Which function returns current active role name?
**Answer:** CURRENT_ROLE().

## 76. Which function returns current warehouse name?
**Answer:** CURRENT_WAREHOUSE().

## 77. Which model supports delegated authentication from enterprise identity provider?
**Answer:** SSO via SAML/OAuth integration.

## 78. Which authentication method is common for service accounts and automation?
**Answer:** Key pair authentication.

## 79. What is the purpose of object ownership transfer?
**Answer:** Move control/grant authority to another role.

## 80. Which statement performs ownership transfer?
**Answer:** GRANT OWNERSHIP.

## 81. Can data providers monetize listings through Snowflake Marketplace?
**Answer:** Yes.

## 82. What is a primary use case for data clean rooms?
**Answer:** Privacy-preserving collaborative analysis.

## 83. Which object type can contain stages, file formats, and tables?
**Answer:** Schema.

## 84. What must be active to run a query requiring compute?
**Answer:** A running virtual warehouse.

## 85. Can cloud services operations incur cost even without warehouse usage?
**Answer:** Yes, some cloud services activities can.

## 86. Which account usage view helps track storage growth trends?
**Answer:** STORAGE_USAGE or related storage views.

## 87. If a query filter matches clustering key columns, expected effect?
**Answer:** Better pruning and faster performance.

## 88. What is the simplest way to isolate unpredictable analyst workloads?
**Answer:** Put them on dedicated warehouse(s).

## 89. Can one warehouse run queries from multiple users concurrently?
**Answer:** Yes.

## 90. If workload is bursty and unpredictable, what warehouse setting helps?
**Answer:** Auto-suspend and auto-resume.

## 91. Which object dependency is required to query a table?
**Answer:** USAGE on database and schema, plus SELECT on table.

## 92. What does PUBLIC role assignment imply?
**Answer:** Every user/role inherits privileges granted to PUBLIC.

## 93. Why should grants to PUBLIC be minimal?
**Answer:** They apply broadly across the account.

## 94. Which operation is serverless: Snowpipe or standard COPY via warehouse?
**Answer:** Snowpipe.

## 95. What is database replication mainly for?
**Answer:** Disaster recovery and cross-region availability.

## 96. What does a failover group coordinate?
**Answer:** Replicated objects and failover orchestration.

## 97. Can clones be created for databases, schemas, and tables?
**Answer:** Yes.

## 98. What is the practical benefit of cloning in CI/testing?
**Answer:** Fast environment reset with low initial storage overhead.

## 99. Which statement is true about Snowflake scaling?
**Answer:** Compute scales independently from storage.

## 100. What is the best short definition of Snowflake?
**Answer:** A cloud-native data platform with separate storage and compute.