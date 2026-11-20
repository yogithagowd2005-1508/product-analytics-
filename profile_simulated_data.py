"""
VELOOP REWARDS - SIMULATED DATA PROFILING & REFERENTIAL INTEGRITY ENGINE
========================================================================
Work Package J: J1 Dataset Profiling, J2 Relationship & Referential Integrity Testing,
J3 KPI Calculability Assessment.

Total Records: 30,150 across 8 datasets:
- Users: 1,000
- Task_Activity: 6,000
- Rewards: 5,000
- Wallet: 3,500
- Withdrawals: 1,200
- Referrals: 900
- Feature_Events: 12,000
- Messy_Data: 550
Sum = 30,150 records.
"""

import os
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
import pandas as pd
import numpy as np

def run_profiling():
    data_dir = 'data'
    files = {
        'Users': 'Users.csv',
        'Task_Activity': 'Task_Activity.csv',
        'Rewards': 'Rewards.csv',
        'Wallet': 'Wallet.csv',
        'Withdrawals': 'Withdrawals.csv',
        'Referrals': 'Referrals.csv',
        'Feature_Events': 'Feature_Events.csv',
        'Messy_Data': 'Messy_Data.csv'
    }

    dfs = {}
    total_records_all = 0
    for name, f in files.items():
        dfs[name] = pd.read_csv(os.path.join(data_dir, f))
        total_records_all += len(dfs[name])

    print("=====================================================================")
    print(f"WORK PACKAGE J1: SIMULATED DATASET PROFILING REPORT (TOTAL: {total_records_all:,} RECORDS)")
    print("=====================================================================")
    
    profiling_summary = []

    for name, df in dfs.items():
        num_records = len(df)
        num_cols = len(df.columns)
        
        # Primary key candidate (first col ending with id or containing id)
        id_cols = [c for c in df.columns if 'id' in c.lower()]
        pk_col = id_cols[0] if id_cols else df.columns[0]
        unique_ids = df[pk_col].nunique()
        duplicate_pk_count = num_records - unique_ids
        
        # Missing values count across all columns
        missing_total = int(df.isna().sum().sum())
        missing_by_col = df.isna().sum()[df.isna().sum() > 0].to_dict()
        
        # Date columns
        date_cols = [c for c in df.columns if 'time' in c.lower() or 'at' in c.lower() or 'date' in c.lower()]
        date_ranges = {}
        for dc in date_cols:
            valid_dates = pd.to_datetime(df[dc], errors='coerce').dropna()
            if len(valid_dates) > 0:
                date_ranges[dc] = f"{valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}"
            else:
                date_ranges[dc] = "No valid dates parsed"
                
        # Status column distribution
        status_cols = [c for c in df.columns if 'status' in c.lower()]
        status_dist = {}
        for sc in status_cols:
            status_dist[sc] = df[sc].value_counts().to_dict()
            
        # Numeric ranges
        num_cols_list = df.select_dtypes(include=[np.number]).columns.tolist()
        num_ranges = {}
        for nc in num_cols_list:
            num_ranges[nc] = f"min: {df[nc].min()}, max: {df[nc].max()}, mean: {df[nc].mean():.2f}"

        profiling_summary.append({
            'dataset_name': name,
            'records_count': num_records,
            'columns_count': num_cols,
            'pk_candidate': pk_col,
            'unique_ids': unique_ids,
            'duplicate_pk_count': duplicate_pk_count,
            'total_missing_cells': missing_total,
            'missing_breakdown': str(missing_by_col),
            'date_range': str(date_ranges),
            'status_distribution': str(status_dist),
            'numeric_ranges': str(num_ranges)
        })
        
        print(f"\n--- Dataset: {name} ---")
        print(f"Records: {num_records:,} | Columns: {num_cols} | PK: {pk_col} (Unique: {unique_ids:,}, Dups: {duplicate_pk_count})")
        print(f"Missing Values: {missing_total:,}")
        print(f"Date Ranges: {date_ranges}")
        print(f"Status Distribution: {status_dist}")
        print(f"Numeric Ranges: {num_ranges}")

    df_summary = pd.DataFrame(profiling_summary)
    df_summary.to_csv('data/profiling_summary.csv', index=False)

    print("\n=====================================================================")
    print("WORK PACKAGE J2: REFERENTIAL INTEGRITY & RELATIONSHIP TESTING (9 PATHS)")
    print("=====================================================================")

    # 9 Distinct Foreign Key Relationships
    relationships = [
        ('Task_Activity', 'user_id', 'Users', 'user_id', 'User owns Task Activity'),
        ('Rewards', 'user_id', 'Users', 'user_id', 'User receives Reward'),
        ('Rewards', 'task_activity_id', 'Task_Activity', 'task_activity_id', 'Reward references Task Activity (nullable for daily login)'),
        ('Wallet', 'user_id', 'Users', 'user_id', 'User owns Wallet balance'),
        ('Wallet (Reward Credits)', 'reference_id', 'Rewards', 'reward_id', 'Wallet reward_credit references Rewards'),
        ('Withdrawals', 'user_id', 'Users', 'user_id', 'User requests Withdrawal'),
        ('Referrals', 'referring_user_id', 'Users', 'user_id', 'Advocate user creates referral link'),
        ('Referrals (Registered Referees)', 'referred_user_id', 'Users', 'user_id', 'Referee user registered (nullable if un-clicked)'),
        ('Feature_Events', 'user_id', 'Users', 'user_id', 'User emits Feature Telemetry Event')
    ]

    rel_results = []
    
    # 1. Task_Activity.user_id -> Users.user_id
    child_vals = dfs['Task_Activity']['user_id'].dropna().astype(str)
    parent_vals = set(dfs['Users']['user_id'].dropna().astype(str))
    orphans = child_vals[~child_vals.isin(parent_vals)]
    rel_results.append({
        'path_id': 'FK-01',
        'relationship_name': 'Task_Activity.user_id -> Users.user_id',
        'child_table': 'Task_Activity',
        'foreign_key': 'user_id',
        'parent_table': 'Users',
        'primary_key': 'user_id',
        'records_tested': len(child_vals),
        'orphan_records': len(orphans),
        'unique_orphans': orphans.nunique(),
        'test_status': 'PASSED (100% Referential Integrity)' if len(orphans) == 0 else f'FAILED ({len(orphans)} orphans)'
    })

    # 2. Rewards.user_id -> Users.user_id
    child_vals = dfs['Rewards']['user_id'].dropna().astype(str)
    orphans = child_vals[~child_vals.isin(parent_vals)]
    rel_results.append({
        'path_id': 'FK-02',
        'relationship_name': 'Rewards.user_id -> Users.user_id',
        'child_table': 'Rewards',
        'foreign_key': 'user_id',
        'parent_table': 'Users',
        'primary_key': 'user_id',
        'records_tested': len(child_vals),
        'orphan_records': len(orphans),
        'unique_orphans': orphans.nunique(),
        'test_status': 'PASSED (100% Referential Integrity)' if len(orphans) == 0 else f'FAILED ({len(orphans)} orphans)'
    })

    # 3. Rewards.task_activity_id -> Task_Activity.task_activity_id
    task_pks = set(dfs['Task_Activity']['task_activity_id'].dropna().astype(str))
    rwd_tasks = dfs['Rewards']['task_activity_id'].dropna()
    rwd_tasks = rwd_tasks[rwd_tasks != ''].astype(str)
    orphans = rwd_tasks[~rwd_tasks.isin(task_pks)]
    rel_results.append({
        'path_id': 'FK-03',
        'relationship_name': 'Rewards.task_activity_id -> Task_Activity.task_activity_id',
        'child_table': 'Rewards',
        'foreign_key': 'task_activity_id',
        'parent_table': 'Task_Activity',
        'primary_key': 'task_activity_id',
        'records_tested': len(rwd_tasks),
        'orphan_records': len(orphans),
        'unique_orphans': orphans.nunique(),
        'test_status': 'PASSED (100% Referential Integrity)' if len(orphans) == 0 else f'FAILED ({len(orphans)} orphans)'
    })

    # 4. Wallet.user_id -> Users.user_id
    child_vals = dfs['Wallet']['user_id'].dropna().astype(str)
    orphans = child_vals[~child_vals.isin(parent_vals)]
    rel_results.append({
        'path_id': 'FK-04',
        'relationship_name': 'Wallet.user_id -> Users.user_id',
        'child_table': 'Wallet',
        'foreign_key': 'user_id',
        'parent_table': 'Users',
        'primary_key': 'user_id',
        'records_tested': len(child_vals),
        'orphan_records': len(orphans),
        'unique_orphans': orphans.nunique(),
        'test_status': 'PASSED (100% Referential Integrity)' if len(orphans) == 0 else f'FAILED ({len(orphans)} orphans)'
    })

    # 5. Wallet (Reward Credits) reference_id -> Rewards.reward_id
    rwd_pks = set(dfs['Rewards']['reward_id'].dropna().astype(str))
    wallet_rwds = dfs['Wallet'][dfs['Wallet']['transaction_type'] == 'reward_credit']['reference_id'].dropna()
    wallet_rwds = wallet_rwds[wallet_rwds != ''].astype(str)
    orphans = wallet_rwds[~wallet_rwds.isin(rwd_pks)]
    rel_results.append({
        'path_id': 'FK-05',
        'relationship_name': 'Wallet.reference_id (reward credits) -> Rewards.reward_id',
        'child_table': 'Wallet',
        'foreign_key': 'reference_id',
        'parent_table': 'Rewards',
        'primary_key': 'reward_id',
        'records_tested': len(wallet_rwds),
        'orphan_records': len(orphans),
        'unique_orphans': orphans.nunique(),
        'test_status': 'PASSED (100% Referential Integrity)' if len(orphans) == 0 else f'FAILED ({len(orphans)} orphans)'
    })

    # 6. Withdrawals.user_id -> Users.user_id
    child_vals = dfs['Withdrawals']['user_id'].dropna().astype(str)
    orphans = child_vals[~child_vals.isin(parent_vals)]
    rel_results.append({
        'path_id': 'FK-06',
        'relationship_name': 'Withdrawals.user_id -> Users.user_id',
        'child_table': 'Withdrawals',
        'foreign_key': 'user_id',
        'parent_table': 'Users',
        'primary_key': 'user_id',
        'records_tested': len(child_vals),
        'orphan_records': len(orphans),
        'unique_orphans': orphans.nunique(),
        'test_status': 'PASSED (100% Referential Integrity)' if len(orphans) == 0 else f'FAILED ({len(orphans)} orphans)'
    })

    # 7. Referrals.referring_user_id -> Users.user_id
    child_vals = dfs['Referrals']['referring_user_id'].dropna().astype(str)
    orphans = child_vals[~child_vals.isin(parent_vals)]
    rel_results.append({
        'path_id': 'FK-07',
        'relationship_name': 'Referrals.referring_user_id -> Users.user_id',
        'child_table': 'Referrals',
        'foreign_key': 'referring_user_id',
        'parent_table': 'Users',
        'primary_key': 'user_id',
        'records_tested': len(child_vals),
        'orphan_records': len(orphans),
        'unique_orphans': orphans.nunique(),
        'test_status': 'PASSED (100% Referential Integrity)' if len(orphans) == 0 else f'FAILED ({len(orphans)} orphans)'
    })

    # 8. Referrals.referred_user_id -> Users.user_id (for registered referees)
    child_vals = dfs['Referrals']['referred_user_id'].dropna()
    child_vals = child_vals[child_vals != ''].astype(str)
    orphans = child_vals[~child_vals.isin(parent_vals)]
    rel_results.append({
        'path_id': 'FK-08',
        'relationship_name': 'Referrals.referred_user_id -> Users.user_id',
        'child_table': 'Referrals',
        'foreign_key': 'referred_user_id',
        'parent_table': 'Users',
        'primary_key': 'user_id',
        'records_tested': len(child_vals),
        'orphan_records': len(orphans),
        'unique_orphans': orphans.nunique(),
        'test_status': 'PASSED (100% Referential Integrity)' if len(orphans) == 0 else f'FAILED ({len(orphans)} orphans)'
    })

    # 9. Feature_Events.user_id -> Users.user_id
    child_vals = dfs['Feature_Events']['user_id'].dropna().astype(str)
    orphans = child_vals[~child_vals.isin(parent_vals)]
    rel_results.append({
        'path_id': 'FK-09',
        'relationship_name': 'Feature_Events.user_id -> Users.user_id',
        'child_table': 'Feature_Events',
        'foreign_key': 'user_id',
        'parent_table': 'Users',
        'primary_key': 'user_id',
        'records_tested': len(child_vals),
        'orphan_records': len(orphans),
        'unique_orphans': orphans.nunique(),
        'test_status': 'PASSED (100% Referential Integrity)' if len(orphans) == 0 else f'FAILED ({len(orphans)} orphans)'
    })

    # Benchmark Control: Messy_Data.user_id -> Users.user_id (Negative Control)
    messy_uids = dfs['Messy_Data']['user_id'].dropna()
    messy_uids = messy_uids[messy_uids != ''].str.strip()
    orphans_messy = messy_uids[~messy_uids.isin(parent_vals)]
    rel_results.append({
        'path_id': 'CONTROL-NEG',
        'relationship_name': 'Messy_Data.user_id -> Users.user_id (Corrupted Audit Control)',
        'child_table': 'Messy_Data',
        'foreign_key': 'user_id',
        'parent_table': 'Users',
        'primary_key': 'user_id',
        'records_tested': len(messy_uids),
        'orphan_records': len(orphans_messy),
        'unique_orphans': orphans_messy.nunique(),
        'test_status': f'DETECTED {len(orphans_messy)} ORPHANS ({orphans_messy.nunique()} unique keys)'
    })

    df_rel = pd.DataFrame(rel_results)
    df_rel.to_csv('data/referential_integrity_test_results.csv', index=False)

    for r in rel_results:
        print(f"[{r['path_id']}] {r['relationship_name']} | Tested: {r['records_tested']:,} | Orphans: {r['orphan_records']} | Status: {r['test_status']}")

    print("\n=====================================================================")
    print("WORK PACKAGE J3: KPI CALCULABILITY ASSESSMENT")
    print("=====================================================================")
    
    kpi_tests = [
        {
            'kpi_id': 'KPI_USR_01',
            'name': 'Daily Active Users (DAU)',
            'formula': 'COUNT(DISTINCT user_id) per day with qualifying event',
            'calculable': 'YES',
            'tables_used': 'Feature_Events, Task_Activity',
            'notes': 'Can be calculated directly using timestamp and user_id across activity datasets.'
        },
        {
            'kpi_id': 'KPI_ENG_04',
            'name': 'Task Completion Rate',
            'formula': 'COUNT(completed tasks) / COUNT(started tasks)',
            'calculable': 'YES',
            'tables_used': 'Task_Activity',
            'notes': 'Can be calculated via status column in Task_Activity.'
        },
        {
            'kpi_id': 'KPI_WDR_06',
            'name': 'Average Withdrawal Processing Duration',
            'formula': 'AVG(final_timestamp - requested_timestamp)',
            'calculable': 'YES',
            'tables_used': 'Withdrawals',
            'notes': 'Directly computable on completed/rejected records with final_timestamp.'
        },
        {
            'kpi_id': 'KPI_REV_01',
            'name': 'Net Ad Revenue per User (ARPU)',
            'formula': 'SUM(gross_ad_revenue - reward_expense) / Total Users',
            'calculable': 'NO',
            'tables_used': 'Task_Activity (incomplete)',
            'notes': 'BLOCKED: Gross third-party ad network payout / eCPM cost data is not captured in Task_Activity. Only internal user reward_amount is tracked.',
            'remedy': 'Ingest ad network provider settlement revenue feeds (e.g. AdMob/IronSource API gross earnings postback).'
        },
        {
            'kpi_id': 'KPI_RET_02',
            'name': 'D30 Rolling Retention Rate',
            'formula': 'COUNT(users active on Day 30) / COUNT(users registered on Day 0)',
            'calculable': 'PARTIAL',
            'tables_used': 'Users, Feature_Events',
            'notes': 'Calculable only for users whose registration was at least 30 days prior to dataset cutoff.',
            'remedy': 'Implement cohort survival modeling table with maturity window flags.'
        },
        {
            'kpi_id': 'KPI_FRD_01',
            'name': 'Multi-Account Collusion Rate',
            'formula': 'COUNT(users sharing device/IP/bank) / Total Users',
            'calculable': 'NO',
            'tables_used': 'None',
            'notes': 'BLOCKED: Hardware device fingerprint (IDFV/GAID), IP address hash, and bank account hashes are not present in User or Withdrawal tables.',
            'remedy': 'Add security telemetry tracking payload (device_fingerprint_hash, ip_asn, payment_destination_hash) to Ingestion Gateway.'
        }
    ]
    
    df_kpi_test = pd.DataFrame(kpi_tests)
    df_kpi_test.to_csv('data/kpi_calculability_test.csv', index=False)
    for t in kpi_tests:
        print(f"KPI: {t['name']} | Calculable: {t['calculable']} | Notes: {t.get('notes', 'Fully supported')}")

if __name__ == '__main__':
    run_profiling()
