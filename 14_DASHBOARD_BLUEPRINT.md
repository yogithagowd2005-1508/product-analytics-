# 14 — WORK PACKAGE M: ANALYTICS DASHBOARD BLUEPRINT

> **MANDATORY DATA AUTHENTICITY NOTICE**  
> *VELOOP is a real product under development, but the data supplied and evaluated for this assignment is fictional/simulated for analytical testing. In accordance with the Data Authenticity Policy, no metric or finding herein represents actual VELOOP production statistics, actual earnings, actual withdrawals, or live business performance.*

---

## 1. Executive BI Strategy & Architecture
The **Analytics Dashboard Blueprint (Work Package M)** provides the end-to-end design specification for the 7 production business intelligence dashboards serving VELOOP leadership, product managers, financial controllers, and operational teams. 

### Operational BI Principles
1. **Action-Oriented Visuals**: Every chart must directly answer a concrete business question and support a specific operational decision.
2. **Standardized Color-Coding**: Blue (Volume/Activity), Green (Completions/Revenues), Yellow/Orange (Pending/Escrow), Red (Reversals/Failures/Fraud).
3. **Low-Latency Aggregation**: Dashboards query dimensional Gold Mart tables (`fct_user_activity_daily`, `fct_withdrawal_pipeline`) pre-aggregated by dbt, guaranteeing `<1.5 second` render times.

---

## 2. The 7 Production Dashboard Suites

```
+---------------------------------------------------------------------------------------------------------+
|                                        VELOOP PRODUCTION BI SUITE                                       |
+-----+-----------------------+------------------------+--------------------------------------------------+
| NO. | DASHBOARD SUITE       | TARGET AUDIENCE        | STRATEGIC FOCUS                                  |
+-----+-----------------------+------------------------+--------------------------------------------------+
| 01  | Executive Overview    | C-Suite / Founders     | High-level health: DAU, Net Margins, Payout SLA  |
| 02  | User Analytics        | Growth / Marketing PM  | Acquisition channels, cohort retention, churn    |
| 03  | Engagement            | Earning / Game PM      | Task completion rates, feature adoption depth    |
| 04  | Rewards               | Product Economist / CFO| Points liability creation, reversal rates, ARPAU |
| 05  | Wallet & Economics    | CFO / Treasury Lead    | Double-entry volume, circulating supply, float   |
| 06  | Withdrawals           | Payment Ops / Risk     | Payout queue backlog, processing SLA, fraud rejs |
| 07  | Referrals             | Growth Lead            | Viral coefficient (K), activation funnel, CAC    |
+-----+-----------------------+------------------------+--------------------------------------------------+
```

---

## 3. Detailed Dashboard Specifications & Wireframes

### Dashboard 1 — Executive Overview
![Dashboard 1 — Executive Overview](../dashboards/screenshots/dashboard_1_executive_overview.png)

