# 11 — WORK PACKAGE I: VELOOP KPI CATALOGUE

> **MANDATORY DATA AUTHENTICITY NOTICE**  
> *VELOOP is a real product under development, but the data supplied and evaluated for this assignment is fictional/simulated for analytical testing. In accordance with the Data Authenticity Policy, no metric or finding herein represents actual VELOOP production statistics, actual earnings, actual withdrawals, or live business performance.*

---

## 1. Executive Framework & Integrity Policy
The **VELOOP KPI Catalogue (Work Package I)** establishes the authoritative single source of truth for all operational, financial, and product metrics.

### Non-Negotiable KPI Integrity Rules
1. **No Fictional Company Targets**: KPIs define reproducible measurement logic, not arbitrary goalposts. (e.g., NOT *"VELOOP should hit 50,000 DAU"*; INSTEAD *"Daily Active Users = unique users generating a qualifying telemetry activity event within a UTC calendar day"*).
2. **Every Metric Must Be Traceable**: Every KPI specifies its exact formula, required data fields, underlying tables, reporting cadence, and target stakeholder.
3. **Explicit Documentation of Limitations**: Every metric states its inherent limitations (e.g. inability to capture uninstalled users, latency of third-party postbacks).

- **Primary Data File**: `deliverables_tables/11_KPI_CATALOGUE.csv`
- **Total KPIs Catalogued**: **35 KPIs** (exceeding the minimum mandate of 30+ KPIs)
- **Coverage Domains**: User (5), Engagement (6), Rewards (5), Wallet (5), Withdrawals (7), Referrals (4), Support/Content (3).

---

## 2. KPI Portfolio Overview

```
+---------------------------------------------------------------------------------------------------------+
|                                      VELOOP KPI CATALOGUE SUMMARY                                       |
+---------------------+-------------+--------------------------+------------------------------------------+
| KPI DOMAIN          | KPI COUNT   | PRIMARY STAKEHOLDER      | CORE BUSINESS FOCUS                      |
+---------------------+-------------+--------------------------+------------------------------------------+
| 1. User KPIs        | 5 KPIs      | Growth / Product Lead    | Acquisition throughput, DAU, MAU, Churn  |
| 2. Engagement KPIs  | 6 KPIs      | Product Manager (Earning)| Task completion rate, session depth, D7  |
| 3. Reward KPIs      | 5 KPIs      | CFO / Product Economist  | Points inflation, liability, ARPAU       |
| 4. Wallet KPIs      | 5 KPIs      | Finance / Web3 Lead      | Supply velocity, circulating float, GTV  |
| 5. Withdrawal KPIs  | 7 KPIs      | Payment Ops / Risk Lead  | Turnaround time, completion rate, volume |
| 6. Referral KPIs    | 4 KPIs      | Head of Growth           | Viral coefficient (K), activation rate   |
| 7. Support KPIs     | 3 KPIs      | Customer Support Lead    | Friction ticket rate, self-serve FAQ     |
+---------------------+-------------+--------------------------+------------------------------------------+
| TOTAL PORTFOLIO     | 35 KPIS     | (Target: 30+)            | Comprehensive 360-degree Platform Health |
+---------------------+-------------+--------------------------+------------------------------------------+
```

---

## 3. Comprehensive KPI Catalogue Table

