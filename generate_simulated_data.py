"""
VELOP REWARDS - SIMULATED DATA GENERATION ENGINE
=================================================
MANDATORY COMPLIANCE HEADER:
SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
This dataset is synthetic/simulated for product analytics readiness, data modelling,
data profiling, and quality testing. It does NOT represent actual VELOOP company statistics,
actual earnings, actual withdrawals, or live production performance.

Methodology:
- Deterministic pseudo-random generation with fixed seed (seed=42) for full reproducibility.
- Models 7 interconnected operational entities plus 1 intentionally corrupted "Messy Data" audit sheet.
- Enforces strict financial accounting invariants:
  1. Opening Balance = 0.00 for all users at registration.
  2. Double-entry ledger sign invariant: Credits > 0, Debits < 0.
  3. No overdrafts: Every user balance remains >= 0.00 at all timestamps.
  4. Positive Circulating Supply: Total Credits > Total Completed Debits.
  5. 100% Referential integrity across all core operational tables.
"""

import os
import random
import datetime
import pandas as pd
import numpy as np

def generate_datasets():
    random.seed(42)
    np.random.seed(42)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    base_date = datetime.datetime(2026, 1, 1, 0, 0, 0)
    end_date = datetime.datetime(2026, 10, 31, 23, 59, 59)
    total_seconds = int((end_date - base_date).total_seconds())

    def random_timestamp():
        offset = random.randint(0, total_seconds)
        return base_date + datetime.timedelta(seconds=offset)

    # ==========================================
    # 1. USERS (1,000 records)
    # ==========================================
    print("Generating Users (1,000 records)...")
    user_ids = [f"USR_{i:05d}" for i in range(1, 1001)]
    reg_sources = ['organic', 'referral', 'paid_ad', 'partner_promo', 'influencer']
    reg_source_weights = [0.35, 0.25, 0.20, 0.12, 0.08]
    campaigns = ['spring_launch_2026', 'summer_boost', 'refer_a_friend_v1', 'creator_code_special', None]
    campaign_weights = [0.25, 0.20, 0.20, 0.15, 0.20]
    platforms = ['Android', 'iOS', 'Web']
    platform_weights = [0.65, 0.28, 0.07]
    countries = ['US', 'GB', 'IN', 'CA', 'DE', 'PH', 'NG', 'BR', 'ID', 'FR']
    country_weights = [0.30, 0.15, 0.18, 0.08, 0.06, 0.08, 0.05, 0.04, 0.04, 0.02]
    statuses = ['active', 'dormant', 'suspended', 'closed']
    status_weights = [0.68, 0.24, 0.05, 0.03]

    users_data = []
    user_reg_map = {}
    for uid in user_ids:
        reg_ts = random_timestamp()
        user_reg_map[uid] = reg_ts
        source = random.choices(reg_sources, weights=reg_source_weights)[0]
        camp = random.choices(campaigns, weights=campaign_weights)[0] if source != 'organic' else None
        plat = random.choices(platforms, weights=platform_weights)[0]
        cntry = random.choices(countries, weights=country_weights)[0]
        status = random.choices(statuses, weights=status_weights)[0]
        
        onboarding_done = random.random() < 0.817 # 81.7% onboarding completion
        if onboarding_done:
            onb_ts = reg_ts + datetime.timedelta(minutes=random.randint(2, 120))
        else:
            onb_ts = None
            
        last_login_offset = random.randint(0, max(1, int((end_date - reg_ts).total_seconds())))
        last_login = reg_ts + datetime.timedelta(seconds=last_login_offset)

        users_data.append({
            'user_id': uid,
            'registration_timestamp': reg_ts.strftime('%Y-%m-%d %H:%M:%S'),
            'registration_source': source,
            'acquisition_campaign': camp if camp else '',
            'device_platform': plat,
            'country_code': cntry,
            'account_status': status,
            'is_onboarding_completed': onboarding_done,
            'onboarding_completed_timestamp': onb_ts.strftime('%Y-%m-%d %H:%M:%S') if onb_ts else '',
            'last_login_timestamp': last_login.strftime('%Y-%m-%d %H:%M:%S')
        })
    df_users = pd.DataFrame(users_data)
    active_user_pool = df_users[df_users['account_status'].isin(['active', 'dormant'])]['user_id'].tolist()

    # ==========================================
    # 2. TASK ACTIVITY (6,000 records)
    # ==========================================
    print("Generating Task Activity (6,000 records)...")
    task_types = ['watch_ad', 'survey', 'tap_earn', 'mining', 'offerwall', 'app_install']
    task_type_weights = [0.40, 0.18, 0.20, 0.10, 0.07, 0.05]
    task_catalog = {
        'watch_ad': ('TK_AD_101', 'AdMob Short Video', 25, 'VEs', 'GoogleAdMob'),
        'survey': ('TK_SURV_201', 'Consumer Opinion Survey', 250, 'VEs', 'Pollfish'),
        'tap_earn': ('TK_TAP_301', 'Daily Energy Tap Session', 40, 'VEs', 'InternalEngine'),
        'mining': ('TK_MINE_401', '6-Hour Cloud Hash Claim', 150, 'VEs', 'InternalEngine'),
        'offerwall': ('TK_OFF_501', 'Reach Level 10 in Castle Quest', 800, 'VEs', 'Tapjoy'),
        'app_install': ('TK_APP_601', 'Download & Open FinApp', 450, 'VEs', 'IronSource')
    }
    
    # 4,357 completed (72.62%), 728 failed (12.13%), 630 abandoned (10.50%), 285 pending (4.75%)
    exact_statuses = (
        ['completed'] * 4357 +
        ['failed'] * 728 +
        ['abandoned'] * 630 +
        ['pending_validation'] * 285
    )
    random.shuffle(exact_statuses)

    task_activity_data = []
    for i in range(1, 6001):
        uid = random.choice(active_user_pool)
        user_reg = user_reg_map[uid]
        sec_avail = max(1, int((end_date - user_reg).total_seconds()))
        start_ts = user_reg + datetime.timedelta(seconds=random.randint(0, sec_avail))
        
        ttype = random.choices(task_types, weights=task_type_weights)[0]
        tid, fcat, r_amt, r_unit, partner = task_catalog[ttype]
        status = exact_statuses[i - 1]
        
        if status in ['completed', 'failed']:
            dur_mins = random.randint(1, 45) if ttype != 'mining' else random.randint(360, 420)
            comp_ts = start_ts + datetime.timedelta(minutes=dur_mins)
            val_status = 'validated' if status == 'completed' else 'rejected'
            err_reason = '' if status == 'completed' else random.choice(['timeout', 'bot_detected', 'screening_failed'])
        elif status == 'abandoned':
            comp_ts = start_ts + datetime.timedelta(minutes=random.randint(1, 5))
            val_status = 'rejected'
            err_reason = 'user_cancelled'
        else: # pending_validation
            comp_ts = None
            val_status = 'pending'
            err_reason = ''

        task_activity_data.append({
            'task_activity_id': f"ACT_{i:06d}",
            'task_id': tid,
            'task_type': ttype,
            'feature_category': fcat,
            'user_id': uid,
            'started_at': start_ts.strftime('%Y-%m-%d %H:%M:%S'),
            'completed_at': comp_ts.strftime('%Y-%m-%d %H:%M:%S') if comp_ts else '',
            'status': status,
            'reward_amount': r_amt,
            'reward_unit': r_unit,
            'validation_status': val_status,
            'partner_provider': partner,
            'error_reason': err_reason
        })
    df_task_activity = pd.DataFrame(task_activity_data)

    # ==========================================
    # 3. REWARDS (5,000 records)
    # ==========================================
    print("Generating Rewards (5,000 records)...")
    reward_types = ['task_completion', 'daily_login', 'streak_bonus', 'referral_bonus', 'spin_wheel', 'badge_milestone']
    reward_weights = [0.60, 0.15, 0.08, 0.07, 0.06, 0.04]
    
    # 4,638 credited (92.76%), 202 pending (4.04%), 160 reversed (3.20%)
    exact_reward_statuses = (
        ['credited'] * 4638 +
        ['pending'] * 202 +
        ['reversed'] * 160
    )
    random.shuffle(exact_reward_statuses)

    completed_tasks = df_task_activity[df_task_activity['validation_status'] == 'validated'].to_dict('records')
    random.shuffle(completed_tasks)
    task_idx = 0

    rewards_data = []
    user_rewards_map = {uid: [] for uid in df_users['user_id']}

    for i in range(1, 5001):
        rtype = random.choices(reward_types, weights=reward_weights)[0]
        r_status = exact_reward_statuses[i - 1]
        
        if rtype == 'task_completion' and task_idx < len(completed_tasks):
            t_row = completed_tasks[task_idx]
            task_idx += 1
            uid = t_row['user_id']
            task_ref = t_row['task_activity_id']
            amt = t_row['reward_amount']
            unit = t_row['reward_unit']
            base_ts = datetime.datetime.strptime(t_row['completed_at'], '%Y-%m-%d %H:%M:%S')
            credit_ts = base_ts + datetime.timedelta(seconds=random.randint(1, 30))
        else:
            uid = random.choice(active_user_pool)
            task_ref = ''
            user_reg = user_reg_map[uid]
            sec_avail = max(1, int((end_date - user_reg).total_seconds()))
            credit_ts = user_reg + datetime.timedelta(seconds=random.randint(0, sec_avail))
            if rtype == 'daily_login':
                amt, unit = 50, 'VEs'
            elif rtype == 'streak_bonus':
                amt, unit = 200, 'VEs'
            elif rtype == 'referral_bonus':
                amt, unit = 300, 'VEs'
            elif rtype == 'spin_wheel':
                amt, unit = random.choice([50, 100, 250, 500]), 'VEs'
            else: # badge_milestone
                amt, unit = 500, 'XP'

        correction_id = f"RWD_{random.randint(1, max(1, i-1)):05d}" if r_status == 'reversed' else ''

        rwd_entry = {
            'reward_id': f"RWD_{i:05d}",
            'user_id': uid,
            'task_activity_id': task_ref,
            'reward_type': rtype,
            'amount': amt,
            'reward_unit': unit,
            'status': r_status,
            'credited_at': credit_ts.strftime('%Y-%m-%d %H:%M:%S'),
            'ledger_status': 'posted' if r_status == 'credited' else ('reversed' if r_status == 'reversed' else 'pending'),
            'correction_reference_id': correction_id
        }
        rewards_data.append(rwd_entry)
        if r_status == 'credited' and unit == 'VEs':
            user_rewards_map[uid].append(rwd_entry)

    df_rewards = pd.DataFrame(rewards_data)

    # ==========================================
    # 4 & 5. WITHDRAWALS (1,200) & WALLET (3,500)
    # CO-GENERATED WITH STRICT BALANCE CONSTRAINTS
    # ==========================================
    print("Co-generating Withdrawals (1,200) and Wallet Ledger (3,500) with Balance Invariants...")
    
    # Track chronological user ledger state:
    # Opening Balance = 0.00. Running balance >= 0.00 at all times.
    user_txns = {uid: [] for uid in df_users['user_id']}

    # Post credited rewards into ledger history first
    credited_rewards = df_rewards[(df_rewards['status'] == 'credited') & (df_rewards['reward_unit'] == 'VEs')].to_dict('records')
    # Sort chronologically
    credited_rewards.sort(key=lambda x: x['credited_at'])

    # We need 2,280 reward credits in Wallet.
    # Take the first 2,280 sorted credited rewards
    selected_reward_credits = credited_rewards[:2280]
    
    for r in selected_reward_credits:
        uid = r['user_id']
        amt = float(r['amount'])
        user_txns[uid].append({
            'timestamp': pd.to_datetime(r['credited_at']),
            'transaction_type': 'reward_credit',
            'amount': amt,
            'unit': 'VEs',
            'status': 'completed',
            'source': 'reward_engine',
            'reference_id': r['reward_id']
        })

    def is_safe_debit(uid, ts_debit, debit_amt):
        test_list = user_txns[uid] + [{'timestamp': ts_debit, 'amount': -debit_amt, 'status': 'completed'}]
        test_list.sort(key=lambda x: x['timestamp'])
        bal = 0.0
        for t in test_list:
            if t['status'] == 'completed':
                bal += t['amount']
                if bal < 0:
                    return False
        return True

    # Prepare Withdrawals (1,200 records)
    wdr_methods = ['PayPal', 'Crypto_USDT', 'GiftCard_Amazon', 'BankTransfer']
    wdr_method_weights = [0.45, 0.28, 0.18, 0.09]
    rejection_reasons = ['KYC_incomplete', 'minimum_threshold_not_met', 'suspected_fraud', 'third_party_provider_error', 'account_mismatch']
    
    # 882 completed (73.5%), 164 rejected (13.67%), 125 processing (10.42%), 29 reversed (2.42%)
    exact_wdr_statuses = (
        ['completed'] * 882 +
        ['rejected'] * 164 +
        ['processing'] * 125 +
        ['reversed'] * 29
    )
    random.shuffle(exact_wdr_statuses)

    earners = [uid for uid, txs in user_txns.items() if len(txs) > 0]
    withdrawals_data = []
    rejected_refund_count = 0

    for i in range(1, 1201):
        status = exact_wdr_statuses[i - 1]
        
        found_user = False
        for attempt in range(50):
            uid = random.choice(earners)
            credits = [t for t in user_txns[uid] if t['transaction_type'] == 'reward_credit']
            anchor = random.choice(credits)
            req_ts = anchor['timestamp'] + datetime.timedelta(hours=random.randint(1, 120))
            if req_ts > end_date:
                req_ts = end_date - datetime.timedelta(hours=random.randint(1, 48))
            proc_ts = req_ts + datetime.timedelta(hours=random.randint(1, 24))
            final_ts = proc_ts + datetime.timedelta(hours=random.randint(2, 48))
            if final_ts > end_date:
                final_ts = end_date
                
            for candidate_amt in [150.0, 100.0, 75.0, 50.0, 25.0, 15.0]:
                if is_safe_debit(uid, final_ts, candidate_amt):
                    amt = candidate_amt
                    found_user = True
                    break
            if found_user:
                break
                
        if not found_user:
            uid = random.choice(earners)
            req_ts = pd.to_datetime('2026-06-01 12:00:00') + datetime.timedelta(days=random.randint(0, 120))
            proc_ts = req_ts + datetime.timedelta(hours=2)
            final_ts = proc_ts + datetime.timedelta(hours=4)
            amt = 25.0
            user_txns[uid].append({
                'timestamp': req_ts - datetime.timedelta(hours=2),
                'amount': 100.0,
                'transaction_type': 'reward_credit',
                'status': 'completed',
                'reference_id': f"RWD_PAD_{i:04d}",
                'source': 'reward_engine',
                'unit': 'VEs'
            })

        method = random.choices(wdr_methods, weights=wdr_method_weights)[0]

        if status == 'completed':
            rej_reason = ''
            tx_hash = f"HASH_{random.randint(10000000, 99999999):X}"
            user_txns[uid].append({
                'timestamp': final_ts,
                'amount': -amt,
                'transaction_type': 'withdrawal_debit',
                'status': 'completed',
                'reference_id': f"WDR_{i:04d}",
                'source': 'withdrawal_engine',
                'unit': 'VEs'
            })
            
        elif status == 'rejected':
            rej_reason = random.choice(rejection_reasons)
            tx_hash = ''
            if rejected_refund_count < 33:
                rejected_refund_count += 1
                refund_ts = final_ts + datetime.timedelta(minutes=30)
                user_txns[uid].append({
                    'timestamp': refund_ts,
                    'amount': amt,
                    'transaction_type': 'withdrawal_refund',
                    'status': 'completed',
                    'reference_id': f"WDR_{i:04d}",
                    'source': 'withdrawal_engine',
                    'unit': 'VEs'
                })
                
        elif status == 'reversed':
            rej_reason = 'provider_payout_failed_reversed'
            tx_hash = ''
            refund_ts = final_ts + datetime.timedelta(minutes=60)
            user_txns[uid].append({
                'timestamp': refund_ts,
                'amount': amt,
                'transaction_type': 'withdrawal_refund',
                'status': 'completed',
                'reference_id': f"WDR_{i:04d}",
                'source': 'withdrawal_engine',
                'unit': 'VEs'
            })
            
        else: # processing (escrow locked)
            final_ts = None
            rej_reason = ''
            tx_hash = ''

        withdrawals_data.append({
            'withdrawal_id': f"WDR_{i:04d}",
            'user_id': uid,
            'requested_amount': amt,
            'currency_unit': 'VEs',
            'withdrawal_method': method,
            'requested_timestamp': req_ts.strftime('%Y-%m-%d %H:%M:%S'),
            'processing_timestamp': proc_ts.strftime('%Y-%m-%d %H:%M:%S'),
            'final_timestamp': final_ts.strftime('%Y-%m-%d %H:%M:%S') if final_ts else '',
            'status': status,
            'rejection_reason_category': rej_reason,
            'payout_reference_hash': tx_hash,
            'fee_amount': round(amt * 0.02, 2)
        })
    df_withdrawals = pd.DataFrame(withdrawals_data)

    # 3. Add Token Exchanges and Admin Adjustments to reach exactly 3,500 entries
    current_entries = sum(len(txs) for txs in user_txns.values())
    admin_adj_target = 66
    needed_exchanges = 3500 - current_entries - admin_adj_target

    token_exchange_count = 0
    while token_exchange_count < needed_exchanges:
        uid = random.choice(earners)
        tx_ts = pd.to_datetime('2026-06-01 00:00:00') + datetime.timedelta(days=random.randint(0, 150))
        for swap_amt in [25.0, 15.0, 10.0, 5.0]:
            if is_safe_debit(uid, tx_ts, swap_amt):
                user_txns[uid].append({
                    'timestamp': tx_ts,
                    'amount': -swap_amt,
                    'transaction_type': 'token_exchange',
                    'status': 'completed',
                    'source': 'exchange_service',
                    'reference_id': f"EXC_{token_exchange_count+1:05d}",
                    'unit': 'VEs'
                })
                token_exchange_count += 1
                break

    # 4. Generate 66 Admin Adjustments
    for adj_idx in range(admin_adj_target):
        uid = random.choice(earners)
        tx_ts = pd.to_datetime('2026-05-01 00:00:00') + datetime.timedelta(days=random.randint(0, 150))
        user_txns[uid].append({
            'timestamp': tx_ts,
            'amount': 25.0,
            'transaction_type': 'admin_adjustment',
            'status': 'completed',
            'source': 'customer_support',
            'reference_id': f"ADJ_{adj_idx+1:05d}",
            'unit': 'VEs'
        })

    all_wallet_entries = []
    for uid, txs in user_txns.items():
        for t in txs:
            t['user_id'] = uid
            t['timestamp'] = t['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            all_wallet_entries.append(t)

    assert len(all_wallet_entries) == 3500, f"Expected 3500 wallet rows, got {len(all_wallet_entries)}"
    all_wallet_entries.sort(key=lambda x: x['timestamp'])

    # 5. Reverse 36 safe debit transactions with parent relationships (reversing a debit only increases balance!)
    wallet_final = []
    debit_indices = [idx for idx, e in enumerate(all_wallet_entries, start=1) if idx > 10 and e['amount'] < 0]
    reversed_indices = set(random.sample(debit_indices, 36))

    for idx, e in enumerate(all_wallet_entries, start=1):
        status = 'reversed' if idx in reversed_indices else e['status']
        rev_id = f"TXN_{random.randint(1, idx-1):06d}" if status == 'reversed' else ''
        
        wallet_final.append({
            'transaction_id': f"TXN_{idx:06d}",
            'user_id': e['user_id'],
            'timestamp': e['timestamp'],
            'transaction_type': e['transaction_type'],
            'amount': e['amount'],
            'unit': e['unit'],
            'status': status,
            'source': e['source'],
            'reference_id': e['reference_id'],
            'reversal_relationship_id': rev_id
        })
    df_wallet = pd.DataFrame(wallet_final)

    # ==========================================
    # 6. REFERRALS (900 records)
    # ==========================================
    print("Generating Referrals (900 records)...")
    channels = ['WhatsApp', 'Telegram', 'Twitter', 'DirectLink', 'SMS']
    channel_weights = [0.38, 0.28, 0.16, 0.12, 0.06]
    
    # 370 converted (41.11%), 190 activated (21.11%), 200 registered (22.22%), 140 link_created (15.56%)
    exact_ref_statuses = (
        ['converted'] * 370 +
        ['activated'] * 190 +
        ['registered'] * 200 +
        ['link_created'] * 140
    )
    random.shuffle(exact_ref_statuses)

    referrals_data = []
    registered_referrals = df_users[df_users['registration_source'] == 'referral']['user_id'].tolist()
    reg_ref_idx = 0

    for i in range(1, 901):
        ref_by = random.choice(active_user_pool)
        create_ts = random_timestamp()
        channel = random.choices(channels, weights=channel_weights)[0]
        r_stat = exact_ref_statuses[i - 1]
        
        if r_stat in ['registered', 'activated', 'converted']:
            if reg_ref_idx < len(registered_referrals):
                ref_user = registered_referrals[reg_ref_idx]
                reg_ref_idx += 1
            else:
                ref_user = random.choice(active_user_pool)
            reg_ts = create_ts + datetime.timedelta(hours=random.randint(1, 72))
        else:
            ref_user = ''
            reg_ts = None
            
        if r_stat in ['activated', 'converted'] and reg_ts:
            act_ts = reg_ts + datetime.timedelta(hours=random.randint(1, 48))
        else:
            act_ts = None
            
        conv_flag = (r_stat == 'converted')

        referrals_data.append({
            'referral_id': f"REF_{i:04d}",
            'referring_user_id': ref_by,
            'referred_user_id': ref_user,
            'invite_channel': channel,
            'creation_timestamp': create_ts.strftime('%Y-%m-%d %H:%M:%S'),
            'registration_timestamp': reg_ts.strftime('%Y-%m-%d %H:%M:%S') if reg_ts else '',
            'activation_timestamp': act_ts.strftime('%Y-%m-%d %H:%M:%S') if act_ts else '',
            'status': r_stat,
            'reward_credited_to_referrer': conv_flag,
            'attribution_source': 'campaign_share_sheet'
        })
    df_referrals = pd.DataFrame(referrals_data)

    # ==========================================
    # 7. FEATURE EVENTS (12,000 records)
    # ==========================================
    print("Generating Feature Events (12,000 records)...")
    event_names = [
        'daily_reward_claimed', 'streak_updated', 'spin_started', 'spin_completed',
        'mission_started', 'mission_completed', 'badge_earned', 'wallet_viewed',
        'help_article_viewed', 'onboarding_milestone'
    ]
    event_weights = [0.22, 0.18, 0.14, 0.13, 0.10, 0.08, 0.05, 0.04, 0.03, 0.03]

    feature_events_data = []
    for i in range(1, 12001):
        uid = random.choice(active_user_pool)
        user_reg = user_reg_map[uid]
        sec_avail = max(1, int((end_date - user_reg).total_seconds()))
        ts = user_reg + datetime.timedelta(seconds=random.randint(0, sec_avail))
        
        ename = random.choices(event_names, weights=event_weights)[0]
        session_id = f"SES_{random.randint(100000, 999999)}"
        platform = random.choices(platforms, weights=platform_weights)[0]
        
        feature_events_data.append({
            'event_id': f"EVT_{i:06d}",
            'user_id': uid,
            'session_id': session_id,
            'event_name': ename,
            'feature_domain': 'engagement' if 'streak' in ename or 'daily' in ename or 'spin' in ename else ('gamification' if 'badge' in ename or 'mission' in ename else 'support'),
            'timestamp': ts.strftime('%Y-%m-%d %H:%M:%S'),
            'device_platform': platform,
            'status': 'success'
        })
    df_feature_events = pd.DataFrame(feature_events_data)

    # ==========================================
    # 8. MESSY DATA (550 records, 14 categories)
    # ==========================================
    print("Generating Messy Data (550 records with deliberate data quality anomalies)...")
    messy_records = []

    # Category 1: Duplicate IDs (30 records)
    for i in range(1, 31):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': 'USR_00100',
            'timestamp': '2026-05-10 14:22:10',
            'event_name': 'task_completed',
            'amount': 50,
            'status': 'completed',
            'platform': 'Android',
            'category': 'Earning',
            'issue_tag': 'duplicate_id'
        })

    # Category 2: Missing IDs (25 records)
    for i in range(31, 56):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': None,
            'timestamp': '2026-05-11 09:12:00',
            'event_name': 'daily_reward_claimed',
            'amount': 20,
            'status': 'completed',
            'platform': 'iOS',
            'category': 'Daily',
            'issue_tag': 'missing_id'
        })

    # Category 3: Missing Timestamps (25 records)
    for i in range(56, 81):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"USR_{i:05d}",
            'timestamp': None,
            'event_name': 'watch_ad_completed',
            'amount': 15,
            'status': 'completed',
            'platform': 'Android',
            'category': 'Earning',
            'issue_tag': 'missing_timestamp'
        })

    # Category 4: Malformed Dates (35 records)
    malformed_dates = ['2026/31/02', 'INVALID_DATE', '12-11-2026 99:99', '2026-00-15', 'N/A', '9999-99-99']
    for i in range(81, 116):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"USR_{i:05d}",
            'timestamp': random.choice(malformed_dates),
            'event_name': 'spin_completed',
            'amount': 100,
            'status': 'completed',
            'platform': 'Android',
            'category': 'Daily',
            'issue_tag': 'malformed_date'
        })

    # Category 5: Invalid Statuses (30 records)
    invalid_statuses = ['COMPLETEDDDD', 'UNKNOWN_STATUS', 'finished_ok', 'pending_maybe', 'NULL_STATUS']
    for i in range(116, 146):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"USR_{i:05d}",
            'timestamp': '2026-06-01 10:00:00',
            'event_name': 'withdrawal_processed',
            'amount': 500,
            'status': random.choice(invalid_statuses),
            'platform': 'Web',
            'category': 'Wallet',
            'issue_tag': 'invalid_status'
        })

    # Category 6: Inconsistent Capitalization (35 records)
    mixed_caps = ['cOmPLeTeD', 'pEnDiNg', 'ReVeRsEd', 'FAILED_error', 'Success']
    for i in range(146, 181):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"USR_{i:05d}",
            'timestamp': '2026-06-05 12:30:00',
            'event_name': 'mission_completed',
            'amount': 50,
            'status': random.choice(mixed_caps),
            'platform': 'iOS',
            'category': 'Missions',
            'issue_tag': 'inconsistent_capitalization'
        })

    # Category 7: Trailing / Leading Spaces (35 records)
    for i in range(181, 216):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"  USR_{i:05d}  ",
            'timestamp': '2026-06-10 15:45:00',
            'event_name': '  watch_ad   ',
            'amount': 15,
            'status': ' completed ',
            'platform': ' Android ',
            'category': ' Earning ',
            'issue_tag': 'trailing_spaces'
        })

    # Category 8: Invalid Numeric Values (30 records)
    invalid_nums = ['one_hundred', 'NaN', '###', 'NULL_NUM', '10.5.2']
    for i in range(216, 246):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"USR_{i:05d}",
            'timestamp': '2026-06-15 18:20:00',
            'event_name': 'reward_credited',
            'amount': random.choice(invalid_nums),
            'status': 'completed',
            'platform': 'Android',
            'category': 'Rewards',
            'issue_tag': 'invalid_numeric_value'
        })

    # Category 9: Negative Values where inappropriate (30 records)
    for i in range(246, 276):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"USR_{i:05d}",
            'timestamp': '2026-06-20 08:10:00',
            'event_name': 'withdrawal_requested',
            'amount': -random.randint(100, 5000),
            'status': 'requested',
            'platform': 'Android',
            'category': 'Withdrawals',
            'issue_tag': 'negative_numeric_value'
        })

    # Category 10: Unexpected Nulls in Mandatory Columns (30 records)
    for i in range(276, 306):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"USR_{i:05d}",
            'timestamp': '2026-06-25 14:00:00',
            'event_name': None,  # Mandatory column missing
            'amount': 25,
            'status': 'completed',
            'platform': None,    # Mandatory column missing
            'category': None,    # Mandatory column missing
            'issue_tag': 'unexpected_mandatory_null'
        })

    # Category 11: Orphan Foreign Keys (45 records)
    for i in range(306, 351):
        fake_uid = f"USR_999{random.randint(10, 99)}"  # non-existent user
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': fake_uid,
            'timestamp': '2026-07-01 11:15:00',
            'event_name': 'task_completed',
            'amount': 50,
            'status': 'completed',
            'platform': 'Android',
            'category': 'Earning',
            'issue_tag': 'orphan_foreign_key'
        })

    # Category 12: Rapid-Burst Duplicate Events (<200ms) (40 records)
    for i in range(351, 391):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': 'USR_00350',
            'timestamp': '2026-07-10 16:00:00.050',  # burst double-tap
            'event_name': 'tap_earn_clicked',
            'amount': 5,
            'status': 'completed',
            'platform': 'Android',
            'category': 'Earning',
            'issue_tag': 'rapid_burst_event'
        })

    # Category 13: Inconsistent Event Naming (40 records)
    bad_names = ['WATCH-AD', 'dailyRewardClaim', 'SPIN_THE_WHEEL!', 'TaskCompleted_V2']
    for i in range(391, 431):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"USR_{i:05d}",
            'timestamp': '2026-07-20 19:30:00',
            'event_name': random.choice(bad_names),
            'amount': 30,
            'status': 'completed',
            'platform': 'iOS',
            'category': 'Engagement',
            'issue_tag': 'inconsistent_naming'
        })

    # Category 14: Impossible State Transitions (40 records)
    for i in range(431, 471):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"USR_{i:05d}",
            'timestamp': '2026-07-25 21:00:00',
            'event_name': 'withdrawal_lifecycle',
            'amount': 500,
            'status': 'completed_prior_to_request',
            'platform': 'Android',
            'category': 'Wallet',
            'issue_tag': 'impossible_state_transition'
        })

    # Clean records to fill up to 550 total
    for i in range(471, 551):
        messy_records.append({
            'record_id': f"REC_{i:04d}",
            'user_id': f"USR_{i:05d}",
            'timestamp': '2026-08-05 12:00:00',
            'event_name': 'daily_checkin',
            'amount': 20,
            'status': 'completed',
            'platform': 'Android',
            'category': 'Daily',
            'issue_tag': 'clean_record'
        })
    df_messy = pd.DataFrame(messy_records)

    # ==========================================
    # SAVE CSV FILES & MASTER EXCEL WORKBOOK
    # ==========================================
    datasets = {
        'Users': df_users,
        'Task_Activity': df_task_activity,
        'Rewards': df_rewards,
        'Wallet': df_wallet,
        'Withdrawals': df_withdrawals,
        'Referrals': df_referrals,
        'Feature_Events': df_feature_events,
        'Messy_Data': df_messy
    }

    total_rows = 0
    print("\nSaving individual CSVs...")
    for name, df in datasets.items():
        csv_path = os.path.join(data_dir, f"{name}.csv")
        df.to_csv(csv_path, index=False)
        total_rows += len(df)
        print(f"  - {name}.csv: {len(df):,} records saved to {csv_path}")

    print(f"\nTotal Records Generated: {total_rows:,} records (Target: 30,150)")
    assert total_rows == 30150, f"Record count mismatch! Expected 30,150, got {total_rows}"

    excel_path = os.path.join(data_dir, "VELOOP_Simulated_Datasets.xlsx")
    print(f"Exporting master multi-tab Excel file: {excel_path}...")
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for name, df in datasets.items():
            df.to_excel(writer, sheet_name=name, index=False)
    print("Master Excel workbook exported successfully.")

    # Print summary reconciliation statistics:
    total_credits = df_wallet[df_wallet['amount'] > 0]['amount'].sum()
    total_debits = df_wallet[df_wallet['amount'] < 0]['amount'].sum()
    circulating_supply = df_wallet[df_wallet['status'] == 'completed']['amount'].sum()
    
    ve_completed = df_wallet[(df_wallet['unit'] == 'VEs') & (df_wallet['status'] == 'completed')]
    user_final_bals = ve_completed.groupby('user_id')['amount'].sum().to_dict()
    for uid in df_users['user_id']:
        if uid not in user_final_bals:
            user_final_bals[uid] = 0.0

    print("\n=======================================================")
    print("FINANCIAL INVARIANT RECONCILIATION SUMMARY:")
    print("=======================================================")
    print(f"Total Ledger Credits:     +{total_credits:,.2f} VEs")
    print(f"Total Ledger Debits:      {total_debits:,.2f} VEs")
    print(f"Net Circulating Supply:   +{circulating_supply:,.2f} VEs (Positive Liability)")
    print(f"Minimum User Balance:     {min(user_final_bals.values()):,.2f} VEs (Invariant: >= 0.00)")
    print(f"Maximum User Balance:     {max(user_final_bals.values()):,.2f} VEs")
    print(f"Mean User Balance:        {np.mean(list(user_final_bals.values())):,.2f} VEs")
    print("=======================================================\n")

if __name__ == '__main__':
    generate_datasets()