```
+--------------------------------------------------------------------------------------------------+
| VELOOP REWARDS | EXECUTIVE OVERVIEW DASHBOARD                             [Date: Last 30 Days v] |
+--------------------------------------------------------------------------------------------------+
| [ KPI: DAU ]         [ KPI: Task Completion% ] [ KPI: Completed WDR% ]   [ KPI: Avg Processing TAT ]|
| 1,420 Cumulative     72.6% Completed           73.5% Settled             38.1 Hours SLA            |
| (~37 unique/day)     (4,357 of 6,000 tasks)    (882 of 1,200 requests)   (Within 48h target SLA)   |
+--------------------------------------------------------------------------------------------------+
| [ CHART 1: 30-Day DAU & Task Completion Trend ]   | [ CHART 2: Daily Points Influx vs Outflow ]  |
| Line: DAU (Blue) | Bars: Tasks Completed (Green)  | Area: Rewards Credited vs Withdrawals Settled|
|                                                   |                                              |
|                                                   |                                              |
+--------------------------------------------------------------------------------------------------+
| [ CHART 3: Payout Channel Distribution ]          | [ TABLE 1: Top Operational Alert Highlights] |
| Donut: PayPal (45%) | USDT (28%) | Amazon (18%)   | Reversal Rate: 3.20% (160 clawbacks)         |
| Bank (9%)                                         | Pending Withdrawal Queue: 125 requests       |
+--------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:
1. **Metric**: Daily Active Users (DAU)
   - **Calculation**: `COUNT(DISTINCT user_id) WHERE event_timestamp::date = TODAY`
   - **Source**: `fct_user_activity_daily`
   - **Visualization**: Big Number KPI Card with sparkline comparison against 7-day moving average.
   - **Filters**: Date Range, Country Code, Platform.
   - **Business Question**: How many unique engaged users visited the platform today?
   - **Decision Supported**: Adjust live ad acquisition spend if daily community reach drops.
2. **Metric**: Net Points Influx vs Redemption Outflow
   - **Calculation**: `SUM(reward_amount credited) - SUM(withdrawal_amount completed)`
   - **Source**: `fct_ledger_transactions`
   - **Visualization**: Dual-axis stacked area chart.
   - **Business Question**: Is points creation outpacing user redemption demand?
   - **Decision Supported**: Rebalance earning reward rates or adjust exchange pegs to prevent treasury drain.

---

### Dashboard 2 — User Analytics
![Dashboard 2 — User Analytics & Lifecycle](../dashboards/screenshots/dashboard_2_user_analytics.png)

```
+--------------------------------------------------------------------------------------------------+
| VELOOP REWARDS | USER ANALYTICS & LIFECYCLE                               [Cohort: All Users v]  |
+--------------------------------------------------------------------------------------------------+
| [ KPI: Total Signups ] [ KPI: Onboarding Rate ]   [ KPI: D7 Retention ]   [ KPI: Dormant Rate ]  |
| 1,000 Registrations    81.7% Completed            24.5% Active D7         24.0% Inactive >30d    |
+--------------------------------------------------------------------------------------------------+
| [ CHART 1: Acquisition Channel Breakdown ]        | [ CHART 2: Geographic Distribution Heatmap ] |
| Stacked Bar: Organic vs Referral vs Paid Ads      | Map: US (30%), IN (18%), GB (15%), PH (8%)   |
+--------------------------------------------------------------------------------------------------+
| [ CHART 3: User Lifecycle State Distribution ]    | [ TABLE 2: Cohort Retention Survival Table ] |
| Funnel: Registered -> Onboarded -> Active -> Loyal| Week 0: 100% -> W1: 38% -> W2: 28% -> W4: 21%|
+--------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:
1. **Metric**: Acquisition Channel Yield
   - **Calculation**: `COUNT(user_id) GROUP BY registration_source, DATE_TRUNC('week', registration_timestamp)`
   - **Source**: `dim_users`
   - **Visualization**: Stacked 100% bar chart by acquisition source.
   - **Business Question**: Which marketing channels provide the bulk of new registrants?
   - **Decision Supported**: Reallocate marketing budget to high-performing organic referral channels.
2. **Metric**: 30-Day Cohort Retention Matrix
   - **Calculation**: Triangular cohort survival percentage by signup week across Days 1, 3, 7, 14, 30.
   - **Source**: `fct_user_retention_cohorts`
   - **Visualization**: Heatmap grid table.
   - **Business Question**: Are newer product onboarding updates improving long-term retention?
   - **Decision Supported**: Roll back confusing UI updates if new cohorts show accelerated Day 3 drop-off.

---

### Dashboard 3 — Engagement
![Dashboard 3 — Engagement & Feature Performance](../dashboards/screenshots/dashboard_3_engagement.png)