| KPI Name | Definition | Formula | Required Fields | Data Source | Frequency | Stakeholder | Business Purpose | Interpretation | Limitation | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **New User Registrations** | Unique user profiles created in period | `COUNT(DISTINCT user_id)` | `user_id`, `reg_timestamp` | `Users` | Daily | Growth Lead | Top-of-funnel acquisition volume | Upward trend reflects acquisition growth | Doesn't measure user quality | Proposed |
| **Daily Active Users (DAU)**| Unique users with >= 1 qualifying event in UTC day | `COUNT(DISTINCT user_id) WHERE qualifying_event = TRUE` | `user_id`, `timestamp`, `event_name` | `Feature_Events`, `Task_Activity` | Daily | Executive Leadership | Core operational community size | Measures daily product utility | May be skewed by background syncs | Proposed |
| **Monthly Active Users (MAU)**| Unique users active within rolling 30-day window | `COUNT(DISTINCT user_id) in 30d window` | `user_id`, `timestamp` | `Feature_Events`, `Task_Activity` | Monthly | Executive / Investors | Macro audience reach indicator | Evaluates total monthly footprint | Masks intra-month churn | Proposed |
| **DAU / MAU Stickiness Ratio**| Ratio of daily to monthly active users (%) | `(DAU / MAU) * 100` | `DAU`, `MAU` | Aggregates | Daily | Product Strategy | Quantifies habitual product stickiness | >20% indicates strong daily habit | Doesn't isolate specific feature drivers | Proposed |
| **Dormant User Rate** | % registered users with no session in 30 days | `(COUNT(last_login < 30d) / Total Users) * 100` | `user_id`, `last_login_timestamp` | `Users` | Weekly | Retention Marketing | Monitors pool of churned/lapsed users | Rising rate signals incentive fatigue | Cannot detect uninstalled apps | Proposed |
| **Task Start Volume** | Total earning tasks initiated by users | `COUNT(task_activity_id)` | `task_activity_id`, `started_at` | `Task_Activity` | Daily | Earning PM | Measures task catalog demand | High starts indicate attractive reward headlines | Doesn't measure completion | Proposed |
| **Task Completion Rate** | % started tasks achieving validated completion | `(COUNT(completed) / COUNT(started)) * 100` | `task_activity_id`, `status` | `Task_Activity` | Daily | Product / Ad Ops | Identifies task friction & broken postbacks | Low rate indicates technical partner bugs | Blends easy ads with hard surveys | Proposed |
| **Tasks Completed per DAU** | Mean validated tasks completed per active user | `COUNT(completed) / COUNT(DISTINCT user_id)` | `task_activity_id`, `user_id`, `status` | `Task_Activity` | Daily | Earning PM | Measures depth of earning per user session | Higher density indicates strong monetization | Skewed by power users / clickers | Proposed |
| **Daily Streak Claim Rate**| % DAU claiming daily calendar check-in reward | `(COUNT(claimants) / DAU) * 100` | `user_id`, `event_name` | `Feature_Events`, `Users` | Daily | Gamification PM | Evaluates daily habit loop adoption | Healthy adoption is >60% of DAU | Doesn't measure streak longevity | Proposed |
| **Spin Wheel Engagement** | Mean spins per participating active user | `COUNT(spin_id) / COUNT(DISTINCT spinners)` | `event_id`, `user_id` | `Feature_Events` | Daily | Gamification PM | Measures minigame popularity & token sinks | Repeat spins show strong engagement | Doesn't isolate free vs paid spins | Proposed |
| **D7 Cohort Task Retention**| % new users completing task on 7th day | `(COUNT(active D7) / COUNT(registered D0)) * 100` | `user_id`, `reg_timestamp`, `started_at` | `Users`, `Task_Activity` | Weekly | Growth Analytics | Standard benchmark for onboarding stickiness | High D7 indicates lasting product fit | Requires 7-day maturity delay | Proposed |
| **Total Reward Issuance** | Aggregate points credited to users | `SUM(amount) WHERE status = 'credited'` | `amount`, `status`, `unit` | `Rewards` | Daily | CFO / Product Ops | Monitors liability creation and point inflation | Must scale with partner revenue | Doesn't measure cash redemption timing | Proposed |
| **Reward Reversal Rate** | % issued rewards clawed back or voided | `(COUNT(reversed) / COUNT(rewards)) * 100` | `reward_id`, `status` | `Rewards` | Weekly | Risk & Fraud Lead | Monitors affiliate postback chargebacks | >2% signals fraud or offerwall spoofing | Reversals lag by 14–30 days | Proposed |
| **Reward Distribution by Feature**| % share of points credited by reward type | `(SUM(feature_points) / SUM(total_points)) * 100` | `amount`, `reward_type` | `Rewards` | Weekly | Product Economist | Identifies dominant reward liability sources | Highlights over-reliance on minigames vs ads | Doesn't account for partner margins | Proposed |
| **Average Reward per DAU** | Mean points credited per active user | `SUM(amount) / DAU` | `amount`, `user_id` | `Rewards`, `Feature_Events` | Daily | Product Economist | Evaluates earning speed competitiveness | Balances user attractiveness vs unit cost | Skewed by top 1% survey grinders | Proposed |
| **Pending Escrow Ratio** | % points locked in escrow vs posted balance | `(SUM(pending) / SUM(credited)) * 100` | `amount`, `status` | `Rewards` | Daily | Risk & Finance | Monitors buffer protecting against unverified claims | Spikes indicate review backlogs | Doesn't predict release probability | Proposed |
| **Total Wallet Txn Volume**| Gross ledger journal entries processed | `COUNT(transaction_id)` | `transaction_id`, `timestamp` | `Wallet` | Daily | Backend Infrastructure | Monitors database ledger throughput | Surges indicate activity or loop bugs | Doesn't measure monetary value | Proposed |
| **Circulating VE Supply** | Total unredeemed points held in user wallets | `SUM(amount) WHERE status = 'completed'` | `amount`, `unit`, `status` | `Wallet` | Daily | CFO / Finance | Measures current balance-sheet liability | Monitors run-on-the-bank liquidity risk | Includes dormant breakage balances | Proposed |
| **Redemption Velocity Ratio**| % points liquidated via payouts within 30 days | `(SUM(withdrawals) / SUM(rewards)) * 100` | `amount`, `transaction_type` | `Wallet` | Monthly | Finance / Strategy | Determines speed of cash drain | >80% signals high liquidity pressure | Constrained by minimum payout rules | Proposed |
| **Wallet Reversal Rate** | % completed transactions requiring reversal | `(COUNT(reversed) / COUNT(total_txns)) * 100` | `transaction_id`, `status` | `Wallet` | Weekly | Operations & Finance | Measures transactional integrity | High reversals indicate buggy payout rails | Doesn't measure elapsed reversal lag | Proposed |
| **Token Exchange Velocity**| Volume of VEs converted to on-chain Tokens | `SUM(amount WHERE type = 'token_exchange')` | `amount`, `type` | `Wallet` | Weekly | Web3 / Tokenomics | Measures adoption of secondary ecosystem tokens | Reduces immediate fiat bank cash drain | Dependent on secondary token utility | Proposed |
| **Withdrawal Request Volume**| Total cash-out submissions submitted | `COUNT(withdrawal_id)` | `withdrawal_id`, `requested_ts`| `Withdrawals` | Daily | Payment Ops / Finance | Monitors gross payout pipeline demand | Surges near month-end or promo campaigns | Includes requests that will fail review | Proposed |
| **Completed Withdrawal Rate**| % payout requests successfully disbursed | `(COUNT(completed) / COUNT(total_requests)) * 100`| `withdrawal_id`, `status` | `Withdrawals` | Weekly | Executive Leadership | Primary reliability and user trust metric | Target >90% for legitimate cohorts | Decreases legitimately during fraud attacks | Proposed |
| **Pending Withdrawal Queue**| Requests currently awaiting review / processing | `COUNT(withdrawal_id WHERE status IN (requested, processing))`| `withdrawal_id`, `status` | `Withdrawals` | Real-time | Payment Ops Lead | Backlog monitoring to prevent support tickets | Backlog indicates review under-staffing | Doesn't reflect dollar value of queue | Proposed |
| **Average Processing Duration**| Mean hours from request to settlement (SLA) | `AVG(final_ts - requested_ts) / 3600` | `requested_ts`, `final_ts`, `status`| `Withdrawals` | Daily | UX PM / Operations | Primary customer satisfaction turnaround metric| Faster payouts drive repeat engagement | Blends instant gift cards with slow wire | Proposed |
| **Withdrawal Rejection Rate**| % payout requests denied for fraud/KYC | `(COUNT(rejected) / COUNT(total_requests)) * 100`| `withdrawal_id`, `status` | `Withdrawals` | Weekly | Risk & Fraud Lead | Audits fraud detection effectiveness | Spikes indicate bot farm cash-out attempts | False positives harm good users | Proposed |
| **Gross Payout Volume** | Total fiat equivalent disbursed to users | `SUM(requested_amount WHERE status = 'completed')`| `requested_amount`, `status` | `Withdrawals` | Monthly | CFO / Finance | Monitors cash outflow against ad revenues | Must stay below net ad network revenues | Excludes payment rail fees | Proposed |
| **Payout Method Distribution**| % share of payouts per rail (PayPal, USDT, etc)| `(COUNT(method) / COUNT(total_completed)) * 100` | `withdrawal_method`, `status` | `Withdrawals` | Monthly | Payment Operations | Treasury cash allocation & fee optimization | Highlights regional user preferences | Constrained by country availability | Proposed |
| **Referral Invites Created**| Personal invite links generated by users | `COUNT(referral_id)` | `referral_id`, `creation_ts` | `Referrals` | Weekly | Growth PM | Measures viral advocate sharing intent | High sharing shows strong viral enthusiasm | Doesn't guarantee clicks or signups | Proposed |
| **Referral Signup Conv. Rate**| % invite links resulting in registered referee | `(COUNT(registered) / COUNT(created)) * 100` | `referral_id`, `status` | `Referrals` | Weekly | Growth Team | Measures landing page appeal & signup friction | Low rate suggests weak value proposition | Unattributed installs escape tracking | Proposed |
| **Referral Activation Rate** | % registered referees completing 1st task | `(COUNT(activated) / COUNT(registered)) * 100` | `referral_id`, `status` | `Referrals` | Weekly | Growth & Product PM | Distinguishes vanity signups from real users | High activation proves good referral quality | Vulnerable to self-referral rings | Proposed |
| **Viral Coefficient (K-Factor)**| New active referees per active user | `(Invites / Users) * (Activations / Invites)` | `referring_uid`, `referred_uid`, `status`| `Referrals`, `Users` | Monthly | Head of Growth | Measures viral compounding sustainability | K > 1.0 implies exponential organic growth | Requires long attribution tracking window | Proposed |
| **Support Tickets per 1k DAU**| Normalized support ticket volume per 1,000 DAU | `COUNT(ticket_id) / (DAU / 1000)` | `ticket_id`, `timestamp`, `DAU` | `Support Tickets`, `Events` | Weekly | Support Lead / Ops | Monitors operational support burden | Spikes indicate bugs or payout delays | Only captures users who bother to file | Proposed |
| **Support Issue Distribution**| % breakdown of inquiries by category | `(COUNT(category) / COUNT(tickets)) * 100` | `ticket_id`, `issue_category` | `Support Tickets` | Weekly | Product & Eng Leads | Prioritizes engineering bug fixes and FAQ | If payouts dominate, UI needs clarity | Subject to manual support agent tagging | Proposed |
| **Help FAQ Deflection Rate** | % article viewers who do not file a ticket in 24h | `(COUNT(views without ticket) / Total Views) * 100`| `user_id`, `timestamp` | `Feature_Events`, `Support` | Monthly | Content & Support | Evaluates self-serve documentation quality | High deflection indicates actionable guides | Frustrated dropouts misclassified as deflected | Proposed |

---
*Deliverable Document Reference: `docs/11_KPI_CATALOGUE.md` | Data File: `deliverables_tables/11_KPI_CATALOGUE.csv`.*
