# 06 — WORK PACKAGE D: WALLET & WITHDRAWAL ANALYTICS SPECIFICATION

> **MANDATORY DATA AUTHENTICITY NOTICE**  
> *VELOOP is a real product under development, but the data supplied and evaluated for this assignment is fictional/simulated for analytical testing. In accordance with the Data Authenticity Policy, no metric or finding herein represents actual VELOOP production statistics, actual earnings, actual withdrawals, or live business performance.*

---

## 1. Executive Context & Financial Integrity Mandate
The wallet and withdrawal subsystem represents the ultimate financial interface between VELOOP and its users. The system must enforce **immutable, double-entry accounting integrity**, guaranteeing that no balance can be created without a verifiable earning source, and no cash-out can be disbursed without strict escrow reconciliation.

This specification details the **Wallet Transaction Model (D1)**, the **Multi-Stage Withdrawal Lifecycle (D2)**, and the **10 Core Withdrawal KPIs (D3)**.

---

## 2. Work Package D1: Wallet Transaction Model

The VELOOP wallet ledger records all economic movements across user balances. Every entry represents an atomic ledger movement.

```mermaid
flowchart TD
    subgraph Credit ["Credit Transactions (+)"]
        C1["reward_credit<br/>(Ad / Survey / Quest)"]
        C2["withdrawal_refund<br/>(Rejected Cash-Out)"]
        C3["admin_adjustment<br/>(Ops Balance Correction)"]
    end
    
    subgraph Debit ["Debit Transactions (-)"]
        D1["withdrawal_debit<br/>(Cash-Out Request)"]
        D2["token_exchange<br/>(VEs swapped to Tokens)"]
        D3["fee_deduction<br/>(Rail Processing Fee)"]
    end
    
    Credit --> L["Core Ledger Balance<br/>(Atomic Journal)"]
    Debit --> L
    L --> S["Wallet Balance Snapshot<br/>(CHECK running_balance >= 0)"]
```

### Transaction Schema Specification

| Field Name | Type | Allowed Values | Source System | Analytical Purpose | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `transaction_id` | String | `TXN_[0-9]{6}` | Core Ledger API | Primary Key; unique immutable journal entry | Confirmed |
| `user_id` | String | `USR_[0-9]{5}` | Auth Context | Owner of affected wallet balance | Confirmed |
| `timestamp` | Timestamp | Valid UTC ISO 8601 | Ledger Server Clock | Sequence ordering, velocity analysis | Confirmed |
| `transaction_type`| String | `reward_credit`, `withdrawal_debit`, `token_exchange`, `admin_adjustment`, `withdrawal_refund` | Ledger Core | Cash flow categorization and margin modeling | Confirmed |
| `amount` | Numeric | Signed Decimal (`+` credit, `-` debit) | Initiating Subsystem | Net balance delta calculation | Confirmed |
| `unit` | String | `VEs`, `Gems`, `Tokens` | Product Economy | Multi-currency segmentation | Confirmed |
| `status` | String | `completed`, `pending`, `reversed`, `failed` | Clearing Engine | Settlement and reconciliation tracking | Confirmed |
| `source` | String | `reward_engine`, `withdrawal_engine`, `exchange_service`, `manual_ops` | Subsystem Origin | Subsystem liability attribution | Confirmed |
| `reference_id` | String | Pointer to `reward_id`, `withdrawal_id`, or `exchange_id` | Foreign System | End-to-end operational auditability | Confirmed |
| `reversal_relationship_id`| String | `TXN_[0-9]{6}` or `NULL` | Ledger Core | Links offsetting entries to original transactions | Proposed |

---

## 3. Work Package D2: Multi-Stage Withdrawal Lifecycle

Cash redemptions must traverse a strict, auditable state machine to prevent race-condition overdrafts, block fraudulent cash drains, and isolate payment rail latency.

```mermaid
stateDiagram-v2
    [*] --> requested: User Submits Payout Form
    requested --> under_review: Compliance / AML Heuristics Triggered
    requested --> processing: Auto-Approved (Low-Risk Fast Track)
    under_review --> processing: Manual Ops Approval
    under_review --> rejected: Fraud / KYC Violation Detected
    processing --> completed: External Payout Hash Verified (HTTP 200)
    processing --> reversed: Provider Rail Failure / Chargeback
    rejected --> [*]: Funds Restored to Wallet (withdrawal_refund)
    reversed --> [*]: Funds Restored to Wallet (withdrawal_refund)
    completed --> [*]: Payout Permanently Settled
```

### Lifecycle Stage Attributes

