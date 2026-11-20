# WORK PACKAGE J2: COMPREHENSIVE FOREIGN-KEY VALIDATION & REFERENTIAL INTEGRITY REPORT

> **MANDATORY DATA AUTHENTICITY NOTICE**  
> *VELOOP is a real product under development, but all data evaluated, profiled, and modeled for this assignment is fictional/simulated for analytical testing. In accordance with the Data Authenticity Policy, no metric or finding herein represents actual VELOOP production statistics, actual earnings, actual withdrawals, or live business performance.*

---

## 1. Executive Summary & Verification Protocol
This report provides the formal empirical validation of all **nine foreign-key relationships** connecting the relational entities of the VELOOP Rewards analytical data model, in direct fulfillment of **Task 01 — Work Package J2 (Test Relationships)**.

To establish absolute data trustworthiness, every foreign-key path was subjected to an automated set-theoretic referential integrity query:
$$\text{Orphans} = \{ c \in \text{ChildTable.ForeignKey} \mid c \notin \text{ParentTable.PrimaryKey} \land c \neq \text{NULL} \}$$

- **Automated Validation Script**: `scripts/profile_simulated_data.py`
- **Output Audit Table**: `data/referential_integrity_test_results.csv`
- **Total Operational Records Tested**: **30,150 Records** across 8 datasets
- **Total Validated FK Relationships**: **9 Core Relational Paths** + **1 Corrupted Negative Control**

---

## 2. Master Foreign-Key Validation Summary Table

```
+--------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                   EMPIRICAL FOREIGN-KEY VALIDATION TEST RESULTS                                                        |
+---------+--------------------------------------------------------------------+---------------+---------------+---------------+-------------------------+
| PATH ID | RELATIONAL PATH (CHILD -> PARENT)                                  | TESTED ROWS   | ORPHAN ROWS   | UNIQUE ORPHANS| ACTUAL TEST VERDICT     |
+---------+--------------------------------------------------------------------+---------------+---------------+---------------+-------------------------+
| FK-01   | Task_Activity.user_id -> Users.user_id                             | 6,000         | 0             | 0             | PASSED (100% Integrity) |
| FK-02   | Rewards.user_id -> Users.user_id                                   | 5,000         | 0             | 0             | PASSED (100% Integrity) |
| FK-03   | Rewards.task_activity_id -> Task_Activity.task_activity_id          | 2,957         | 0             | 0             | PASSED (100% Integrity) |
| FK-04   | Wallet.user_id -> Users.user_id                                    | 3,500         | 0             | 0             | PASSED (100% Integrity) |
| FK-05   | Wallet.reference_id (reward credits) -> Rewards.reward_id          | 2,280         | 0             | 0             | PASSED (100% Integrity) |
| FK-06   | Withdrawals.user_id -> Users.user_id                               | 1,200         | 0             | 0             | PASSED (100% Integrity) |
| FK-07   | Referrals.referring_user_id -> Users.user_id                       | 900           | 0             | 0             | PASSED (100% Integrity) |
| FK-08   | Referrals.referred_user_id -> Users.user_id                        | 760           | 0             | 0             | PASSED (100% Integrity) |
| FK-09   | Feature_Events.user_id -> Users.user_id                            | 12,000        | 0             | 0             | PASSED (100% Integrity) |
+---------+--------------------------------------------------------------------+---------------+---------------+---------------+-------------------------+
| CONTROL | Messy_Data.user_id -> Users.user_id (Corrupted Audit Sheet)        | 525           | 45            | 10            | DETECTED 45 ORPHANS     |
+---------+--------------------------------------------------------------------+---------------+---------------+---------------+-------------------------+
| TOTAL   | Clean Operational Relational Core (9 Paths)                        | 34,597 checks | 0 Orphans     | 0 Unique      | 100% RELATIONAL INTEGRITY|
+---------+--------------------------------------------------------------------+---------------+---------------+---------------+-------------------------+
```

---

## 3. Deep-Dive Forensic Evaluation of Each Foreign-Key Path

