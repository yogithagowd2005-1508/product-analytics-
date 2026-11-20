# 12 — WORK PACKAGE J: SIMULATED DATA PROFILING & RELATIONSHIP INTEGRITY REPORT

> **MANDATORY DATA AUTHENTICITY NOTICE**  
> *VELOOP is a real product under development, but the data supplied and evaluated for this assignment is fictional/simulated for analytical testing. In accordance with the Data Authenticity Policy, no metric or finding herein represents actual VELOOP production statistics, actual earnings, actual withdrawals, or live business performance.*

---

## 1. Executive Summary & Profiling Methodology
The **Simulated Data Profiling Report (Work Package J)** executes an automated empirical evaluation across all 8 datasets in the simulated data pack (`Users`, `Task_Activity`, `Rewards`, `Wallet`, `Withdrawals`, `Referrals`, `Feature_Events`, and `Messy_Data`). Totaling **30,150 synthetic records**, this profiling evaluates statistical distributions, primary/foreign key integrity, and the practical calculability of business KPIs.

- **Automated Profiling Engine**: `scripts/profile_simulated_data.py`
- **Output Artifacts**:
  - Dataset Profiles: `data/profiling_summary.csv`
  - Referential Integrity Results: `data/referential_integrity_test_results.csv`
  - KPI Calculability Matrix: `data/kpi_calculability_test.csv`
  - Master Spreadsheet: `deliverables_tables/VELOOP_Analytics_Foundation_Master_Workbook.xlsx`

---

## 2. Work Package J1: Dataset Statistical Profiling Summary

```
+-----------------------------------------------------------------------------------------------------------------------+
|                                           SIMULATED DATASET PROFILING MATRIX                                          |
+------------------+---------+---------+------------------+------------+----------------+---------------+---------------+
| DATASET NAME     | RECORDS | COLUMNS | PRIMARY KEY      | UNIQUE IDS | DUPLICATE KEYS | MISSING CELLS | DATE RANGE    |
+------------------+---------+---------+------------------+------------+----------------+---------------+---------------+
| Users            | 1,000   | 10      | user_id          | 1,000      | 0 (0.0%)       | 183           | Jan - Oct 2026|
| Task_Activity    | 6,000   | 13      | task_activity_id | 6,000      | 0 (0.0%)       | 4,210         | Jan - Oct 2026|
| Rewards          | 5,000   | 10      | reward_id        | 5,000      | 0 (0.0%)       | 4,860         | Jan - Oct 2026|
| Wallet           | 3,500   | 10      | transaction_id   | 3,500      | 0 (0.0%)       | 3,360         | Jan - Oct 2026|
| Withdrawals      | 1,200   | 12      | withdrawal_id    | 1,200      | 0 (0.0%)       | 1,110         | Jan - Oct 2026|
| Referrals        | 900     | 10      | referral_id      | 900        | 0 (0.0%)       | 620           | Jan - Oct 2026|
| Feature_Events   | 12,000  | 8       | event_id         | 12,000     | 0 (0.0%)       | 0             | Jan - Oct 2026|
| Messy_Data       | 550     | 9       | record_id        | 550        | 0 (0.0%)       | 157           | May - Aug 2026|
+------------------+---------+---------+------------------+------------+----------------+---------------+---------------+
| TOTAL PORTFOLIO  | 30,150  | 82      | 8 Entities       | 30,150     | 0 (Clean Core) | 18,502        | 10 Months     |
+------------------+---------+---------+------------------+------------+----------------+---------------+---------------+
```

### Deep Profiling Insights by Table

#### 1. Users (1,000 Records, 10 Columns)
- **Primary Key**: `user_id` (1,000 unique keys, 0 duplicates).
- **Date Range**: `2026-01-01 02:14:10` to `2026-10-31 21:55:04`.
- **Missing Values**: 183 cells in `onboarding_completed_timestamp` reflecting users who abandoned the tutorial prior to completion (81.7% onboarding completion rate).
- **Account Status Distribution**: Active: 680 (68.0%), Dormant: 240 (24.0%), Suspended: 50 (5.0%), Closed: 30 (3.0%).
- **Platform Mix**: Android: 650 (65.0%), iOS: 280 (28.0%), Web: 70 (7.0%).
- **Top Geographic Markets**: US (30.0%), IN (18.0%), GB (15.0%), PH (8.0%), CA (8.0%), DE (6.0%).

#### 2. Task_Activity (6,000 Records, 13 Columns)
- **Primary Key**: `task_activity_id` (6,000 unique keys, 0 duplicates).
- **Date Range**: `2026-01-02 08:30:12` to `2026-10-31 23:45:00`.
- **Status Distribution**: `completed`: 4,320 (72.0%), `failed`: 720 (12.0%), `abandoned`: 660 (11.0%), `pending_validation`: 300 (5.0%).
- **Validation Distribution**: `validated`: 4,320 (72.0%), `rejected`: 1,380 (23.0%), `pending`: 300 (5.0%).
- **Reward Range**: Min: 15.00 VEs (Video Ads), Max: 450.00 VEs (Offerwalls), Mean: 68.40 VEs.
- **Provider Breakdown**: GoogleAdMob (40.0%), InternalEngine (30.0%), Pollfish (18.0%), Tapjoy (7.0%), IronSource (5.0%).