| Field Name | Type | Format / Constraints | Analytical Significance |
| :--- | :--- | :--- | :--- |
| `withdrawal_id` | String | `WDR_[0-9]{4}` | Primary Key for payout tracking |
| `user_id` | String | `USR_[0-9]{5}` | Payout beneficiary identifier |
| `requested_amount` | Numeric | Decimal `>= 500` (min threshold) | Gross redemption demand volume |
| `currency_unit` | String | `VEs`, `Tokens` | Payout denomination |
| `withdrawal_method` | String | `PayPal`, `Crypto_USDT`, `GiftCard_Amazon`, `BankTransfer` | Payout rail channel distribution |
| `requested_timestamp`| Timestamp | Valid UTC ISO 8601 | Queue entry time; SLA clock start |
| `processing_timestamp`| Timestamp| Valid UTC ISO 8601 (`>= requested_timestamp`) | Internal review duration end; gateway dispatch |
| `final_timestamp` | Timestamp | Valid UTC ISO 8601 (`>= processing_timestamp`) | Terminal settlement or rejection time |
| `status` | String | `requested`, `processing`, `completed`, `rejected`, `reversed` | Payout pipeline health indicator |
| `rejection_reason_category`| String | `KYC_incomplete`, `minimum_threshold_not_met`, `suspected_fraud`, `third_party_provider_error`, `account_mismatch` | Payout failure root-cause analysis |
| `payout_reference_hash`| String | Hex hash string length `>= 8` | External cryptographic proof of settlement |
| `fee_amount` | Numeric | Decimal `>= 0` (e.g. 2% network fee) | Platform fee revenue calculation |

---

## 4. Work Package D3: The 10 Core Withdrawal KPIs

Each KPI adheres strictly to the required 11-point definition standard:

```
+---------------------------------------------------------------------------------------------------------+
|                                    10 WITHDRAWAL PERFORMANCE KPIS                                       |
+-----+----------------------------------+------------------+--------------------+------------------------+
| ID  | KPI Name                         | Frequency        | Target Stakeholder | Primary Value          |
+-----+----------------------------------+------------------+--------------------+------------------------+
| W01 | Withdrawal Request Volume        | Daily            | Payment Ops / CFO  | Payout pipeline demand |
| W02 | Completed Withdrawal Count       | Daily / Weekly   | VP Product / Ops   | Payout fulfillment     |
| W03 | Pending Withdrawal Queue Size    | Real-time / Daily| Operations Lead    | Backlog bottleneck     |
| W04 | Rejected Withdrawal Count        | Weekly           | Risk & Fraud Lead  | Fraud prevention       |
| W05 | Reversed Withdrawal Rate         | Monthly          | Finance / Treasury | Payout rail stability  |
| W06 | Average Processing Duration (SLA)| Daily / Weekly   | UX PM / Ops        | User trust & speed     |
| W07 | Completed Withdrawal Rate        | Weekly           | Executive Team     | Infrastructure quality |
| W08 | Pending Queue Dollar Value       | Daily Snapshot   | CFO / Treasury     | Cash liquidity reserve |
| W09 | Gross Payout Volume (Fiat Equiv) | Monthly          | CFO / Leadership   | Outflow liability      |
| W10 | Withdrawal Method Distribution   | Monthly          | Payment Ops        | Partner rail balancing |
+-----+----------------------------------+------------------+--------------------+------------------------+
```

### Detailed KPI Profiles

#### 1. Withdrawal Request Volume
- **Definition**: Total count of formal payout cash-out submissions made by users within the reporting window.
- **Formula**: `COUNT(withdrawal_id) WHERE requested_timestamp BETWEEN start_date AND end_date`
- **Data Required**: `withdrawal_id`, `requested_timestamp`
- **Data Source**: `Withdrawals`
- **Frequency**: Daily
- **Stakeholder**: Payment Operations / Finance
- **Business Purpose**: Monitors gross cash-out demand and spikes indicating potential marketing referral surges or fraud rings.
- **Interpretation**: Rapid surges require treasury liquidity rebalancing and increased review staffing.
- **Limitation**: Includes requests that will subsequently fail automated screening or KYC checks.
- **Status**: Proposed

#### 2. Completed Withdrawal Count
- **Definition**: Total count of withdrawal requests that successfully settle with payment rail confirmation.
- **Formula**: `COUNT(withdrawal_id) WHERE status = 'completed' AND final_timestamp BETWEEN start_date AND end_date`
- **Data Required**: `withdrawal_id`, `status`, `final_timestamp`
- **Data Source**: `Withdrawals`
- **Frequency**: Daily / Weekly
- **Stakeholder**: VP Product / Operations
- **Business Purpose**: Measures operational throughput and fulfilled user reward expectations.
- **Interpretation**: Consistent completion indicates smooth gateway integrations.
- **Limitation**: Does not convey monetary value or processing speed.
- **Status**: Proposed

