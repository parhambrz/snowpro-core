# SnowPro Core Mock Exam 05 (100 Questions)

## 1. A data engineer needs low-latency ingestion from cloud object storage notifications. Which Snowflake service fits?
**Answer:** Snowpipe with auto-ingest.

## 2. A DBA wants to replay table state from yesterday noon. Which feature is used?
**Answer:** Time Travel.

## 3. A user asks for direct SQL access to Fail-safe snapshots. Is that supported?
**Answer:** No.

## 4. What is the first architecture concept tested in SnowPro Core frequently?
**Answer:** Separation of storage, compute, and cloud services.

## 5. What scales independently when you resize a warehouse?
**Answer:** Compute only.

## 6. Does warehouse suspension remove local cache benefits permanently?
**Answer:** Suspending can clear warehouse-local cache.

## 7. Which setting prevents paying for long idle periods?
**Answer:** Auto-suspend.

## 8. Which setting reduces user friction after suspension?
**Answer:** Auto-resume.

## 9. Which warehouse type handles sudden concurrency surges best?
**Answer:** Multi-cluster warehouse.

## 10. Which object should separate finance and marketing workloads for cost attribution?
**Answer:** Separate warehouses.

## 11. Which usage source helps report credits consumed over time?
**Answer:** ACCOUNT_USAGE views.

## 12. Which source helps locate top expensive SQL statements?
**Answer:** QUERY_HISTORY.

## 13. Which source helps detect query queueing trends?
**Answer:** WAREHOUSE_LOAD_HISTORY.

## 14. Which source tracks COPY file ingestion outcomes?
**Answer:** COPY_HISTORY.

## 15. Which object defines parsing details for staged data files?
**Answer:** FILE FORMAT.

## 16. Which statement ingests from stage into table?
**Answer:** COPY INTO table.

## 17. Which statement exports table/query result to stage?
**Answer:** COPY INTO location.

## 18. Which stage is Snowflake-managed?
**Answer:** Internal stage.

## 19. Which stage references customer cloud bucket/container?
**Answer:** External stage.

## 20. Which command uploads from local machine to internal stage?
**Answer:** PUT.

## 21. Which command retrieves files from internal stage to local machine?
**Answer:** GET.

## 22. What is the primary type for semi-structured data in Snowflake?
**Answer:** VARIANT.

## 23. Which function parses JSON text into VARIANT format?
**Answer:** PARSE_JSON.

## 24. Which function expands nested arrays/objects into rows?
**Answer:** FLATTEN.

## 25. What does micro-partition pruning reduce?
**Answer:** Amount of data scanned.

## 26. What often improves pruning for range filters?
**Answer:** Effective clustering key choice.

## 27. Should clustering keys be added to every table by default?
**Answer:** No.

## 28. What does result cache provide for repeated eligible queries?
**Answer:** Fast responses without warehouse compute use.

## 29. Can result cache be reused if underlying data changes?
**Answer:** No.

## 30. Which feature creates test copies quickly with minimal initial storage?
**Answer:** Zero-copy cloning.

## 31. Are clones read-only?
**Answer:** No, clones are independent writable objects.

## 32. What tracks net row changes for downstream processing?
**Answer:** Stream object.

## 33. What schedules SQL execution in Snowflake pipelines?
**Answer:** Task object.

## 34. Best pair for incremental ELT in Snowflake-native design?
**Answer:** Streams and tasks.

## 35. Which statement is commonly used with stream data to sync target table?
**Answer:** MERGE.

## 36. Which role model controls Snowflake access?
**Answer:** RBAC.

## 37. Which built-in role should be tightly limited to few admins?
**Answer:** ACCOUNTADMIN.

## 38. Which role is commonly associated with object creation/ownership workflows?
**Answer:** SYSADMIN.

## 39. Which role often manages users and role grants?
**Answer:** USERADMIN.

## 40. Which role often manages privilege grants and security structure?
**Answer:** SECURITYADMIN.

## 41. To query table data, which privilege is mandatory on the table?
**Answer:** SELECT.

## 42. To resolve table namespace, which additional privileges are needed?
**Answer:** USAGE on database and schema.

## 43. What is least privilege principle?
**Answer:** Grant only permissions required for the task.

## 44. Why minimize privileges on PUBLIC role?
**Answer:** PUBLIC is inherited broadly by all users/roles.

## 45. Which statement changes active role?
**Answer:** USE ROLE.

## 46. Which statement changes active warehouse?
**Answer:** USE WAREHOUSE.

## 47. Which statement changes active database?
**Answer:** USE DATABASE.

## 48. Which statement changes active schema?
**Answer:** USE SCHEMA.

## 49. What does GRANT OWNERSHIP do?
**Answer:** Transfers ownership and control of an object.

## 50. Which feature enables secure live data access without copying?
**Answer:** Secure data sharing.

## 51. Which object packages data to share with consumer accounts?
**Answer:** Share object.

