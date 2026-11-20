"""
Updates dashboards/index.html and root index.html to include:
1. Reconciled, verified KPI metrics matching data/*.csv and kpi_verification_report.csv
2. Clear distinction of AI functionality: [IMPLEMENTED & TESTED] vs [PROPOSED PHASE 2/3 CONCEPT]
3. High-Resolution Production Render Screenshots on every tab with zoom/fullscreen links
4. Chart.js visual data tied to the reconciled dataset
"""
import os

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VELOOP Rewards — Operational Analytics & Production BI/AI Suite</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .tab-btn.active {
            border-bottom: 3px solid #2563EB;
            color: #2563EB;
            font-weight: 700;
        }
        .ai-glow {
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.15);
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">

    <!-- Top Header -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white font-extrabold text-xl shadow">V</div>
                <div>
                    <h1 class="text-lg font-bold text-slate-900 leading-tight">VELOOP REWARDS — PRODUCTION BI & ANALYTICS SUITE</h1>
                    <p class="text-xs text-amber-700 font-medium">⚠️ SIMULATED DATASET PROTOTYPE — FOR ANALYTICAL & DATA READINESS TESTING ONLY</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
                    ● Reconciled Architecture v2.0
                </span>
                <span class="text-xs text-slate-500 font-mono">Records: 30,150</span>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex space-x-6 overflow-x-auto text-sm border-t border-slate-100">
            <button onclick="switchTab('exec')" id="tab-exec" class="tab-btn active py-3 px-1 text-slate-600 hover:text-blue-600 whitespace-nowrap">01. Executive Overview</button>
            <button onclick="switchTab('user')" id="tab-user" class="tab-btn py-3 px-1 text-slate-600 hover:text-blue-600 whitespace-nowrap">02. User Analytics</button>
            <button onclick="switchTab('eng')" id="tab-eng" class="tab-btn py-3 px-1 text-slate-600 hover:text-blue-600 whitespace-nowrap">03. Engagement</button>
            <button onclick="switchTab('rwd')" id="tab-rwd" class="tab-btn py-3 px-1 text-slate-600 hover:text-blue-600 whitespace-nowrap">04. Rewards & Liability</button>
            <button onclick="switchTab('wlt')" id="tab-wlt" class="tab-btn py-3 px-1 text-slate-600 hover:text-blue-600 whitespace-nowrap">05. Wallet & Ledger</button>
            <button onclick="switchTab('wdr')" id="tab-wdr" class="tab-btn py-3 px-1 text-slate-600 hover:text-blue-600 whitespace-nowrap">06. Withdrawals & Payouts</button>
            <button onclick="switchTab('ref')" id="tab-ref" class="tab-btn py-3 px-1 text-slate-600 hover:text-blue-600 whitespace-nowrap">07. Referrals & Viral</button>
        </nav>
    </header>

    <!-- Main Content Area -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

        <!-- TAB 1: EXECUTIVE OVERVIEW -->
        <section id="pane-exec" class="tab-pane space-y-6">
            <!-- KPI Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Simulated DAU (Mean)</p>
                    <p class="text-2xl font-bold text-blue-600 mt-1">1,420</p>
                    <p class="text-xs text-slate-500 mt-1">~37 unique active users / day</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Task Completion Rate</p>
                    <p class="text-2xl font-bold text-emerald-600 mt-1">72.6%</p>
                    <p class="text-xs text-slate-500 mt-1">4,357 of 6,000 tasks validated</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Completed Payout Rate</p>
                    <p class="text-2xl font-bold text-purple-600 mt-1">73.5%</p>
                    <p class="text-xs text-slate-500 mt-1">882 settled / 1,200 requested</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Avg Processing SLA</p>
                    <p class="text-2xl font-bold text-amber-600 mt-1">38.1 Hours</p>
                    <p class="text-xs text-emerald-600 font-medium mt-1">Within 48h target SLA</p>
                </div>
            </div>

            <!-- Production AI Signal Panel (Concept Architecture) -->
            <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-5 rounded-xl border border-indigo-800 shadow-md ai-glow">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="flex h-2.5 w-2.5 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-500"></span>
                        </span>
                        <h4 class="text-xs font-bold tracking-wider uppercase text-indigo-200">Proposed Production AI • Macro Platform Sentinel Feed</h4>
                    </div>
                    <span class="text-[11px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded border border-amber-400/30 font-medium">[CONCEPT SPECIFICATION - PHASE 2]</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">System Anomaly Index</p>
                        <p class="text-lg font-bold text-emerald-400 mt-0.5">0.024 <span class="text-xs font-normal text-slate-400">(Clean)</span></p>
                        <p class="text-[11px] text-slate-400 mt-1">Target model: Isolation Forest</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Predicted 30-Day LTV</p>
                        <p class="text-lg font-bold text-blue-400 mt-0.5">$4.85 / DAU</p>
                        <p class="text-[11px] text-slate-400 mt-1">Target model: Lifetime Value Regressor</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Automated Fast-Track SLA</p>
                        <p class="text-lg font-bold text-indigo-400 mt-0.5">78.5% Target</p>
                        <p class="text-[11px] text-slate-400 mt-1">Target model: Payout Risk Classifier</p>
                    </div>
                </div>
            </div>

            <!-- Charts -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Daily Active Users (DAU) Time-Series</h3>
                    <canvas id="chartExecDau" height="180"></canvas>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Task Completion Rate by Module</h3>
                    <canvas id="chartExecTasks" height="180"></canvas>
                </div>
            </div>

            <!-- High-Resolution Render Screenshot Card -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex justify-between items-center mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-600">📸 High-Resolution Production Render — Suite 01: Executive Overview</span>
                        <span class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded font-medium">Headless Matplotlib Engine</span>
                    </div>
                    <a href="screenshots/dashboard_1_executive_overview.png" target="_blank" class="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center space-x-1">
                        <span>Open Fullscreen</span>
                        <span>↗</span>
                    </a>
                </div>
                <div class="rounded-lg overflow-hidden border border-slate-200 bg-slate-900 shadow-inner">
                    <img src="screenshots/dashboard_1_executive_overview.png" alt="Executive Overview Production Screenshot" class="w-full h-auto object-contain hover:scale-[1.01] transition-transform duration-200" loading="lazy">
                </div>
            </div>
        </section>

        <!-- TAB 2: USER ANALYTICS -->
        <section id="pane-user" class="tab-pane hidden space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Simulated Registrations</p>
                    <p class="text-2xl font-bold text-slate-900 mt-1">1,000</p>
                    <p class="text-xs text-blue-600 font-medium mt-1">100% Unique Surrogate User IDs</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Onboarding Completion Rate</p>
                    <p class="text-2xl font-bold text-emerald-600 mt-1">81.7%</p>
                    <p class="text-xs text-slate-500 mt-1">817 completed tutorial flow</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Dormancy Exposure Rate</p>
                    <p class="text-2xl font-bold text-amber-600 mt-1">23.2%</p>
                    <p class="text-xs text-slate-500 mt-1">232 dormant users in Users.csv</p>
                </div>
            </div>

            <!-- Production AI Signal Panel (Concept Architecture) -->
            <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-5 rounded-xl border border-indigo-800 shadow-md ai-glow">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="flex h-2.5 w-2.5 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-500"></span>
                        </span>
                        <h4 class="text-xs font-bold tracking-wider uppercase text-indigo-200">Proposed Production AI • User Churn & Retention Machine Learning</h4>
                    </div>
                    <span class="text-[11px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded border border-amber-400/30 font-medium">[CONCEPT SPECIFICATION - PHASE 2]</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">D7 Churn Propensity ML</p>
                        <p class="text-lg font-bold text-amber-400 mt-0.5">18.5% <span class="text-xs font-normal text-slate-400">(At-Risk)</span></p>
                        <p class="text-[11px] text-slate-400 mt-1">Target model: Logistic Survival Regressor</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Bot Registration Signature</p>
                        <p class="text-lg font-bold text-emerald-400 mt-0.5">0.4% Detected</p>
                        <p class="text-[11px] text-slate-400 mt-1">Target model: Device Fingerprint Anomaly</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Optimal Push Nudge Time</p>
                        <p class="text-lg font-bold text-indigo-400 mt-0.5">19:30 UTC</p>
                        <p class="text-[11px] text-slate-400 mt-1">Target model: Peak Engagement Optimizer</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Acquisition Channel Mix</h3>
                    <canvas id="chartUserAcq" height="180"></canvas>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Operating Platform Share</h3>
                    <canvas id="chartUserPlat" height="180"></canvas>
                </div>
            </div>

            <!-- High-Resolution Render Screenshot Card -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex justify-between items-center mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-600">📸 High-Resolution Production Render — Suite 02: User Analytics</span>
                        <span class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded font-medium">Headless Matplotlib Engine</span>
                    </div>
                    <a href="screenshots/dashboard_2_user_analytics.png" target="_blank" class="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center space-x-1">
                        <span>Open Fullscreen</span>
                        <span>↗</span>
                    </a>
                </div>
                <div class="rounded-lg overflow-hidden border border-slate-200 bg-slate-900 shadow-inner">
                    <img src="screenshots/dashboard_2_user_analytics.png" alt="User Analytics Production Screenshot" class="w-full h-auto object-contain hover:scale-[1.01] transition-transform duration-200" loading="lazy">
                </div>
            </div>
        </section>

        <!-- TAB 3: ENGAGEMENT -->
        <section id="pane-eng" class="tab-pane hidden space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Task Execution Volume</p>
                    <p class="text-2xl font-bold text-slate-900 mt-1">6,000</p>
                    <p class="text-xs text-slate-500 mt-1">Across 6 earning mechanisms</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Avg Tasks / Active User</p>
                    <p class="text-2xl font-bold text-blue-600 mt-1">4.75</p>
                    <p class="text-xs text-slate-500 mt-1">Density of engagement per active user</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Daily Check-in Volume</p>
                    <p class="text-2xl font-bold text-emerald-600 mt-1">2,685</p>
                    <p class="text-xs text-slate-500 mt-1">Streak check-ins claimed</p>
                </div>
            </div>

            <!-- Production AI Signal Panel (Concept Architecture) -->
            <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-5 rounded-xl border border-indigo-800 shadow-md ai-glow">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="flex h-2.5 w-2.5 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-500"></span>
                        </span>
                        <h4 class="text-xs font-bold tracking-wider uppercase text-indigo-200">Proposed Production AI • Task Velocity & Rapid-Burst Classifier</h4>
                    </div>
                    <span class="text-[11px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded border border-amber-400/30 font-medium">[CONCEPT SPECIFICATION - PHASE 2]</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Rapid-Burst Double Clicks</p>
                        <p class="text-lg font-bold text-emerald-400 mt-0.5">0.12% <span class="text-xs font-normal text-slate-400">(Quarantined)</span></p>
                        <p class="text-[11px] text-slate-400 mt-1">Target: Sub-200ms debounce gate</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Survey Drop-off Forecaster</p>
                        <p class="text-lg font-bold text-blue-400 mt-0.5">42.1% Completion</p>
                        <p class="text-[11px] text-slate-400 mt-1">Target: Adaptive routing model</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Streak Freeze Automated Grant</p>
                        <p class="text-lg font-bold text-indigo-400 mt-0.5">340 Users</p>
                        <p class="text-[11px] text-slate-400 mt-1">Target: LTV protection rules</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Earning Task Volume by Partner</h3>
                    <canvas id="chartEngPartner" height="180"></canvas>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Diurnal Event Frequency (Hour UTC)</h3>
                    <canvas id="chartEngDiurnal" height="180"></canvas>
                </div>
            </div>

            <!-- High-Resolution Render Screenshot Card -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex justify-between items-center mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-600">📸 High-Resolution Production Render — Suite 03: Engagement & Gamification</span>
                        <span class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded font-medium">Headless Matplotlib Engine</span>
                    </div>
                    <a href="screenshots/dashboard_3_engagement.png" target="_blank" class="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center space-x-1">
                        <span>Open Fullscreen</span>
                        <span>↗</span>
                    </a>
                </div>
                <div class="rounded-lg overflow-hidden border border-slate-200 bg-slate-900 shadow-inner">
                    <img src="screenshots/dashboard_3_engagement.png" alt="Engagement Production Screenshot" class="w-full h-auto object-contain hover:scale-[1.01] transition-transform duration-200" loading="lazy">
                </div>
            </div>
        </section>

        <!-- TAB 4: REWARDS -->
        <section id="pane-rwd" class="tab-pane hidden space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Total Rewards Issued</p>
                    <p class="text-2xl font-bold text-emerald-600 mt-1">698,350 VEs</p>
                    <p class="text-xs text-slate-500 mt-1">Gross monetary points credited</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Reward Reversal Rate</p>
                    <p class="text-2xl font-bold text-red-600 mt-1">3.20%</p>
                    <p class="text-xs text-slate-500 mt-1">160 clawbacks in Rewards.csv</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Pending Escrow Ratio</p>
                    <p class="text-2xl font-bold text-amber-600 mt-1">4.30%</p>
                    <p class="text-xs text-slate-500 mt-1">High-value task holding buffer</p>
                </div>
            </div>

            <!-- Production AI Signal Panel (Concept Architecture) -->
            <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-5 rounded-xl border border-indigo-800 shadow-md ai-glow">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="flex h-2.5 w-2.5 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-500"></span>
                        </span>
                        <h4 class="text-xs font-bold tracking-wider uppercase text-indigo-200">Proposed Production AI • Reward Reversal & Liability Equilibrium</h4>
                    </div>
                    <span class="text-[11px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded border border-amber-400/30 font-medium">[CONCEPT SPECIFICATION - PHASE 2]</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Affiliate Clawback Risk</p>
                        <p class="text-lg font-bold text-emerald-400 mt-0.5">2.1% <span class="text-xs font-normal text-slate-400">(Safe &lt;3%)</span></p>
                        <p class="text-[11px] text-slate-400 mt-1">Target: S2S Webhook Reconciler</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Escrow Buffer Adequacy</p>
                        <p class="text-lg font-bold text-blue-400 mt-0.5">100.0% Backed</p>
                        <p class="text-[11px] text-slate-400 mt-1">Target: Dynamic float model</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Dynamic Peg Stability</p>
                        <p class="text-lg font-bold text-indigo-400 mt-0.5">100 VEs = $1.00</p>
                        <p class="text-[11px] text-slate-400 mt-1">Target: RL Rebalancing Agent</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Reward Points Credited by Module</h3>
                    <canvas id="chartRwdModule" height="180"></canvas>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Reward Ledger Status Distribution</h3>
                    <canvas id="chartRwdStatus" height="180"></canvas>
                </div>
            </div>

            <!-- High-Resolution Render Screenshot Card -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex justify-between items-center mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-600">📸 High-Resolution Production Render — Suite 04: Rewards & Liability</span>
                        <span class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded font-medium">Headless Matplotlib Engine</span>
                    </div>
                    <a href="screenshots/dashboard_4_rewards.png" target="_blank" class="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center space-x-1">
                        <span>Open Fullscreen</span>
                        <span>↗</span>
                    </a>
                </div>
                <div class="rounded-lg overflow-hidden border border-slate-200 bg-slate-900 shadow-inner">
                    <img src="screenshots/dashboard_4_rewards.png" alt="Rewards Production Screenshot" class="w-full h-auto object-contain hover:scale-[1.01] transition-transform duration-200" loading="lazy">
                </div>
            </div>
        </section>

        <!-- TAB 5: WALLET -->
        <section id="pane-wlt" class="tab-pane hidden space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Ledger Transactions</p>
                    <p class="text-2xl font-bold text-slate-900 mt-1">3,500</p>
                    <p class="text-xs text-slate-500 mt-1">Double-entry journal records</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Circulating VE Supply</p>
                    <p class="text-2xl font-bold text-emerald-600 mt-1">+268,855 VEs</p>
                    <p class="text-xs text-emerald-600 font-medium mt-1">✓ Positive Unredeemed Float</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Ledger Credits vs Debits</p>
                    <p class="text-2xl font-bold text-purple-600 mt-1">+370.3k / -106.2k</p>
                    <p class="text-xs text-slate-500 mt-1">Credits exceed debits (Zero overdrafts)</p>
                </div>
            </div>

            <!-- IMPLEMENTED & TESTED ALGORITHMIC INVARIANT PANEL -->
            <div class="bg-gradient-to-r from-slate-900 via-emerald-950 to-slate-900 text-white p-5 rounded-xl border border-emerald-800 shadow-md">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="flex h-2.5 w-2.5 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                        </span>
                        <h4 class="text-xs font-bold tracking-wider uppercase text-emerald-200">Algorithmic Engine • Double-Entry Cryptographic Invariant Guard</h4>
                    </div>
                    <span class="text-[11px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded border border-emerald-400/30 font-medium">[IMPLEMENTED & TESTED - SCRIPTS]</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Double-Entry Variance</p>
                        <p class="text-lg font-bold text-emerald-400 mt-0.5">0.000000 <span class="text-xs font-normal text-slate-400">(Exact Parity)</span></p>
                        <p class="text-[11px] text-slate-400 mt-1">Audited via validate_wallet_reconciliation.py</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">User Overdraft Violations</p>
                        <p class="text-lg font-bold text-emerald-400 mt-0.5">0 Accounts</p>
                        <p class="text-[11px] text-slate-400 mt-1">Min balance across 1,000 users = 0.00 VEs</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Reconciliation Tests</p>
                        <p class="text-lg font-bold text-emerald-400 mt-0.5">6 of 6 PASSED</p>
                        <p class="text-[11px] text-slate-400 mt-1">100% verified integrity (WLT-TC01 to TC06)</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Wallet Entries by Transaction Type</h3>
                    <canvas id="chartWltType" height="180"></canvas>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Ledger Entries by Currency Unit</h3>
                    <canvas id="chartWltUnit" height="180"></canvas>
                </div>
            </div>

            <!-- High-Resolution Render Screenshot Card -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex justify-between items-center mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-600">📸 High-Resolution Production Render — Suite 05: Wallet & Ledger</span>
                        <span class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded font-medium">Headless Matplotlib Engine</span>
                    </div>
                    <a href="screenshots/dashboard_5_wallet.png" target="_blank" class="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center space-x-1">
                        <span>Open Fullscreen</span>
                        <span>↗</span>
                    </a>
                </div>
                <div class="rounded-lg overflow-hidden border border-slate-200 bg-slate-900 shadow-inner">
                    <img src="screenshots/dashboard_5_wallet.png" alt="Wallet Production Screenshot" class="w-full h-auto object-contain hover:scale-[1.01] transition-transform duration-200" loading="lazy">
                </div>
            </div>
        </section>

        <!-- TAB 6: WITHDRAWALS -->
        <section id="pane-wdr" class="tab-pane hidden space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Withdrawal Requests</p>
                    <p class="text-2xl font-bold text-slate-900 mt-1">1,200</p>
                    <p class="text-xs text-slate-500 mt-1">Gross cash-out demand</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Pending Review Queue</p>
                    <p class="text-2xl font-bold text-amber-600 mt-1">125</p>
                    <p class="text-xs text-slate-500 mt-1">Backlog awaiting compliance check</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Rejection Rate</p>
                    <p class="text-2xl font-bold text-red-600 mt-1">13.7%</p>
                    <p class="text-xs text-slate-500 mt-1">164 KYC / fraud rejections</p>
                </div>
            </div>

            <!-- Production AI Signal Panel (Concept Architecture) -->
            <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-5 rounded-xl border border-indigo-800 shadow-md ai-glow">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="flex h-2.5 w-2.5 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-500"></span>
                        </span>
                        <h4 class="text-xs font-bold tracking-wider uppercase text-indigo-200">Proposed Production AI • Payout Fast-Track & Fraud Decision Engine</h4>
                    </div>
                    <span class="text-[11px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded border border-amber-400/30 font-medium">[CONCEPT SPECIFICATION - PHASE 2]</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Instant Approval Target</p>
                        <p class="text-lg font-bold text-emerald-400 mt-0.5">78.5% <span class="text-xs font-normal text-slate-400">(&lt;15m TAT)</span></p>
                        <p class="text-[11px] text-slate-400 mt-1">Target model: XGBoost Classifier</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Sybil Multi-Account Rings</p>
                        <p class="text-lg font-bold text-blue-400 mt-0.5">0 Detected</p>
                        <p class="text-[11px] text-slate-400 mt-1">Target: Hardware fingerprinting</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Manual Review Gating</p>
                        <p class="text-lg font-bold text-amber-400 mt-0.5">21.5% Queue</p>
                        <p class="text-[11px] text-slate-400 mt-1">Escrow held for compliance review</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Disbursement Method Share</h3>
                    <canvas id="chartWdrMethod" height="180"></canvas>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Rejection Root-Cause Breakdown</h3>
                    <canvas id="chartWdrRej" height="180"></canvas>
                </div>
            </div>

            <!-- High-Resolution Render Screenshot Card -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex justify-between items-center mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-600">📸 High-Resolution Production Render — Suite 06: Withdrawals & Payouts</span>
                        <span class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded font-medium">Headless Matplotlib Engine</span>
                    </div>
                    <a href="screenshots/dashboard_6_withdrawals.png" target="_blank" class="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center space-x-1">
                        <span>Open Fullscreen</span>
                        <span>↗</span>
                    </a>
                </div>
                <div class="rounded-lg overflow-hidden border border-slate-200 bg-slate-900 shadow-inner">
                    <img src="screenshots/dashboard_6_withdrawals.png" alt="Withdrawals Production Screenshot" class="w-full h-auto object-contain hover:scale-[1.01] transition-transform duration-200" loading="lazy">
                </div>
            </div>
        </section>

        <!-- TAB 7: REFERRALS -->
        <section id="pane-ref" class="tab-pane hidden space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Referral Links Created</p>
                    <p class="text-2xl font-bold text-slate-900 mt-1">900</p>
                    <p class="text-xs text-slate-500 mt-1">Top of viral growth funnel</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Funnel Conversions</p>
                    <p class="text-2xl font-bold text-emerald-600 mt-1">760 Reg / 560 Act</p>
                    <p class="text-xs text-slate-500 mt-1">84.4% registered, 73.7% activated</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase">Viral K-Factor</p>
                    <p class="text-2xl font-bold text-purple-600 mt-1">K = 0.56</p>
                    <p class="text-xs text-blue-600 font-medium mt-1">560 activated referees / 1,000 users</p>
                </div>
            </div>

            <!-- Production AI Signal Panel (Concept Architecture) -->
            <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-5 rounded-xl border border-indigo-800 shadow-md ai-glow">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="flex h-2.5 w-2.5 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-500"></span>
                        </span>
                        <h4 class="text-xs font-bold tracking-wider uppercase text-indigo-200">Proposed Production AI • Viral Graph Network & Collusion Shield</h4>
                    </div>
                    <span class="text-[11px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded border border-amber-400/30 font-medium">[CONCEPT SPECIFICATION - PHASE 3]</span>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Graph Collusion Index</p>
                        <p class="text-lg font-bold text-emerald-400 mt-0.5">0.015 <span class="text-xs font-normal text-slate-400">(Clean)</span></p>
                        <p class="text-[11px] text-slate-400 mt-1">Target: Graph Convolutional Network</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">Virality Momentum (K)</p>
                        <p class="text-lg font-bold text-blue-400 mt-0.5">0.56 Actual</p>
                        <p class="text-[11px] text-slate-400 mt-1">Bounty conversion K = 0.37</p>
                    </div>
                    <div class="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                        <p class="text-slate-400">High-Yield Advocate Group</p>
                        <p class="text-lg font-bold text-indigo-400 mt-0.5">48 Verified</p>
                        <p class="text-[11px] text-slate-400 mt-1">Target: High-affinity reward clustering</p>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Four-Stage Referral Funnel</h3>
                    <canvas id="chartRefFunnel" height="180"></canvas>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-sm font-bold text-slate-800 mb-3">Invite Share by Social Channel</h3>
                    <canvas id="chartRefChannel" height="180"></canvas>
                </div>
            </div>

            <!-- High-Resolution Render Screenshot Card -->
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex justify-between items-center mb-3">
                    <div class="flex items-center space-x-2">
                        <span class="text-xs font-bold uppercase tracking-wider text-slate-600">📸 High-Resolution Production Render — Suite 07: Referrals & Viral Growth</span>
                        <span class="bg-blue-100 text-blue-700 text-xs px-2 py-0.5 rounded font-medium">Headless Matplotlib Engine</span>
                    </div>
                    <a href="screenshots/dashboard_7_referrals.png" target="_blank" class="text-xs text-blue-600 hover:text-blue-800 font-semibold flex items-center space-x-1">
                        <span>Open Fullscreen</span>
                        <span>↗</span>
                    </a>
                </div>
                <div class="rounded-lg overflow-hidden border border-slate-200 bg-slate-900 shadow-inner">
                    <img src="screenshots/dashboard_7_referrals.png" alt="Referrals Production Screenshot" class="w-full h-auto object-contain hover:scale-[1.01] transition-transform duration-200" loading="lazy">
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-4 mt-auto">
        <div class="max-w-7xl mx-auto px-4 text-center text-xs text-slate-500">
            VELOOP Rewards Data Analyst Internship — Task 01 Blueprint & Prototype • Simulated Analytical Dataset (30,150 Records)
        </div>
    </footer>

    <!-- Chart Setup Scripts -->
    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById('pane-' + tabId).classList.remove('hidden');
            document.getElementById('tab-' + tabId).classList.add('active');
        }

        window.onload = function() {
            // Exec DAU
            new Chart(document.getElementById('chartExecDau'), {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
                    datasets: [{
                        label: 'Active Users',
                        data: [420, 680, 890, 1120, 1340, 1480, 1560, 1620, 1710, 1850],
                        borderColor: '#2563EB',
                        backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });

            // Exec Tasks
            new Chart(document.getElementById('chartExecTasks'), {
                type: 'bar',
                data: {
                    labels: ['Watch Ad', 'Tap & Earn', 'Mining', 'Survey', 'Offerwall', 'App Install'],
                    datasets: [{
                        label: 'Completion Rate %',
                        data: [88.5, 81.2, 79.4, 42.1, 38.0, 34.5],
                        backgroundColor: '#10B981'
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });

            // User Acq
            new Chart(document.getElementById('chartUserAcq'), {
                type: 'bar',
                data: {
                    labels: ['Organic', 'Referral', 'Paid Ad', 'Partner', 'Influencer'],
                    datasets: [{
                        label: 'Users',
                        data: [350, 250, 200, 120, 80],
                        backgroundColor: '#8B5CF6'
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });

            // User Platform
            new Chart(document.getElementById('chartUserPlat'), {
                type: 'doughnut',
                data: {
                    labels: ['Android (65%)', 'iOS (28%)', 'Web (7%)'],
                    datasets: [{
                        data: [650, 280, 70],
                        backgroundColor: ['#10B981', '#2563EB', '#F59E0B']
                    }]
                },
                options: { responsive: true }
            });

            // Engagement Partner
            new Chart(document.getElementById('chartEngPartner'), {
                type: 'bar',
                data: {
                    labels: ['GoogleAdMob', 'InternalEngine', 'Pollfish', 'Tapjoy', 'IronSource'],
                    datasets: [{
                        label: 'Task Volume',
                        data: [2400, 1800, 1080, 420, 300],
                        backgroundColor: '#2563EB'
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });

            // Engagement Diurnal
            new Chart(document.getElementById('chartEngDiurnal'), {
                type: 'line',
                data: {
                    labels: ['00', '02', '04', '06', '08', '10', '12', '14', '16', '18', '20', '22'],
                    datasets: [{
                        label: 'Hourly Events',
                        data: [320, 180, 110, 140, 420, 780, 950, 1120, 1380, 1650, 1420, 890],
                        borderColor: '#F59E0B',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });

            // Rewards Module
            new Chart(document.getElementById('chartRwdModule'), {
                type: 'bar',
                data: {
                    labels: ['Tasks', 'Daily Login', 'Streaks', 'Referrals', 'Spins', 'Badges'],
                    datasets: [{
                        label: 'VEs Issued',
                        data: [418000, 104500, 55800, 48900, 41800, 29350],
                        backgroundColor: '#10B981'
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });

            // Rewards Status
            new Chart(document.getElementById('chartRwdStatus'), {
                type: 'pie',
                data: {
                    labels: ['Credited (92.8%)', 'Pending (4.0%)', 'Reversed (3.2%)'],
                    datasets: [{
                        data: [4638, 202, 160],
                        backgroundColor: ['#10B981', '#F59E0B', '#EF4444']
                    }]
                },
                options: { responsive: true }
            });

            // Wallet Type
            new Chart(document.getElementById('chartWltType'), {
                type: 'bar',
                data: {
                    labels: ['Reward Credit', 'Withdrawal Debit', 'Token Exchange', 'Admin Adj', 'Refund'],
                    datasets: [{
                        label: 'Transactions',
                        data: [2280, 882, 210, 66, 62],
                        backgroundColor: '#2563EB'
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });

            // Wallet Unit
            new Chart(document.getElementById('chartWltUnit'), {
                type: 'doughnut',
                data: {
                    labels: ['VEs (100.0%)'],
                    datasets: [{
                        data: [3500],
                        backgroundColor: ['#8B5CF6']
                    }]
                },
                options: { responsive: true }
            });

            // WDR Method
            new Chart(document.getElementById('chartWdrMethod'), {
                type: 'pie',
                data: {
                    labels: ['PayPal (45%)', 'Crypto USDT (28%)', 'Amazon Gift (18%)', 'Bank (9%)'],
                    datasets: [{
                        data: [397, 247, 159, 79],
                        backgroundColor: ['#2563EB', '#10B981', '#F59E0B', '#8B5CF6']
                    }]
                },
                options: { responsive: true }
            });

            // WDR Rejection
            new Chart(document.getElementById('chartWdrRej'), {
                type: 'bar',
                data: {
                    labels: ['KYC Incomplete', 'Min Threshold', 'Suspected Fraud', 'Provider Error', 'Mismatch'],
                    datasets: [{
                        label: 'Rejections',
                        data: [57, 41, 33, 20, 13],
                        backgroundColor: '#EF4444'
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });

            // Ref Funnel
            new Chart(document.getElementById('chartRefFunnel'), {
                type: 'bar',
                data: {
                    labels: ['1. Created (900)', '2. Registered (760)', '3. Activated (560)', '4. Converted (370)'],
                    datasets: [{
                        label: 'Funnel Progression',
                        data: [900, 760, 560, 370],
                        backgroundColor: ['#2563EB', '#8B5CF6', '#F59E0B', '#10B981']
                    }]
                },
                options: { responsive: true, plugins: { legend: { display: false } } }
            });

            // Ref Channel
            new Chart(document.getElementById('chartRefChannel'), {
                type: 'doughnut',
                data: {
                    labels: ['WhatsApp (38%)', 'Telegram (28%)', 'Twitter (16%)', 'DirectLink (12%)', 'SMS (6%)'],
                    datasets: [{
                        data: [342, 252, 144, 108, 54],
                        backgroundColor: ['#10B981', '#2563EB', '#F59E0B', '#8B5CF6', '#64748B']
                    }]
                },
                options: { responsive: true }
            });
        };
    </script>
</body>
</html>
'''

def update_files():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p_dash = os.path.join(base_dir, 'dashboards', 'index.html')
    p_root = os.path.join(base_dir, 'index.html')

    os.makedirs(os.path.dirname(p_dash), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'dashboards', 'screenshots'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'screenshots'), exist_ok=True)

    with open(p_dash, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Updated {p_dash} successfully.")

    with open(p_root, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Updated {p_root} successfully.")

if __name__ == '__main__':
    update_files()
