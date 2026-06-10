# SnowPro Core Mock Exam 04 (100 Questions)

## 1. An analyst says queries are slow only on Monday mornings with many users. First architecture-level fix?
**Answer:** Enable multi-cluster warehouse or separate user groups by warehouse.

## 2. What does warehouse auto-resume reduce?
**Answer:** Manual start delays before query execution.

## 3. Which Snowflake feature avoids copying data to create QA environment quickly?
**Answer:** Zero-copy cloning.

## 4. What is the key distinction between cloning and sharing?
**Answer:** Clone creates independent object copy-on-write; sharing exposes live read-only data.

## 5. A table dropped 2 hours ago must be restored. Which command family helps?
**Answer:** UNDROP command.

## 6. Which feature has configurable retention period on many objects?
**Answer:** Time Travel.

## 7. Which recovery layer is always 7 days for permanent data?
**Answer:** Fail-safe.

## 8. Who initiates Fail-safe recovery?
**Answer:** Snowflake Support.

## 9. Which statement about micro-partitions is true?
**Answer:** Users do not manage them manually.

## 10. What improves micro-partition pruning for selective predicates?
**Answer:** Effective clustering on filtered columns.

## 11. Which command loads data from stage files into a table?
**Answer:** COPY INTO table.

## 12. Which command unloads table/query results to a stage location?
**Answer:** COPY INTO location.

## 13. Which option in COPY helps skip malformed records?
**Answer:** ON_ERROR = CONTINUE.

## 14. Which object centralizes file parsing settings used by COPY?
**Answer:** FILE FORMAT.

## 15. Which stage is best when source files already reside in S3 bucket?
**Answer:** External stage.

## 16. Can GET download from an external stage?
**Answer:** No, GET is for internal stages.

## 17. Which ingestion service is event-driven and serverless?
**Answer:** Snowpipe.

## 18. Which objects enable incremental processing without full table scans?
**Answer:** Streams and tasks.

## 19. What does a stream store physically?
**Answer:** Change tracking metadata, not full duplicated table data.

## 20. Which SQL statement is common after reading stream changes?
**Answer:** MERGE.

## 21. Which role hierarchy approach is recommended?
**Answer:** Grant privileges to roles, then grant roles to users.

## 22. Why avoid direct object grants to individual users at scale?
**Answer:** Harder governance and maintenance.

## 23. Which role has global account management power and should be restricted?
**Answer:** ACCOUNTADMIN.

## 24. Which role is commonly used for creating/managing business objects?
**Answer:** SYSADMIN.

## 25. Which role manages security grants and role assignments typically?
**Answer:** SECURITYADMIN.

## 26. To query table sales.orders, what object-level privilege is mandatory?
**Answer:** SELECT on the table.

## 27. To reference database and schema, what privilege is also needed?
**Answer:** USAGE on database and schema.

## 28. What does GRANT OWNERSHIP accomplish?
**Answer:** Transfers ownership control to another role.

## 29. Why is PUBLIC role sensitive in governance?
**Answer:** Privileges granted to PUBLIC are inherited broadly.

## 30. What is the purpose of masking policies?
**Answer:** Dynamic column value redaction based on context.

## 31. What is the purpose of row access policies?
**Answer:** Restrict row visibility by condition and role.

## 32. What do tags enable when combined with policies?
**Answer:** Scalable classification-driven governance.

## 33. Which security control limits allowed IP addresses?
**Answer:** Network policy.

## 34. Which authentication enhancement is strongly recommended for human users?
**Answer:** MFA.

## 35. Which authentication method is passwordless and key-based?
**Answer:** Key pair authentication.

## 36. Which integration often provides enterprise SSO?
**Answer:** SAML 2.0 identity provider integration.

## 37. Is data at rest encrypted by default?
**Answer:** Yes.

## 38. Is data in transit encrypted by default?
**Answer:** Yes.

## 39. Tri-Secret Secure mainly adds what?
**Answer:** Customer-managed key participation in encryption.

## 40. Which object limits compute spend by thresholds and actions?
**Answer:** Resource monitor.

## 41. Can resource monitor trigger warehouse suspension?
**Answer:** Yes.

## 42. What is Snowflake compute billing unit?
**Answer:** Credits.

## 43. Which account metadata source is typically used for cost reporting dashboards?
**Answer:** ACCOUNT_USAGE views.

## 44. Which history source helps inspect query duration and bytes scanned?
**Answer:** QUERY_HISTORY.

## 45. Which source helps detect warehouse queuing pressure?
**Answer:** WAREHOUSE_LOAD_HISTORY.

## 46. Which source tracks file load status events?
**Answer:** COPY_HISTORY.

## 47. What is the result cache key advantage?
**Answer:** Faster repeated query responses with no warehouse compute use.

## 48. One dashboard query is identical but returns fresh data after ETL update. Why?
**Answer:** Result cache was invalidated by data change.

## 49. Which table type is best for transient staging where Fail-safe is unnecessary?
**Answer:** Transient table.

## 50. Which table type is best for session-scoped scratch work?
**Answer:** Temporary table.

## 51. Can temporary and permanent table with same name coexist in same schema for that session?
**Answer:** Yes, temp table can shadow name resolution in session context.