### Path FK-01: `Task_Activity.user_id` $\rightarrow$ `Users.user_id`
- **Relationship Type**: Many-to-One ($N:1$).
- **Business Rule**: Every task execution attempt must be mapped to a registered user account.
- **Verification Query (SQL)**:
  ```sql
  SELECT t.user_id 
  FROM Task_Activity t 
  LEFT JOIN Users u ON t.user_id = u.user_id 
  WHERE u.user_id IS NULL;
  ```
- **Empirical Test Result**:
  - Total records tested: **6,000**
  - Matched parent records: **6,000** (100%)
  - Orphan records detected: **0**
  - **Verdict**: **PASSED**. Zero orphan task executions.

---

### Path FK-02: `Rewards.user_id` $\rightarrow$ `Users.user_id`
- **Relationship Type**: Many-to-One ($N:1$).
- **Business Rule**: No reward point liability may be created without a verified beneficiary account.
- **Verification Query (SQL)**:
  ```sql
  SELECT r.reward_id, r.user_id 
  FROM Rewards r 
  LEFT JOIN Users u ON r.user_id = u.user_id 
  WHERE u.user_id IS NULL;
  ```
- **Empirical Test Result**:
  - Total records tested: **5,000**
  - Matched parent records: **5,000** (100%)
  - Orphan records detected: **0**
  - **Verdict**: **PASSED**. Every issued reward is bound to a valid user.

---

### Path FK-03: `Rewards.task_activity_id` $\rightarrow$ `Task_Activity.task_activity_id`
- **Relationship Type**: Conditional One-to-One ($1:1$).
- **Business Rule**: Task-based rewards must strictly reference their originating task execution attempt. Non-task rewards (daily streak bonuses, spin wheels) carry a valid `NULL` foreign key.
- **Verification Query (SQL)**:
  ```sql
  SELECT r.reward_id, r.task_activity_id 
  FROM Rewards r 
  LEFT JOIN Task_Activity t ON r.task_activity_id = t.task_activity_id 
  WHERE r.task_activity_id IS NOT NULL 
    AND r.task_activity_id <> '' 
    AND t.task_activity_id IS NULL;
  ```
- **Empirical Test Result**:
  - Total non-null task foreign keys tested: **2,957**
  - Null non-task reward records: **2,043** (Daily check-ins, spin wheel, badges)
  - Orphan records detected: **0**
  - **Verdict**: **PASSED**. 100% of task-derived rewards trace back to an authentic task execution.

---

### Path FK-04: `Wallet.user_id` $\rightarrow$ `Users.user_id`
- **Relationship Type**: Many-to-One ($N:1$).
- **Business Rule**: Every double-entry ledger movement must impact an existing user wallet.
- **Verification Query (SQL)**:
  ```sql
  SELECT w.transaction_id, w.user_id 
  FROM Wallet w 
  LEFT JOIN Users u ON w.user_id = u.user_id 
  WHERE u.user_id IS NULL;
  ```
- **Empirical Test Result**:
  - Total records tested: **3,500**
  - Matched parent records: **3,500** (100%)
  - Orphan records detected: **0**
  - **Verdict**: **PASSED**. Ledger user accounts are 100% referentially sound.

---

### Path FK-05: `Wallet.reference_id` (Reward Credits) $\rightarrow$ `Rewards.reward_id`
- **Relationship Type**: Many-to-One ($N:1$).
- **Business Rule**: Every wallet entry of type `reward_credit` must cite the originating `reward_id` in its `reference_id` column.
- **Verification Query (SQL)**:
  ```sql
  SELECT w.transaction_id, w.reference_id 
  FROM Wallet w 
  LEFT JOIN Rewards r ON w.reference_id = r.reward_id 
  WHERE w.transaction_type = 'reward_credit' 
    AND r.reward_id IS NULL;
  ```
- **Empirical Test Result**:
  - Total reward credit transactions tested: **2,280**
  - Matched parent reward records: **2,280** (100%)
  - Orphan records detected: **0**
  - **Verdict**: **PASSED**. Full financial auditability from wallet credit back to reward issuance.