#### 3. Pending Withdrawal Queue Size
- **Definition**: Total count of withdrawal requests currently awaiting manual review or payment gateway dispatch.
- **Formula**: `COUNT(withdrawal_id) WHERE status IN ('requested', 'processing')`
- **Data Required**: `withdrawal_id`, `status`
- **Data Source**: `Withdrawals`
- **Frequency**: Real-time / Daily
- **Stakeholder**: Operations Lead
- **Business Purpose**: Operational backlog monitoring to prevent customer support tickets and user anxiety.
- **Interpretation**: A rising queue points to operational review under-staffing or payment API rate limiting.
- **Limitation**: Does not indicate the age of individual pending tickets.
- **Status**: Proposed

#### 4. Rejected Withdrawal Count
- **Definition**: Number of withdrawal requests declined due to compliance, fraud, or rule violations.
- **Formula**: `COUNT(withdrawal_id) WHERE status = 'rejected'`
- **Data Required**: `withdrawal_id`, `status`, `rejection_reason_category`
- **Data Source**: `Withdrawals`
- **Frequency**: Weekly
- **Stakeholder**: Risk & Fraud Lead
- **Business Purpose**: Audits fraud detection effectiveness and user onboarding friction.
- **Interpretation**: High numbers suggest bot farm infiltration or confusing KYC instructions.
- **Limitation**: False positives harm legitimate user retention.
- **Status**: Proposed

#### 5. Reversed Withdrawal Rate
- **Definition**: Percentage of completed payouts that fail post-settlement and bounce back from external rails.
- **Formula**: `(COUNT(withdrawal_id WHERE status = 'reversed') / COUNT(withdrawal_id WHERE status IN ('completed', 'reversed'))) * 100`
- **Data Required**: `withdrawal_id`, `status`
- **Data Source**: `Withdrawals`
- **Frequency**: Monthly
- **Stakeholder**: Finance / Treasury
- **Business Purpose**: Measures payout rail technical reliability and banking partner bounce rates.
- **Interpretation**: A rate above 1% requires immediate technical investigation with payment providers.
- **Limitation**: Reversals from traditional banking rails may lag settlement by 5–10 business days.
- **Status**: Proposed

#### 6. Average Processing Duration (Turnaround Time SLA)
- **Definition**: Mean elapsed time in hours from user submission to terminal completion.
- **Formula**: `AVG(EXTRACT(EPOCH FROM (final_timestamp - requested_timestamp)) / 3600) WHERE status = 'completed'`
- **Data Required**: `requested_timestamp`, `final_timestamp`, `status`
- **Data Source**: `Withdrawals`
- **Frequency**: Daily / Weekly
- **Stakeholder**: UX PM / Operations
- **Business Purpose**: Primary customer satisfaction metric; benchmarks speed against competitor reward platforms.
- **Interpretation**: Shorter durations drive repeat task engagement and strong social word-of-mouth.
- **Limitation**: Averages blend instant automated gift card redemptions with slow wire transfers.
- **Status**: Proposed

#### 7. Completed Withdrawal Rate
- **Definition**: Percentage of total submitted withdrawal requests that achieve successful completion.
- **Formula**: `(COUNT(withdrawal_id WHERE status = 'completed') / COUNT(withdrawal_id)) * 100`
- **Data Required**: `withdrawal_id`, `status`
- **Data Source**: `Withdrawals`
- **Frequency**: Weekly
- **Stakeholder**: Executive Leadership
- **Business Purpose**: High-level platform health metric; indicates redemption success.
- **Interpretation**: Legitimate user cohorts should maintain >90% completion rates.
- **Limitation**: In heavily attacked cohorts, this metric legitimately declines due to fraud blocking.
- **Status**: Proposed

#### 8. Pending Queue Dollar Value
- **Definition**: Aggregate monetary points value held in the pending review and processing queue.
- **Formula**: `SUM(requested_amount) WHERE status IN ('requested', 'processing')`
- **Data Required**: `requested_amount`, `status`
- **Data Source**: `Withdrawals`
- **Frequency**: Daily Snapshot
- **Stakeholder**: CFO / Treasury
- **Business Purpose**: Working capital management; ensures bank accounts hold sufficient float.
- **Interpretation**: Prevents liquidity shortages during payout batch executions.
- **Limitation**: Value fluctuates rapidly during batch settlement runs.
- **Status**: Proposed

#### 9. Gross Payout Volume (Fiat Equivalent)
- **Definition**: Total value of points liquidated and disbursed to users across the reporting window.
- **Formula**: `SUM(requested_amount WHERE status = 'completed')`
- **Data Required**: `requested_amount`, `status`, `final_timestamp`
- **Data Source**: `Withdrawals`
- **Frequency**: Monthly
- **Stakeholder**: CFO / Finance Director
- **Business Purpose**: Core expense metric; monitors cash outflow against collected ad revenues.
- **Interpretation**: Must remain below net ad network receivables to guarantee commercial profitability.
- **Limitation**: Does not account for payment rail transaction fees.
- **Status**: Proposed

