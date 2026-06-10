# SnowPro Core Mock Exam 03 (100 Questions)

## 1. A finance team requires strict DR in another region. Which Snowflake capability is needed?
**Answer:** Replication with failover groups.

## 2. What component executes SQL statements in Snowflake?
**Answer:** Virtual warehouse compute layer.

## 3. What component stores table data in Snowflake?
**Answer:** Centralized storage layer.

## 4. What component coordinates transactions and metadata?
**Answer:** Cloud services.

## 5. If warehouse is suspended, can queries still run?
**Answer:** It must resume first; then queries run.

## 6. What configuration minimizes idle compute spend?
**Answer:** Short auto-suspend with auto-resume enabled.

## 7. Why might an XL warehouse outperform four separate small warehouses for one heavy query?
**Answer:** More compute for a single query execution path.

## 8. Why might multiple warehouses be better than one large shared warehouse?
**Answer:** Better workload isolation and predictable performance.

## 9. Which feature allows point-in-time query of a table’s older state?
**Answer:** Time Travel.

## 10. Which feature is not user-self-service: Time Travel or Fail-safe?
**Answer:** Fail-safe.

## 11. Can Fail-safe period be set to zero for permanent tables?
**Answer:** No, Fail-safe applies to permanent objects.

## 12. Which table type has no Fail-safe by design?
**Answer:** Transient table.

## 13. Which table type disappears after session end?
**Answer:** Temporary table.

## 14. What does zero-copy clone optimize first?
**Answer:** Speed and storage efficiency at creation time.

## 15. What happens to storage after clone and source diverge with updates?
**Answer:** Additional storage is used for changed micro-partitions.

## 16. Which statement best describes micro-partitions?
**Answer:** Automatically created immutable storage units with metadata.

## 17. What is the main performance advantage of clustering keys?
**Answer:** Better pruning for selective filters.

## 18. Should every table have a clustering key?
**Answer:** No, only when query patterns justify it.

## 19. Which operation is typically serverless: task with serverless compute or user warehouse query?
**Answer:** Serverless task execution.

## 20. Which object captures CDC-style offsets in Snowflake tables?
**Answer:** Stream.

## 21. What type of stream tracks inserted/deleted rows on standard tables?
**Answer:** Standard stream.

## 22. What object triggers stream consumption on a schedule?
**Answer:** Task.

## 23. Best ELT pattern for incremental nightly upsert?
**Answer:** Stream feeding MERGE inside scheduled task.

## 24. Which command is best for idempotent upsert logic?
**Answer:** MERGE.

## 25. Which command copies staged files into Snowflake tables?
**Answer:** COPY INTO table.

## 26. Which object stores reusable CSV delimiter and header options?
**Answer:** FILE FORMAT object.

## 27. Which stage type is managed by customer cloud account?
**Answer:** External stage.

## 28. Which stage type supports PUT command from local machine?
**Answer:** Internal stage.

## 29. A JSON file has nested arrays. Which function helps explode array elements?
**Answer:** FLATTEN.

## 30. Which function turns JSON string into queryable VARIANT?
**Answer:** PARSE_JSON.

## 31. Which SQL notation extracts JSON field value from VARIANT?
**Answer:** Dot or bracket path notation.

## 32. What does secure data sharing avoid?
**Answer:** ETL duplication and data copy.

## 33. Which object lists data objects available to consumers?
**Answer:** Share.

## 34. Can a consumer modify provider objects through secure sharing?
**Answer:** No, shared data is read-only to consumer.

## 35. What enables sharing with non-Snowflake customers?
**Answer:** Reader account.

## 36. What does RBAC grant to users indirectly?
**Answer:** Privileges through roles.

## 37. Which role should be tightly controlled and rarely used?
**Answer:** ACCOUNTADMIN.

## 38. Which role generally owns created objects in many deployments?
**Answer:** SYSADMIN or delegated functional owner role.

## 39. To query a table, what minimum hierarchy privileges are needed?
**Answer:** USAGE on database/schema and SELECT on table.

## 40. What risk comes from granting broad privileges to PUBLIC?
**Answer:** Unintended account-wide access exposure.

## 41. Which policy type masks SSN values except for authorized roles?
**Answer:** Masking policy.

## 42. Which policy type enforces country-based row restrictions?
**Answer:** Row access policy.

## 43. What is the purpose of object tags in governance programs?
**Answer:** Classification, discovery, and policy binding.

## 44. Which security control restricts login requests by source IP?
**Answer:** Network policy.

## 45. Is MFA an authorization or authentication control?
**Answer:** Authentication control.

## 46. What does SSO simplify for enterprise users?
**Answer:** Centralized identity access and login experience.

## 47. Which auth method often supports automated services without passwords?
**Answer:** Key pair authentication.

## 48. What is the unit measured by resource monitors?
**Answer:** Credit consumption.

## 49. Can a resource monitor issue alerts before hard suspension?
**Answer:** Yes, at configured thresholds.

## 50. What is the practical value of warehouse-level resource monitors?
**Answer:** Spend control and budget enforcement.

