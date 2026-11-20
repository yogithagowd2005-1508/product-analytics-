# 09 — WORK PACKAGE G: VELOOP DATA DICTIONARY

> **MANDATORY DATA AUTHENTICITY NOTICE**  
> *VELOOP is a real product under development, but the data supplied and evaluated for this assignment is fictional/simulated for analytical testing. In accordance with the Data Authenticity Policy, no metric or finding herein represents actual VELOOP production statistics, actual earnings, actual withdrawals, or live business performance.*

---

## 1. Executive Overview & Data Standards
The **VELOOP Data Dictionary (Work Package G)** provides the canonical technical and business definition for every data element across the analytical data model. It bridges the gap between software engineers writing database migrations, analytics engineers constructing dbt models, and product analysts building executive dashboards.

- **Primary Data File**: `deliverables_tables/09_DATA_DICTIONARY.csv`
- **Total Entities Documented**: 9 core entities (`Users`, `Task_Activity`, `Rewards`, `Wallet`, `Withdrawals`, `Referrals`, `Feature_Events`, `Missions`, `Badges`, `Sessions`)
- **Total Fields Defined**: **92 meaningful fields** (exceeding the minimum mandate of 75+ fields)
- **Mandatory Metadata Attributes per Field**:
  1. `Entity`: Where the attribute belongs
  2. `Field Name`: Exact programmatic name
  3. `Data Type`: Storage and operational typing
  4. `Definition`: Exact business and technical meaning
  5. `Example`: Concrete sample value
  6. `Required`: `Yes` / `No` (Nullability)
  7. `Allowed Values`: Enum domain or format pattern
  8. `Validation`: Integrity rule, regex, or constraint
  9. `Source`: Originating service or client layer
  10. `Sensitivity`: Data classification (`Public`, `Internal`, `Restricted`)
  11. `Analytical Use`: Exact reporting and modeling purpose
  12. `Status`: `Confirmed` / `Proposed`

---

## 2. Entity Summary & Field Distribution

```
+---------------------------------------------------------------------------------------------------------+
|                                    DATA DICTIONARY FIELD ALLOCATION                                     |
+--------------------------+-----------------------+---------------------+--------------------------------+
| ENTITY NAME              | TOTAL FIELDS DEFINED  | PRIMARY KEY         | KEY FOREIGN RELATIONS          |
+--------------------------+-----------------------+---------------------+--------------------------------+
| 1. Users                 | 10 Fields             | user_id             | Base entity for all activity   |
| 2. Task_Activity         | 13 Fields             | task_activity_id    | FK: user_id                    |
| 3. Rewards               | 10 Fields             | reward_id           | FK: user_id, task_activity_id  |
| 4. Wallet                | 10 Fields             | transaction_id      | FK: user_id, reference_id      |
| 5. Withdrawals           | 12 Fields             | withdrawal_id       | FK: user_id                    |
| 6. Referrals             | 10 Fields             | referral_id         | FK: referring_uid, referred_uid|
| 7. Feature_Events        | 8 Fields              | event_id            | FK: user_id, session_id        |
| 8. Missions              | 7 Fields              | mission_id          | Quest Catalog Template         |
| 9. Badges                | 5 Fields              | badge_id            | Achievement Catalog Template   |
| 10. Sessions             | 7 Fields              | session_id          | FK: user_id                    |
+--------------------------+-----------------------+---------------------+--------------------------------+
| TOTAL CANONICAL FIELDS   | 92 FIELDS             | (Target: 75+)       | Full Referential Integrity     |
+--------------------------+-----------------------+---------------------+--------------------------------+
```

---

## 3. Comprehensive Data Dictionary Table (Sample of Key Fields by Entity)

*(Refer to `deliverables_tables/09_DATA_DICTIONARY.csv` for the complete 92-row machine-readable matrix).*