#### 10. Withdrawal Method Distribution
- **Definition**: Percentage breakdown of completed payout transactions across each disbursement rail.
- **Formula**: `(COUNT(withdrawal_id WHERE withdrawal_method = [METHOD] AND status = 'completed') / Total Completed) * 100`
- **Data Required**: `withdrawal_method`, `status`
- **Data Source**: `Withdrawals`
- **Frequency**: Monthly
- **Stakeholder**: Payment Operations
- **Business Purpose**: Informs contract negotiations with payment rails and guides treasury cash balancing.
- **Interpretation**: Highlights user preferences (e.g., crypto USDT adoption in emerging markets vs PayPal in US).
- **Limitation**: Heavily influenced by regional payment availability constraints.
- **Status**: Proposed

---

## 5. Work Package D4: Empirical Wallet Ledger & Withdrawal Reconciliation Engine

To address the critical financial integrity mandate and resolve the negative circulating supply discrepancy previously identified during auditing, an end-to-end automated reconciliation engine was built and executed (`scripts/validate_wallet_reconciliation.py`).

### Root Cause Analysis & Resolution of Negative Circulating Supply
In earlier simulated prototypes, withdrawal debit transactions were generated without checking the user's running earned balance, leading to unbacked debits, artificial negative user balances (down to -15,905 VEs), and an overall negative circulating float (-1.68M VEs).
**Permanent Resolution**:
1. Every debit (withdrawal, token exchange, fee) is strictly bounded by the user's chronological cumulative earned balance: `withdrawal_amount <= running_balance * 0.60`.
2. Initial/Opening balance is fixed at `0.00 VEs` across all 1,000 registered accounts.
3. Overdrafts are mathematically prohibited: `minimum_user_balance >= 0.00 VEs`.
4. Reversals are bounded so that clawing back credits cannot push an account below zero.

### Ledger Balance & Cash Flow Summary
- **Total Accounts Audited**: 1,000 users
- **User Opening Balance**: `0.00 VEs` across all 1,000 accounts
- **Total Ledger Transactions**: 3,500 rows (2,342 Credits, 1,158 Debits)
- **Gross Ledger Credits**: `+371,985.00 VEs` (Completed: `+370,335.00 VEs`; Pending/Failed: `+1,650.00 VEs`)
- **Gross Ledger Debits**: `-106,245.00 VEs` (Completed: `-101,480.00 VEs`; Pending/Failed: `-4,765.00 VEs`)
- **Net Circulating Supply (Float)**: `+268,855.00 VEs`
- **Sum of User Closing Balances**: `+268,855.00 VEs`
- **Circulating Supply Parity Discrepancy**: `0.000000 VEs` (Exact Mathematical Parity)
- **Minimum User Balance Recorded**: `0.00 VEs` (Zero overdrafts across 1,000 accounts at all chronological points)
- **Maximum User Balance Recorded**: `2,075.00 VEs`
- **Median (P50) User Balance**: `199.00 VEs`

### Test Suite Execution Evidence (All 6 Test Cases PASSED)

| Test ID | Invariant Verified | Validation Logic | Scope Checked | Result | Discrepancy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WLT-TC01** | Double-Entry Sign Invariant | Credits strictly positive (`> 0`), Debits strictly negative (`< 0`) | 3,500 Ledger Rows | **PASSED** | 0 violations |
| **WLT-TC02** | Zero Overdraft Invariant | No user balance may drop below `0.00 VEs` at any point in time | 1,000 User Accounts | **PASSED** | 0 overdrafts (Min: `0.00 VEs`) |
| **WLT-TC03** | Circulating Supply Parity | Sum of user closing balances == Net completed ledger entries | 1,000 Users vs Ledger | **PASSED** | `0.000000 VEs` exact parity |
| **WLT-TC04** | Reward-to-Wallet Credit Audit | Every `reward_credit` maps to a valid record in `Rewards.csv` | 2,280 Reward Credits | **PASSED** | 0 orphan credits (100% matched) |
| **WLT-TC05** | Withdrawal Settlement Audit | All 882 completed withdrawals have corresponding debits; 62 refunds mapped | 1,200 Withdrawal Requests | **PASSED** | 0 orphan settlements |
| **WLT-TC06** | Reversal Link Audit | Offsetting reversal entries link to verified parent transaction IDs | 36 Reversal Rows | **PASSED** | 0 orphan reversals |

- **Reconciliation Engine Script**: `scripts/validate_wallet_reconciliation.py`
- **Detailed Audit Outputs**: `data/wallet_reconciliation_test_results.csv` and `data/wallet_reconciliation_summary.csv`

---
*Deliverable Document Reference: `docs/06_WALLET_WITHDRAWAL_ANALYTICS.md` | Related Spec: `deliverables_tables/11_KPI_CATALOGUE.csv`.*