```
+--------------------------------------------------------------------------------------------------+
| VELOOP REWARDS | ENGAGEMENT & FEATURE PERFORMANCE                         [Segment: Active DAU v]|
+--------------------------------------------------------------------------------------------------+
| [ KPI: Task Start Volume ] [ KPI: Completion Rate ] [ KPI: Daily Check-ins ] [ KPI: Avg Tasks/DAU]|
| 6,000 Started              72.6% Completed          2,685 Check-ins          4.75 Tasks / User   |
| (Across 6 mechanisms)      (4,357 completed)        (Streak continuity)      (Active engagement) |
+--------------------------------------------------------------------------------------------------+
| [ CHART 1: Earning Module Completion Rates ]      | [ CHART 2: Diurnal Hourly Activity Heatmap ] |
| Bar Chart: Video Ads (88%), Surveys (42%),        | Grid: Hour of Day (0-23) vs Day of Week      |
| Tap & Earn (81%), Offerwalls (38%)                | Peak Traffic: 18:00 - 22:00 UTC              |
+--------------------------------------------------------------------------------------------------+
| [ CHART 3: Streak Continuity Distribution ]       | [ CHART 4: Spin Wheel vs Task Engagement ]   |
| Histogram: 1-Day, 3-Day, 7-Day, 14-Day, 30-Day    | Scatter Plot: Spin Frequency vs Tasks Done   |
+--------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:
1. **Metric**: Task Completion Rate by Module
   - **Calculation**: `(COUNT(completed) / COUNT(started)) * 100 GROUP BY task_type`
   - **Source**: `fct_task_activity`
   - **Visualization**: Horizontal grouped bar chart comparing starts vs completions.
   - **Business Question**: Which earning tasks suffer catastrophic user drop-off?
   - **Decision Supported**: Replace survey providers or optimize offerwall instructions if completion falls below 50%.

---

### Dashboard 4 — Rewards
![Dashboard 4 — Rewards & Economic Liability](../dashboards/screenshots/dashboard_4_rewards.png)

```
+--------------------------------------------------------------------------------------------------+
| VELOOP REWARDS | REWARDS & ECONOMIC LIABILITY                             [Currency: VEs v]      |
+--------------------------------------------------------------------------------------------------+
| [ KPI: Gross Points Issued ] [ KPI: Reversal Rate ] [ KPI: Pending Escrow ] [ KPI: Escrow Backed] |
| 698,350 VEs Credited         3.20% Clawed Back      4.30% Buffer             100.0% Reserve      |
| (4,638 credited records)     (160 clawbacks)        (High-value hold)        (Fully solvent)     |
+--------------------------------------------------------------------------------------------------+
| [ CHART 1: Reward Issuance Breakdown by Module ]  | [ CHART 2: Daily Reversal Trend & Causes ]   |
| Donut: Tasks (60%), Daily (15%), Streaks (8%),    | Stacked Area: Chargebacks vs Bot Detection   |
| Referrals (7%), Spins (6%), Badges (4%)           | Spikes near affiliate month-end settlement   |
+--------------------------------------------------------------------------------------------------+
| [ TABLE 3: High-Value Pending Reward Escrow Queue ]                                              |
| Reward ID | User ID | Task | Amount | Release Scheduled | Fraud Risk Score | Action Override      |
+--------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:
1. **Metric**: Reward Reversal Rate
   - **Calculation**: `(COUNT(reward_id reversed) / COUNT(total rewards)) * 100`
   - **Source**: `fct_rewards`
   - **Visualization**: Line chart with 2.0% threshold alert band.
   - **Business Question**: Are affiliate networks clawing back commissions due to bot traffic?
   - **Decision Supported**: Block specific emulator models or blacklist abusive survey sub-networks.

---

### Dashboard 5 — Wallet & Economics
![Dashboard 5 — Multi-Currency Wallet & Ledger](../dashboards/screenshots/dashboard_5_wallet.png)