---

### Path FK-06: `Withdrawals.user_id` $\rightarrow$ `Users.user_id`
- **Relationship Type**: Many-to-One ($N:1$).
- **Business Rule**: Withdrawal cash-out requests can only be initiated by registered user profiles.
- **Verification Query (SQL)**:
  ```sql
  SELECT wdr.withdrawal_id, wdr.user_id 
  FROM Withdrawals wdr 
  LEFT JOIN Users u ON wdr.user_id = u.user_id 
  WHERE u.user_id IS NULL;
  ```
- **Empirical Test Result**:
  - Total records tested: **1,200**
  - Matched parent records: **1,200** (100%)
  - Orphan records detected: **0**
  - **Verdict**: **PASSED**. Payout pipeline is completely free of orphan requests.

---

### Path FK-07: `Referrals.referring_user_id` $\rightarrow$ `Users.user_id`
- **Relationship Type**: Many-to-One ($N:1$).
- **Business Rule**: Referral links must originate from an existing platform user.
- **Verification Query (SQL)**:
  ```sql
  SELECT ref.referral_id, ref.referring_user_id 
  FROM Referrals ref 
  LEFT JOIN Users u ON ref.referring_user_id = u.user_id 
  WHERE u.user_id IS NULL;
  ```
- **Empirical Test Result**:
  - Total records tested: **900**
  - Matched parent records: **900** (100%)
  - Orphan records detected: **0**
  - **Verdict**: **PASSED**. All referral campaigns originate from valid advocates.

---

### Path FK-08: `Referrals.referred_user_id` $\rightarrow$ `Users.user_id`
- **Relationship Type**: Many-to-One ($N:1$, Nullable).
- **Business Rule**: When an invite link converts to a registration, the `referred_user_id` must point to a real account row. Un-clicked links maintain a valid `NULL`.
- **Verification Query (SQL)**:
  ```sql
  SELECT ref.referral_id, ref.referred_user_id 
  FROM Referrals ref 
  LEFT JOIN Users u ON ref.referred_user_id = u.user_id 
  WHERE ref.referred_user_id IS NOT NULL 
    AND ref.referred_user_id <> '' 
    AND u.user_id IS NULL;
  ```
- **Empirical Test Result**:
  - Total registered referee foreign keys tested: **760**
  - Un-clicked/unregistered invite links: **140** (Valid Nulls)
  - Orphan records detected: **0**
  - **Verdict**: **PASSED**. 100% of registered referees map to actual accounts.

---

### Path FK-09: `Feature_Events.user_id` $\rightarrow$ `Users.user_id`
- **Relationship Type**: Many-to-One ($N:1$).
- **Business Rule**: All feature telemetry must attribute to a registered user identity.
- **Verification Query (SQL)**:
  ```sql
  SELECT e.event_id, e.user_id 
  FROM Feature_Events e 
  LEFT JOIN Users u ON e.user_id = u.user_id 
  WHERE u.user_id IS NULL;
  ```
- **Empirical Test Result**:
  - Total records tested: **12,000**
  - Matched parent records: **12,000** (100%)
  - Orphan records detected: **0**
  - **Verdict**: **PASSED**. Telemetry stream exhibits perfect referential integrity.

---

### Negative Control: `Messy_Data.user_id` $\rightarrow$ `Users.user_id`
- **Test Objective**: Prove the sensitivity of the validation test script on corrupted data.
- **Empirical Test Result**:
  - Total non-null records tested: **525**
  - Matched parent records: **480**
  - **Orphan records detected**: **45 records** (80 references across 10 unique non-existent keys: `USR_99901` through `USR_99909` and `USR_99900`).
  - **Verdict**: **FAILED / ANOMALY DETECTED**. Confirms that unvalidated raw inputs suffer orphan corruption and proves that our automated detection engine successfully catches foreign key defects.

---
*Deliverable Document Reference: `docs/FOREIGN_KEY_VALIDATION_REPORT.md` | Data File: `data/referential_integrity_test_results.csv`.*