## 52. Can data consumers update provider shared base tables directly?
**Answer:** No.

## 53. Which option allows sharing with organizations that do not have Snowflake account?
**Answer:** Reader account.

## 54. Which policy hides sensitive values conditionally?
**Answer:** Masking policy.

## 55. Which policy enforces row-level filtering by role or context?
**Answer:** Row access policy.

## 56. Which metadata feature supports classification-driven governance?
**Answer:** Tags.

## 57. Which control restricts network source addresses for login?
**Answer:** Network policy.

## 58. Which security measure strengthens password-based access?
**Answer:** MFA.

## 59. Which authentication method is key-based and common for service users?
**Answer:** Key pair authentication.

## 60. Is Snowflake data encrypted at rest by default?
**Answer:** Yes.

## 61. Is Snowflake data encrypted in transit by default?
**Answer:** Yes.

## 62. What does Tri-Secret Secure provide at high level?
**Answer:** Additional customer key control in encryption model.

## 63. Which object helps cap warehouse credit usage with thresholds?
**Answer:** Resource monitor.

## 64. Can resource monitor suspend warehouse automatically?
**Answer:** Yes.

## 65. Compute charges are measured in what unit?
**Answer:** Credits.

## 66. For one long-running heavy query, what is often best first scaling step?
**Answer:** Increase warehouse size.

## 67. For many short concurrent queries, what is often best first step?
**Answer:** Increase concurrency via multi-cluster or workload separation.

## 68. Which diagnostic view shows plan operators and timing breakdown?
**Answer:** Query Profile.

## 69. Which table type has Fail-safe?
**Answer:** Permanent table.

## 70. Which table type avoids Fail-safe to reduce storage cost?
**Answer:** Transient table.

## 71. Which table type is session-specific and auto-dropped?
**Answer:** Temporary table.

## 72. Which command restores dropped table in retention window?
**Answer:** UNDROP TABLE.

## 73. Which command removes all rows and retains structure quickly?
**Answer:** TRUNCATE TABLE.

## 74. Which command supports selective row deletion by condition?
**Answer:** DELETE.

## 75. Which object can speed recurring expensive query patterns by precomputation?
**Answer:** Materialized view.

## 76. What is key tradeoff of materialized views?
**Answer:** Faster reads, added maintenance cost.

## 77. Which view type limits underlying query logic exposure?
**Answer:** Secure view.

## 78. Which object generates incremental unique numeric values?
**Answer:** Sequence.

## 79. Which metadata collection is SQL standard and scoped by database?
**Answer:** INFORMATION_SCHEMA.

## 80. Which metadata collection is operational and account-wide?
**Answer:** ACCOUNT_USAGE.

## 81. Which command is generally used to switch context before running unqualified object names?
**Answer:** USE DATABASE and USE SCHEMA.

## 82. Which behavior is true for CREATE OR REPLACE?
**Answer:** It recreates object definition and replaces existing object.

## 83. Can cloned objects be used for quick rollback strategy in non-prod?
**Answer:** Yes.

## 84. Which Snowflake feature supports marketplace-style data distribution?
**Answer:** Listings and Snowflake Marketplace.

## 85. Which is serverless by default: Snowpipe or standard warehouse query?
**Answer:** Snowpipe.

## 86. Why isolate ELT and BI warehouses even with same data?
**Answer:** To prevent contention and simplify cost governance.

## 87. If users complain about first query delay after inactivity, what setting likely caused it?
**Answer:** Auto-suspend with warehouse resume delay.

## 88. Is this delay usually acceptable for cost optimization?
**Answer:** Yes, depending on SLA.

## 89. Which function returns currently active role?
**Answer:** CURRENT_ROLE().

## 90. Which function returns current user identity?
**Answer:** CURRENT_USER().

## 91. Which function returns active warehouse context?
**Answer:** CURRENT_WAREHOUSE().

## 92. What does warehouse isolation provide besides performance?
**Answer:** Cleaner chargeback/showback.

## 93. Which object category is not shared through secure share: compute warehouse or database objects?
**Answer:** Compute warehouse.

## 94. Which command family should be used to inspect load failures quickly?
**Answer:** COPY history and validation options.

## 95. Which access strategy supports separation of duties best?
**Answer:** Role hierarchy by job function.

## 96. Which admin practice reduces accidental production changes?
**Answer:** Use lower-privilege roles for daily operations.

## 97. Which strategy helps with rapid environment provisioning for QA/UAT?
**Answer:** Clone production-like schemas/databases.

## 98. Which factor determines if query uses fewer micro-partitions?
**Answer:** Predicate selectivity and data layout.

## 99. What is the exam-appropriate reason to use Snowflake-native features first?
**Answer:** Simpler operations, scalability, and governance alignment.

## 100. In one line, what should guide SnowPro Core answers?
**Answer:** Prefer secure, cost-aware, and scalable native Snowflake design choices.