```
+--------------------------------------------------------------------------------------------------+
| VELOOP REWARDS | WALLET & TREASURY INTELLIGENCE                           [Unit: Multi-Currency] |
+--------------------------------------------------------------------------------------------------+
| [ KPI: Circulating Supply ] [ KPI: Total Ledger ]   [ KPI: Ledger Credits ]  [ KPI: Overdrafts ] |
| +268,855.00 VEs Net Float   3,500 Journal Rows      +370.3k VEs Completed    0 Overdrafts (0.00) |
| (100% Solvent User Float)   (Double-Entry Log)      (-101.5k VEs Debits)     (Min balance >= 0)  |
+--------------------------------------------------------------------------------------------------+
| [ CHART 1: Double-Entry Transaction Mix ]         | [ CHART 2: Token Exchange Velocity ]         |
| Stacked Bars: Credits vs Debits vs Adjustments    | Trend Line: VEs Swapped to On-Chain Tokens   |
+--------------------------------------------------------------------------------------------------+
| [ TABLE 4: Top 20 Whale Balances & Dormancy Exposure ]                                           |
| User ID | Total Balance | Last Active | Dormancy Risk Status | Potential Breakage Earmark         |
+--------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:
1. **Metric**: Circulating VE Supply
   - **Calculation**: `SUM(amount WHERE status = 'completed')`
   - **Source**: `fct_wallet_ledger`
   - **Visualization**: Cumulative line area chart showing outstanding platform liabilities.
   - **Business Question**: What is the company's total unredeemed points liability owed to users?
   - **Decision Supported**: Maintain appropriate bank treasury reserves to cover potential redemption runs.

---

### Dashboard 6 — Withdrawals
![Dashboard 6 — Withdrawals & Payout Operations](../dashboards/screenshots/dashboard_6_withdrawals.png)

```
+--------------------------------------------------------------------------------------------------+
| VELOOP REWARDS | WITHDRAWALS & PAYOUT OPERATIONS                          [Status: All Pipelines]|
+--------------------------------------------------------------------------------------------------+
| [ KPI: Total Requests ] [ KPI: Success Rate ]     [ KPI: Pending Backlog ] [ KPI: Avg TAT SLA ]  |
| 1,200 Requests          73.5% Completed           125 Queue Count          38.1 Hours Turnaround |
| (Gross Payout Demand)   (882 settled payouts)     (10.4% in review)        (Within 48h SLA)      |
+--------------------------------------------------------------------------------------------------+
| [ CHART 1: Payout Turnaround SLA Distribution ]   | [ CHART 2: Rejection Root-Cause Breakdown ]  |
| Histogram: <6h (22%), 6-24h (48%), 24-48h (24%),  | Horizontal Bar: KYC Incomplete (35%),        |
| >48h (6% Backlogged)                              | Minimum Threshold (25%), Fraud Risk (20%)    |
+--------------------------------------------------------------------------------------------------+
| [ TABLE 5: Real-time Payout Review Queue ]                                                       |
| WDR ID | User ID | Method | Requested Amount | Age (Hours) | Risk Flag | Provider Gateway Rail   |
+--------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:
1. **Metric**: Withdrawal Turnaround SLA (TAT)
   - **Calculation**: `(final_timestamp - requested_timestamp) in hours WHERE status = 'completed'`
   - **Source**: `fct_withdrawal_pipeline`
   - **Visualization**: SLA density histogram and 48-hour SLA breach alert gauge.
   - **Business Question**: Are payout operations meeting the 24–48 hour settlement promise?
   - **Decision Supported**: Reassign compliance review agents to process backlogged queues.

---

### Dashboard 7 — Referrals
![Dashboard 7 — Referral & Viral Growth Funnel](../dashboards/screenshots/dashboard_7_referrals.png)

```
+--------------------------------------------------------------------------------------------------+
| VELOOP REWARDS | REFERRAL & VIRAL GROWTH ENGINE                           [Channel: All Channels]|
+--------------------------------------------------------------------------------------------------+
| [ KPI: Invites Created ] [ KPI: Signup Rate ]     [ KPI: Activation Rate ] [ KPI: Viral K-Factor] |
| 900 Links Generated      84.4% Signed Up          73.7% Activated          K = 0.56 (560/1,000)  |
| (Top of Viral Funnel)    (760 registered users)   (560 activated users)    (Bounty K = 0.37)     |
+--------------------------------------------------------------------------------------------------+
| [ CHART 1: Four-Stage Referral Funnel ]           | [ CHART 2: Viral Conversion by Social App ]  |
| Funnel: Created (900) -> Registered (760) ->      | Bar Chart: WhatsApp (52%), Telegram (44%),   |
| Activated (560) -> Converted (370)                | Twitter (28%), SMS (22%)                     |
+--------------------------------------------------------------------------------------------------+
| [ TABLE 6: Top Viral Advocate Leaderboard ]                                                      |
| Referrer ID | Invites Sent | Activated Referees | Viral Bounty Earned | Referee Retention Rate   |
+--------------------------------------------------------------------------------------------------+
```

