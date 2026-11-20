# 08 — WORK PACKAGE F: PRODUCTION EVENT TRACKING PLAN

> **MANDATORY DATA AUTHENTICITY NOTICE**  
> *VELOOP is a real product under development, but the data supplied and evaluated for this assignment is fictional/simulated for analytical testing. In accordance with the Data Authenticity Policy, no metric or finding herein represents actual VELOOP production statistics, actual earnings, actual withdrawals, or live business performance.*

---

## 1. Executive Context & Standardization Standard
The **Production Event Tracking Plan (Work Package F)** is one of the most critical engineering deliverables of this blueprint. It establishes an unambiguous tracking contract between frontend developers, mobile engineers, backend architects, and data analysts.

### Event Naming Standard: `domain_object_action`
VELOOP strictly enforces the **`domain_object_action`** snake_case naming standard (e.g., `account_user_registered`, `task_ad_completed`, `withdrawal_payout_requested`).

#### Justification for `domain_object_action`:
1. **Namespace Partitioning**: Prefixing with the functional subsystem (`account_`, `task_`, `reward_`, `engagement_`, `gamification_`, `referral_`, `wallet_`, `withdrawal_`, `support_`) prevents naming collisions across decoupled microservices.
2. **Alphabetical Directory Grouping**: In data warehouses (BigQuery/Snowflake) and BI tools (Metabase/Looker), events naturally group into logical domain clusters, facilitating intuitive discovery for analysts.
3. **Deterministic Querying**: Engineers can query entire product areas using wildcard syntax (e.g., `WHERE event_name LIKE 'withdrawal_%'`).

---

## 2. Universal Base Telemetry Payload Contract
Every client and server event emitted across the ecosystem must include a standard envelope containing the following mandatory base attributes:

```json
{
  "event_id": "c4b182e0-2f9a-4e2b-bb68-54c3e804f3d1",
  "event_name": "task_ad_completed",
  "timestamp": "2026-07-15T14:32:10.450Z",
  "user_id": "USR_00142",
  "session_id": "SES_918234",
  "device_platform": "Android",
  "app_version": "v2.4.1",
  "properties": { ... }
}
```

---

## 3. Production Event Tracking Catalogue (30 Standardized Events)

The following catalogue contains the full 30 production-ready events, covering every requirement specified across Account, Tasks, Rewards, Daily/Engagement, Referrals, Wallet, and Withdrawals.

- **Primary Data File**: `deliverables_tables/08_EVENT_TRACKING_PLAN.csv`
- **Total Standardized Events**: 30 events
- **Coverage Domains**: 7 core operational domains