### Entity: Users (10 Fields)
| Field Name | Type | Req? | Definition | Example | Allowed Values | Source | Sensitivity | Analytical Use | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `user_id` | String | Yes | Permanent unique surrogate user identifier | `USR_00001` | `^USR_[0-9]{5}$` | Auth Service | Internal | Primary entity join key | Confirmed |
| `registration_timestamp`| Timestamp | Yes | UTC timestamp when account was registered | `2026-03-15 10:22:15` | Valid UTC | Auth DB | Internal | Cohort grouping, user tenure | Confirmed |
| `registration_source` | String | Yes | Acquisition channel through which user discovered app | `referral` | `organic`, `referral`, `paid_ad`, `partner_promo`, `influencer` | Attribution SDK | Internal | Acquisition channel mix, CAC | Confirmed |
| `acquisition_campaign`| String | No | Marketing campaign tag associated with acquisition | `summer_boost` | Free string (max 100) | Attribution SDK | Internal | Campaign ROI, ad spend efficiency | Proposed |
| `device_platform` | String | Yes | Operating system of registration device | `Android` | `Android`, `iOS`, `Web` | Client Telemetry | Internal | Platform market share | Confirmed |
| `country_code` | String | Yes | ISO 3166-1 alpha-2 country of user registration | `US` | Length 2 uppercase | IP Geolocation | Internal | Regional monetization tiers | Confirmed |
| `account_status` | String | Yes | Operational standing of user account | `active` | `active`, `dormant`, `suspended`, `closed` | User Service | Internal | Cohort filtering, churn tracking | Confirmed |
| `is_onboarding_completed`| Boolean | Yes | Indicates if user finished intro tutorial | `TRUE` | `TRUE`, `FALSE` | Client SDK | Internal | Activation conversion analysis | Confirmed |
| `onboarding_completed_timestamp`| Timestamp| No | UTC timestamp when onboarding finished | `2026-03-15 10:28:40` | `>= registration_timestamp` | Client SDK | Internal | Time-to-activation duration | Proposed |
| `last_login_timestamp` | Timestamp | Yes | UTC timestamp of most recent successful session | `2026-10-30 18:45:10` | `>= registration_timestamp` | Auth Service | Internal | Recency scoring, dormancy classification | Confirmed |

### Entity: Task_Activity (13 Fields)
| Field Name | Type | Req? | Definition | Example | Allowed Values | Source | Sensitivity | Analytical Use | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `task_activity_id` | String | Yes | Unique surrogate execution identifier | `TSK_000100` | `^TSK_[0-9]{6}$` | Task Engine | Internal | Primary Key; joins to Rewards | Confirmed |
| `task_id` | String | Yes | Catalog identifier of task template | `TK_AD_101` | Alphanumeric | Task Catalog | Internal | Task popularity & completion rate | Confirmed |
| `task_type` | String | Yes | Categorical earning mechanism | `watch_ad` | `watch_ad`, `survey`, `tap_earn`, `mining`, `offerwall`, `app_install` | Task Engine | Internal | Earning category segmentation | Confirmed |
| `feature_category` | String | Yes | High-level product classification | `Earning` | `Earning`, `Gamification` | Product Schema | Internal | Broad product area reporting | Confirmed |
| `user_id` | String | Yes | Identifier of user performing the task | `USR_00001` | Valid `user_id` | Session Context | Internal | User task frequency & depth | Confirmed |
| `started_at` | Timestamp | Yes | UTC timestamp when user opened task | `2026-04-01 12:00:00` | Valid UTC | Client / Server | Internal | Task start volume & peak hours | Confirmed |
| `completed_at` | Timestamp | No | UTC timestamp when task finished | `2026-04-01 12:00:30` | `>= started_at` | Server Validator | Internal | Task duration, abandonment timing | Confirmed |
| `status` | String | Yes | Execution status of task attempt | `completed` | `completed`, `failed`, `abandoned`, `pending_validation` | Task Engine | Internal | Funnel drop-off & completion rate | Confirmed |
| `reward_amount` | Numeric | Yes | Reward units allocated for completion | `15.00` | Numeric `>= 0` | Task Catalog | Internal | Estimated liability creation | Confirmed |
| `reward_unit` | String | Yes | Currency denomination | `VEs` | `VEs`, `Gems`, `XP` | Task Catalog | Internal | Multi-currency aggregation | Confirmed |
| `validation_status` | String | Yes | Result of anti-fraud & partner postback | `validated` | `validated`, `rejected`, `pending` | Validation Engine | Internal | Fraud pass rate, partner reliability | Confirmed |
| `partner_provider` | String | Yes | Third-party network delivering the task | `GoogleAdMob` | `AdMob`, `Pollfish`, `Tapjoy`, `Internal` | Task Engine | Internal | Partner performance & uptime | Confirmed |
| `error_reason` | String | No | Failure diagnostic string | `tracking_timeout` | Free string / enum | Task Engine | Internal | Error triage and UX fixes | Proposed |