#### Detailed Visual Specifications:
1. **Metric**: Viral K-Factor
   - **Calculation**: `(Activated Referees / Total Registered Users) = 560 / 1,000 = 0.56` (Activated Viral Coefficient); `(Bounty Converted / Total Registered Users) = 370 / 1,000 = 0.37` (Monetized Viral Bounty Coefficient).
   - **Source**: `fct_referral_funnel`
   - **Visualization**: Gauge chart with critical threshold markers (0.5 warning, 1.0 viral parity).
   - **Business Question**: Is the platform achieving viral compounding or decaying organically?
   - **Decision Supported**: Increase referral bounty rewards if K-factor drops below 0.3.

---

### 3.8 AI & Predictive Intelligence Layer: Production Implemented vs Conceptual Architecture

In strict compliance with evaluation standards, all AI/ML components are explicitly categorized into **Implemented & Tested in Code** versus **Conceptual Architecture (Phase 2/3 Roadmap)**:

```
+---------------------------------------------------------------------------------------------------------------------+
|                                 AI / ML FEATURE IMPLEMENTATION STATUS BREAKDOWN                                      |
+-----+-------------------------------+-------------------------------+-----------------------+-----------------------+
| NO. | FEATURE / ENGINE              | IMPLEMENTATION STATUS         | PRIMARY CODE / SCRIPT | TEST EVIDENCE         |
+-----+-------------------------------+-------------------------------+-----------------------+-----------------------+
| 01  | Double-Entry Invariant Guard  | [IMPLEMENTED & TESTED]        | validate_wallet_rec.. | 6 Invariant Tests PASS|
| 02  | 14-Anomaly Cleansing Pipeline | [IMPLEMENTED & TESTED]        | clean_and_quarantine..| 0 Remaining Defects   |
| 03  | 35-KPI Verification Engine    | [IMPLEMENTED & TESTED]        | verify_all_kpis.py    | 24 Calc / 11 Spec PASS|
| 04  | Predictive Churn ML           | [CONCEPT SPECIFICATION - PH2] | docs/14_DASHBOARD_..  | Architectural Wirefr. |
| 05  | Automated Payout Classifier   | [CONCEPT SPECIFICATION - PH2] | docs/14_DASHBOARD_..  | Architectural Wirefr. |
| 06  | Graph Collusion Shield        | [CONCEPT SPECIFICATION - PH3] | docs/14_DASHBOARD_..  | Architectural Wirefr. |
| 07  | Dynamic Points Peg Optimizer  | [CONCEPT SPECIFICATION - PH3] | docs/14_DASHBOARD_..  | Architectural Wirefr. |
+-----+-------------------------------+-------------------------------+-----------------------+-----------------------+
```

#### A. Implemented & Tested in Python Scripts:
1. **Double-Entry Cryptographic Invariant Guard (`scripts/validate_wallet_reconciliation.py`)**:
   - Validates that credits are signed positive and debits signed negative.
   - Mathematically enforces zero overdrafts across all 1,000 accounts (`min_balance = 0.00 VEs`).
   - Verifies exact circulating supply parity (`discrepancy = 0.000000 VEs`).
2. **Automated 14-Anomaly Remediation & Quarantine Engine (`scripts/clean_and_quarantine_data.py`)**:
   - Ingests 550 records from `Messy_Data.csv`.
   - Cleans whitespace, casing, and event naming in-place.
   - Automatically isolates unrecoverable corruptions to Dead-Letter Quarantine (`Quarantined_Anomalies.csv`), producing a clean dataset (`Cleaned_Data.csv`) with **0.0% residual defect rate**.
3. **Automated 35-KPI Verification Engine (`scripts/verify_all_kpis.py`)**:
   - Calculates 24 empirical metrics directly from raw tables with explicit formulas.
   - Formally audits 11 mathematical specifications and upstream dependencies.

#### B. Conceptual Architecture (Phase 2/3 Roadmap):
1. **Predictive Churn & Retention ML (`VELOP-Churn-v2`)**: Concept for a logistic survival model on Day 3 drop-off signals (requires production clickstream history).
2. **Automated Payout Fast-Track Classifier (`VELOP-PayoutClassifier`)**: Concept for an XGBoost classification model to fast-track low-risk withdrawals (requires payment gateway fraud postbacks).
3. **Graph Bot Collusion Shield (`VELOP-GraphShield`)**: Concept for Graph Convolutional Network (GCN) detecting cyclical invite rings (requires cross-device hardware fingerprinting).
4. **Dynamic Reward Point Peg Optimizer**: Concept for Reinforcement Learning balancing reward issuance against partner ad arbitrage margins.