## 52. Which object stores nested JSON while preserving structure?
**Answer:** VARIANT.

## 53. Which function parses JSON text payload into VARIANT?
**Answer:** PARSE_JSON.

## 54. Which function converts VARIANT back to JSON text?
**Answer:** TO_JSON.

## 55. Which function unnests arrays from VARIANT column?
**Answer:** FLATTEN.

## 56. What is a secure view’s primary exam-relevant property?
**Answer:** It limits exposure of underlying logic and metadata.

## 57. What is materialized view’s primary tradeoff?
**Answer:** Faster reads with maintenance compute overhead.

## 58. Which operation is ideal for selective row removal by predicate?
**Answer:** DELETE.

## 59. Which operation removes all rows with minimal syntax and keeps structure?
**Answer:** TRUNCATE TABLE.

## 60. Which statement supports insert/update/delete logic in one construct?
**Answer:** MERGE.

## 61. Which statement changes active role in session?
**Answer:** USE ROLE.

## 62. Which statement changes active warehouse?
**Answer:** USE WAREHOUSE.

## 63. Which statement changes active database?
**Answer:** USE DATABASE.

## 64. Which statement changes active schema?
**Answer:** USE SCHEMA.

## 65. Which object can be cloned quickly for test refresh?
**Answer:** Databases, schemas, and tables.

## 66. After clone, if source table is dropped, does clone survive?
**Answer:** Yes, clone remains independent.

## 67. Why split ETL and ad-hoc workloads to different warehouses?
**Answer:** Prevent resource contention and improve predictability.

## 68. What is common first response to BI concurrency spikes?
**Answer:** Add multi-cluster capability or dedicated BI warehouse.

## 69. What is common first response to heavy transformation runtime?
**Answer:** Increase warehouse size or optimize query patterns.

## 70. Which Snowflake feature supports data products without replication copies?
**Answer:** Secure data sharing/listings.

## 71. What does reader account allow for providers?
**Answer:** Share data with consumers who lack Snowflake account.

## 72. Can consumer write back to provider shared tables?
**Answer:** No.

## 73. Which kind of metadata view is SQL standard and database-scoped?
**Answer:** INFORMATION_SCHEMA.

## 74. Which kind of metadata view is account-scoped and operational?
**Answer:** ACCOUNT_USAGE.

## 75. What is best immediate source to analyze one slow query plan?
**Answer:** Query Profile.

## 76. Which object gives repeatable numeric IDs without sequence table hacks?
**Answer:** Sequence.

## 77. Which file format type is often best for analytics interchange with schema support?
**Answer:** Parquet.

## 78. What is a frequent reason for JSON extraction errors?
**Answer:** Incorrect path or unexpected data type.

## 79. Which command is used for local file upload to internal stage?
**Answer:** PUT.

## 80. Which command is used for internal stage download to local filesystem?
**Answer:** GET.

## 81. Can Snowflake scale storage and compute independently?
**Answer:** Yes.

## 82. Why is this separation important operationally?
**Answer:** It allows flexible performance tuning without data movement.

## 83. What defines a warehouse size class effect?
**Answer:** Amount of compute resources available.

## 84. Which setting controls minimum and maximum clusters in multi-cluster warehouse?
**Answer:** Warehouse MIN_CLUSTER_COUNT and MAX_CLUSTER_COUNT.

## 85. What happens when warehouse reaches max clusters and demand still grows?
**Answer:** Additional queries may queue.

## 86. Which monitoring signals help avoid persistent queueing?
**Answer:** Queue time and load history trends.

## 87. What does least privilege reduce besides security risk?
**Answer:** Blast radius of operational mistakes.

## 88. Which grant type helps future-proof access for newly created tables?
**Answer:** Future grants.

## 89. Why use dedicated roles per function (loader, analyst, admin)?
**Answer:** Clear separation of duties.

## 90. Which Snowflake feature supports governance classification at object/column level?
**Answer:** Tags.

## 91. Which feature supports private collaborative analytics with controls?
**Answer:** Snowflake clean room capabilities.

## 92. Which command recovers dropped database if still retained?
**Answer:** UNDROP DATABASE.

## 93. Does dropping and recreating object with CREATE OR REPLACE preserve grants automatically in all cases?
**Answer:** Not in all cases; review object and grant behavior.

## 94. What is the benefit of using task graphs?
**Answer:** Orchestrated dependency-based pipeline execution.

## 95. Which function returns active warehouse context?
**Answer:** CURRENT_WAREHOUSE().

## 96. Which function returns active database context?
**Answer:** CURRENT_DATABASE().

## 97. Which function returns active schema context?
**Answer:** CURRENT_SCHEMA().

## 98. What is the simplest spend control pattern for non-critical dev warehouse?
**Answer:** Aggressive auto-suspend plus resource monitor cap.

## 99. If analysts need fresh low-latency dashboards after frequent loads, what should be tuned?
**Answer:** Ingestion cadence, warehouse sizing, and query design/pruning.

## 100. One-line SnowPro Core exam mindset?
**Answer:** Choose the safest, scalable, and simplest Snowflake-native solution.