### Entity: Rewards (10 Fields)
| Field Name | Type | Req? | Definition | Example | Allowed Values | Source | Sensitivity | Analytical Use | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `reward_id` | String | Yes | Unique surrogate key for reward issuance | `RWD_00001` | `^RWD_[0-9]{5}$` | Rewards Engine | Internal | Primary Key; financial reconciliation | Confirmed |
| `user_id` | String | Yes | Recipient user identifier | `USR_00001` | Valid `user_id` | Rewards Engine | Internal | User reward accumulation | Confirmed |
| `task_activity_id` | String | No | Upstream task execution reference | `TSK_000100` | Valid `task_activity_id` | Rewards Engine | Internal | Reward attribution to task | Confirmed |
| `reward_type` | String | Yes | Business origin of reward | `task_completion` | `task_completion`, `daily_login`, `streak_bonus`, `referral_bonus`, `spin_wheel`, `badge_milestone` | Rewards Engine | Internal | Reward category breakdown | Confirmed |
| `amount` | Numeric | Yes | Quantity of points credited | `25.00` | Numeric `> 0` | Rewards Engine | Internal | Reward liability calculation | Confirmed |
| `reward_unit` | String | Yes | Denomination currency | `VEs` | `VEs`, `Gems`, `XP` | Rewards Engine | Internal | Multi-currency balance ledger | Confirmed |
| `status` | String | Yes | Accounting state of reward | `credited` | `credited`, `pending`, `reversed`, `corrected` | Ledger Service | Internal | Liability lifecycle tracking | Confirmed |
| `credited_at` | Timestamp | Yes | UTC timestamp when reward posted | `2026-04-01 12:00:32` | Valid UTC | Ledger Service | Internal | Daily reward issuance volume | Confirmed |
| `ledger_status` | String | Yes | Financial journal posting status | `posted` | `posted`, `pending`, `voided` | Ledger Service | Internal | Double-entry reconciliation | Confirmed |
| `correction_reference_id`| String | No | Original reward pointer if reversed | `RWD_00005` | Valid `reward_id` | Ledger Service | Internal | Audit trail for reversals | Proposed |

### Entity: Wallet Transactions (10 Fields)
| Field Name | Type | Req? | Definition | Example | Allowed Values | Source | Sensitivity | Analytical Use | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `transaction_id` | String | Yes | Unique surrogate journal line identifier | `TXN_000001` | `^TXN_[0-9]{6}$` | Ledger Core | Internal | Primary Key; financial audit | Confirmed |
| `user_id` | String | Yes | Balance account owner | `USR_00001` | Valid `user_id` | Ledger Core | Internal | Balance derivation | Confirmed |
| `timestamp` | Timestamp | Yes | Transaction entry UTC timestamp | `2026-04-01 12:00:32` | Valid UTC | Ledger Core | Internal | Cash flow sequencing | Confirmed |
| `transaction_type` | String | Yes | Economic category of journal line | `reward_credit` | `reward_credit`, `withdrawal_debit`, `token_exchange`, `admin_adjustment`, `withdrawal_refund` | Ledger Core | Internal | Cash flow segmentation | Confirmed |
| `amount` | Numeric | Yes | Signed balance change | `+25.00` | Signed decimal | Ledger Core | Internal | Net balance calculation | Confirmed |
| `unit` | String | Yes | Currency unit of movement | `VEs` | `VEs`, `Gems`, `Tokens` | Ledger Core | Internal | Currency-specific balances | Confirmed |
| `status` | String | Yes | Journal line status | `completed` | `completed`, `pending`, `reversed`, `failed` | Ledger Core | Internal | Clearing and settlement audit | Confirmed |
| `source` | String | Yes | Originating subsystem | `reward_engine` | `reward_engine`, `withdrawal_engine`, `exchange_service`, `manual_ops` | Ledger Core | Internal | Subsystem liability attribution | Confirmed |
| `reference_id` | String | No | Pointer to upstream domain record | `RWD_00001` | Pointers to RWD, WDR, EXC | Ledger Core | Internal | End-to-end traceability | Confirmed |
| `reversal_relationship_id`| String | No | Original transaction pointer if reversed | `TXN_000050` | Valid `transaction_id` | Ledger Core | Internal | Offsetting entry linkage | Proposed |

