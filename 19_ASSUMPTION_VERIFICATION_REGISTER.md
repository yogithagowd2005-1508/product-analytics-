# 19 — WORK PACKAGE S: ASSUMPTION & VERIFICATION REGISTER

> **MANDATORY DATA AUTHENTICITY NOTICE**  
> *VELOOP is a real product under development, but the data supplied and evaluated for this assignment is fictional/simulated for analytical testing. In accordance with the Data Authenticity Policy, no metric or finding herein represents actual VELOOP production statistics, actual earnings, actual withdrawals, or live business performance.*

---

## 1. Executive Mandate & Unknown Governance
In accordance with **Work Package S (Assumption & Verification Discipline)**, an analyst inside a developing product company must never silently convert assumptions into facts. Whenever technical specifications, business rules, or backend behaviors are unverified, they must be explicitly cataloged with designated verification owners.

- **Primary Data File**: `deliverables_tables/19_ASSUMPTION_VERIFICATION_REGISTER.csv`
- **Total Unknowns Tracked**: 10 High-Risk Product & Architectural Unknowns
- **Status Classification**: `To Be Verified` (Pending engineering test) | `Proposed` (Architectural recommendation) | `Confirmed` (Formally verified)

---

## 2. Complete Assumption & Verification Register Table

| ID | Unknown / Assumption | Why It Matters | Source Checked | Risk Level | Verification Owner | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A001** | Does the backend currently emit distinct `task_completed` events separate from ledger rewards? | Critical for distinguishing task execution success from monetary settlement and partner error rates. | Product Docs / Simulated Schema | High | Backend Engineering | To Be Verified |
| **A002** | What is the precise conversion peg rate between VEs, Tokens, and cash withdrawal amounts? | Required for financial liability calculations, unit economics, treasury float modeling, and withdrawal KPIs. | Product Documentation | Critical | Product Economics / Finance | To Be Verified |
| **A003** | Are session IDs generated and maintained persistently across mobile app restarts? | Essential for session duration, bounce rate, screens-per-session, and session-level attribution. | Client Mobile Telemetry | High | Mobile SDK Team | To Be Verified |
| **A004** | Do third-party ad networks (AdMob/IronSource) send client or server postbacks for ad views? | Dictates whether ad view validation occurs on client device or via authenticated backend webhook. | Partner Integration Docs | Critical | Ad Operations / Engineering | To Be Verified |
| **A005** | Are duplicate withdrawal requests debited immediately or held in escrow? | Fundamental to double-entry ledger design and preventing race-condition overdrafts. | Wallet Architecture Spec | Critical | Ledger Core Team | Confirmed |
| **A006** | What constitutes the exact qualifying threshold for referral activation? | Prevents gaming of referral bounties by requiring meaningful user activity before releasing bonuses. | Growth Strategy Brief | High | Growth Product Manager | Proposed |
| **A007** | Are streak freeze items purchasable with Gems or earned strictly via daily activity? | Affects sink mechanics in tokenomic modeling and gamification engagement loops. | Game Economy Design | Medium | Game Designer | Proposed |
| **A008** | Is KYC mandatory for all withdrawal amounts or only transactions above a dollar threshold? | Determines withdrawal drop-off rate, compliance pipeline volume, and user friction. | Compliance Policy | High | Legal & Compliance Lead | To Be Verified |
| **A009** | Does the client mobile SDK queue telemetry events offline and flush upon reconnection? | If offline queueing exists, event timestamps may significantly lag server ingestion time. | Mobile Architecture | High | Mobile Lead | To Be Verified |
| **A010** | What is the server-side deduplication window for client-emitted event IDs? | Ensures rapid double-taps do not cause duplicate reward disbursements or ledger anomalies. | API Gateway Spec | Critical | Backend Architecture | Proposed |

---

## 3. Risk Mitigation Protocol for Critical Unknowns
For all items flagged as **Critical Risk** (`A002`, `A004`, `A005`, `A010`):
1. **Engineering Sync**: Scheduled bi-weekly architectural alignment between Data Analytics and Core Engineering.
2. **Defensive Telemetry Design**: Schemas are designed defensively—assuming asynchronous postbacks and enforcing server-side escrow buffers regardless of current frontend behavior.
3. **Audit Closure Requirement**: No feature may transition from `Beta` to `General Availability (GA)` until all associated register items are marked `Confirmed`.

---
*Deliverable Document Reference: `docs/19_ASSUMPTION_VERIFICATION_REGISTER.md` | Data File: `deliverables_tables/19_ASSUMPTION_VERIFICATION_REGISTER.csv`.*