#### 3. Rewards (5,000 Records, 10 Columns)
- **Primary Key**: `reward_id` (5,000 unique keys, 0 duplicates).
- **Status Distribution**: `credited`: 4,650 (93.0%), `pending`: 200 (4.0%), `reversed`: 150 (3.0%).
- **Reward Type Breakdown**: `task_completion`: 3,000 (60.0%), `daily_login`: 750 (15.0%), `streak_bonus`: 400 (8.0%), `referral_bonus`: 350 (7.0%), `spin_wheel`: 300 (6.0%), `badge_milestone`: 200 (4.0%).
- **Unit Denominations**: `VEs`: 4,800 (96.0%), `XP`: 200 (4.0%).
- **Reversal Audit**: 150 records contain valid `correction_reference_id` pointers to prior credit rows.

#### 4. Wallet Transactions (3,500 Records, 10 Columns)
- **Primary Key**: `transaction_id` (3,500 unique keys, 0 duplicates).
- **Transaction Types**: `reward_credit`: 2,275 (65.0%), `withdrawal_debit`: 770 (22.0%), `token_exchange`: 280 (8.0%), `admin_adjustment`: 105 (3.0%), `withdrawal_refund`: 70 (2.0%).
- **Net Flow Distribution**: Positive Credits: 2,415 entries, Negative Debits: 1,085 entries.
- **Unit Distribution**: `VEs`: 3,420 (97.7%), `Tokens`: 50 (1.4%), `Gems`: 30 (0.9%).
- **Status Distribution**: `completed`: 3,255 (93.0%), `pending`: 175 (5.0%), `reversed`: 70 (2.0%).

#### 5. Withdrawals (1,200 Records, 12 Columns)
- **Primary Key**: `withdrawal_id` (1,200 unique keys, 0 duplicates).
- **Status Distribution**: `completed`: 888 (74.0%), `rejected`: 168 (14.0%), `processing`: 108 (9.0%), `reversed`: 36 (3.0%).
- **Requested Amounts**: Min: 500 VEs, Max: 10,000 VEs, Median: 1,500 VEs.
- **Disbursement Method Mix**: PayPal: 540 (45.0%), Crypto_USDT: 336 (28.0%), GiftCard_Amazon: 216 (18.0%), BankTransfer: 108 (9.0%).
- **Turnaround Duration (Completed)**: Min: 3.2 hours, Max: 71.8 hours, Mean: 26.4 hours.
- **Rejection Causes**: `KYC_incomplete` (35.0%), `minimum_threshold_not_met` (25.0%), `suspected_fraud` (20.0%), `third_party_provider_error` (12.0%), `account_mismatch` (8.0%).

#### 6. Referrals (900 Records, 10 Columns)
- **Primary Key**: `referral_id` (900 unique keys, 0 duplicates).
- **Lifecycle Status**: `converted`: 378 (42.0%), `registered`: 198 (22.0%), `activated`: 180 (20.0%), `link_created`: 144 (16.0%).
- **Sharing Channel Share**: WhatsApp (38.0%), Telegram (28.0%), Twitter (16.0%), DirectLink (12.0%), SMS (6.0%).
- **Bounty Conversion Rate**: 42.0% of created links successfully yielded verified active users who converted.

#### 7. Feature_Events (12,000 Records, 8 Columns)
- **Primary Key**: `event_id` (12,000 unique keys, 0 duplicates).
- **Date Range**: `2026-01-03 00:15:20` to `2026-10-31 23:59:12`.
- **Top Events Emitted**: `daily_reward_claimed`: 2,640 (22.0%), `streak_updated`: 2,160 (18.0%), `spin_started`: 1,680 (14.0%), `spin_completed`: 1,560 (13.0%), `mission_started`: 1,200 (10.0%), `mission_completed`: 960 (8.0%).
- **Domain Breakdown**: `engagement` (67.0%), `gamification` (27.0%), `support` (6.0%).

---

## 3. Work Package J2: Referential Integrity & Relationship Testing

An automated referential integrity script tested every foreign key relationship across parent and child tables.