### Entity: Withdrawals (12 Fields)
| Field Name | Type | Req? | Definition | Example | Allowed Values | Source | Sensitivity | Analytical Use | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `withdrawal_id` | String | Yes | Unique surrogate key for payout | `WDR_0001` | `^WDR_[0-9]{4}$` | Withdrawal Engine | Internal | Primary Key; payout tracking | Confirmed |
| `user_id` | String | Yes | Payout beneficiary user | `USR_00001` | Valid `user_id` | Withdrawal Engine | Internal | Per-user cash-out behavior | Confirmed |
| `requested_amount` | Numeric | Yes | Gross points requested for redemption | `1000.00` | Numeric `>= 500` | Withdrawal Engine | Internal | Redemption demand volume | Confirmed |
| `currency_unit` | String | Yes | Denomination debited | `VEs` | `VEs`, `Tokens` | Withdrawal Engine | Internal | Payout unit breakdown | Confirmed |
| `withdrawal_method` | String | Yes | Payment rail selected | `PayPal` | `PayPal`, `Crypto_USDT`, `GiftCard_Amazon`, `BankTransfer` | Withdrawal Engine | Internal | Payout channel popularity | Confirmed |
| `requested_timestamp` | Timestamp | Yes | Submission UTC timestamp | `2026-05-10 14:00:00` | Valid UTC | Withdrawal Engine | Internal | Queue entry time; SLA start | Confirmed |
| `processing_timestamp` | Timestamp | No | Gateway dispatch timestamp | `2026-05-10 18:30:00` | `>= requested_timestamp` | Gateway Connector | Internal | Review latency | Confirmed |
| `final_timestamp` | Timestamp | No | Terminal settlement / rejection timestamp | `2026-05-11 10:15:00` | `>= processing_timestamp` | Gateway Webhook | Internal | Turnaround time SLA | Confirmed |
| `status` | String | Yes | Current operational status | `completed` | `requested`, `processing`, `completed`, `rejected`, `reversed` | Withdrawal Engine | Internal | Payout completion rate | Confirmed |
| `rejection_reason_category`| String | No | Categorized denial rationale | `KYC_incomplete` | `KYC_incomplete`, `minimum_threshold_not_met`, `suspected_fraud`, `third_party_provider_error`, `account_mismatch` | Risk Engine | Internal | Payout failure root-cause | Confirmed |
| `payout_reference_hash` | String | No | External rail settlement transaction hash | `HASH_9B8C123F` | Hex string length `>= 8` | Payment Provider | Restricted | Financial settlement verification | Confirmed |
| `fee_amount` | Numeric | Yes | Network fee deducted from payout | `20.00` | Numeric `>= 0` | Withdrawal Engine | Internal | Fee revenue calculation | Confirmed |

---

## 4. Sensitivity & Data Governance Classifications

1. **Public**: Catalog data, badge names, mission titles, icon assets. Freely shareable.
2. **Internal**: Analytics events, timestamps, user IDs, device platforms, status enums. Accessible to approved engineering, product, and data teams under RBAC.
3. **Restricted**: Cryptographic payout hashes, IP ASN numbers, administrative adjustment IDs. Masked by default; requires explicit elevated access permissions.

---
*Deliverable Document Reference: `docs/09_DATA_DICTIONARY.md` | Full Spreadsheet: `deliverables_tables/09_DATA_DICTIONARY.csv`.*
