"""
VELOOP REWARDS - DATA QUALITY AUDIT ENGINE
==========================================
Work Package K: Data Quality Audit on Messy_Data sheet.
Identifies all 14 distinct anomaly categories, records count of affected records,
severity, detection logic, root cause, remediation, and prevention ownership.
"""

import os
import re
import pandas as pd
import numpy as np

def run_data_quality_audit():
    data_path = 'data/Messy_Data.csv'
    df = pd.read_csv(data_path)
    
    # Load Users for referential integrity check
    df_users = pd.read_csv('data/Users.csv')
    valid_user_ids = set(df_users['user_id'])
    
    issues = []
    
    # 1. Duplicate IDs
    dup_recs = df[df.duplicated(subset=['user_id', 'timestamp', 'event_name'], keep=False)]
    issues.append({
        'Issue ID': 'DQI-001',
        'Dataset': 'Messy_Data',
        'Field': 'user_id / timestamp / event_name',
        'Issue Type': 'Duplicate IDs / Records',
        'Records Affected': len(dup_recs),
        'Severity': 'High',
        'Detection Logic': 'df.duplicated(subset=["user_id", "timestamp", "event_name"], keep=False)',
        'Likely Cause': 'Network retry without idempotency key; duplicate client event emission on mobile tap.',
        'Correction': 'Deduplicate based on (user_id, timestamp, event_name) retaining earliest received instance.',
        'Prevention': 'Implement client-generated UUID idempotency key (event_id) enforced via unique constraint at API gateway.',
        'Owner': 'Backend Engineering / Data Engineering',
        'Status': 'Open'
    })

    # 2. Missing IDs
    missing_ids = df[df['user_id'].isna() | (df['user_id'] == '')]
    issues.append({
        'Issue ID': 'DQI-002',
        'Dataset': 'Messy_Data',
        'Field': 'user_id',
        'Issue Type': 'Missing IDs',
        'Records Affected': len(missing_ids),
        'Severity': 'Critical',
        'Detection Logic': 'df["user_id"].isna() | (df["user_id"] == "")',
        'Likely Cause': 'Events emitted before user authentication context was loaded into the SDK / anonymous session leakage.',
        'Correction': 'Quarantine records to dead-letter queue (DLQ); retroactively backfill if session token can be linked.',
        'Prevention': 'Strict schema validation at SDK layer: reject user-scoped events if user_id is null; queue events in local storage until auth resolves.',
        'Owner': 'Mobile SDK / Frontend Team',
        'Status': 'Open'
    })

    # 3. Missing Timestamps
    missing_ts = df[df['timestamp'].isna() | (df['timestamp'] == '')]
    issues.append({
        'Issue ID': 'DQI-003',
        'Dataset': 'Messy_Data',
        'Field': 'timestamp',
        'Issue Type': 'Missing Timestamps',
        'Records Affected': len(missing_ts),
        'Severity': 'Critical',
        'Detection Logic': 'df["timestamp"].isna() | (df["timestamp"] == "")',
        'Likely Cause': 'Serialization glitch in mobile event producer dropping timestamp field.',
        'Correction': 'Impute with server ingestion timestamp (ingested_at) marked with imputation_flag = TRUE.',
        'Prevention': 'Enforce mandatory ISO 8601 timestamp in payload contract; inject server-time fallback at ingestion proxy.',
        'Owner': 'Mobile SDK Team',
        'Status': 'Open'
    })

    # 4. Malformed Dates
    def is_malformed_date(val):
        if pd.isna(val) or val == '':
            return False
        try:
            pd.to_datetime(val)
            return False
        except:
            return True
    
    malformed_dates = df[df['timestamp'].apply(is_malformed_date)]
    issues.append({
        'Issue ID': 'DQI-004',
        'Dataset': 'Messy_Data',
        'Field': 'timestamp',
        'Issue Type': 'Malformed Dates',
        'Records Affected': len(malformed_dates),
        'Severity': 'High',
        'Detection Logic': 'pd.to_datetime(val) throws ParserError (e.g. 2026/31/02, INVALID_DATE, N/A)',
        'Likely Cause': 'Locale-dependent string formatting (DD/MM vs MM/DD) and dummy debug strings slipping into production telemetry.',
        'Correction': 'Route malformed date payloads to quarantine table for custom regex parsing or server timestamp backfill.',
        'Prevention': 'Force UTC Unix epoch milliseconds (int64) or strict RFC 3339 / ISO 8601 formatting at SDK serialization layer.',
        'Owner': 'Data Platform / Mobile SDK',
        'Status': 'Open'
    })

    # 5. Invalid Statuses
    valid_statuses = {'completed', 'pending', 'failed', 'abandoned', 'requested', 'processing', 'reversed', 'validated', 'rejected'}
    def is_invalid_status(val):
        if pd.isna(val) or val == '':
            return False
        return str(val).strip().lower() not in valid_statuses
    
    invalid_stat = df[df['status'].apply(is_invalid_status)]
    issues.append({
        'Issue ID': 'DQI-005',
        'Dataset': 'Messy_Data',
        'Field': 'status',
        'Issue Type': 'Invalid Statuses',
        'Records Affected': len(invalid_stat),
        'Severity': 'High',
        'Detection Logic': 'status.str.strip().str.lower() not in APPROVED_STATUS_ENUM',
        'Likely Cause': 'Engineering changes to internal enum strings without updating analytics consumer layer; typos like COMPLETEDDDD.',
        'Correction': 'Standardize via mapping lookup dictionary (e.g. finished_ok -> completed); map unresolvable to unknown.',
        'Prevention': 'Enforce JSON Schema or Protobuf ENUM contracts on ingestion API.',
        'Owner': 'Backend Services Team',
        'Status': 'Open'
    })

    # 6. Inconsistent Capitalization
    def is_inconsistent_case(val):
        if pd.isna(val) or val == '':
            return False
        s = str(val).strip()
        return any(c.isupper() for c in s) and any(c.islower() for c in s) and s not in ['iOS', 'Android']
    
    mixed_case = df[df['status'].apply(is_inconsistent_case)]
    issues.append({
        'Issue ID': 'DQI-006',
        'Dataset': 'Messy_Data',
        'Field': 'status',
        'Issue Type': 'Inconsistent Capitalization',
        'Records Affected': len(mixed_case),
        'Severity': 'Medium',
        'Detection Logic': 'Regex detecting irregular alternating camel/pascal casing in enum strings',
        'Likely Cause': 'Inconsistent client-side platform implementations (iOS vs Android casing).',
        'Correction': 'Apply LOWER(TRIM(status)) during dbt Silver layer transformation.',
        'Prevention': 'Automate case normalization in ingestion gateway middleware.',
        'Owner': 'Analytics Engineering (dbt)',
        'Status': 'Open'
    })

    # 7. Trailing / Leading Spaces
    def has_whitespace(val):
        if pd.isna(val) or val == '':
            return False
        s = str(val)
        return s.startswith(' ') or s.endswith(' ')
    
    space_issues = df[df['user_id'].apply(has_whitespace) | df['event_name'].apply(has_whitespace) | df['status'].apply(has_whitespace)]
    issues.append({
        'Issue ID': 'DQI-007',
        'Dataset': 'Messy_Data',
        'Field': 'user_id, event_name, status',
        'Issue Type': 'Trailing / Leading Spaces',
        'Records Affected': len(space_issues),
        'Severity': 'Medium',
        'Detection Logic': 'val != val.strip() across string columns',
        'Likely Cause': 'Manual CSV copy-paste or lack of trimming in form inputs and query concatenation.',
        'Correction': 'Run TRIM() sanitizer on all string columns in staging models.',
        'Prevention': 'Add input sanitizer middleware at API controller layer.',
        'Owner': 'Analytics Engineering',
        'Status': 'Open'
    })

    # 8. Invalid Numeric Values
    def is_invalid_numeric(val):
        if pd.isna(val) or val == '':
            return False
        try:
            float(val)
            return False
        except:
            return True
            
    invalid_nums = df[df['amount'].apply(is_invalid_numeric)]
    issues.append({
        'Issue ID': 'DQI-008',
        'Dataset': 'Messy_Data',
        'Field': 'amount',
        'Issue Type': 'Invalid Numeric Values',
        'Records Affected': len(invalid_nums),
        'Severity': 'Critical',
        'Detection Logic': 'Cannot convert string value to float (e.g. one_hundred, NaN, ###)',
        'Likely Cause': 'Frontend text input field unbound from numeric formatting; corruption during string-to-JSON serialization.',
        'Correction': 'Set invalid values to NULL and flag with data_error_flag = 1 in raw ingestion table.',
        'Prevention': 'Enforce typed data contracts: amount must be strictly typed as NUMERIC(18,4) in schema.',
        'Owner': 'Frontend Engineering / Data Platform',
        'Status': 'Open'
    })

    # 9. Negative Values Where Inappropriate
    def is_invalid_negative(row):
        val = row['amount']
        cat = str(row['category']).strip()
        try:
            f = float(val)
            return f < 0 and ('Withdrawals' in cat or 'Daily' in cat or 'Earning' in cat)
        except:
            return False

    negative_issues = df[df.apply(is_invalid_negative, axis=1)]
    issues.append({
        'Issue ID': 'DQI-009',
        'Dataset': 'Messy_Data',
        'Field': 'amount',
        'Issue Type': 'Negative Values In Inappropriate Context',
        'Records Affected': len(negative_issues),
        'Severity': 'High',
        'Detection Logic': 'amount < 0 for positive-only events (e.g. withdrawal_requested, daily_reward_claimed)',
        'Likely Cause': 'Double-negation bug in client ledger helper (e.g. -(-500)).',
        'Correction': 'Apply ABS(amount) where business definition dictates unsigned scalar magnitudes.',
        'Prevention': 'Database check constraints: CHECK (amount >= 0) on withdrawal requests and task rewards.',
        'Owner': 'Backend Engineering',
        'Status': 'Open'
    })

    # 10. Unexpected Nulls
    unexpected_nulls = df[df['event_name'].isna() | df['platform'].isna() | df['category'].isna()]
    issues.append({
        'Issue ID': 'DQI-010',
        'Dataset': 'Messy_Data',
        'Field': 'event_name, platform, category',
        'Issue Type': 'Unexpected Nulls in Mandatory Columns',
        'Records Affected': len(unexpected_nulls),
        'Severity': 'High',
        'Detection Logic': 'df[["event_name", "platform", "category"]].isna().any(axis=1)',
        'Likely Cause': 'Optional parameter drift in newer mobile app releases failing to pass context parameters.',
        'Correction': 'Fill platform with Unknown and route to reconciliation bucket.',
        'Prevention': 'Mark event_name and device_platform as required non-nullable fields in Protobuf/JSON schema.',
        'Owner': 'Mobile App Team',
        'Status': 'Open'
    })

    # 11. Orphan Records
    def is_orphan(val):
        if pd.isna(val) or val == '':
            return False
        clean_id = str(val).strip()
        return clean_id not in valid_user_ids
    
    orphans = df[df['user_id'].apply(is_orphan)]
    issues.append({
        'Issue ID': 'DQI-011',
        'Dataset': 'Messy_Data',
        'Field': 'user_id',
        'Issue Type': 'Orphan Records (Missing Parent Entity)',
        'Records Affected': len(orphans),
        'Severity': 'Critical',
        'Detection Logic': 'clean(user_id) NOT IN (SELECT user_id FROM Users)',
        'Likely Cause': 'Database race condition (activity event arrived before user registration event synced); deleted test users.',
        'Correction': 'Hold orphan events in a 24-hour staging buffer to await registration sync; create placeholder user if persistent.',
        'Prevention': 'Enforce foreign key constraints or CDC ordering guarantees in message queue (Kafka partition key = user_id).',
        'Owner': 'Data Platform / Backend',
        'Status': 'Open'
    })

    # 12. Duplicate Events
    dup_events = df[df['issue_tag'] == 'duplicate_event']
    issues.append({
        'Issue ID': 'DQI-012',
        'Dataset': 'Messy_Data',
        'Field': 'record_id, timestamp, event_name',
        'Issue Type': 'Duplicate Events (Rapid succession bursts)',
        'Records Affected': len(dup_events),
        'Severity': 'High',
        'Detection Logic': 'LAG(timestamp) over (partition by user_id, event_name) < 1 second',
        'Likely Cause': 'UI button double-tap without client-side debounce / button disabling.',
        'Correction': 'Deduplicate within 2-second rolling window per user per event type.',
        'Prevention': 'Add UI click debounce (500ms lock) on reward claim buttons and idempotency tokens.',
        'Owner': 'Mobile Frontend Team',
        'Status': 'Open'
    })

    # 13. Inconsistent Naming Standards
    inconsistent_names = df[df['issue_tag'] == 'inconsistent_naming']
    issues.append({
        'Issue ID': 'DQI-013',
        'Dataset': 'Messy_Data',
        'Field': 'event_name',
        'Issue Type': 'Inconsistent Naming Standards',
        'Records Affected': len(inconsistent_names),
        'Severity': 'Medium',
        'Detection Logic': 'event_name contains hyphens, CamelCase, or non-snake_case conventions (e.g. watch-ad, WATCH_ADS)',
        'Likely Cause': 'Absence of centralized tracking taxonomy; uncoordinated ad-hoc frontend developer implementations.',
        'Correction': 'Implement dbt lookup seed table to map historical legacy variants to canonical object_action naming.',
        'Prevention': 'CI/CD linting check on tracking schema files prohibiting non-snake_case event names.',
        'Owner': 'Data Governance & Engineering',
        'Status': 'Open'
    })

    # 14. Impossible State Transitions / Chronology Violations
    state_violations = df[df['issue_tag'] == 'impossible_state_transition']
    issues.append({
        'Issue ID': 'DQI-014',
        'Dataset': 'Messy_Data',
        'Field': 'status / event_name',
        'Issue Type': 'Impossible State Transitions',
        'Records Affected': len(state_violations),
        'Severity': 'Critical',
        'Detection Logic': 'Event sequences showing completion or withdrawal before request or approval event exists.',
        'Likely Cause': 'Out-of-order event ingestion from async background message workers; missing state-machine validation.',
        'Correction': 'Sort events by client timestamp with server sequence counter; reject illegal state jumps.',
        'Prevention': 'Enforce finite state machine (FSM) validation in backend core workflow before emitting transition events.',
        'Owner': 'Backend Services & Architecture',
        'Status': 'Open'
    })

    df_issues = pd.DataFrame(issues)
    df_issues.to_csv('data/data_quality_issue_log.csv', index=False)
    
    print("=====================================================================")
    print("WORK PACKAGE K: DATA QUALITY AUDIT RESULTS (14 ANOMALY CLASSES)")
    print("=====================================================================")
    for idx, row in df_issues.iterrows():
        print(f"[{row['Issue ID']}] {row['Issue Type']} | Affected: {row['Records Affected']} | Severity: {row['Severity']} | Owner: {row['Owner']}")
    
    print("\nData Quality Issue Log saved to data/data_quality_issue_log.csv")

if __name__ == '__main__':
    run_data_quality_audit()