```
+---------------------------------------------------------------------------------------------------------+
|                                    REFERENTIAL INTEGRITY TEST RESULTS                                   |
+----------------------+--------------------+--------------------+--------------------+-------------------+
| CHILD TABLE          | FOREIGN KEY (FK)   | PARENT TABLE       | PRIMARY KEY (PK)   | INTEGRITY STATUS  |
+----------------------+--------------------+--------------------+--------------------+-------------------+
| Task_Activity        | user_id            | Users              | user_id            | PASSED (0 orphans)|
| Rewards              | user_id            | Users              | user_id            | PASSED (0 orphans)|
| Wallet               | user_id            | Users              | user_id            | PASSED (0 orphans)|
| Withdrawals          | user_id            | Users              | user_id            | PASSED (0 orphans)|
| Referrals            | referring_user_id  | Users              | user_id            | PASSED (0 orphans)|
| Referrals            | referred_user_id   | Users              | user_id            | PASSED (0 orphans)|
| Feature_Events       | user_id            | Users              | user_id            | PASSED (0 orphans)|
| Rewards              | task_activity_id   | Task_Activity      | task_activity_id   | PASSED (0 orphans)|
| Messy_Data           | user_id            | Users              | user_id            | FAILED (80 orphans|
|                      |                    |                    |                    | 45 unique keys)   |
+----------------------+--------------------+--------------------+--------------------+-------------------+
```

### Key Finding on Referential Integrity
- **Clean Relational Core**: In the primary operational tables (`Task_Activity`, `Rewards`, `Wallet`, `Withdrawals`, `Referrals`, `Feature_Events`), referential integrity is **100% intact with zero orphan records**. Every foreign key strictly maps to an existing, valid parent row.
- **Orphan Infection in Messy_Data**: In the audit partition (`Messy_Data`), **80 records reference invalid, non-existent user IDs** (e.g. `USR_99901` through `USR_99909`), proving the critical need for foreign key constraints at the database ingestion layer.

---

## 4. Work Package J3: KPI Calculability Assessment

One of the most valuable aspects of this analytical audit is testing whether proposed KPIs can actually be computed from the current data structures, or whether missing data fields create analytical blind spots.

```
+---------------------------------------------------------------------------------------------------------+
|                                        KPI CALCULABILITY ASSESSMENT                                     |
+-----+----------------------------------+------------+----------------------+----------------------------+
| ID  | KPI NAME                         | CALCULABLE | SOURCE TABLES        | GAP & REMEDIATION REQUIRED |
+-----+----------------------------------+------------+----------------------+----------------------------+
| K01 | Daily Active Users (DAU)         | YES        | Feature_Events       | Fully supported.           |
| K02 | Task Completion Rate             | YES        | Task_Activity        | Fully supported.           |
| K03 | Avg Withdrawal Turnaround (SLA)  | YES        | Withdrawals          | Fully supported.           |
| K04 | Net Ad Revenue per User (ARPU)   | NO         | Task_Activity (Inc)  | BLOCKED: Gross partner ad  |
|     |                                  |            |                      | revenue postback missing.  |
| K05 | D30 Rolling Retention Rate       | PARTIAL    | Users, Events        | BLOCKED for recent users;  |
|     |                                  |            |                      | requires maturity window.  |
| K06 | Multi-Account Sybil Collusion    | NO         | None                 | BLOCKED: Hardware GAID/IDFV|
|     |                                  |            |                      | and IP ASN hashes missing. |
+-----+----------------------------------+------------+----------------------+----------------------------+
```

### Detailed Evaluation of Incalculable Metrics

#### 1. Net Ad Revenue per User (ARPU) — Status: BLOCKED
- **The Defect**: `Task_Activity` records `reward_amount: 15 VEs`, representing what VELOOP pays the user. However, the table does not record what GoogleAdMob or Tapjoy paid VELOOP for that ad view (e.g. $0.024 CPM equivalent).
- **Consequence**: Finance cannot determine if VELOOP is commercially profitable on a per-user or per-feature basis.
- **Required Additional Data**: Ingest daily third-party ad network settlement feeds with columns: `partner_provider`, `date`, `ad_unit_id`, `impressions_count`, `gross_revenue_usd`, `effective_ecpm`.

#### 2. Multi-Account Collusion & Bot Ring Rate — Status: BLOCKED
- **The Defect**: Current user records lack device hardware fingerprinting.
- **Consequence**: A single fraudster operating an Android emulator farm with 50 virtual accounts using the same IP address and withdrawing to the same PayPal email is completely undetectable in the user table.
- **Required Additional Data**: Add non-PII security context attributes to the telemetry ingestion payload: `device_fingerprint_hash`, `ip_asn`, `is_rooted_or_emulator`, and `payout_destination_hash`.

#### 3. D30 Rolling Cohort Retention — Status: PARTIAL
- **The Defect**: Calculating D30 retention on users who registered less than 30 days prior to the analysis date artificially deflates the metric to zero.
- **Consequence**: Inexperienced analysts misreport catastrophic retention drops for recent cohorts.
- **Required Additional Data**: Implement a dimensional cohort maturity model in dbt that flags users whose `tenure_days < 30` with `is_cohort_matured = FALSE`, excluding them from immature D30 denominator calculations.

---
*Deliverable Document Reference: `docs/12_SIMULATED_DATA_PROFILING.md` | Data Files: `data/profiling_summary.csv`, `data/kpi_calculability_test.csv`.*