| Event Name | Trigger | Definition | User ID | Event ID | Timestamp | Feature | Status | Required Properties | Optional Properties | Data Type | Validation | Source | Business Purpose | KPI Dependency | Implementation Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `account_user_registered` | User submits signup credentials | Persisted profile in auth DB | `user_id` | `event_id` | `timestamp` | User Accounts | `success` | `user_id`, `reg_source`, `platform`, `country` | `campaign`, `referral_code` | JSON | Non-null `user_id` & `source` | Backend Auth API | Top-of-funnel acquisition tracking | New User Registrations, CAC | Proposed |
| `account_user_logged_in` | Valid auth token issued | Authenticated session initialized | `user_id` | `event_id` | `timestamp` | User Accounts | `success` | `user_id`, `session_id`, `platform`, `app_version` | `network_type`, `battery_level` | JSON | Valid `session_id` format | Client / Auth Proxy | Core active user measurement | DAU, WAU, MAU, Login Frequency | Proposed |
| `account_user_logged_out` | User logs out or token expires | Formal session termination | `user_id` | `event_id` | `timestamp` | User Accounts | `success` | `user_id`, `session_id`, `logout_reason` | `session_duration_seconds` | JSON | `reason IN (user, expired, revoke)` | Client SDK / Server | Session length & security audit | Average Session Duration | Proposed |
| `account_onboarding_started` | 1st walkthrough slide rendered | User enters tutorial | `user_id` | `event_id` | `timestamp` | Onboarding | `success` | `user_id`, `flow_version`, `platform` | `locale`, `screen_res` | JSON | Non-empty `flow_version` | Mobile Client SDK | Tutorial entrance tracking | Onboarding Start Rate | Proposed |
| `account_onboarding_completed`| Final slide dismissed | User finishes onboarding | `user_id` | `event_id` | `timestamp` | Onboarding | `success` | `user_id`, `flow_version`, `duration_seconds` | `skipped_steps_count` | JSON | `duration > 0 and <= 3600` | Mobile Client SDK | Tutorial effectiveness & activation | Onboarding Completion Rate | Proposed |
| `task_viewed` | Task card 50% visible for 1s | Impression event for earning task | `user_id` | `event_id` | `timestamp` | Tasks | `success` | `user_id`, `task_id`, `task_type`, `reward_amount` | `feed_position`, `provider` | JSON | `task_id` exists in catalog | Client Viewport SDK | Earning opportunity discovery | Task Impressions, CTR | Proposed |
| `task_opened` | Taps task card for details | User expresses task intent | `user_id` | `event_id` | `timestamp` | Tasks | `success` | `user_id`, `task_id`, `task_type` | `estimated_duration` | JSON | Non-null `task_id` | Client UI Interaction | Mid-funnel interest quantification | Task Open-to-Start Rate | Proposed |
| `task_started` | Clicks "Start Task" / Ad loaded| Task timer officially begins | `user_id` | `event_id` | `timestamp` | Tasks | `in_progress` | `user_id`, `task_activity_id`, `task_id`, `provider` | `offer_id`, `creative_id` | JSON | Unique `task_activity_id` | Client & Gateway | Earning activity initiation | Task Starts, Completion Rate | Proposed |
| `task_completed` | Task criteria met & verified | Formal completion verification | `user_id` | `event_id` | `timestamp` | Tasks | `completed` | `user_id`, `task_activity_id`, `task_type`, `amount` | `partner_tx_id`, `quality` | JSON | `amount > 0` & valid duration | Backend Validator | Earning fulfillment verification | Completed Tasks, Task Velocity | Proposed |
| `task_failed` | Task aborted, timed out, denied | Unsuccessful task termination | `user_id` | `event_id` | `timestamp` | Tasks | `failed` | `user_id`, `task_activity_id`, `failure_category` | `error_code`, `elapsed_sec` | JSON | `failure_category IN (5 enum values)`| Backend / Client SDK | Bug triage and obstacle discovery | Task Failure Rate | Proposed |
| `reward_credited` | Ledger credits positive balance | Balance incremented on ledger | `user_id` | `event_id` | `timestamp` | Rewards | `credited` | `user_id`, `reward_id`, `reward_type`, `amount`, `unit`| `task_activity_id`, `streak_id`| JSON | `amount > 0` & `status == posted` | Backend Ledger API | Primary points liability creation | Total Rewards Credited, ARPPU | Proposed |
| `reward_pending` | Large offer placed in escrow | Escrow hold for anti-fraud | `user_id` | `event_id` | `timestamp` | Rewards | `pending` | `user_id`, `reward_id`, `amount`, `release_at` | `task_activity_id`, `hold_reason`| JSON | `release_at > timestamp` | Escrow Daemon | High-value fraud mitigation | Pending Escrow Ratio | Proposed |
| `reward_reversed` | Partner revokes commission | Debits previously credited reward | `user_id` | `event_id` | `timestamp` | Rewards | `reversed` | `user_id`, `reward_id`, `original_reward_id`, `amount` | `chargeback_id`, `reason` | JSON | `original_reward_id` in Rewards | Backend Ledger API | Protects margin from chargebacks | Reward Reversal Rate | Proposed |
| `engagement_daily_reward_claimed`| Taps claim on check-in card | Credits daily check-in bonus | `user_id` | `event_id` | `timestamp` | Daily Streaks | `success` | `user_id`, `streak_day`, `reward_amount`, `unit` | `is_multiplier_active` | JSON | `streak_day BETWEEN 1 AND 365` | Backend Rewards Engine | Habit formation & retention metric | Daily Claim Rate, D7 Retention | Proposed |
| `engagement_streak_updated` | Streak evaluation worker runs | Logs streak state transition | `user_id` | `event_id` | `timestamp` | Daily Streaks | `success` | `user_id`, `previous_streak`, `new_streak`, `action` | `freeze_tokens_left` | JSON | `action IN (increment, reset, freeze)`| Streak Worker Daemon | Streak breakage & churn analysis | Streak Break Rate | Proposed |
| `gamification_spin_started` | User initiates lucky wheel spin | Wheel animation begins | `user_id` | `event_id` | `timestamp` | Spin Wheel | `in_progress` | `user_id`, `spin_id`, `spin_cost_type` | `token_cost_amount` | JSON | `cost_type IN (free, paid, ad)` | Client Game Engine | Gamification funnel entry | Spin Participation Rate | Proposed |
| `gamification_spin_completed` | Wheel lands on prize segment | Records prize and issues reward | `user_id` | `event_id` | `timestamp` | Spin Wheel | `completed` | `user_id`, `spin_id`, `prize_tier`, `prize_amount` | `jackpot_flag` | JSON | `prize_amount >= 0` | Backend RNG Service | Audits RNG prize distribution | Minigame Payout Volume | Proposed |
| `gamification_mission_started` | User accepts composite quest | Quest criteria tracking begins | `user_id` | `event_id` | `timestamp` | Missions | `in_progress` | `user_id`, `mission_id`, `type`, `target_count` | `expiration_timestamp` | JSON | Non-null `mission_id` | Missions Engine | Goal-directed engagement funnel | Mission Adoption Rate | Proposed |
| `gamification_mission_completed`| All quest criteria satisfied | Unlocks quest chest bonus | `user_id` | `event_id` | `timestamp` | Missions | `completed` | `user_id`, `mission_id`, `duration_hours`, `bonus` | `chest_tier` | JSON | `bonus >= 0` | Missions Engine | Evaluates quest completion difficulty | Mission Completion Rate | Proposed |
| `gamification_badge_earned` | User reaches achievement threshold| Awards collectible profile badge | `user_id` | `event_id` | `timestamp` | Badges | `success` | `user_id`, `badge_id`, `badge_category`, `xp_granted` | `rarity_tier` | JSON | `badge_id` in Badge Catalog | Achievement Service | Long-term user progression | Badges Unlocked per Active User | Proposed |
| `referral_link_created` | User taps share invite button | Encodes unique deep-link token | `user_id` | `event_id` | `timestamp` | Referrals | `success` | `referral_id`, `referring_user_id`, `channel` | `campaign_tag` | JSON | Valid `channel` enum | Client SDK | Measures viral sharing intent | Invites Generated, K-Factor | Proposed |
| `referral_referee_registered` | Referee completes account signup | Binds referee to referrer | `user_id` | `event_id` | `timestamp` | Referrals | `registered` | `referral_id`, `referring_user_id`, `referred_user_id` | `attribution_delay_hours` | JSON | `referring_uid != referred_uid` | Auth / Referral Service | Downstream viral signup conversion | Referral Registration Rate | Proposed |
| `referral_referee_activated` | Referee completes 1st valid task | Proves referee is genuine user | `user_id` | `event_id` | `timestamp` | Referrals | `activated` | `referral_id`, `referring_uid`, `referred_uid`, `task_id`| `time_to_activate_hours`| JSON | `task_id.status == validated` | Referral Attribution | Filters bot accounts from real users | Referral Activation Rate | Proposed |
| `referral_bonus_converted` | Anti-fraud passes; bounty paid | Releases referral bonus to inviter| `user_id` | `event_id` | `timestamp` | Referrals | `converted` | `referral_id`, `referring_uid`, `referred_uid`, `bonus` | `referrer_reward_id` | JSON | `bonus > 0` | Referral Attribution | Evaluates paid viral marketing ROI | Referral Conversion Rate, CAC | Proposed |
| `wallet_transaction_created` | Any ledger journal initiated | Double-entry journal opened | `user_id` | `event_id` | `timestamp` | Wallet | `pending` | `user_id`, `transaction_id`, `type`, `amount`, `unit` | `reference_id` | JSON | Valid `transaction_type` enum | Core Ledger API | Double-entry audit & balance locks | Gross Transaction Volume | Proposed |
| `wallet_transaction_completed`| Journal transaction committed | Updates available balance | `user_id` | `event_id` | `timestamp` | Wallet | `completed` | `user_id`, `transaction_id`, `balance_snapshot` | `cleared_timestamp` | JSON | `balance_snapshot >= 0` | Core Ledger API | Financial balance snapshot audit | Circulating Supply, Liquidity | Proposed |
| `wallet_transaction_reversed` | Entry cancelled / rolled back | Offsetting entry restores balance | `user_id` | `event_id` | `timestamp` | Wallet | `reversed` | `user_id`, `transaction_id`, `reversal_rel_id`, `reason`| `operator_id` | JSON | Valid `reversal_rel_id` pointer | Core Ledger API | Dispute resolution & fraud audit | Wallet Reversal Rate | Proposed |
| `withdrawal_requested` | User submits cash-out form | Locks funds in escrow | `user_id` | `event_id` | `timestamp` | Withdrawals | `requested` | `withdrawal_id`, `user_id`, `amount`, `method`, `fee` | `destination_account_hash` | JSON | `amount >= min_payout` | Withdrawal Engine | Payout demand pipeline monitoring | Withdrawal Request Volume | Proposed |
| `withdrawal_processing` | Passes fraud check; sent to rail| Dispatched to external gateway | `user_id` | `event_id` | `timestamp` | Withdrawals | `processing` | `withdrawal_id`, `user_id`, `provider_batch_id` | `estimated_clearing_hours` | JSON | Non-null `batch_id` | Gateway Connector | Payment rail processing SLA monitoring | Pending Withdrawal Queue Size | Proposed |
| `withdrawal_completed` | Payout provider confirms settlement| Funds confirmed in user account | `user_id` | `event_id` | `timestamp` | Withdrawals | `completed` | `withdrawal_id`, `user_id`, `amount`, `tx_hash`, `duration`| `fiat_amount` | JSON | `tx_hash length >= 8` | Gateway Webhook | Core redemption fulfillment success | Completed Withdrawal Rate, TAT | Proposed |
| `withdrawal_rejected` | Compliance declines payout | Releases escrow back to user | `user_id` | `event_id` | `timestamp` | Withdrawals | `rejected` | `withdrawal_id`, `user_id`, `rejection_reason_category` | `reviewer_notes` | JSON | Valid `reason_category` enum | Risk Engine / Admin | Risk audit & obstacle discovery | Withdrawal Rejection Rate | Proposed |

---

## 4. Implementation Guidelines for Engineering
1. **Never Buffer Unsent Financial Events Across Sessions**: Financial ledger events (`wallet_`, `withdrawal_`) must be dispatched synchronously with immediate network acknowledgment.
2. **Batch High-Frequency Engagement Events**: Micro-telemetry (`task_tap_completed`, scroll impressions) should be batched on the client device in 10-second intervals or 20-event buffers before transmission.
3. **Dead-Letter Handling**: Any telemetry payload failing JSON schema validation at the API gateway must be written to a dedicated dead-letter queue (DLQ) with error headers for rapid developer inspection.

---
*Deliverable Document Reference: `docs/08_EVENT_TRACKING_PLAN.md` | Data File: `deliverables_tables/08_EVENT_TRACKING_PLAN.csv`.*
