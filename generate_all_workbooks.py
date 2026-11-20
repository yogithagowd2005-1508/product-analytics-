"""
VELOOP REWARDS - MASTER WORKBOOK & SPECIFICATION GENERATOR
==========================================================
Generates all structured tabular deliverables for Task 01:
- Deliverable 03: Data Coverage Matrix
- Deliverable 04: User Analytics Specification
- Deliverable 08: Event Tracking Plan (30 events, 16 attributes)
- Deliverable 09: Data Dictionary (85+ fields, 12 attributes)
- Deliverable 11: KPI Catalogue (35 KPIs, 11 attributes)
- Deliverable 19: Assumption & Verification Register
- Deliverable 20: Implementation Backlog
- Master Excel Workbook: VELOOP_Analytics_Foundation_Master_Workbook.xlsx
"""

import os
import pandas as pd

def generate_specifications():
    out_dir = 'deliverables_tables'
    os.makedirs(out_dir, exist_ok=True)

    # =========================================================================
    # DELIVERABLE 03: DATA COVERAGE MATRIX
    # =========================================================================
    print("Generating Deliverable 03: Data Coverage Matrix...")
    coverage_rows = [
        {
            'Product Area': 'User Accounts',
            'Feature': 'Registration',
            'User Action': 'Submits signup form or social auth',
            'System Action': 'Creates user row, generates user_id, sets initial wallet balance',
            'Business Outcome': 'New user registered; acquisition channel credited',
            'Data Required': 'user_id, registration_timestamp, registration_source, acquisition_campaign, device_platform, country_code',
            'Proposed Event': 'account_user_registered',
            'Source': 'Auth Service / Backend',
            'Business Question': 'Which acquisition channels and campaigns drive the highest initial signups?',
            'Status': 'Proposed',
            'Priority': 'Critical'
        },
        {
            'Product Area': 'User Accounts',
            'Feature': 'Login',
            'User Action': 'Authenticates into application',
            'System Action': 'Validates credentials, creates session token, updates last_login_timestamp',
            'Business Outcome': 'Active session initiated; user authenticated',
            'Data Required': 'user_id, session_id, login_timestamp, device_platform, app_version',
            'Proposed Event': 'account_user_logged_in',
            'Source': 'Auth Service / Client SDK',
            'Business Question': 'What is the frequency of daily/weekly logins per user cohort?',
            'Status': 'Proposed',
            'Priority': 'Critical'
        },
        {
            'Product Area': 'User Accounts',
            'Feature': 'Onboarding Flow',
            'User Action': 'Views and completes introduction walkthrough screens',
            'System Action': 'Records step progress, sets is_onboarding_completed flag',
            'Business Outcome': 'User activation readiness; drop-off reduction',
            'Data Required': 'user_id, step_name, step_number, time_spent_seconds, is_completed',
            'Proposed Event': 'account_onboarding_completed',
            'Source': 'Mobile Client SDK',
            'Business Question': 'Where in the onboarding funnel do users abandon the app before their first task?',
            'Status': 'Proposed',
            'Priority': 'High'
        },
        {
            'Product Area': 'Earning Activities',
            'Feature': 'Watch Ads',
            'User Action': 'Clicks "Watch Video Ad" and watches until completion',
            'System Action': 'Requests ad from partner SDK, validates view postback, credits reward',
            'Business Outcome': 'Ad impression monetized; user earns micro-reward',
            'Data Required': 'user_id, task_activity_id, partner_provider, ad_unit_id, duration_seconds, reward_amount',
            'Proposed Event': 'task_ad_completed',
            'Source': 'Ad Partner SDK / Backend Postback',
            'Business Question': 'What is the video completion rate and ad yield per active user?',
            'Status': 'Proposed',
            'Priority': 'Critical'
        },
        {
            'Product Area': 'Earning Activities',
            'Feature': 'Surveys',
            'User Action': 'Selects survey from wall, answers qualification screening and questions',
            'System Action': 'Redirects to provider, awaits server-to-server webhook callback, issues reward',
            'Business Outcome': 'High-yield research survey fulfilled; partner payment earned',
            'Data Required': 'user_id, task_activity_id, provider_id, survey_length_minutes, reward_amount, validation_status',
            'Proposed Event': 'task_survey_completed',
            'Source': 'Survey Partner Webhook',
            'Business Question': 'What percentage of survey attempts suffer disqualification or screening dropout?',
            'Status': 'Proposed',
            'Priority': 'High'
        },
        {
            'Product Area': 'Earning Activities',
            'Feature': 'Tap & Earn',
            'User Action': 'Taps interactive screen element to consume energy and harvest micro-rewards',
            'System Action': 'Decrements energy counter, tracks tap cadence, batches reward credits',
            'Business Outcome': 'Micro-session engagement; time-in-app increase',
            'Data Required': 'user_id, session_id, taps_count, energy_consumed, batch_reward_amount',
            'Proposed Event': 'task_tap_completed',
            'Source': 'Client SDK / Game Engine',
            'Business Question': 'Does tap activity drive sustained retention or rapid churn after energy exhaustion?',
            'Status': 'Proposed',
            'Priority': 'Medium'
        },
        {
            'Product Area': 'Earning Activities',
            'Feature': 'Mining / Cloud Claim',
            'User Action': 'Activates 6-hour mining cycle and claims accumulated yield',
            'System Action': 'Initializes server timer, computes hash rate, credits balance upon claim',
            'Business Outcome': 'Scheduled return habit formed; re-engagement prompt trigger',
            'Data Required': 'user_id, cycle_id, activation_timestamp, claim_timestamp, yield_amount',
            'Proposed Event': 'task_mining_claimed',
            'Source': 'Backend Mining Daemon',
            'Business Question': 'How many users claim within 1 hour of mining cycle completion?',
            'Status': 'Proposed',
            'Priority': 'High'
        },
        {
            'Product Area': 'Daily Rewards & Streaks',
            'Feature': 'Daily Check-in',
            'User Action': 'Opens calendar modal and taps "Claim Day N"',
            'System Action': 'Verifies calendar eligibility (24h window), increments streak counter, issues bonus',
            'Business Outcome': 'Daily Active User (DAU) habit reinforcement',
            'Data Required': 'user_id, streak_day_number, reward_amount, streak_freeze_used',
            'Proposed Event': 'engagement_daily_reward_claimed',
            'Source': 'Backend Rewards Engine',
            'Business Question': 'What is the drop-off rate between Day 3 and Day 7 streak thresholds?',
            'Status': 'Proposed',
            'Priority': 'Critical'
        },
        {
            'Product Area': 'Daily Rewards & Streaks',
            'Feature': 'Streak Protection / Freeze',
            'User Action': 'Consumes Gems or watches ad to save broken streak',
            'System Action': 'Restores previous streak index, records freeze consumption',
            'Business Outcome': 'Churn prevention for lapsed habitual users',
            'Data Required': 'user_id, current_streak, cost_currency, cost_amount, restored_timestamp',
            'Proposed Event': 'engagement_streak_restored',
            'Source': 'Backend Rewards Engine',
            'Business Question': 'Does streak restoration preserve 30-day retention compared to unpreserved breaks?',
            'Status': 'Proposed',
            'Priority': 'Medium'
        },
        {
            'Product Area': 'Gamification',
            'Feature': 'Spin Wheel',
            'User Action': 'Spins lucky prize wheel using daily free ticket or tokens',
            'System Action': 'Executes server-side RNG, determines prize tier, writes reward record',
            'Business Outcome': 'Variable reward dopamine loop; daily session incentive',
            'Data Required': 'user_id, spin_id, ticket_type, prize_tier, prize_amount, prize_unit',
            'Proposed Event': 'gamification_spin_completed',
            'Source': 'Backend RNG Service',
            'Business Question': 'Are spin wheel rewards cannibalizing or amplifying task participation?',
            'Status': 'Proposed',
            'Priority': 'High'
        },
        {
            'Product Area': 'Gamification',
            'Feature': 'Missions & Quests',
            'User Action': 'Completes composite objective (e.g. "Watch 3 Ads + Do 1 Survey")',
            'System Action': 'Tracks composite progression, marks mission complete, unlocks quest chest',
            'Business Outcome': 'Cross-feature exploration and diversified feature usage',
            'Data Required': 'user_id, mission_id, criteria_tags, completed_timestamp, bonus_amount',
            'Proposed Event': 'gamification_mission_completed',
            'Source': 'Mission Evaluation Engine',
            'Business Question': 'Which mission combinations achieve the highest completion velocity?',
            'Status': 'Proposed',
            'Priority': 'High'
        },
        {
            'Product Area': 'Gamification',
            'Feature': 'Badges & Levels (XP)',
            'User Action': 'Reaches lifetime XP threshold through cumulative platform activity',
            'System Action': 'Promotes user level tier, grants profile badge, boosts earning multiplier',
            'Business Outcome': 'Long-term user progression and status investment',
            'Data Required': 'user_id, previous_level, new_level, total_xp_accumulated, earning_boost_pct',
            'Proposed Event': 'gamification_level_up',
            'Source': 'Player Profile Engine',
            'Business Question': 'Does leveling up correlate with higher lifetime withdrawal retention?',
            'Status': 'Proposed',
            'Priority': 'Medium'
        },
        {
            'Product Area': 'Referrals',
            'Feature': 'Invite Creation',
            'User Action': 'Generates and copies personal referral link/code to share via social apps',
            'System Action': 'Creates referral tracking record with unique tracking token',
            'Business Outcome': 'Viral loop initiation; organic acquisition pipeline',
            'Data Required': 'referral_id, referring_user_id, invite_channel, share_timestamp',
            'Proposed Event': 'referral_link_generated',
            'Source': 'Mobile Client / Deep-Link Router',
            'Business Question': 'Which sharing channels (WhatsApp vs Twitter vs Telegram) generate the highest click-throughs?',
            'Status': 'Proposed',
            'Priority': 'High'
        },
        {
            'Product Area': 'Referrals',
            'Feature': 'Referee Activation',
            'User Action': 'New referee completes their first qualified earning task',
            'System Action': 'Validates fraud checks, flags referral as converted, schedules referrer bonus',
            'Business Outcome': 'Verified high-intent user acquired; viral conversion achieved',
            'Data Required': 'referral_id, referring_user_id, referred_user_id, qualifying_task_id, bonus_amount',
            'Proposed Event': 'referral_converted',
            'Source': 'Referral Attribution Engine',
            'Business Question': 'What is the average time lag between referee registration and referral activation?',
            'Status': 'Proposed',
            'Priority': 'Critical'
        },
        {
            'Product Area': 'Wallet & Economics',
            'Feature': 'Token Exchange / Conversion',
            'User Action': 'Converts earned VEs into cash-out Tokens or Gems',
            'System Action': 'Applies exchange peg rate, validates minimum balance, executes atomic double-entry debit/credit',
            'Business Outcome': 'Currency conversion for withdrawal eligibility',
            'Data Required': 'user_id, transaction_id, source_unit, source_amount, target_unit, target_amount, exchange_rate',
            'Proposed Event': 'wallet_currency_exchanged',
            'Source': 'Core Ledger Service',
            'Business Question': 'What proportion of earned VEs are converted into Tokens versus retained in wallet?',
            'Status': 'Proposed',
            'Priority': 'Critical'
        },
        {
            'Product Area': 'Withdrawals',
            'Feature': 'Withdrawal Request',
            'User Action': 'Selects payout method, enters payment address/account, submits cash-out request',
            'System Action': 'Locks requested funds in escrow, verifies KYC tier, puts request in review queue',
            'Business Outcome': 'Payout pipeline initiated; platform utility realization',
            'Data Required': 'withdrawal_id, user_id, requested_amount, payout_method, destination_hash, fee_amount',
            'Proposed Event': 'withdrawal_requested',
            'Source': 'Withdrawal Engine / Core Ledger',
            'Business Question': 'What is the distribution of requested cash-out amounts across payment rails?',
            'Status': 'Proposed',
            'Priority': 'Critical'
        },
        {
            'Product Area': 'Withdrawals',
            'Feature': 'Under Review / AML Check',
            'User Action': 'None (System automated or Ops review)',
            'System Action': 'Runs anti-fraud heuristics, checks IP/device duplication, approves or flags',
            'Business Outcome': 'Risk mitigation; fraudulent drain prevention',
            'Data Required': 'withdrawal_id, user_id, risk_score, automated_decision, reviewer_id',
            'Proposed Event': 'withdrawal_review_processed',
            'Source': 'Risk Engine / Backoffice Admin',
            'Business Question': 'What percentage of withdrawal requests require manual fraud investigation?',
            'Status': 'Proposed',
            'Priority': 'Critical'
        },
        {
            'Product Area': 'Withdrawals',
            'Feature': 'Disbursement / Settlement',
            'User Action': 'Receives cash/gift card in external destination account',
            'System Action': 'Executes payment provider API transfer, receives settlement confirmation, permanently debits wallet escrow',
            'Business Outcome': 'Successful monetary reward fulfillment; high trust milestone',
            'Data Required': 'withdrawal_id, user_id, provider_tx_hash, settled_amount, processing_duration_seconds',
            'Proposed Event': 'withdrawal_completed',
            'Source': 'Payment Gateway Webhook',
            'Business Question': 'What is the end-to-end SLA duration from withdrawal request to settlement?',
            'Status': 'Proposed',
            'Priority': 'Critical'
        },
        {
            'Product Area': 'Withdrawals',
            'Feature': 'Withdrawal Rejection / Cancellation',
            'User Action': 'Receives notice of declined cash-out',
            'System Action': 'Releases locked escrow funds back to user wallet, records rejection category',
            'Business Outcome': 'Escrow restored; fraud blocked or user alerted to correct credentials',
            'Data Required': 'withdrawal_id, user_id, rejection_reason_category, restored_amount, refund_transaction_id',
            'Proposed Event': 'withdrawal_rejected',
            'Source': 'Withdrawal Engine',
            'Business Question': 'What are the top drivers of withdrawal rejection (KYC vs Threshold vs Fraud)?',
            'Status': 'Proposed',
            'Priority': 'Critical'
        },
        {
            'Product Area': 'Support & Content',
            'Feature': 'Help Center Navigation',
            'User Action': 'Searches FAQ or opens troubleshooting guide',
            'System Action': 'Logs article impression and search query string',
            'Business Outcome': 'Self-serve problem resolution; support deflection',
            'Data Required': 'user_id, article_id, category_name, search_query, was_helpful_vote',
            'Proposed Event': 'support_article_viewed',
            'Source': 'Help Desk SDK',
            'Business Question': 'Which features generate the highest friction/confusion inquiries?',
            'Status': 'Proposed',
            'Priority': 'Medium'
        }
    ]
    df_coverage = pd.DataFrame(coverage_rows)
    df_coverage.to_csv(os.path.join(out_dir, '03_DATA_COVERAGE_MATRIX.csv'), index=False)

    # =========================================================================
    # DELIVERABLE 04: USER ANALYTICS SPECIFICATION
    # =========================================================================
    print("Generating Deliverable 04: User Analytics Specification...")
    user_spec_rows = [
        {'Field': 'user_id', 'Type': 'String (UUID / USR_XXXXX)', 'Required?': 'Yes', 'Purpose': 'Permanent unique surrogate identifier for user entity', 'Source': 'Auth Service', 'Validation': '^USR_[0-9]{5}$ or RFC 4122 UUID', 'Status': 'Confirmed'},
        {'Field': 'registration_timestamp', 'Type': 'Timestamp (ISO 8601 UTC)', 'Required?': 'Yes', 'Purpose': 'Cohort definition, tenure calculation, maturity analysis', 'Source': 'Auth Service DB', 'Validation': 'Valid UTC timestamp <= CURRENT_TIMESTAMP', 'Status': 'Confirmed'},
        {'Field': 'registration_source', 'Type': 'String (Enum)', 'Required?': 'Yes', 'Purpose': 'Acquisition channel performance and CAC attribution', 'Source': 'Client DeepLink / Attribution SDK', 'Validation': 'IN (organic, referral, paid_ad, partner_promo, influencer)', 'Status': 'Proposed'},
        {'Field': 'acquisition_campaign', 'Type': 'String', 'Required?': 'No', 'Purpose': 'Campaign-specific ROI and CPA evaluation', 'Source': 'Branch / AppsFlyer attribution token', 'Validation': 'MaxLength 100, sanitized alphanumeric', 'Status': 'Proposed'},
        {'Field': 'device_platform', 'Type': 'String (Enum)', 'Required?': 'Yes', 'Purpose': 'Cross-platform UX segmentation and telemetry routing', 'Source': 'Client OS Telemetry', 'Validation': 'IN (Android, iOS, Web)', 'Status': 'Confirmed'},
        {'Field': 'device_os_version', 'Type': 'String', 'Required?': 'Yes', 'Purpose': 'Bug triage, SDK deprecation tracking', 'Source': 'Client OS Telemetry', 'Validation': 'Semantic version pattern (e.g. 14.2.1)', 'Status': 'Proposed'},
        {'Field': 'app_version', 'Type': 'String', 'Required?': 'Yes', 'Purpose': 'Release tracking, feature rollout cohorting', 'Source': 'App Manifest / Build Info', 'Validation': 'SemVer string (e.g. v2.4.1)', 'Status': 'Proposed'},
        {'Field': 'country_code', 'Type': 'String (ISO 3166-1 alpha-2)', 'Required?': 'Yes', 'Purpose': 'Geographic market segmentation, ad monetization tiers', 'Source': 'Client IP Geolocation / Device Locale', 'Validation': 'Length 2, uppercase alpha', 'Status': 'Confirmed'},
        {'Field': 'account_status', 'Type': 'String (Enum)', 'Required?': 'Yes', 'Purpose': 'User lifecycle state tracking, active cohort filtering', 'Source': 'User Profile Service', 'Validation': 'IN (active, dormant, suspended, closed)', 'Status': 'Confirmed'},
        {'Field': 'is_onboarding_completed', 'Type': 'Boolean', 'Required?': 'Yes', 'Purpose': 'Activation milestone tracking', 'Source': 'Onboarding Service', 'Validation': 'Boolean (TRUE/FALSE)', 'Status': 'Confirmed'},
        {'Field': 'onboarding_completed_timestamp', 'Type': 'Timestamp (ISO 8601 UTC)', 'Required?': 'No', 'Purpose': 'Time-to-activation duration measurement', 'Source': 'Onboarding Service', 'Validation': 'Valid UTC timestamp >= registration_timestamp', 'Status': 'Proposed'},
        {'Field': 'last_login_timestamp', 'Type': 'Timestamp (ISO 8601 UTC)', 'Required?': 'Yes', 'Purpose': 'Recency scoring, dormancy classification (7d/30d)', 'Source': 'Auth Session Manager', 'Validation': 'Valid UTC timestamp >= registration_timestamp', 'Status': 'Confirmed'},
        {'Field': 'current_streak_count', 'Type': 'Integer', 'Required?': 'Yes', 'Purpose': 'Daily engagement habit tracking', 'Source': 'Streak Service', 'Validation': 'Integer >= 0', 'Status': 'Proposed'},
        {'Field': 'lifetime_xp', 'Type': 'Integer', 'Required?': 'Yes', 'Purpose': 'Gamification progression and level tiering', 'Source': 'Gamification Service', 'Validation': 'Integer >= 0', 'Status': 'Proposed'},
        {'Field': 'kyc_status', 'Type': 'String (Enum)', 'Required?': 'Yes', 'Purpose': 'Withdrawal eligibility compliance tracking', 'Source': 'Compliance Service', 'Validation': 'IN (none, pending, verified, rejected)', 'Status': 'Proposed'}
    ]
    df_user_spec = pd.DataFrame(user_spec_rows)
    df_user_spec.to_csv(os.path.join(out_dir, '04_USER_ANALYTICS_SPEC.csv'), index=False)

    # =========================================================================
    # DELIVERABLE 08: EVENT TRACKING PLAN (30 PRODUCTION EVENTS)
    # =========================================================================
    print("Generating Deliverable 08: Event Tracking Plan (30 events)...")
    event_plan_rows = [
        # Account Domain
        {
            'Event Name': 'account_user_registered',
            'Trigger': 'User successfully submits signup credentials or OAuth handshake',
            'Definition': 'Triggered once when new user profile row is persisted in authentication database',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'User Accounts',
            'Status': 'success',
            'Required Properties': 'user_id, registration_source, device_platform, country_code',
            'Optional Properties': 'acquisition_campaign, referral_code, invite_token',
            'Data Type': 'JSON Object',
            'Validation': 'Must contain valid user_id and non-null registration_source',
            'Source': 'Backend Auth API',
            'Business Purpose': 'Baseline acquisition metric; denominator for onboarding funnel',
            'KPI Dependency': 'New User Registrations, CAC by Channel',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'account_user_logged_in',
            'Trigger': 'User opens app and valid auth token is issued or refreshed',
            'Definition': 'Emitted whenever an authenticated session is initialized',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'User Accounts',
            'Status': 'success',
            'Required Properties': 'user_id, session_id, device_platform, app_version',
            'Optional Properties': 'network_type, battery_level',
            'Data Type': 'JSON Object',
            'Validation': 'session_id must match active session token regex',
            'Source': 'Client SDK / Auth Proxy',
            'Business Purpose': 'Core active user measurement and session attribution',
            'KPI Dependency': 'DAU, WAU, MAU, Login Frequency',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'account_user_logged_out',
            'Trigger': 'User explicitly taps Log Out or session token expires/revoked',
            'Definition': 'Records explicit or forced termination of user session',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'User Accounts',
            'Status': 'success',
            'Required Properties': 'user_id, session_id, logout_reason',
            'Optional Properties': 'session_duration_seconds',
            'Data Type': 'JSON Object',
            'Validation': 'logout_reason IN (user_initiated, token_expired, security_revoke)',
            'Source': 'Client SDK / Auth Server',
            'Business Purpose': 'Session length calculation and security auditing',
            'KPI Dependency': 'Average Session Duration',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'account_onboarding_started',
            'Trigger': 'First screen of walkthrough rendered on newly installed device',
            'Definition': 'Marks entrance of user into onboarding tutorial',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Onboarding',
            'Status': 'success',
            'Required Properties': 'user_id, flow_version, device_platform',
            'Optional Properties': 'locale, screen_resolution',
            'Data Type': 'JSON Object',
            'Validation': 'flow_version string not empty',
            'Source': 'Mobile Client SDK',
            'Business Purpose': 'Top of onboarding funnel tracking',
            'KPI Dependency': 'Onboarding Start Rate',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'account_onboarding_completed',
            'Trigger': 'Final slide dismissed or initial profile setup saved',
            'Definition': 'Indicates user has completed all onboarding tutorial requirements',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Onboarding',
            'Status': 'success',
            'Required Properties': 'user_id, flow_version, duration_seconds',
            'Optional Properties': 'skipped_steps_count',
            'Data Type': 'JSON Object',
            'Validation': 'duration_seconds > 0 and <= 3600',
            'Source': 'Mobile Client SDK',
            'Business Purpose': 'Evaluates tutorial UX effectiveness and activation readiness',
            'KPI Dependency': 'Onboarding Completion Rate, Time to Activate',
            'Implementation Status': 'Proposed'
        },
        # Tasks Domain
        {
            'Event Name': 'task_viewed',
            'Trigger': 'Task card or earning feed item becomes visible in viewport (50% area, 1s)',
            'Definition': 'Impression event for earning task opportunity',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Tasks / Earning',
            'Status': 'success',
            'Required Properties': 'user_id, task_id, task_type, reward_amount, reward_unit',
            'Optional Properties': 'feed_position, provider_name',
            'Data Type': 'JSON Object',
            'Validation': 'task_id must exist in active task catalog',
            'Source': 'Client UI Viewport Observer',
            'Business Purpose': 'Task discovery and catalog impression measurement',
            'KPI Dependency': 'Task Impression Volume, Task Click-Through Rate (CTR)',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'task_opened',
            'Trigger': 'User taps on task card to view full instructions or launch modal',
            'Definition': 'User expresses intent to investigate task requirements',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Tasks / Earning',
            'Status': 'success',
            'Required Properties': 'user_id, task_id, task_type',
            'Optional Properties': 'estimated_duration_minutes',
            'Data Type': 'JSON Object',
            'Validation': 'task_id not null',
            'Source': 'Client UI Interaction',
            'Business Purpose': 'Mid-funnel interest quantification',
            'KPI Dependency': 'Task Open-to-Start Conversion Rate',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'task_started',
            'Trigger': 'User clicks "Start Task" / video ad request dispatched',
            'Definition': 'Execution of task officially initiated; timer starts',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Tasks / Earning',
            'Status': 'in_progress',
            'Required Properties': 'user_id, task_activity_id, task_id, task_type, partner_provider',
            'Optional Properties': 'offer_id, creative_id',
            'Data Type': 'JSON Object',
            'Validation': 'task_activity_id unique UUID/ID',
            'Source': 'Client SDK & Backend Gateway',
            'Business Purpose': 'Earning activity funnel milestone; start volume metric',
            'KPI Dependency': 'Task Starts, Task Completion Rate',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'task_completed',
            'Trigger': 'User finishes task criteria and partner postback/internal validation passes',
            'Definition': 'Formal completion and verification of task objective',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Tasks / Earning',
            'Status': 'completed',
            'Required Properties': 'user_id, task_activity_id, task_id, task_type, reward_amount, reward_unit, duration_seconds',
            'Optional Properties': 'partner_transaction_id, quality_score',
            'Data Type': 'JSON Object',
            'Validation': 'reward_amount > 0 and duration_seconds >= min_task_threshold',
            'Source': 'Backend Validation Engine',
            'Business Purpose': 'Successful earning fulfillment; input for reward crediting',
            'KPI Dependency': 'Completed Tasks, Task Completion Rate, Task Velocity',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'task_failed',
            'Trigger': 'Task aborted by user, failed verification, or timed out by provider',
            'Definition': 'Unsuccessful termination of an initiated task activity',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Tasks / Earning',
            'Status': 'failed',
            'Required Properties': 'user_id, task_activity_id, task_id, failure_category',
            'Optional Properties': 'partner_error_code, elapsed_seconds',
            'Data Type': 'JSON Object',
            'Validation': 'failure_category IN (task_failed, tracking_failed, validation_failed, user_abandoned, system_error)',
            'Source': 'Backend Validator / Client SDK',
            'Business Purpose': 'Identify broken ad units, scam offerwalls, or UX obstacles',
            'KPI Dependency': 'Task Failure Rate, Abandonment Rate',
            'Implementation Status': 'Proposed'
        },
        # Rewards Domain
        {
            'Event Name': 'reward_credited',
            'Trigger': 'Rewards engine successfully writes positive credit to ledger',
            'Definition': 'Points/VEs/XP balance is incremented on behalf of the user',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Rewards Engine',
            'Status': 'credited',
            'Required Properties': 'user_id, reward_id, reward_type, amount, reward_unit, ledger_status',
            'Optional Properties': 'task_activity_id, streak_reference_id',
            'Data Type': 'JSON Object',
            'Validation': 'amount > 0 and ledger_status == "posted"',
            'Source': 'Backend Ledger Service',
            'Business Purpose': 'Core liability creation event; tracks user monetary earnings',
            'KPI Dependency': 'Total Rewards Credited, Gross VE Influx, ARPPU',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'reward_pending',
            'Trigger': 'Reward generated by high-value offer placed in anti-fraud holding escrow',
            'Definition': 'Balance marked as provisional pending hold maturity (e.g. 72h)',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Rewards Engine',
            'Status': 'pending',
            'Required Properties': 'user_id, reward_id, amount, reward_unit, release_scheduled_at',
            'Optional Properties': 'task_activity_id, risk_hold_reason',
            'Data Type': 'JSON Object',
            'Validation': 'release_scheduled_at > timestamp',
            'Source': 'Risk Escrow Daemon',
            'Business Purpose': 'Fraud prevention on chargeback-prone affiliate offers',
            'KPI Dependency': 'Pending Reward Liability, Escrow Ratio',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'reward_reversed',
            'Trigger': 'Affiliate partner revokes commission or chargeback fraud detected',
            'Definition': 'Previously credited reward is debited/voided with audit trail',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Rewards Engine',
            'Status': 'reversed',
            'Required Properties': 'user_id, reward_id, original_reward_id, amount, reversal_reason',
            'Optional Properties': 'partner_chargeback_id',
            'Data Type': 'JSON Object',
            'Validation': 'original_reward_id must exist in Rewards table',
            'Source': 'Backend Ledger Service',
            'Business Purpose': 'Protect platform economics against affiliate fraud / chargebacks',
            'KPI Dependency': 'Reward Reversal Rate, Chargeback Volume',
            'Implementation Status': 'Proposed'
        },
        # Daily & Engagement Domain
        {
            'Event Name': 'engagement_daily_reward_claimed',
            'Trigger': 'User taps claim on daily calendar widget',
            'Definition': 'Credits daily streak milestone reward',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Daily Streaks',
            'Status': 'success',
            'Required Properties': 'user_id, streak_day, reward_amount, reward_unit',
            'Optional Properties': 'is_streak_multiplier_active',
            'Data Type': 'JSON Object',
            'Validation': 'streak_day >= 1 and streak_day <= 365',
            'Source': 'Backend Rewards Engine',
            'Business Purpose': 'Habit formation metric and retention tracker',
            'KPI Dependency': 'Daily Claim Rate, 7-Day Streak Retention',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'engagement_streak_updated',
            'Trigger': 'Daily streak counter is evaluated (incremented, reset, or protected)',
            'Definition': 'Audit log of user streak continuity state transition',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Daily Streaks',
            'Status': 'success',
            'Required Properties': 'user_id, previous_streak, new_streak, streak_action',
            'Optional Properties': 'freeze_tokens_remaining',
            'Data Type': 'JSON Object',
            'Validation': 'streak_action IN (increment, reset, freeze_applied)',
            'Source': 'Streak Worker Daemon',
            'Business Purpose': 'Understand streak breakage patterns and churn risk',
            'KPI Dependency': 'Streak Break Rate, Average Streak Length',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'gamification_spin_started',
            'Trigger': 'User initiates lucky wheel spin',
            'Definition': 'Wheel animation begins; ticket/cost debited',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Spin Wheel',
            'Status': 'in_progress',
            'Required Properties': 'user_id, spin_id, spin_cost_type',
            'Optional Properties': 'token_cost_amount',
            'Data Type': 'JSON Object',
            'Validation': 'spin_cost_type IN (daily_free, token_purchase, rewarded_video)',
            'Source': 'Client Game Engine',
            'Business Purpose': 'Engagement funnel entry for minigames',
            'KPI Dependency': 'Spin Wheel Participation Rate',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'gamification_spin_completed',
            'Trigger': 'Spin wheel lands on segment and prize is computed by RNG',
            'Definition': 'Records prize awarded and writes corresponding reward record',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Spin Wheel',
            'Status': 'completed',
            'Required Properties': 'user_id, spin_id, prize_tier, prize_amount, prize_unit',
            'Optional Properties': 'jackpot_flag',
            'Data Type': 'JSON Object',
            'Validation': 'prize_amount >= 0',
            'Source': 'Backend RNG Service',
            'Business Purpose': 'Audit prize payout distribution against mathematical expectation',
            'KPI Dependency': 'Minigame Reward Payout Volume',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'gamification_mission_started',
            'Trigger': 'User accepts or system assigns weekly/daily quest',
            'Definition': 'Initializes progress counters for structured mission',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Missions',
            'Status': 'in_progress',
            'Required Properties': 'user_id, mission_id, mission_type, target_criteria_count',
            'Optional Properties': 'expiration_timestamp',
            'Data Type': 'JSON Object',
            'Validation': 'mission_id not null',
            'Source': 'Missions Engine',
            'Business Purpose': 'Goal-directed gamification funnel top',
            'KPI Dependency': 'Mission Adoption Rate',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'gamification_mission_completed',
            'Trigger': 'All mission criteria verified complete',
            'Definition': 'Marks quest fulfilled and unlocks reward milestone',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Missions',
            'Status': 'completed',
            'Required Properties': 'user_id, mission_id, duration_hours, bonus_reward_amount',
            'Optional Properties': 'quest_chest_tier',
            'Data Type': 'JSON Object',
            'Validation': 'bonus_reward_amount >= 0',
            'Source': 'Missions Engine',
            'Business Purpose': 'Assess mission engagement velocity and completion difficulty',
            'KPI Dependency': 'Mission Completion Rate',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'gamification_badge_earned',
            'Trigger': 'User fulfills criteria for achievement badge',
            'Definition': 'Awards collectible badge to user profile',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Badges & Achievements',
            'Status': 'success',
            'Required Properties': 'user_id, badge_id, badge_category, xp_granted',
            'Optional Properties': 'rarity_tier',
            'Data Type': 'JSON Object',
            'Validation': 'badge_id in badge catalog',
            'Source': 'Achievement Service',
            'Business Purpose': 'Gamification milestone metric; long-term stickiness',
            'KPI Dependency': 'Badges Unlocked per Active User',
            'Implementation Status': 'Proposed'
        },
        # Referral Domain
        {
            'Event Name': 'referral_link_created',
            'Trigger': 'User taps share/invite button to generate referral link or code',
            'Definition': 'Registers unique deep-link token bound to referrer',
            'User ID': 'referring_user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Referrals',
            'Status': 'success',
            'Required Properties': 'referral_id, referring_user_id, invite_channel',
            'Optional Properties': 'campaign_tag',
            'Data Type': 'JSON Object',
            'Validation': 'invite_channel IN (WhatsApp, Telegram, Twitter, DirectLink, SMS)',
            'Source': 'Mobile Client SDK',
            'Business Purpose': 'Measures viral intent and channel sharing preference',
            'KPI Dependency': 'Referral Invites Generated, Viral Coefficient (K-factor)',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'referral_referee_registered',
            'Trigger': 'New user signs up attributing referral code/token',
            'Definition': 'Connects referred user ID with referring user ID at registration',
            'User ID': 'referred_user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Referrals',
            'Status': 'registered',
            'Required Properties': 'referral_id, referring_user_id, referred_user_id',
            'Optional Properties': 'attribution_delay_hours',
            'Data Type': 'JSON Object',
            'Validation': 'referring_user_id != referred_user_id (prevent self-referral)',
            'Source': 'Auth Service / Referral Engine',
            'Business Purpose': 'First downstream viral conversion step',
            'KPI Dependency': 'Referral Signup Conversion Rate',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'referral_referee_activated',
            'Trigger': 'Referred user completes their 1st earning task (e.g. ad, survey)',
            'Definition': 'Confirms referee is a legitimate, active user',
            'User ID': 'referred_user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Referrals',
            'Status': 'activated',
            'Required Properties': 'referral_id, referring_user_id, referred_user_id, qualifying_task_id',
            'Optional Properties': 'time_to_activate_hours',
            'Data Type': 'JSON Object',
            'Validation': 'qualifying_task_id must have status == validated',
            'Source': 'Referral Attribution Engine',
            'Business Purpose': 'Filters bot registrations from real referred active users',
            'KPI Dependency': 'Referral Activation Rate',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'referral_bonus_converted',
            'Trigger': 'Referral meets all anti-fraud checks and bonus is released to referrer',
            'Definition': 'Marks referral conversion closed and issues bounty',
            'User ID': 'referring_user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Referrals',
            'Status': 'converted',
            'Required Properties': 'referral_id, referring_user_id, referred_user_id, bonus_reward_amount',
            'Optional Properties': 'referrer_reward_id',
            'Data Type': 'JSON Object',
            'Validation': 'bonus_reward_amount > 0',
            'Source': 'Referral Attribution Engine',
            'Business Purpose': 'Viral loop completion; evaluates true paid referral efficiency',
            'KPI Dependency': 'Referral Conversion Rate, Cost per Activated Referee',
            'Implementation Status': 'Proposed'
        },
        # Wallet Domain
        {
            'Event Name': 'wallet_transaction_created',
            'Trigger': 'Any ledger transaction is initiated (credit, debit, hold)',
            'Definition': 'Opens double-entry ledger journal record',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Wallet & Ledger',
            'Status': 'pending',
            'Required Properties': 'user_id, transaction_id, transaction_type, amount, unit, source',
            'Optional Properties': 'reference_id',
            'Data Type': 'JSON Object',
            'Validation': 'transaction_type IN (reward_credit, withdrawal_debit, token_exchange, admin_adjustment, withdrawal_refund)',
            'Source': 'Core Ledger API',
            'Business Purpose': 'Double-entry transactional integrity and pending balance locks',
            'KPI Dependency': 'Gross Transaction Volume (GTV)',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'wallet_transaction_completed',
            'Trigger': 'Transaction permanently commits to ledger state',
            'Definition': 'Updates user available balance and closes journal entry',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Wallet & Ledger',
            'Status': 'completed',
            'Required Properties': 'user_id, transaction_id, running_balance_snapshot',
            'Optional Properties': 'cleared_timestamp',
            'Data Type': 'JSON Object',
            'Validation': 'running_balance_snapshot >= 0 (no unapproved negative balances)',
            'Source': 'Core Ledger API',
            'Business Purpose': 'Core financial balance snapshot; audit ledger trail',
            'KPI Dependency': 'Circulating VE Supply, Net Wallet Liquidity',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'wallet_transaction_reversed',
            'Trigger': 'Transaction is cancelled, refunded, or rolled back',
            'Definition': 'Applies balancing offsetting journal entry to restore balance',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Wallet & Ledger',
            'Status': 'reversed',
            'Required Properties': 'user_id, transaction_id, reversal_relationship_id, reason',
            'Optional Properties': 'operator_user_id',
            'Data Type': 'JSON Object',
            'Validation': 'reversal_relationship_id must point to completed transaction',
            'Source': 'Core Ledger API',
            'Business Purpose': 'Dispute handling, fraud remediation, and withdrawal failure return',
            'KPI Dependency': 'Wallet Reversal Rate',
            'Implementation Status': 'Proposed'
        },
        # Withdrawal Domain
        {
            'Event Name': 'withdrawal_requested',
            'Trigger': 'User submits cash-out request in wallet UI',
            'Definition': 'Initiates payout workflow; locks funds in escrow',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Withdrawals',
            'Status': 'requested',
            'Required Properties': 'withdrawal_id, user_id, requested_amount, currency_unit, withdrawal_method, fee_amount',
            'Optional Properties': 'destination_account_hash',
            'Data Type': 'JSON Object',
            'Validation': 'requested_amount >= min_payout_threshold and fee_amount >= 0',
            'Source': 'Withdrawal Engine',
            'Business Purpose': 'Demand for fiat/crypto exit; financial pipeline backlog metric',
            'KPI Dependency': 'Withdrawal Request Volume, Cash-out Demand',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'withdrawal_processing',
            'Trigger': 'Withdrawal passes fraud check and is dispatched to payout rail',
            'Definition': 'Request enters external payment gateway processing queue',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Withdrawals',
            'Status': 'processing',
            'Required Properties': 'withdrawal_id, user_id, provider_batch_id',
            'Optional Properties': 'estimated_clearing_hours',
            'Data Type': 'JSON Object',
            'Validation': 'provider_batch_id not null',
            'Source': 'Payment Gateway Connector',
            'Business Purpose': 'Monitors payment provider processing SLAs',
            'KPI Dependency': 'Pending Withdrawal Queue Size, Gateway Latency',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'withdrawal_completed',
            'Trigger': 'Payment rail returns HTTP 200 / successful settlement postback',
            'Definition': 'Funds confirmed received by user external destination account',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Withdrawals',
            'Status': 'completed',
            'Required Properties': 'withdrawal_id, user_id, requested_amount, payout_reference_hash, total_duration_seconds',
            'Optional Properties': 'actual_fiat_amount',
            'Data Type': 'JSON Object',
            'Validation': 'payout_reference_hash length >= 8',
            'Source': 'Payment Provider Webhook',
            'Business Purpose': 'Core redemption success metric; platform trust fulfillment',
            'KPI Dependency': 'Completed Withdrawal Rate, Average Processing Time, Payout Volume',
            'Implementation Status': 'Proposed'
        },
        {
            'Event Name': 'withdrawal_rejected',
            'Trigger': 'Internal fraud heuristic triggers or compliance/provider declines payout',
            'Definition': 'Declines withdrawal and restores escrow balance to user',
            'User ID': 'user_id (String)',
            'Event ID': 'event_id (UUID v4)',
            'Timestamp': 'timestamp (ISO 8601 UTC)',
            'Feature': 'Withdrawals',
            'Status': 'rejected',
            'Required Properties': 'withdrawal_id, user_id, rejection_reason_category',
            'Optional Properties': 'reviewer_notes, appeals_eligible',
            'Data Type': 'JSON Object',
            'Validation': 'rejection_reason_category IN (KYC_incomplete, minimum_threshold_not_met, suspected_fraud, third_party_provider_error, account_mismatch)',
            'Source': 'Risk Engine / Backoffice Admin',
            'Business Purpose': 'Risk mitigation auditing and user payout obstacle discovery',
            'KPI Dependency': 'Withdrawal Rejection Rate, Fraud Prevention Yield',
            'Implementation Status': 'Proposed'
        }
    ]
    df_event_plan = pd.DataFrame(event_plan_rows)
    df_event_plan.to_csv(os.path.join(out_dir, '08_EVENT_TRACKING_PLAN.csv'), index=False)

    # =========================================================================
    # DELIVERABLE 09: DATA DICTIONARY (85+ FIELDS)
    # =========================================================================
    print("Generating Deliverable 09: Data Dictionary (85+ fields)...")
    dict_rows = []

    def add_dict_field(entity, name, dtype, definition, example, required, allowed, validation, source, sensitivity, use, status='Proposed'):
        dict_rows.append({
            'Entity': entity,
            'Field Name': name,
            'Data Type': dtype,
            'Definition': definition,
            'Example': example,
            'Required': required,
            'Allowed Values': allowed,
            'Validation': validation,
            'Source': source,
            'Sensitivity': sensitivity,
            'Analytical Use': use,
            'Status': status
        })

    # Entity: Users
    add_dict_field('Users', 'user_id', 'String', 'Permanent unique identifier for registered user', 'USR_00001', 'Yes', 'USR_[0-9]{5}', 'Regex match ^USR_[0-9]{5}$', 'Auth Service', 'Internal', 'Primary Key; cross-entity join key', 'Confirmed')
    add_dict_field('Users', 'registration_timestamp', 'Timestamp', 'UTC timestamp when user record was created', '2026-03-15 10:22:15', 'Yes', 'Valid UTC', 'Past or present UTC timestamp', 'Auth DB', 'Internal', 'Cohort grouping, user tenure, aging', 'Confirmed')
    add_dict_field('Users', 'registration_source', 'String', 'Acquisition channel through which user discovered app', 'referral', 'Yes', 'organic, referral, paid_ad, partner_promo, influencer', 'Enum member', 'Attribution SDK', 'Internal', 'Channel performance, CAC calculation', 'Confirmed')
    add_dict_field('Users', 'acquisition_campaign', 'String', 'Marketing campaign tag associated with acquisition', 'summer_boost', 'No', 'Free string', 'MaxLength 100', 'Attribution SDK', 'Internal', 'Campaign ROI, ad spend efficiency', 'Proposed')
    add_dict_field('Users', 'device_platform', 'String', 'Operating system of registration device', 'Android', 'Yes', 'Android, iOS, Web', 'Enum member', 'Client Telemetry', 'Internal', 'Platform breakdown, cross-platform retention', 'Confirmed')
    add_dict_field('Users', 'country_code', 'String', 'ISO 3166-1 alpha-2 country of user registration', 'US', 'Yes', 'ISO alpha-2 codes', 'Length 2, uppercase', 'IP Geolocation', 'Internal', 'Geographic analysis, regional monetization', 'Confirmed')
    add_dict_field('Users', 'account_status', 'String', 'Current operational lifecycle standing of user account', 'active', 'Yes', 'active, dormant, suspended, closed', 'Enum member', 'User Service', 'Internal', 'Cohort filtering, churn analysis', 'Confirmed')
    add_dict_field('Users', 'is_onboarding_completed', 'Boolean', 'Indicates if user finished onboarding tutorial flow', 'TRUE', 'Yes', 'TRUE, FALSE', 'Boolean', 'Client SDK', 'Internal', 'Activation conversion analysis', 'Confirmed')
    add_dict_field('Users', 'onboarding_completed_timestamp', 'Timestamp', 'UTC timestamp when onboarding was marked complete', '2026-03-15 10:28:40', 'No', 'Valid UTC', 'Must be >= registration_timestamp', 'Client SDK', 'Internal', 'Time-to-activation duration metric', 'Proposed')
    add_dict_field('Users', 'last_login_timestamp', 'Timestamp', 'UTC timestamp of most recent successful session authentication', '2026-10-30 18:45:10', 'Yes', 'Valid UTC', 'Must be >= registration_timestamp', 'Auth Service', 'Internal', 'Recency calculation, active status thresholding', 'Confirmed')

    # Entity: Task_Activity
    add_dict_field('Task_Activity', 'task_activity_id', 'String', 'Unique surrogate key for an individual task execution attempt', 'TSK_000100', 'Yes', 'TSK_[0-9]{6}', 'Regex match ^TSK_[0-9]{6}$', 'Task Engine', 'Internal', 'Primary Key; joins to Rewards', 'Confirmed')
    add_dict_field('Task_Activity', 'task_id', 'String', 'Identifier of the catalog task template or campaign', 'TK_AD_101', 'Yes', 'Alphanumeric ID', 'Must exist in Tasks catalog', 'Task Catalog', 'Internal', 'Task popularitity, task-level completion rate', 'Confirmed')
    add_dict_field('Task_Activity', 'task_type', 'String', 'Categorical classification of the earning mechanism', 'watch_ad', 'Yes', 'watch_ad, survey, tap_earn, mining, offerwall, app_install', 'Enum member', 'Task Engine', 'Internal', 'Earning category segmentation', 'Confirmed')
    add_dict_field('Task_Activity', 'feature_category', 'String', 'High-level product classification', 'Earning', 'Yes', 'Earning, Gamification, Daily', 'String enum', 'Product Schema', 'Internal', 'High-level product area reporting', 'Confirmed')
    add_dict_field('Task_Activity', 'user_id', 'String', 'Identifier of user performing the task', 'USR_00001', 'Yes', 'Valid user_id', 'Foreign key to Users.user_id', 'Session Context', 'Internal', 'User task frequency, individual earning velocity', 'Confirmed')
    add_dict_field('Task_Activity', 'started_at', 'Timestamp', 'UTC timestamp when user launched the task', '2026-04-01 12:00:00', 'Yes', 'Valid UTC', 'Valid datetime', 'Client / Server', 'Internal', 'Start volume, diurnal usage patterns', 'Confirmed')
    add_dict_field('Task_Activity', 'completed_at', 'Timestamp', 'UTC timestamp when task reached terminal completion state', '2026-04-01 12:00:30', 'No', 'Valid UTC', 'Must be >= started_at', 'Server Validation', 'Internal', 'Task duration calculation, abandonment timing', 'Confirmed')
    add_dict_field('Task_Activity', 'status', 'String', 'Execution status of the task attempt', 'completed', 'Yes', 'completed, failed, abandoned, pending_validation', 'Enum member', 'Task Engine', 'Internal', 'Task funnel completion rate', 'Confirmed')
    add_dict_field('Task_Activity', 'reward_amount', 'Numeric', 'Magnitude of reward units allocated for completion', '15.00', 'Yes', 'Numeric >= 0', 'Unsigned decimal', 'Task Catalog', 'Internal', 'Reward liability estimation', 'Confirmed')
    add_dict_field('Task_Activity', 'reward_unit', 'String', 'Currency or gamification unit denomination', 'VEs', 'Yes', 'VEs, Gems, XP', 'Enum member', 'Task Catalog', 'Internal', 'Unit-specific aggregation', 'Confirmed')
    add_dict_field('Task_Activity', 'validation_status', 'String', 'Result of anti-fraud and partner verification checks', 'validated', 'Yes', 'validated, rejected, pending', 'Enum member', 'Validation Engine', 'Internal', 'Fraud monitoring, partner postback verification rate', 'Confirmed')
    add_dict_field('Task_Activity', 'partner_provider', 'String', 'Name of third-party network delivering the task', 'GoogleAdMob', 'Yes', 'GoogleAdMob, Pollfish, Tapjoy, InternalEngine', 'String enum', 'Task Engine', 'Internal', 'Partner performance, network yield evaluation', 'Confirmed')
    add_dict_field('Task_Activity', 'error_reason', 'String', 'Diagnostic reason string for failed or abandoned tasks', 'tracking_timeout', 'No', 'Free string / enum', 'MaxLength 100', 'Task Engine', 'Internal', 'Error triage and UX remediation', 'Proposed')

    # Entity: Rewards
    add_dict_field('Rewards', 'reward_id', 'String', 'Unique surrogate key for reward distribution event', 'RWD_00001', 'Yes', 'RWD_[0-9]{5}', 'Regex match ^RWD_[0-9]{5}$', 'Rewards Engine', 'Internal', 'Primary Key; financial reconciliation', 'Confirmed')
    add_dict_field('Rewards', 'user_id', 'String', 'Recipient user identifier', 'USR_00001', 'Yes', 'Valid user_id', 'Foreign key to Users.user_id', 'Rewards Engine', 'Internal', 'Per-user reward accumulation', 'Confirmed')
    add_dict_field('Rewards', 'task_activity_id', 'String', 'Reference to upstream task execution (null for streaks)', 'TSK_000100', 'No', 'Valid task_activity_id', 'Foreign key to Task_Activity', 'Rewards Engine', 'Internal', 'Reward attribution to specific task', 'Confirmed')
    add_dict_field('Rewards', 'reward_type', 'String', 'Business origin of reward issuance', 'task_completion', 'Yes', 'task_completion, daily_login, streak_bonus, referral_bonus, spin_wheel, badge_milestone', 'Enum member', 'Rewards Engine', 'Internal', 'Reward category distribution', 'Confirmed')
    add_dict_field('Rewards', 'amount', 'Numeric', 'Quantity of reward credited', '25.00', 'Yes', 'Numeric > 0', 'Strictly positive numeric', 'Rewards Engine', 'Internal', 'Reward expense calculation', 'Confirmed')
    add_dict_field('Rewards', 'reward_unit', 'String', 'Denomination currency of reward', 'VEs', 'Yes', 'VEs, Gems, XP', 'Enum member', 'Rewards Engine', 'Internal', 'Multi-currency ledger segmentation', 'Confirmed')
    add_dict_field('Rewards', 'status', 'String', 'Current accounting state of reward', 'credited', 'Yes', 'credited, pending, reversed, corrected', 'Enum member', 'Ledger Service', 'Internal', 'Liability status tracking', 'Confirmed')
    add_dict_field('Rewards', 'credited_at', 'Timestamp', 'UTC timestamp when reward entered ledger', '2026-04-01 12:00:32', 'Yes', 'Valid UTC', 'Valid datetime', 'Ledger Service', 'Internal', 'Daily reward issuance volume', 'Confirmed')
    add_dict_field('Rewards', 'ledger_status', 'String', 'Posting status in core financial ledger', 'posted', 'Yes', 'posted, pending, voided', 'Enum member', 'Ledger Service', 'Internal', 'Accounting reconciliation', 'Confirmed')
    add_dict_field('Rewards', 'correction_reference_id', 'String', 'Pointer to original reward if reversed or adjusted', 'RWD_00005', 'No', 'Valid reward_id', 'Self-referencing foreign key', 'Ledger Service', 'Internal', 'Reversal audit trail', 'Proposed')

    # Entity: Wallet
    add_dict_field('Wallet', 'transaction_id', 'String', 'Unique surrogate identifier for wallet journal line', 'TXN_000001', 'Yes', 'TXN_[0-9]{6}', 'Regex match ^TXN_[0-9]{6}$', 'Ledger Core', 'Internal', 'Primary Key; financial audit', 'Confirmed')
    add_dict_field('Wallet', 'user_id', 'String', 'Owner of the affected wallet balance', 'USR_00001', 'Yes', 'Valid user_id', 'Foreign key to Users.user_id', 'Ledger Core', 'Internal', 'User balance ledger aggregation', 'Confirmed')
    add_dict_field('Wallet', 'timestamp', 'Timestamp', 'UTC timestamp of transaction entry', '2026-04-01 12:00:32', 'Yes', 'Valid UTC', 'Valid datetime', 'Ledger Core', 'Internal', 'Transaction velocity, temporal audit', 'Confirmed')
    add_dict_field('Wallet', 'transaction_type', 'String', 'Economic category of transaction', 'reward_credit', 'Yes', 'reward_credit, withdrawal_debit, token_exchange, admin_adjustment, withdrawal_refund', 'Enum member', 'Ledger Core', 'Internal', 'Cash flow segmentation', 'Confirmed')
    add_dict_field('Wallet', 'amount', 'Numeric', 'Signed numeric change to user balance', '25.00', 'Yes', 'Signed numeric', 'Numeric value (+ for credit, - for debit)', 'Ledger Core', 'Internal', 'Net balance calculation', 'Confirmed')
    add_dict_field('Wallet', 'unit', 'String', 'Currency unit of balance change', 'VEs', 'Yes', 'VEs, Gems, Tokens', 'Enum member', 'Ledger Core', 'Internal', 'Currency-specific balances', 'Confirmed')
    add_dict_field('Wallet', 'status', 'String', 'State of the journal transaction', 'completed', 'Yes', 'completed, pending, reversed, failed', 'Enum member', 'Ledger Core', 'Internal', 'Clearing and settlement analysis', 'Confirmed')
    add_dict_field('Wallet', 'source', 'String', 'Subsystem initiating the transaction', 'reward_engine', 'Yes', 'reward_engine, withdrawal_engine, exchange_service, manual_ops', 'Enum member', 'Ledger Core', 'Internal', 'Subsystem volume attribution', 'Confirmed')
    add_dict_field('Wallet', 'reference_id', 'String', 'External identifier linking to upstream record', 'RWD_00001', 'No', 'Alphanumeric ID', 'Pointers to RWD, WDR, or EXC IDs', 'Ledger Core', 'Internal', 'Auditability, end-to-end traceability', 'Confirmed')
    add_dict_field('Wallet', 'reversal_relationship_id', 'String', 'Pointer to original transaction if this row is a reversal', 'TXN_000050', 'No', 'Valid transaction_id', 'Self-referencing foreign key', 'Ledger Core', 'Internal', 'Reversal linkage', 'Proposed')

    # Entity: Withdrawals
    add_dict_field('Withdrawals', 'withdrawal_id', 'String', 'Unique surrogate key for withdrawal request', 'WDR_0001', 'Yes', 'WDR_[0-9]{4}', 'Regex match ^WDR_[0-9]{4}$', 'Withdrawal Engine', 'Internal', 'Primary Key; payment tracking', 'Confirmed')
    add_dict_field('Withdrawals', 'user_id', 'String', 'User requesting payout', 'USR_00001', 'Yes', 'Valid user_id', 'Foreign key to Users.user_id', 'Withdrawal Engine', 'Internal', 'Per-user cash-out behavior', 'Confirmed')
    add_dict_field('Withdrawals', 'requested_amount', 'Numeric', 'Quantity of units requested for redemption', '1000.00', 'Yes', 'Numeric >= 500', 'Must exceed minimum threshold', 'Withdrawal Engine', 'Internal', 'Redemption demand volume', 'Confirmed')
    add_dict_field('Withdrawals', 'currency_unit', 'String', 'Currency unit debited for payout', 'VEs', 'Yes', 'VEs, Tokens', 'Enum member', 'Withdrawal Engine', 'Internal', 'Payout unit breakdown', 'Confirmed')
    add_dict_field('Withdrawals', 'withdrawal_method', 'String', 'Disbursement rail selected by user', 'PayPal', 'Yes', 'PayPal, Crypto_USDT, GiftCard_Amazon, BankTransfer', 'Enum member', 'Withdrawal Engine', 'Internal', 'Payment channel popularity', 'Confirmed')
    add_dict_field('Withdrawals', 'requested_timestamp', 'Timestamp', 'UTC timestamp when user submitted cash-out form', '2026-05-10 14:00:00', 'Yes', 'Valid UTC', 'Valid datetime', 'Withdrawal Engine', 'Internal', 'Backlog queue aging, SLA clock start', 'Confirmed')
    add_dict_field('Withdrawals', 'processing_timestamp', 'Timestamp', 'UTC timestamp when payout passed review and reached gateway', '2026-05-10 18:30:00', 'No', 'Valid UTC', 'Must be >= requested_timestamp', 'Gateway Connector', 'Internal', 'Internal review latency', 'Confirmed')
    add_dict_field('Withdrawals', 'final_timestamp', 'Timestamp', 'UTC timestamp when terminal settlement or rejection occurred', '2026-05-11 10:15:00', 'No', 'Valid UTC', 'Must be >= processing_timestamp', 'Gateway Webhook', 'Internal', 'End-to-end turnaround time (TAT)', 'Confirmed')
    add_dict_field('Withdrawals', 'status', 'String', 'Current operational status of withdrawal', 'completed', 'Yes', 'requested, processing, completed, rejected, reversed', 'Enum member', 'Withdrawal Engine', 'Internal', 'Withdrawal funnel completion rate', 'Confirmed')
    add_dict_field('Withdrawals', 'rejection_reason_category', 'String', 'Categorized rationale if payout declined', 'KYC_incomplete', 'No', 'KYC_incomplete, minimum_threshold_not_met, suspected_fraud, third_party_provider_error, account_mismatch', 'Enum member', 'Risk Engine', 'Internal', 'Root-cause analysis of payment failures', 'Confirmed')
    add_dict_field('Withdrawals', 'payout_reference_hash', 'String', 'External payment provider settlement transaction hash', 'HASH_9B8C123F', 'No', 'Alphanumeric hash', 'Hex string length >= 8', 'Payment Provider', 'Restricted', 'Financial settlement verification', 'Confirmed')
    add_dict_field('Withdrawals', 'fee_amount', 'Numeric', 'Processing fee deducted from gross payout', '20.00', 'Yes', 'Numeric >= 0', 'Unsigned decimal', 'Withdrawal Engine', 'Internal', 'Fee revenue calculation', 'Confirmed')

    # Entity: Referrals
    add_dict_field('Referrals', 'referral_id', 'String', 'Unique surrogate key for referral tracking lifecycle', 'REF_0001', 'Yes', 'REF_[0-9]{4}', 'Regex match ^REF_[0-9]{4}$', 'Referral Engine', 'Internal', 'Primary Key; viral funnel analysis', 'Confirmed')
    add_dict_field('Referrals', 'referring_user_id', 'String', 'User who shared the invite link', 'USR_00001', 'Yes', 'Valid user_id', 'Foreign key to Users.user_id', 'Client DeepLink', 'Internal', 'Referrer viral productivity, K-factor', 'Confirmed')
    add_dict_field('Referrals', 'referred_user_id', 'String', 'New user registered via referral link', 'USR_00025', 'No', 'Valid user_id', 'Foreign key to Users.user_id', 'Auth Service', 'Internal', 'Referee retention tracking', 'Confirmed')
    add_dict_field('Referrals', 'invite_channel', 'String', 'Social sharing app or medium used', 'WhatsApp', 'Yes', 'WhatsApp, Telegram, Twitter, DirectLink, SMS', 'Enum member', 'Client Share Sheet', 'Internal', 'Channel-level viral conversion efficiency', 'Confirmed')
    add_dict_field('Referrals', 'creation_timestamp', 'Timestamp', 'UTC timestamp when invite link/token was generated', '2026-02-10 09:00:00', 'Yes', 'Valid UTC', 'Valid datetime', 'Client SDK', 'Internal', 'Share frequency, viral intent volume', 'Confirmed')
    add_dict_field('Referrals', 'registration_timestamp', 'Timestamp', 'UTC timestamp when referee completed account creation', '2026-02-10 14:30:00', 'No', 'Valid UTC', 'Must be >= creation_timestamp', 'Auth Service', 'Internal', 'Invite-to-signup latency', 'Confirmed')
    add_dict_field('Referrals', 'activation_timestamp', 'Timestamp', 'UTC timestamp when referee completed first valid earning task', '2026-02-11 11:20:00', 'No', 'Valid UTC', 'Must be >= registration_timestamp', 'Task Engine', 'Internal', 'Signup-to-activation velocity', 'Confirmed')
    add_dict_field('Referrals', 'status', 'String', 'Lifecycle milestone reached in referral funnel', 'converted', 'Yes', 'link_created, registered, activated, converted', 'Enum member', 'Referral Engine', 'Internal', 'Referral funnel stage drop-off', 'Confirmed')
    add_dict_field('Referrals', 'reward_credited_to_referrer', 'Boolean', 'Indicates whether referral bounty was posted to referrer', 'TRUE', 'Yes', 'TRUE, FALSE', 'Boolean', 'Rewards Engine', 'Internal', 'Referral reward cost accounting', 'Confirmed')
    add_dict_field('Referrals', 'attribution_source', 'String', 'Attribution technical mechanism', 'campaign_share_sheet', 'Yes', 'campaign_share_sheet, web_landing_cookie, manual_code', 'String enum', 'Attribution SDK', 'Internal', 'Attribution reliability audit', 'Proposed')

    # Entity: Feature_Events
    add_dict_field('Feature_Events', 'event_id', 'String', 'Unique surrogate key for telemetry event instance', 'EVT_000001', 'Yes', 'EVT_[0-9]{6}', 'Regex match ^EVT_[0-9]{6}$', 'Event Gateway', 'Internal', 'Primary Key; event deduplication', 'Confirmed')
    add_dict_field('Feature_Events', 'user_id', 'String', 'User who generated the event', 'USR_00001', 'Yes', 'Valid user_id', 'Foreign key to Users.user_id', 'Session Context', 'Internal', 'User-level behavioral modeling', 'Confirmed')
    add_dict_field('Feature_Events', 'session_id', 'String', 'Identifier of user session during event occurrence', 'SES_123456', 'Yes', 'SES_[0-9]{6}', 'Alphanumeric session token', 'Client SDK', 'Internal', 'Session boundary analysis, events per session', 'Confirmed')
    add_dict_field('Feature_Events', 'event_name', 'String', 'Standardized domain_object_action name of event', 'daily_reward_claimed', 'Yes', 'Standardized event taxonomy', 'Snake_case string', 'Telemetry SDK', 'Internal', 'Event stream filtering, feature usage volume', 'Confirmed')
    add_dict_field('Feature_Events', 'feature_domain', 'String', 'Product subsystem owning the event', 'engagement', 'Yes', 'engagement, gamification, support, navigation', 'Enum member', 'Event Schema', 'Internal', 'Subsystem telemetry volume breakdown', 'Confirmed')
    add_dict_field('Feature_Events', 'timestamp', 'Timestamp', 'UTC timestamp when event occurred on client or server', '2026-05-12 16:20:00', 'Yes', 'Valid UTC', 'Valid datetime', 'Client / Server', 'Internal', 'Time-series activity aggregation', 'Confirmed')
    add_dict_field('Feature_Events', 'device_platform', 'String', 'Client operating platform emitting telemetry', 'Android', 'Yes', 'Android, iOS, Web', 'Enum member', 'Client SDK', 'Internal', 'Platform telemetry segmentation', 'Confirmed')
    add_dict_field('Feature_Events', 'status', 'String', 'Result of client action triggering event', 'success', 'Yes', 'success, failed, pending', 'Enum member', 'Client SDK', 'Internal', 'Feature error rate tracking', 'Confirmed')

    # Entity: Missions
    add_dict_field('Missions', 'mission_id', 'String', 'Unique surrogate key for gamification quest template', 'MSN_101', 'Yes', 'MSN_[0-9]{3}', 'Regex match ^MSN_[0-9]{3}$', 'Mission Service', 'Internal', 'Primary Key; quest catalog', 'Proposed')
    add_dict_field('Missions', 'mission_name', 'String', 'User-facing title of mission', 'Weekend Warrior', 'Yes', 'Free string', 'MaxLength 100', 'Mission Service', 'Public', 'Display in client UI', 'Proposed')
    add_dict_field('Missions', 'mission_type', 'String', 'Recurrence window of mission', 'weekly', 'Yes', 'daily, weekly, special_event', 'Enum member', 'Mission Service', 'Internal', 'Mission cadence categorization', 'Proposed')
    add_dict_field('Missions', 'required_task_type', 'String', 'Target task type required for completion', 'watch_ad', 'Yes', 'watch_ad, survey, tap_earn, any', 'Enum member', 'Mission Service', 'Internal', 'Criteria validation logic', 'Proposed')
    add_dict_field('Missions', 'required_count', 'Integer', 'Number of task completions required', '5', 'Yes', 'Integer > 0', 'Positive integer', 'Mission Service', 'Internal', 'Threshold evaluation', 'Proposed')
    add_dict_field('Missions', 'reward_bonus_amount', 'Numeric', 'Additional bonus VEs/XP granted upon completion', '100.00', 'Yes', 'Numeric >= 0', 'Unsigned decimal', 'Mission Service', 'Internal', 'Gamification expense estimation', 'Proposed')
    add_dict_field('Missions', 'is_active', 'Boolean', 'Indicates if mission is currently live in catalog', 'TRUE', 'Yes', 'TRUE, FALSE', 'Boolean', 'Mission Service', 'Internal', 'Active catalog filtering', 'Proposed')

    # Entity: Badges
    add_dict_field('Badges', 'badge_id', 'String', 'Unique identifier for collectible badge', 'BDG_EARN_01', 'Yes', 'BDG_[A-Z_0-9]+', 'Regex match', 'Badge Service', 'Internal', 'Primary Key; achievement catalog', 'Proposed')
    add_dict_field('Badges', 'badge_title', 'String', 'User-facing title of the badge', 'Ad Enthusiast', 'Yes', 'Free string', 'MaxLength 100', 'Badge Service', 'Public', 'UI display', 'Proposed')
    add_dict_field('Badges', 'badge_category', 'String', 'Domain of achievement represented', 'earning_volume', 'Yes', 'earning_volume, streak_mastery, viral_champion', 'Enum member', 'Badge Service', 'Internal', 'Achievement segmentation', 'Proposed')
    add_dict_field('Badges', 'xp_reward_amount', 'Integer', 'XP granted when badge is unlocked', '250', 'Yes', 'Integer >= 0', 'Positive integer', 'Badge Service', 'Internal', 'Gamification balance calculation', 'Proposed')
    add_dict_field('Badges', 'icon_asset_uri', 'String', 'URL/path to visual artwork asset', 'https://cdn.veloop.io/badges/earn_01.png', 'Yes', 'Valid URI', 'URI format', 'CDN', 'Public', 'UI image rendering', 'Proposed')

    # Entity: Sessions
    add_dict_field('Sessions', 'session_id', 'String', 'Unique surrogate key for authenticated user session', 'SES_123456', 'Yes', 'SES_[0-9]{6}', 'Alphanumeric token', 'Auth Service', 'Internal', 'Primary Key; joins to Feature_Events', 'Proposed')
    add_dict_field('Sessions', 'user_id', 'String', 'User associated with the session', 'USR_00001', 'Yes', 'Valid user_id', 'Foreign key to Users.user_id', 'Auth Service', 'Internal', 'Session per user aggregation', 'Proposed')
    add_dict_field('Sessions', 'session_start_timestamp', 'Timestamp', 'UTC timestamp when app session began', '2026-05-12 16:00:00', 'Yes', 'Valid UTC', 'Valid datetime', 'Client SDK', 'Internal', 'Session frequency, DAU derivation', 'Proposed')
    add_dict_field('Sessions', 'session_end_timestamp', 'Timestamp', 'UTC timestamp when app session closed or timed out', '2026-05-12 16:25:30', 'No', 'Valid UTC', 'Must be >= start_timestamp', 'Client SDK', 'Internal', 'Session duration calculation', 'Proposed')
    add_dict_field('Sessions', 'session_duration_seconds', 'Integer', 'Total length of session in elapsed seconds', '1530', 'No', 'Integer >= 0', 'Non-negative integer', 'Computed', 'Internal', 'Average session length KPI', 'Proposed')
    add_dict_field('Sessions', 'events_count', 'Integer', 'Total number of telemetry events emitted in session', '14', 'Yes', 'Integer >= 1', 'Positive integer', 'Computed', 'Internal', 'Session depth and engagement intensity', 'Proposed')
    add_dict_field('Sessions', 'ip_asn', 'String', 'Autonomous system network number of user connection', 'AS15169', 'No', 'AS[0-9]+', 'ASN regex', 'Gateway Proxy', 'Restricted', 'Bot and proxy detection', 'Proposed')

    df_dict = pd.DataFrame(dict_rows)
    print(f"Total fields in Data Dictionary: {len(df_dict)}")
    df_dict.to_csv(os.path.join(out_dir, '09_DATA_DICTIONARY.csv'), index=False)

    # =========================================================================
    # DELIVERABLE 11: KPI CATALOGUE (35 KPIs)
    # =========================================================================
    print("Generating Deliverable 11: KPI Catalogue (35 KPIs)...")
    kpi_rows = [
        # User KPIs (1-5)
        {
            'KPI Name': 'New User Registrations',
            'Definition': 'Count of distinct unique user profiles created within the reporting window',
            'Formula': 'COUNT(DISTINCT user_id) WHERE registration_timestamp BETWEEN start_date AND end_date',
            'Required Fields': 'user_id, registration_timestamp',
            'Data Source': 'Users',
            'Frequency': 'Daily / Weekly / Monthly',
            'Stakeholder': 'Growth Lead / Product Manager',
            'Business Purpose': 'Evaluates top-of-funnel acquisition throughput and channel velocity',
            'Interpretation': 'An upward trend reflects growing user acquisition; segmenting by source reveals channel mix',
            'Limitation': 'Does not measure user quality or intent without downstream activation tracking',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Daily Active Users (DAU)',
            'Definition': 'Unique individual users who generate at least one qualifying telemetry activity or task event in a calendar day (UTC)',
            'Formula': 'COUNT(DISTINCT user_id) WHERE event_timestamp::date = reporting_date AND qualifying_event_flag = TRUE',
            'Required Fields': 'user_id, timestamp, event_name',
            'Data Source': 'Feature_Events, Task_Activity',
            'Frequency': 'Daily',
            'Stakeholder': 'Product Leadership / CEO',
            'Business Purpose': 'Primary operational metric measuring daily platform engagement and community size',
            'Interpretation': 'Sustained DAU growth indicates strong user utility; spikes without retention indicate low-quality marketing bursts',
            'Limitation': 'Can be artificially inflated by background syncs if non-interactive events are not strictly excluded',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Monthly Active Users (MAU)',
            'Definition': 'Unique individual users who generate at least one qualifying activity event within a rolling 30-day window',
            'Formula': 'COUNT(DISTINCT user_id) WHERE event_timestamp BETWEEN (reporting_date - INTERVAL 30 DAYS) AND reporting_date',
            'Required Fields': 'user_id, timestamp, event_name',
            'Data Source': 'Feature_Events, Task_Activity',
            'Frequency': 'Monthly',
            'Stakeholder': 'Executive Leadership / Investors',
            'Business Purpose': 'Macro platform reach and active audience footprint indicator',
            'Interpretation': 'Measures aggregate monthly user reach and platform scale',
            'Limitation': 'Masks intra-month churn and seasonality swings',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'DAU / MAU Stickiness Ratio',
            'Definition': 'Ratio of Daily Active Users to Monthly Active Users expressed as a percentage',
            'Formula': '(DAU / MAU) * 100',
            'Required Fields': 'DAU, MAU',
            'Data Source': 'Derived from Feature_Events aggregates',
            'Frequency': 'Daily (rolling)',
            'Stakeholder': 'Product Strategy / Growth',
            'Business Purpose': 'Quantifies habitual engagement and product stickiness',
            'Interpretation': 'Higher percentage (>20%) indicates habitual daily utility; lower (<10%) indicates transactional or episodic usage',
            'Limitation': 'Does not identify which specific feature drives the daily habit',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Dormant User Rate',
            'Definition': 'Proportion of registered users with no recorded active session in the past 30 days',
            'Formula': '(COUNT(user_id WHERE last_login_timestamp < reporting_date - INTERVAL 30 DAYS) / Total Registered Users) * 100',
            'Required Fields': 'user_id, last_login_timestamp, account_status',
            'Data Source': 'Users',
            'Frequency': 'Weekly',
            'Stakeholder': 'Retention & Lifecycle Marketing',
            'Business Purpose': 'Monitors the pool of lapsed users needing win-back push messaging',
            'Interpretation': 'Rising dormancy indicates fatigue, broken incentives, or poor feature stickiness',
            'Limitation': 'Does not differentiate between soft dormancy (ignoring notifications) and uninstalled apps',
            'Status': 'Proposed'
        },
        # Engagement KPIs (6-11)
        {
            'KPI Name': 'Task Start Volume',
            'Definition': 'Total count of earning tasks initiated by users across all earning modules',
            'Formula': 'COUNT(task_activity_id) WHERE started_at BETWEEN start_date AND end_date',
            'Required Fields': 'task_activity_id, started_at',
            'Data Source': 'Task_Activity',
            'Frequency': 'Daily',
            'Stakeholder': 'Product Manager (Earning)',
            'Business Purpose': 'Evaluates user willingness to engage with available earning opportunities',
            'Interpretation': 'High starts indicate attractive reward headlines or high user intent',
            'Limitation': 'Does not measure whether users successfully completed the task or abandoned early',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Task Completion Rate',
            'Definition': 'Percentage of started tasks that successfully achieve completed and validated status',
            'Formula': '(COUNT(task_activity_id WHERE status = "completed") / COUNT(task_activity_id WHERE started_at IS NOT NULL)) * 100',
            'Required Fields': 'task_activity_id, status, validation_status',
            'Data Source': 'Task_Activity',
            'Frequency': 'Daily / Weekly',
            'Stakeholder': 'Product Manager / Ad Operations',
            'Business Purpose': 'Identifies task friction, technical partner failures, or excessive task difficulty',
            'Interpretation': 'A low completion rate indicates broken partner postbacks, lengthy surveys, or misleading task descriptions',
            'Limitation': 'Aggregates easy short ad videos with complex multi-stage game offers unless filtered by task_type',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Average Tasks Completed per Active User',
            'Definition': 'Mean number of validated tasks completed by each daily active user',
            'Formula': 'COUNT(task_activity_id WHERE status = "completed") / COUNT(DISTINCT user_id with qualifying task activity)',
            'Required Fields': 'task_activity_id, user_id, status',
            'Data Source': 'Task_Activity',
            'Frequency': 'Daily / Weekly',
            'Stakeholder': 'Product Manager (Earning)',
            'Business Purpose': 'Measures depth of earning engagement per session',
            'Interpretation': 'Higher density indicates compelling reward mechanics; lower density signals quick user drop-off',
            'Limitation': 'Skewed by power-users / bot-like clickers unless trimmed mean or median is used',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Daily Streak Claim Rate',
            'Definition': 'Percentage of daily active users who claim their daily calendar check-in reward',
            'Formula': '(COUNT(DISTINCT user_id claiming daily reward) / DAU) * 100',
            'Required Fields': 'user_id, event_name, timestamp',
            'Data Source': 'Feature_Events, Users',
            'Frequency': 'Daily',
            'Stakeholder': 'Gamification PM',
            'Business Purpose': 'Evaluates daily retention mechanics and baseline habit adoption',
            'Interpretation': 'Healthy adoption is >60% of DAU; low percentage indicates hidden UI or unrewarding streak payoffs',
            'Limitation': 'Does not measure how many days the user maintains the streak consecutively',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Spin Wheel Engagement Frequency',
            'Definition': 'Average number of wheel spins executed per participating active user per day',
            'Formula': 'COUNT(spin_id) / COUNT(DISTINCT user_id participating in spin)',
            'Required Fields': 'event_id, user_id, event_name, timestamp',
            'Data Source': 'Feature_Events',
            'Frequency': 'Daily',
            'Stakeholder': 'Gamification PM',
            'Business Purpose': 'Measures minigame popularity and ticket currency circulation',
            'Interpretation': 'Consistent repeat spins show excitement; sudden drops signal prize pool staleness',
            'Limitation': 'Does not measure whether users spin using free tokens vs watching video ads',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'D7 Cohort Task Retention Rate',
            'Definition': 'Percentage of new registrants who complete at least one task on the 7th calendar day following signup',
            'Formula': '(COUNT(DISTINCT user_id active on Day 7) / COUNT(DISTINCT user_id registered on Day 0)) * 100',
            'Required Fields': 'user_id, registration_timestamp, started_at',
            'Data Source': 'Users, Task_Activity',
            'Frequency': 'Weekly cohort maturity',
            'Stakeholder': 'Growth & Product Analytics',
            'Business Purpose': 'Standard mobile industry benchmark for onboarding stickiness and product fit',
            'Interpretation': 'Higher D7 retention indicates lasting user interest beyond initial curiosity',
            'Limitation': 'Requires 7-day maturity delay before calculation can finalize',
            'Status': 'Proposed'
        },
        # Reward KPIs (12-16)
        {
            'KPI Name': 'Total Reward Issuance Volume',
            'Definition': 'Aggregate sum of reward points (VEs) credited to users during the period',
            'Formula': 'SUM(amount) WHERE status = "credited" AND reward_unit = "VEs"',
            'Required Fields': 'amount, status, reward_unit, credited_at',
            'Data Source': 'Rewards',
            'Frequency': 'Daily / Weekly',
            'Stakeholder': 'CFO / Product Operations',
            'Business Purpose': 'Monitors platform points inflation and monetary liability creation',
            'Interpretation': 'Must scale proportionally with partner ad revenue; unbacked growth indicates exploitation',
            'Limitation': 'Does not measure when the rewards will be liquidated via cash withdrawals',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Reward Reversal Rate',
            'Definition': 'Percentage of issued reward records that are subsequently cancelled, clawed back, or reversed',
            'Formula': '(COUNT(reward_id WHERE status = "reversed") / COUNT(reward_id)) * 100',
            'Required Fields': 'reward_id, status',
            'Data Source': 'Rewards',
            'Frequency': 'Weekly / Monthly',
            'Stakeholder': 'Risk & Fraud Operations',
            'Business Purpose': 'Monitors affiliate partner postback reversals and chargeback clawbacks',
            'Interpretation': 'A rate above 2% signals fraudulent offerwall activity, VPN spoofing, or partner discrepancies',
            'Limitation': 'Reversals often arrive 14-30 days post-issuance from external affiliate networks',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Reward Distribution by Feature',
            'Definition': 'Percentage share of total points credited broken down by reward source type',
            'Formula': '(SUM(amount WHERE reward_type = [TYPE]) / SUM(amount)) * 100',
            'Required Fields': 'amount, reward_type, status',
            'Data Source': 'Rewards',
            'Frequency': 'Weekly',
            'Stakeholder': 'Product Economist / PM',
            'Business Purpose': 'Identifies which product mechanics dominate the company points liability',
            'Interpretation': 'Highlights over-reliance on low-margin minigames versus high-margin surveys/offers',
            'Limitation': 'Does not reflect partner margin differentials between reward types',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Average Reward per Active User (ARPAU)',
            'Definition': 'Mean points credited per daily active user in a given time period',
            'Formula': 'SUM(amount WHERE status = "credited") / COUNT(DISTINCT user_id in DAU)',
            'Required Fields': 'amount, user_id, credited_at',
            'Data Source': 'Rewards, Feature_Events',
            'Frequency': 'Daily / Weekly',
            'Stakeholder': 'Product Economist',
            'Business Purpose': 'Evaluates earning density and incentive competitiveness against rival reward apps',
            'Interpretation': 'Healthy balance ensures attractive earning speed without bankrupting unit economics',
            'Limitation': 'Can be skewed by top 1% survey grinders',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Pending Reward Escrow Ratio',
            'Definition': 'Proportion of total rewards held in pending verification state relative to posted rewards',
            'Formula': '(SUM(amount WHERE status = "pending") / SUM(amount WHERE status = "credited")) * 100',
            'Required Fields': 'amount, status',
            'Data Source': 'Rewards',
            'Frequency': 'Daily',
            'Stakeholder': 'Risk & Finance',
            'Business Purpose': 'Monitors pending escrow buffer protecting against unverified affiliate claims',
            'Interpretation': 'Spikes indicate backlog in manual review or delayed third-party postbacks',
            'Limitation': 'Does not indicate the probability of eventual release vs rejection',
            'Status': 'Proposed'
        },
        # Wallet KPIs (17-21)
        {
            'KPI Name': 'Total Wallet Transaction Volume',
            'Definition': 'Gross count of financial ledger entries processed across all transaction types',
            'Formula': 'COUNT(transaction_id) WHERE timestamp BETWEEN start_date AND end_date',
            'Required Fields': 'transaction_id, timestamp',
            'Data Source': 'Wallet',
            'Frequency': 'Daily',
            'Stakeholder': 'Engineering / Backend Infrastructure',
            'Business Purpose': 'Monitors database ledger throughput and concurrency scaling',
            'Interpretation': 'Surges indicate high platform engagement or infinite-loop transaction bugs',
            'Limitation': 'Does not measure monetary value, only ledger row count',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Circulating VE Supply',
            'Definition': 'Total outstanding points balance held in user wallets that have not been redeemed or burned',
            'Formula': 'SUM(amount WHERE unit = "VEs" AND status = "completed")',
            'Required Fields': 'amount, unit, status',
            'Data Source': 'Wallet',
            'Frequency': 'Daily snapshot',
            'Stakeholder': 'CFO / Finance Lead',
            'Business Purpose': 'Measures current balance-sheet liability owed to the user base',
            'Interpretation': 'Monitors potential run-on-the-bank liquidity risk if redemption velocity spikes',
            'Limitation': 'Includes dormant user balances that may never be redeemed (breakage)',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Redemption Velocity Ratio',
            'Definition': 'Proportion of newly credited points that are liquidated via withdrawals within 30 days',
            'Formula': '(SUM(ABS(amount) WHERE transaction_type = "withdrawal_debit") / SUM(amount WHERE transaction_type = "reward_credit")) * 100',
            'Required Fields': 'amount, transaction_type, status',
            'Data Source': 'Wallet',
            'Frequency': 'Monthly',
            'Stakeholder': 'Finance / Product Strategy',
            'Business Purpose': 'Key metric for unit economics: determines platform cash drain speed',
            'Interpretation': 'A ratio > 80% means high liquidity pressure; a ratio < 40% suggests high token retention / breakage',
            'Limitation': 'Subject to withdrawal minimum payout thresholds delaying redemption',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Wallet Reversal Rate',
            'Definition': 'Percentage of completed wallet transactions that require reversal due to errors or fraud',
            'Formula': '(COUNT(transaction_id WHERE status = "reversed") / COUNT(transaction_id)) * 100',
            'Required Fields': 'transaction_id, status',
            'Data Source': 'Wallet',
            'Frequency': 'Weekly',
            'Stakeholder': 'Operations & Finance',
            'Business Purpose': 'Measures transactional integrity and manual intervention overhead',
            'Interpretation': 'High reversals point to buggy withdrawal rails or faulty reward calculations',
            'Limitation': 'Does not measure the elapsed duration between initial entry and reversal',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Token Exchange Velocity',
            'Definition': 'Volume of VEs converted into on-chain Tokens or secondary game Gems',
            'Formula': 'SUM(ABS(amount) WHERE transaction_type = "token_exchange")',
            'Required Fields': 'amount, transaction_type, status',
            'Data Source': 'Wallet',
            'Frequency': 'Weekly',
            'Stakeholder': 'Tokenomics / Web3 Lead',
            'Business Purpose': 'Measures internal ecosystem liquidity and adoption of secondary tokens',
            'Interpretation': 'Higher internal conversion reduces immediate fiat cash drain from bank accounts',
            'Limitation': 'Dependent on the attractiveness of secondary token utility',
            'Status': 'Proposed'
        },
        # Withdrawal KPIs (22-28)
        {
            'KPI Name': 'Withdrawal Request Volume',
            'Definition': 'Total count of formal payout cash-out submissions made by users',
            'Formula': 'COUNT(withdrawal_id) WHERE requested_timestamp BETWEEN start_date AND end_date',
            'Required Fields': 'withdrawal_id, requested_timestamp',
            'Data Source': 'Withdrawals',
            'Frequency': 'Daily / Weekly',
            'Stakeholder': 'Payment Operations / Finance',
            'Business Purpose': 'Monitors cash-out demand queue and liquidity requirements',
            'Interpretation': 'Surges occur near month-end or following major marketing referral payouts',
            'Limitation': 'Includes fraudulent or invalid requests that will eventually be rejected',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Completed Withdrawal Rate',
            'Definition': 'Percentage of total submitted withdrawal requests that successfully settle with payment confirmation',
            'Formula': '(COUNT(withdrawal_id WHERE status = "completed") / COUNT(withdrawal_id)) * 100',
            'Required Fields': 'withdrawal_id, status',
            'Data Source': 'Withdrawals',
            'Frequency': 'Weekly / Monthly',
            'Stakeholder': 'VP Product / Finance',
            'Business Purpose': 'Core reliability metric for payout infrastructure; primary driver of user trust',
            'Interpretation': 'Target is >90% for legitimate users; dips signal gateway outage or fraud spikes',
            'Limitation': 'Influenced by fraud blocking policies which legitimately decrease the rate',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Pending Withdrawal Queue Count',
            'Definition': 'Number of withdrawal requests currently awaiting review or gateway processing',
            'Formula': 'COUNT(withdrawal_id WHERE status IN ("requested", "processing"))',
            'Required Fields': 'withdrawal_id, status',
            'Data Source': 'Withdrawals',
            'Frequency': 'Real-time / Daily',
            'Stakeholder': 'Payment Operations Manager',
            'Business Purpose': 'Operational queue monitoring to prevent review bottlenecks',
            'Interpretation': 'Growing backlog indicates manual review under-staffing or payment API rate limits',
            'Limitation': 'Does not indicate monetary value of the backlog queue',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Average Withdrawal Processing Duration',
            'Definition': 'Mean elapsed time in hours from initial user request to terminal completion',
            'Formula': 'AVG(EXTRACT(EPOCH FROM (final_timestamp - requested_timestamp)) / 3600) WHERE status = "completed"',
            'Required Fields': 'requested_timestamp, final_timestamp, status',
            'Data Source': 'Withdrawals',
            'Frequency': 'Daily / Weekly',
            'Stakeholder': 'Payment Operations / UX PM',
            'Business Purpose': 'Customer satisfaction metric; benchmarks cash-out speed against competitors',
            'Interpretation': 'Shorter duration increases user trust and repeat engagement',
            'Limitation': 'Masks variation between automated gift cards (minutes) and wire transfers (days)',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Withdrawal Rejection Rate',
            'Definition': 'Percentage of withdrawal requests that are denied due to fraud, KYC failure, or threshold breach',
            'Formula': '(COUNT(withdrawal_id WHERE status = "rejected") / COUNT(withdrawal_id)) * 100',
            'Required Fields': 'withdrawal_id, status',
            'Data Source': 'Withdrawals',
            'Frequency': 'Weekly',
            'Stakeholder': 'Risk & Fraud Operations',
            'Business Purpose': 'Quantifies fraud prevention volume and user onboarding friction',
            'Interpretation': 'Spikes indicate automated bot farm attacks attempting to cash out illicit balances',
            'Limitation': 'Legitimate users facing incorrect KYC rejection will also inflate this metric',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Withdrawal Payout Volume (Fiat Equiv)',
            'Definition': 'Total value of points successfully disbursed to users through payment gateways',
            'Formula': 'SUM(requested_amount WHERE status = "completed")',
            'Required Fields': 'requested_amount, status, final_timestamp',
            'Data Source': 'Withdrawals',
            'Frequency': 'Daily / Weekly / Monthly',
            'Stakeholder': 'CFO / Finance Director',
            'Business Purpose': 'Direct cash outflow monitoring; treasury management',
            'Interpretation': 'Must be covered by collected ad network receivables and reserve capital',
            'Limitation': 'Does not include gateway transaction processing fees',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Withdrawal Method Distribution',
            'Definition': 'Percentage share of completed payouts processed per payment rail (PayPal, USDT, Gift Card, Bank)',
            'Formula': '(COUNT(withdrawal_id WHERE withdrawal_method = [METHOD]) / COUNT(withdrawal_id)) * 100',
            'Required Fields': 'withdrawal_method, status',
            'Data Source': 'Withdrawals',
            'Frequency': 'Monthly',
            'Stakeholder': 'Payment Operations',
            'Business Purpose': 'Treasury allocation and partner rail fee optimization',
            'Interpretation': 'Directs corporate treasury to maintain sufficient float across specific payout channels',
            'Limitation': 'Constrained by country-specific availability of certain rails',
            'Status': 'Proposed'
        },
        # Referral KPIs (29-32)
        {
            'KPI Name': 'Referral Invites Created',
            'Definition': 'Total number of personal referral invite links generated by existing users',
            'Formula': 'COUNT(referral_id) WHERE creation_timestamp BETWEEN start_date AND end_date',
            'Required Fields': 'referral_id, creation_timestamp',
            'Data Source': 'Referrals',
            'Frequency': 'Weekly',
            'Stakeholder': 'Growth Product Manager',
            'Business Purpose': 'Top of viral growth loop; measures user willingness to advocate for the app',
            'Interpretation': 'Higher sharing indicates strong product enthusiasm and perceived referral reward value',
            'Limitation': 'Does not guarantee that the link was actually received or clicked by an external recipient',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Referral Registration Conversion Rate',
            'Definition': 'Percentage of created referral links that result in a successfully registered referee account',
            'Formula': '(COUNT(referral_id WHERE status IN ("registered", "activated", "converted")) / COUNT(referral_id)) * 100',
            'Required Fields': 'referral_id, status',
            'Data Source': 'Referrals',
            'Frequency': 'Weekly',
            'Stakeholder': 'Growth Team',
            'Business Purpose': 'Measures viral landing page appeal and friction in referee signup',
            'Interpretation': 'A low rate suggests weak recipient value proposition or broken deep-linking',
            'Limitation': 'Referees who sign up without deep-link attribution escape tracking',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Referral Activation Rate',
            'Definition': 'Percentage of registered referees who complete their first qualifying earning task',
            'Formula': '(COUNT(referral_id WHERE status IN ("activated", "converted")) / COUNT(referral_id WHERE status IN ("registered", "activated", "converted"))) * 100',
            'Required Fields': 'referral_id, status',
            'Data Source': 'Referrals',
            'Frequency': 'Weekly',
            'Stakeholder': 'Growth & Product PM',
            'Business Purpose': 'Distinguishes between vanity signups and genuine engaged viral users',
            'Interpretation': 'Higher activation proves that the referral messaging attracted genuine target users',
            'Limitation': 'Vulnerable to incentivized self-referral ring manipulation',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Viral Coefficient (K-Factor)',
            'Definition': 'Average number of active new referees generated by each existing active user',
            'Formula': '(Total Invites Sent / Total Users) * (Activated Referees / Total Invites Sent)',
            'Required Fields': 'referring_user_id, referred_user_id, status',
            'Data Source': 'Referrals, Users',
            'Frequency': 'Monthly',
            'Stakeholder': 'Head of Growth / Leadership',
            'Business Purpose': 'Measures viral compounding effect and organic growth sustainability',
            'Interpretation': 'K > 1.0 implies exponential self-sustaining growth; K < 1.0 requires paid marketing reinforcement',
            'Limitation': 'Difficult to measure accurately without long tracking windows and mature attribution models',
            'Status': 'Proposed'
        },
        # Support & Content KPIs (33-35)
        {
            'KPI Name': 'Support Request Volume per 1,000 DAU',
            'Definition': 'Normalized rate of support tickets filed per 1,000 daily active users',
            'Formula': '(COUNT(ticket_id) / (DAU / 1000))',
            'Required Fields': 'ticket_id, timestamp, DAU',
            'Data Source': 'Support Tickets, Feature_Events',
            'Frequency': 'Weekly',
            'Stakeholder': 'Customer Support Lead / Product Ops',
            'Business Purpose': 'Monitors product friction and customer support operational burden',
            'Interpretation': 'Spikes indicate bug outbreaks, delayed withdrawal batching, or confusing task rules',
            'Limitation': 'Only captures users who bother to file formal tickets rather than churning silently',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Support Ticket Category Distribution',
            'Definition': 'Percentage breakdown of user inquiries by root issue (Withdrawals, Missing Points, KYC, Tech)',
            'Formula': '(COUNT(ticket_id WHERE category = [CAT]) / COUNT(ticket_id)) * 100',
            'Required Fields': 'ticket_id, issue_category',
            'Data Source': 'Support Tickets',
            'Frequency': 'Weekly / Monthly',
            'Stakeholder': 'Product & Engineering Leads',
            'Business Purpose': 'Prioritizes engineering bug fixes and self-serve FAQ documentation updates',
            'Interpretation': 'If withdrawals dominate (>50%), payout transparency in the UI must be urgently redesigned',
            'Limitation': 'Subject to subjective categorization by frontline support agents',
            'Status': 'Proposed'
        },
        {
            'KPI Name': 'Help Center Article Self-Serve Deflection Rate',
            'Definition': 'Percentage of users who view a help article and do not subsequently submit a ticket within 24 hours',
            'Formula': '(COUNT(article_views without ticket in 24h) / Total Article Views) * 100',
            'Required Fields': 'user_id, timestamp, event_name',
            'Data Source': 'Feature_Events, Support Tickets',
            'Frequency': 'Monthly',
            'Stakeholder': 'Content & Support Operations',
            'Business Purpose': 'Measures the effectiveness of help documentation in deflecting expensive support contacts',
            'Interpretation': 'Higher deflection indicates clear, actionable troubleshooting guides',
            'Limitation': 'Users who give up entirely out of frustration are misclassified as deflected',
            'Status': 'Proposed'
        }
    ]
    df_kpi = pd.DataFrame(kpi_rows)
    print(f"Total KPIs in Catalogue: {len(df_kpi)}")
    df_kpi.to_csv(os.path.join(out_dir, '11_KPI_CATALOGUE.csv'), index=False)

    # =========================================================================
    # DELIVERABLE 19: ASSUMPTION & VERIFICATION REGISTER
    # =========================================================================
    print("Generating Deliverable 19: Assumption & Verification Register...")
    assumption_rows = [
        {
            'ID': 'A001',
            'Unknown': 'Does the backend currently emit distinct task_completed events separate from ledger rewards?',
            'Why It Matters': 'Critical for distinguishing task execution success from monetary settlement',
            'Source Checked': 'Product Docs / Simulated Schema',
            'Risk': 'High',
            'Verification Owner': 'Backend Engineering',
            'Status': 'To Be Verified'
        },
        {
            'ID': 'A002',
            'Unknown': 'What is the precise conversion peg rate between VEs and cash withdrawal amounts?',
            'Why It Matters': 'Required for financial liability calculations, unit economics, and withdrawal KPIs',
            'Source Checked': 'Product Documentation',
            'Risk': 'Critical',
            'Verification Owner': 'Product Economics / Finance',
            'Status': 'To Be Verified'
        },
        {
            'ID': 'A003',
            'Unknown': 'Are session IDs generated and maintained persistently across mobile app restarts?',
            'Why It Matters': 'Essential for session duration, bounce rate, and session-level analytics',
            'Source Checked': 'Client Mobile Telemetry',
            'Risk': 'High',
            'Verification Owner': 'Mobile SDK Team',
            'Status': 'To Be Verified'
        },
        {
            'ID': 'A004',
            'Unknown': 'Do third-party ad networks (AdMob/IronSource) send client or server postbacks for ad views?',
            'Why It Matters': 'Dictates whether ad view validation occurs on client device or backend webhook',
            'Source Checked': 'Partner Integration Docs',
            'Risk': 'Critical',
            'Verification Owner': 'Ad Operations / Engineering',
            'Status': 'To Be Verified'
        },
        {
            'ID': 'A005',
            'Unknown': 'Are duplicate withdrawal requests debited immediately or held in escrow?',
            'Why It Matters': 'Fundamental to double-entry ledger design and preventing race-condition overdrafts',
            'Source Checked': 'Wallet Architecture Spec',
            'Risk': 'Critical',
            'Verification Owner': 'Ledger Core Team',
            'Status': 'Confirmed'
        },
        {
            'ID': 'A006',
            'Unknown': 'What constitutes the exact qualifying threshold for referral activation?',
            'Why It Matters': 'Prevents gaming of referral bounties by requiring meaningful user activity',
            'Source Checked': 'Growth Strategy Brief',
            'Risk': 'High',
            'Verification Owner': 'Growth Product Manager',
            'Status': 'Proposed'
        },
        {
            'ID': 'A007',
            'Unknown': 'Are streak freeze items purchasable with Gems or earned strictly via daily activity?',
            'Why It Matters': 'Affects sink mechanics in tokenomic modeling',
            'Source Checked': 'Game Economy Design',
            'Risk': 'Medium',
            'Verification Owner': 'Game Designer',
            'Status': 'Proposed'
        },
        {
            'ID': 'A008',
            'Unknown': 'Is KYC mandatory for all withdrawal amounts or only transactions above a dollar threshold?',
            'Why It Matters': 'Determines withdrawal drop-off rate and compliance pipeline volume',
            'Source Checked': 'Compliance Policy',
            'Risk': 'High',
            'Verification Owner': 'Legal & Compliance Lead',
            'Status': 'To Be Verified'
        },
        {
            'ID': 'A009',
            'Unknown': 'Does the client mobile SDK queue telemetry events offline and flush upon reconnection?',
            'Why It Matters': 'If offline queuing exists, event timestamps may significantly lag server ingestion time',
            'Source Checked': 'Mobile Architecture',
            'Risk': 'High',
            'Verification Owner': 'Mobile Lead',
            'Status': 'To Be Verified'
        },
        {
            'ID': 'A010',
            'Unknown': 'What is the server-side deduplication window for client-emitted event IDs?',
            'Why It Matters': 'Ensures rapid double-taps do not cause duplicate reward disbursements',
            'Source Checked': 'API Gateway Spec',
            'Risk': 'Critical',
            'Verification Owner': 'Backend Architecture',
            'Status': 'Proposed'
        }
    ]
    df_assumptions = pd.DataFrame(assumption_rows)
    df_assumptions.to_csv(os.path.join(out_dir, '19_ASSUMPTION_VERIFICATION_REGISTER.csv'), index=False)

    # =========================================================================
    # DELIVERABLE 20: IMPLEMENTATION BACKLOG
    # =========================================================================
    print("Generating Deliverable 20: Implementation Backlog...")
    backlog_rows = [
        {
            'Priority': 'Critical',
            'Requirement': 'Implement Stable Surrogate User ID across all microservices and telemetry',
            'Reason': 'Required for cross-event analysis, user identity resolution, and referential integrity',
            'Dependency': 'Auth Service Architecture',
            'Owner': 'Core Backend Team',
            'Stage': 'Pre-launch'
        },
        {
            'Priority': 'Critical',
            'Requirement': 'Deploy Double-Entry Ledger Transaction ID with Idempotency Constraints',
            'Reason': 'Guarantees transactional integrity, eliminates balance discrepancies, and prevents duplicate credits',
            'Dependency': 'Core Ledger Architecture',
            'Owner': 'Ledger / Backend Engineering',
            'Stage': 'Pre-launch'
        },
        {
            'Priority': 'Critical',
            'Requirement': 'Standardize Event Tracking SDK with Mandatory Event ID and ISO Timestamps',
            'Reason': 'Eliminates malformed dates, missing timestamps, and rapid client duplicate bursts',
            'Dependency': 'Mobile Telemetry SDK',
            'Owner': 'Mobile App / Data Platform',
            'Stage': 'Pre-launch'
        },
        {
            'Priority': 'Critical',
            'Requirement': 'Build Withdrawal State Machine Enforcing Strict State Transitions',
            'Reason': 'Prevents impossible transitions (completed prior to requested) and ensures escrow synchronization',
            'Dependency': 'Withdrawal Engine',
            'Owner': 'Payment Engineering',
            'Stage': 'Pre-launch'
        },
        {
            'Priority': 'High',
            'Requirement': 'Implement Ingestion Gateway Data Quality Filter & Quarantine DLQ',
            'Reason': 'Intercepts invalid statuses, non-numeric values, and un-trimmed strings before database landing',
            'Dependency': 'API Gateway / Kafka Broker',
            'Owner': 'Data Engineering',
            'Stage': 'Pre-launch'
        },
        {
            'Priority': 'High',
            'Requirement': 'Instrument Server-to-Server Affiliate Webhook Ingestion Pipeline',
            'Reason': 'Captures partner postbacks for surveys and offerwalls with validation verification',
            'Dependency': 'Partner Ad Integrations',
            'Owner': 'Ad Operations / Backend',
            'Stage': 'Pre-launch'
        },
        {
            'Priority': 'High',
            'Requirement': 'Establish Referral Attribution & Anti-Fraud Conversion Engine',
            'Reason': 'Enforces distinction between registration and activation; prevents self-referral rings',
            'Dependency': 'Deep-Link Routing SDK',
            'Owner': 'Growth Engineering',
            'Stage': 'Pre-launch'
        },
        {
            'Priority': 'High',
            'Requirement': 'Build Automated dbt Transformation Pipeline for Medallion Layers (Bronze/Silver/Gold)',
            'Reason': 'Automates cleansing, case normalization, and aggregate KPI modeling for BI reporting',
            'Dependency': 'Analytical Data Warehouse',
            'Owner': 'Analytics Engineering',
            'Stage': 'Pre-launch'
        },
        {
            'Priority': 'Medium',
            'Requirement': 'Deploy Core Operational BI Dashboards (Executive, Earning, Withdrawals)',
            'Reason': 'Provides executive leadership and product managers with real-time operational health visibility',
            'Dependency': 'Gold Layer Data Models',
            'Owner': 'BI / Analytics Team',
            'Stage': 'Post-launch'
        },
        {
            'Priority': 'Medium',
            'Requirement': 'Implement Hardware Device Fingerprinting & Proxy Detection Telemetry',
            'Reason': 'Required for advanced multi-account collusion detection and sybil attack mitigation',
            'Dependency': 'Security SDK Integration',
            'Owner': 'Fraud / Security Team',
            'Stage': 'Post-launch'
        },
        {
            'Priority': 'Medium',
            'Requirement': 'Build Automated Data Quality Alerting Bot on Metric Anomalies',
            'Reason': 'Notifies on-call engineers when event drop-offs or failure rates exceed standard deviations',
            'Dependency': 'Observability Infrastructure',
            'Owner': 'Data Platform Team',
            'Stage': 'Post-launch'
        },
        {
            'Priority': 'Low',
            'Requirement': 'Develop Machine Learning Predictive Churn and Lifetime Value (LTV) Models',
            'Reason': 'Optimizes user acquisition bidding and personalized win-back notifications',
            'Dependency': '6 Months of Production Data',
            'Owner': 'Data Science Team',
            'Stage': 'Post-launch'
        }
    ]
    df_backlog = pd.DataFrame(backlog_rows)
    df_backlog.to_csv(os.path.join(out_dir, '20_IMPLEMENTATION_BACKLOG.csv'), index=False)

    # =========================================================================
    # MASTER EXCEL WORKBOOK GENERATION
    # =========================================================================
    master_excel_path = os.path.join('deliverables_tables', 'VELOOP_Analytics_Foundation_Master_Workbook.xlsx')
    print(f"Creating Master Excel Workbook at {master_excel_path}...")
    with pd.ExcelWriter(master_excel_path, engine='openpyxl') as writer:
        df_coverage.to_excel(writer, sheet_name='03_Data_Coverage_Matrix', index=False)
        df_user_spec.to_excel(writer, sheet_name='04_User_Analytics_Spec', index=False)
        df_event_plan.to_excel(writer, sheet_name='08_Event_Tracking_Plan', index=False)
        df_dict.to_excel(writer, sheet_name='09_Data_Dictionary', index=False)
        df_kpi.to_excel(writer, sheet_name='11_KPI_Catalogue', index=False)
        pd.read_csv('data/profiling_summary.csv').to_excel(writer, sheet_name='12_Profiling_Summary', index=False)
        pd.read_csv('data/referential_integrity_test_results.csv').to_excel(writer, sheet_name='12_Referential_Integrity', index=False)
        pd.read_csv('data/data_quality_issue_log.csv').to_excel(writer, sheet_name='13_Data_Quality_Issue_Log', index=False)
        df_assumptions.to_excel(writer, sheet_name='19_Assumptions_Register', index=False)
        df_backlog.to_excel(writer, sheet_name='20_Implementation_Backlog', index=False)
    print("Master Excel Workbook created successfully!")

if __name__ == '__main__':
    generate_specifications()