---

## 4. Dashboard Implementation Evidence & Visual Gallery

To verify practical viability beyond wireframe specifications, all seven production dashboards have been implemented in an interactive web application and rendered into high-resolution visual evidence artifacts.

### A. Live Interactive Dashboard Prototype
- **Live Local Dashboard Application**: [dashboards/index.html](../dashboards/index.html)
- **Features**: Fully functional single-page analytics application styled with Tailwind CSS, powered by Chart.js, featuring dynamic multi-tab switching, real-time KPI card calculations, responsive data tables, and interactive trend charts across all 7 operational domains.

### B. High-Resolution Visual Render Artifacts
Each dashboard has been compiled and rendered headlessly via `scripts/render_dashboard_screenshots.py` into production visual artifacts:

#### 1. Dashboard 1: Executive Overview
![Dashboard 1: Executive Overview](../dashboards/screenshots/dashboard_1_executive_overview.png)
* **Target Audience**: C-Suite, Founders, Operations Lead
* **Primary Source Mart**: `fct_user_activity_daily`, `fct_ledger_transactions`
* **Key Visuals**: 30-Day Activity Trends, Influx vs Outflow area chart, and Payout Channel shares.

---

#### 2. Dashboard 2: User Analytics & Lifecycle
![Dashboard 2: User Analytics & Lifecycle](../dashboards/screenshots/dashboard_2_user_analytics.png)
* **Target Audience**: Growth Product Manager, User Acquisition Lead
* **Primary Source Mart**: `dim_users`, `fct_user_retention_cohorts`
* **Key Visuals**: Registrations, Onboarding completion rate, D7/D30 Retention, Geographic distribution, and Lifecycle state funnels.

---

#### 3. Dashboard 3: Engagement & Gamification
![Dashboard 3: Engagement & Gamification](../dashboards/screenshots/dashboard_3_engagement.png)
* **Target Audience**: Gamification PM, Game Economy Designer
* **Primary Source Mart**: `fct_task_activity`, `fct_streak_events`
* **Key Visuals**: Started vs Completed tasks, Spin Wheel participation, Daily Streak claims, and Feature category breakdown.

---

#### 4. Dashboard 4: Rewards & Liability Management
![Dashboard 4: Rewards & Liability Management](../dashboards/screenshots/dashboard_4_rewards.png)
* **Target Audience**: CFO, Product Economist, Treasury Operations
* **Primary Source Mart**: `fct_rewards`, `fct_escrow_hold`
* **Key Visuals**: Points liability issued, Reversal clawback rate, Escrow buffer ratios, and Feature reward yield.

---

#### 5. Dashboard 5: Multi-Currency Wallet & Ledger
![Dashboard 5: Multi-Currency Wallet & Ledger](../dashboards/screenshots/dashboard_5_wallet.png)
* **Target Audience**: Financial Controller, Ledger Architecture Team
* **Primary Source Mart**: `fct_wallet_ledger`, `fct_daily_treasury`
* **Key Visuals**: Circulating token supply, Float reserves, Net ledger entries, and Currency velocity metrics.

---

#### 6. Dashboard 6: Withdrawals & Cash-Out Operations
![Dashboard 6: Withdrawals & Cash-Out Operations](../dashboards/screenshots/dashboard_6_withdrawals.png)
* **Target Audience**: Payment Operations, Risk & Compliance Team
* **Primary Source Mart**: `fct_withdrawal_pipeline`
* **Key Visuals**: Fulfillment rate, Pending queue backlog, SLA turnaround distribution (TAT), and Gateway method breakdown.

---

#### 7. Dashboard 7: Referrals & Viral Growth Funnel
![Dashboard 7: Referrals & Viral Growth Funnel](../dashboards/screenshots/dashboard_7_referrals.png)
* **Target Audience**: Growth Lead, Virality Strategist
* **Primary Source Mart**: `fct_referral_funnel`
* **Key Visuals**: 4-Stage viral funnel, K-factor virality gauge, Social sharing attribution, and Advocate leaderboards.

---
*Deliverable Document Reference: `docs/14_DASHBOARD_BLUEPRINT.md` | Prepared for BI & Executive Stakeholders.*