## 51. Which view family is preferred for account-wide historical billing analysis?
**Answer:** ACCOUNT_USAGE.

## 52. Which view helps identify expensive SQL statements?
**Answer:** QUERY_HISTORY.

## 53. Which diagnostic artifact shows query operator tree and scan volume?
**Answer:** Query Profile.

## 54. Which optimization can make repeated identical SELECT appear instant?
**Answer:** Result cache.

## 55. What invalidates result reuse most directly?
**Answer:** Underlying data or query text/context changes.

## 56. Is warehouse cache shared across different warehouses?
**Answer:** No.

## 57. Does resizing a warehouse lose stored table data?
**Answer:** No.

## 58. What is the first action when queueing is high but CPU per query is low?
**Answer:** Improve concurrency via multi-cluster or separate warehouses.

## 59. What is the first action when single query runtime is high?
**Answer:** Increase warehouse size or optimize SQL/pruning.

## 60. Which statement sets current role for the session?
**Answer:** USE ROLE.

## 61. Which statement sets current schema for object resolution?
**Answer:** USE SCHEMA.

## 62. Which statement sets current database?
**Answer:** USE DATABASE.

## 63. Which statement can restore dropped schema inside retention period?
**Answer:** UNDROP SCHEMA.

## 64. Which command removes table rows quickly without row-by-row predicate?
**Answer:** TRUNCATE TABLE.

## 65. Which operation supports conditional update and delete clauses together?
**Answer:** MERGE.

## 66. Which object secures hidden logic for data consumers?
**Answer:** Secure view.

## 67. Which object stores precomputed query results maintained by Snowflake?
**Answer:** Materialized view.

## 68. What is the tradeoff of materialized views?
**Answer:** Faster reads but maintenance cost.

## 69. Which object generates unique numbers for surrogate keys?
**Answer:** Sequence.

## 70. In COPY, what does PURGE option do when enabled?
**Answer:** Removes loaded files from internal stage.

## 71. In COPY, why use pattern filters?
**Answer:** Load only matching staged files.

## 72. What is a common reason for load errors with CSV files?
**Answer:** File format mismatch.

## 73. Which feature helps inspect rejected records after load attempt?
**Answer:** COPY validation/error output.

## 74. What is a best practice before production bulk load?
**Answer:** Validate with sample files and file format.

## 75. What does data retention parameter control?
**Answer:** Time Travel window length.

## 76. For strict compliance, which is preferred: broad direct user grants or role hierarchy?
**Answer:** Role hierarchy with centralized grants.

## 77. Which role inheritance direction is correct?
**Answer:** Child role granted to parent role.

## 78. What does future grant help with?
**Answer:** Automatically granting privileges on new objects.

## 79. Why separate dev and prod Snowflake roles?
**Answer:** Reduce accidental production impact.

## 80. Why separate compute warehouses by department?
**Answer:** Cost attribution and performance isolation.

## 81. Which Snowflake feature supports governed external data products?
**Answer:** Listings/Marketplace sharing.

## 82. Which function returns current active user?
**Answer:** CURRENT_USER().

## 83. Which function returns active region/account context details?
**Answer:** CURRENT_ACCOUNT() and related context functions.

## 84. If warehouse auto-suspend is 10 minutes, when is billing stopped?
**Answer:** After it suspends at inactivity threshold.

## 85. Can Snowpipe load files without keeping a warehouse running?
**Answer:** Yes, it uses serverless compute.

## 86. Which statement about storage scaling is accurate?
**Answer:** Storage scales independently of warehouse size.

## 87. Which statement about compute scaling is accurate?
**Answer:** Compute can be resized without data redistribution by users.

## 88. What does ACCOUNT_USAGE latency imply?
**Answer:** Some views are near-real-time, others delayed.

## 89. Which type of stage can reference S3 bucket path?
**Answer:** External stage.

## 90. What does ownership privilege include beyond usage?
**Answer:** Full control, including grant management.

## 91. Which command changes object owner?
**Answer:** GRANT OWNERSHIP.

## 92. Why is using a dedicated loader role recommended?
**Answer:** Limits privileges and improves auditability.

## 93. What is the purpose of access history-style auditing?
**Answer:** Track who accessed which data objects.

## 94. Which feature allows secure collaboration without exporting raw data?
**Answer:** Data sharing and clean room patterns.

## 95. What is a key benefit of Snowflake for mixed workloads?
**Answer:** Elastic compute isolation on shared storage.

## 96. If a warehouse is resized from M to L, what changes immediately?
**Answer:** Available compute resources.

## 97. What does auto-resume improve for end users?
**Answer:** Reduced manual operations and faster first query.

## 98. Which object type cannot be shared directly: warehouse or database objects?
**Answer:** Warehouse cannot be shared.

## 99. What should be monitored to tune concurrency settings?
**Answer:** Queueing metrics and warehouse load history.

## 100. Core Snowflake value proposition in one line?
**Answer:** Decoupled storage and compute with governed data platform capabilities.