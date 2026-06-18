/* ============================================================
   FINANCEAI — app.js
   Complete frontend logic
   ============================================================ */

// ── Session ──────────────────────────────────────────────────
const SID = localStorage.getItem('fai_sid')
  || 'sid_' + Math.random().toString(36).substr(2, 9);
localStorage.setItem('fai_sid', SID);

let userProfile  = null;
let sipChart     = null;
let ringChart    = null;
let chatOpen     = false;

// ── Init ─────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  setupNav();
  setupChat();
  checkProfile();
  initSIP();
  updateSIP();
});

// ── TOAST ────────────────────────────────────────────────────
function toast(msg, type = 'info', duration = 3500) {
  const icons = { success:'✅', error:'❌', info:'ℹ️', warning:'⚠️' };
  const el    = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.innerHTML = `
    <span class="toast-icon">${icons[type]||'ℹ️'}</span>
    <span class="toast-text">${msg}</span>`;
  document.getElementById('toast-container').appendChild(el);
  setTimeout(() => {
    el.classList.add('toast-out');
    setTimeout(() => el.remove(), 280);
  }, duration);
}

// ── NAVIGATION ───────────────────────────────────────────────
function setupNav() {
  document.querySelectorAll('[data-page]').forEach(btn => {
    btn.addEventListener('click', () => gotoPage(btn.dataset.page, btn));
  });

  document.getElementById('learn-mf').addEventListener('click',
    () => { openChat(); chatSend('Teach me about mutual funds in detail'); });
  document.getElementById('learn-stocks').addEventListener('click',
    () => { openChat(); chatSend('Teach me about stocks — how they work and how to start'); });
  document.getElementById('learn-ppf').addEventListener('click',
    () => { openChat(); chatSend('Teach me about PPF — benefits and how to open an account'); });
  document.getElementById('learn-gold').addEventListener('click',
    () => { openChat(); chatSend('Teach me about investing in gold — SGB vs ETF vs physical'); });
  document.getElementById('fraud-check').addEventListener('click',
    () => { openChat(); chatSend('What are the most common investment scams in India right now? How do I spot them?'); });

  document.getElementById('profile-btn')?.addEventListener('click', showWizard);
}

function gotoPage(name, triggerEl) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn, .sidebar-btn').forEach(b => {
    b.classList.remove('active');
  });

  const page = document.getElementById('page-' + name);
  if (page) page.classList.add('active');

  document.querySelectorAll(`[data-page="${name}"]`)
    .forEach(b => b.classList.add('active'));

  if (name === 'goals')     loadGoals();
  if (name === 'portfolio') loadPortfolio();
}

// ── PROFILE / WIZARD ─────────────────────────────────────────
const WIZARD_STEPS = [
  {
    icon: '👋',
    title: 'Welcome to FinanceAI',
    subtitle: 'Your complete personalised money guide. Takes 2 minutes to set up — then every answer is specific to you.',
    fields: [
      { id: 'w-name', label: 'Your Name', type: 'text', placeholder: 'e.g. Rahul' },
      { id: 'w-age',  label: 'Your Age',  type: 'number', placeholder: 'e.g. 26' }
    ]
  },
  {
    icon: '💵',
    title: 'Your Monthly Money',
    subtitle: 'This helps us calculate your savings rate, emergency fund target, and investment capacity.',
    fields: [
      { id: 'w-income',   label: 'Monthly Income (₹)',   type: 'number', placeholder: 'e.g. 50000' },
      { id: 'w-expenses', label: 'Monthly Expenses (₹)', type: 'number', placeholder: 'e.g. 28000' }
    ]
  },
  {
    icon: '🎯',
    title: 'Your Goals & Risk',
    subtitle: 'This shapes your investment roadmap and the kind of advice we give you.',
    fields: [
      { id: 'w-goals', label: 'Financial Goals', type: 'text',
        placeholder: 'e.g. buy house in 5 years, retire at 55' },
      { id: 'w-risk', label: 'Risk Tolerance', type: 'select',
        options: [
          { value: 'low',    label: 'Low — safe investments only' },
          { value: 'medium', label: 'Medium — balanced approach', selected: true },
          { value: 'high',   label: 'High — I can handle volatility' }
        ]
      }
    ]
  },
  {
    icon: '🏦',
    title: 'Current Financial Situation',
    subtitle: 'Be honest — this helps us find your exact gaps and build the right plan.',
    fields: [
      { id: 'w-investments', label: 'Existing Investments',
        type: 'text', placeholder: 'e.g. none, or PPF + some FD' },
      { id: 'w-debts', label: 'Debts / EMIs',
        type: 'text', placeholder: 'e.g. none, or car loan ₹5000/month' }
    ]
  },
  {
    icon: '🛡️',
    title: 'Insurance & Dependents',
    subtitle: 'This determines your insurance needs and how much life cover you require.',
    fields: [
      { id: 'w-insurance', label: 'Do you have insurance?', type: 'select',
        options: [
          { value: 'false', label: 'No — I need to get it' },
          { value: 'true',  label: 'Yes — I have health/life insurance' }
        ]
      },
      { id: 'w-dependents', label: 'Number of Dependents',
        type: 'number', placeholder: 'e.g. 0 or 2' }
    ]
  }
];

let wizardStep   = 0;
let wizardData   = {};

function showWizard() {
  document.getElementById('wizard').style.display = 'flex';
  wizardStep = 0;
  wizardData = {};
  renderWizardStep();
}

function renderWizardStep() {
  const step = WIZARD_STEPS[wizardStep];
  const total = WIZARD_STEPS.length;

  // dots
  document.getElementById('wizard-dots').innerHTML =
    Array.from({ length: total }, (_, i) =>
      `<div class="wizard-step-dot ${
        i < wizardStep ? 'done' : i === wizardStep ? 'active' : ''
      }"></div>`
    ).join('');

  // content
  const fieldsHTML = step.fields.map(f => {
    if (f.type === 'select') {
      const opts = f.options.map(o =>
        `<option value="${o.value}" ${o.selected ? 'selected' : ''}>${o.label}</option>`
      ).join('');
      return `<div class="form-group">
        <label>${f.label}</label>
        <select class="form-select" id="${f.id}">${opts}</select>
      </div>`;
    }
    return `<div class="form-group">
      <label>${f.label}</label>
      <input class="form-input" id="${f.id}"
        type="${f.type}" placeholder="${f.placeholder || ''}"/>
    </div>`;
  }).join('');

  const isLast  = wizardStep === total - 1;
  const isFirst = wizardStep === 0;

  document.getElementById('wizard-content').innerHTML = `
    <div class="wizard-icon">${step.icon}</div>
    <div class="wizard-title">${step.title}</div>
    <div class="wizard-subtitle">${step.subtitle}</div>
    ${fieldsHTML}
    <div class="wizard-nav">
      <button class="wizard-back" onclick="wizardBack()"
        style="${isFirst ? 'visibility:hidden' : ''}">← Back</button>
      <button class="btn btn-primary"
        onclick="${isLast ? 'submitWizard()' : 'wizardNext()'}">
        ${isLast ? '🚀 Start FinanceAI' : 'Continue →'}
      </button>
    </div>`;

  restoreWizardStepValues(step);
  if (userProfile) prefillWizardStep(step);
}

function restoreWizardStepValues(step) {
  step.fields.forEach(f => {
    const el = document.getElementById(f.id);
    if (!el) return;
    const value = wizardData[f.id];
    if (value === undefined) return;
    el.value = value;
  });
}

function saveWizardStepValues() {
  const step = WIZARD_STEPS[wizardStep];
  if (!step || !step.fields) return;

  step.fields.forEach(f => {
    const el = document.getElementById(f.id);
    if (!el) return;
    wizardData[f.id] = el.value.trim();
  });
}

function prefillWizardStep(step) {
  const map = {
    'w-name': 'name', 'w-age': 'age',
    'w-income': 'monthly_income', 'w-expenses': 'monthly_expenses',
    'w-goals': 'financial_goals', 'w-risk': 'risk_tolerance',
    'w-investments': 'existing_investments', 'w-debts': 'debts',
    'w-insurance': 'has_insurance', 'w-dependents': 'dependents'
  };
  step.fields.forEach(f => {
    const el  = document.getElementById(f.id);
    const key = map[f.id];
    if (el && key && userProfile[key] !== undefined) {
      if (f.id === 'w-insurance') {
        el.value = userProfile[key] ? 'true' : 'false';
      } else {
        el.value = userProfile[key];
      }
      wizardData[f.id] = el.value;
    }
  });
}

function wizardNext() {
  saveWizardStepValues();
  wizardStep++;
  renderWizardStep();
}

function wizardBack() {
  saveWizardStepValues();
  if (wizardStep > 0) { wizardStep--; renderWizardStep(); }
}

async function submitWizard() {
  saveWizardStepValues();

  const get = id => {
    const el = document.getElementById(id);
    return el ? el.value.trim() : '';
  };

  const name     = wizardData['w-name'] || '';
  const age      = parseInt(wizardData['w-age'] || '0');
  const income   = parseFloat(wizardData['w-income'] || '0');
  const expenses = parseFloat(wizardData['w-expenses'] || '0');

  if (!name || !age || !income || !expenses) {
    toast('Please fill in all required fields', 'error');
    return;
  }

  const profile = {
    session_id:           SID,
    name,
    age,
    monthly_income:       income,
    monthly_expenses:     expenses,
    risk_tolerance:       wizardData['w-risk'] || 'medium',
    financial_goals:      wizardData['w-goals'] || 'not specified',
    existing_investments: wizardData['w-investments'] || 'none',
    has_insurance:        wizardData['w-insurance'] === 'true',
    dependents:           parseInt(wizardData['w-dependents'] || '0') || 0,
    debts:                wizardData['w-debts'] || 'none'
  };

  try {
    const res  = await fetch('/profile', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(profile)
    });
    const data = await res.json();
    if (data.success) {
      userProfile = profile;
      document.getElementById('wizard').style.display = 'none';
      updateProfileUI();
      refreshDashboard();
      toast(`Welcome to FinanceAI, ${name}! 🎉`, 'success');
    }
  } catch (e) {
    toast('Error saving profile. Please try again.', 'error');
  }
}

async function checkProfile() {
  try {
    const res  = await fetch('/profile/' + SID);
    const data = await res.json();
    if (data.exists) {
      userProfile = data.profile;
      updateProfileUI();
      refreshDashboard();
      loadPulse();
    } else {
      showWizard();
    }
  } catch (e) {
    showWizard();
  }
}

function updateProfileUI() {
  if (!userProfile) return;
  const btn = document.getElementById('profile-btn');
  if (btn) btn.style.display = 'flex';

  const av = document.getElementById('profile-avatar');
  if (av) av.textContent = userProfile.name.charAt(0).toUpperCase();

  const nb = document.getElementById('profile-name-btn');
  if (nb) nb.textContent = userProfile.name;

  // Fill metrics immediately
  const income   = userProfile.monthly_income;
  const expenses = userProfile.monthly_expenses;
  const savings  = income - expenses;
  const pct      = Math.round(savings / income * 100);

  setMetric('m-income',   '₹' + fmt(income),    '',
    income > 0 ? 'take-home' : '');
  setMetric('m-savings',  '₹' + fmt(savings),
    pct + '% of income',
    savings >= 0 ? 't-green' : 't-red');
  setMetric('m-emergency', '₹' + fmt(expenses * 6), '6 months expenses', 't-amber');
}

function setMetric(id, value, sub, colorClass) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = value;
  el.className   = 'metric-value ' + (colorClass || '');
  if (sub) {
    const subEl = el.nextElementSibling;
    if (subEl) subEl.textContent = sub;
  }
}

// ── DASHBOARD REFRESH ─────────────────────────────────────────
async function refreshDashboard() {
  await refreshScore();
  loadAlerts();
  loadPulse();
}

// ── HEALTH SCORE ──────────────────────────────────────────────
async function refreshScore() {
  try {
    const res  = await fetch('/health-score', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ session_id: SID })
    });
    const data = await res.json();
    if (data.error) return;

    const s = data.score_data;

    // Hide skeleton, show real
    document.getElementById('hero-skeleton').style.display = 'none';
    const real = document.getElementById('hero-real');
    real.style.display = 'flex';

    document.getElementById('score-number').textContent = s.score;
    document.getElementById('hero-greeting').textContent =
      'Hey ' + s.name + ', your financial health';
    document.getElementById('hero-sub').textContent =
      s.label + ' — ' + s.score + '/100';
    document.getElementById('hero-next-action').innerHTML =
      '<strong>Next step:</strong> ' + s.next_action;

    const grade = document.getElementById('hero-grade');
    grade.textContent = 'Grade ' + s.grade + ' — ' + s.label;
    grade.className   = 'grade-pill grade-' + s.color;

    drawRing(s.score, s.color);
    renderBreakdown(s.breakdown);

  } catch (e) {
    console.error('Score error:', e);
  }
}

const RING_COLORS = {
  green: '#00d084',
  blue:  '#4a8fff',
  amber: '#ffb547',
  red:   '#ff4d4d'
};

function drawRing(score, color) {
  const ctx = document.getElementById('score-ring').getContext('2d');
  if (ringChart) ringChart.destroy();
  const c = RING_COLORS[color] || '#4a8fff';
  ringChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      datasets: [{
        data: [score, 100 - score],
        backgroundColor: [c, '#162540'],
        borderWidth: 0
      }]
    },
    options: {
      cutout: '80%',
      responsive: false,
      animation: { duration: 1000, easing: 'easeInOutQuart' },
      plugins: { legend: { display: false }, tooltip: { enabled: false } }
    }
  });
}

function renderBreakdown(breakdown) {
  const grid = document.getElementById('breakdown-grid');
  grid.innerHTML = breakdown.map(b => {
    const pct = Math.round(b.score / b.max * 100);
    const col = pct >= 80 ? 'var(--green)'
               : pct >= 50 ? 'var(--blue)'
               : 'var(--red)';
    return `<div class="breakdown-item">
      <div class="breakdown-top">
        <span class="breakdown-cat">${b.category}</span>
        <span class="breakdown-pts" style="color:${col}">
          ${b.score}/${b.max}
        </span>
      </div>
      <div class="breakdown-bar">
        <div class="breakdown-fill"
          style="width:${pct}%;background:${col}"></div>
      </div>
      <div class="breakdown-status">${b.status}</div>
    </div>`;
  }).join('');
}

// ── ALERTS ────────────────────────────────────────────────────
async function loadAlerts() {
  try {
    const res  = await fetch('/daily-tips', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ session_id: SID })
    });
    const data = await res.json();
    const body = document.getElementById('alerts-body');
    if (data.error || !data.alerts || !data.alerts.length) {
      body.innerHTML = `<div class="empty-state" style="padding:20px">
        <p>No critical alerts — you're on track! ✅</p></div>`;
      return;
    }
    const map = {
      CRITICAL: 'alert-crit',
      HIGH:     'alert-high',
      MEDIUM:   'alert-medium',
      INFO:     'alert-info'
    };
    body.innerHTML = data.alerts.slice(0, 4).map(a =>
      `<div class="alert-item ${map[a.priority] || 'alert-medium'}">
        <div class="alert-icon">${a.icon}</div>
        <div>
          <div class="alert-title">${a.alert}</div>
          <div class="alert-action">${a.action}</div>
        </div>
      </div>`
    ).join('');
  } catch (e) {}
}

// ── MARKET PULSE ─────────────────────────────────────────────
async function loadPulse() {
  const items = [
    { sym: '^NSEI',    val: 'p-nifty',  chg: 'p-nifty-c',  label: 'Nifty 50' },
    { sym: '^NSEBANK', val: 'p-bnifty', chg: 'p-bnifty-c', label: 'Bank Nifty' },
    { sym: '^BSESN',   val: 'p-sensex', chg: 'p-sensex-c', label: 'Sensex' },
    { sym: 'GC=F',     val: 'p-gold',   chg: 'p-gold-c',   label: 'Gold' }
  ];

  for (const item of items) {
    try {
      const r = await fetch('/quick-price/' + encodeURIComponent(item.sym));
      const d = await r.json();
      const ve = document.getElementById(item.val);
      const ce = document.getElementById(item.chg);
      if (ve && d.current_price) {
        ve.textContent = '₹' + Math.round(d.current_price).toLocaleString('en-IN');
        ve.className   = 'pulse-value';
        if (ce) {
          ce.textContent = '● Live';
          ce.className   = 'pulse-change pulse-up';
        }
      }
    } catch (e) {
      const ve = document.getElementById(item.val);
      if (ve) { ve.textContent = '--'; ve.className = 'pulse-value'; }
    }
  }
}

// ── SIP CALCULATOR ───────────────────────────────────────────
function initSIP() {
  const ctx = document.getElementById('sip-chart').getContext('2d');
  sipChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [
        { label: 'Invested', data: [], backgroundColor: '#1a3a6a', borderWidth: 0 },
        { label: 'Returns',  data: [], backgroundColor: '#00d084', borderWidth: 0 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#4a6a8a', font: { size: 10 }, boxWidth: 10 } }
      },
      scales: {
        x: {
          stacked: true,
          ticks: { color: '#2a4a6a', font: { size: 10 } },
          grid: { color: '#0f1f38' }
        },
        y: {
          stacked: true,
          ticks: {
            color: '#2a4a6a',
            font: { size: 10 },
            callback: v =>
              v >= 10000000 ? (v/10000000).toFixed(1) + 'Cr'
            : v >= 100000  ? (v/100000).toFixed(1)   + 'L'
            : v >= 1000    ? (v/1000).toFixed(0)     + 'K'
            : v
          },
          grid: { color: '#0f1f38' }
        }
      }
    }
  });
}

function updateSIP() {
  const amt = parseInt(document.getElementById('sip-s1').value);
  const yrs = parseInt(document.getElementById('sip-s2').value);
  const rt  = parseInt(document.getElementById('sip-s3').value);

  document.getElementById('sip-v1').textContent = amt.toLocaleString('en-IN');
  document.getElementById('sip-v2').textContent = yrs;
  document.getElementById('sip-v3').textContent = rt;

  const r  = rt / 12 / 100;
  const n  = yrs * 12;
  const fv = r > 0 ? amt * (((1+r)**n - 1)/r) * (1+r) : amt * n;
  const iv = amt * n;
  const rv = fv - iv;

  document.getElementById('sip-r1').textContent = '₹' + fmtCr(iv);
  document.getElementById('sip-r2').textContent = '₹' + fmtCr(rv);
  document.getElementById('sip-r3').textContent = '₹' + fmtCr(fv);

  if (!sipChart) return;
  const labels = [], idata = [], rdata = [];
  const step   = Math.max(1, Math.floor(yrs / 7));
  for (let y = step; y <= yrs; y += step) {
    const nn  = y * 12;
    const fvy = r > 0 ? amt*(((1+r)**nn-1)/r)*(1+r) : amt*nn;
    const iny = amt * nn;
    labels.push(y + 'y');
    idata.push(Math.round(iny));
    rdata.push(Math.round(fvy - iny));
  }
  sipChart.data.labels              = labels;
  sipChart.data.datasets[0].data    = idata;
  sipChart.data.datasets[1].data    = rdata;
  sipChart.update('none');
}

// ── STOCKS ───────────────────────────────────────────────────
async function doAnalyze() {
  const sym = document.getElementById('stock-input').value.trim().toUpperCase();
  if (!sym) { toast('Enter a stock symbol like RELIANCE or TCS', 'warning'); return; }
  await runAnalysis(sym);
}

async function qa(sym) {
  document.getElementById('stock-input').value = sym;
  await runAnalysis(sym);
}

async function runAnalysis(sym) {
  const btn = document.getElementById('analyze-btn');
  btn.disabled = true;
  btn.textContent = '⏳ Fetching...';

  const res_div = document.getElementById('stock-result');
  res_div.innerHTML = `<div class="card">
    <div class="skeleton sk-box" style="margin-bottom:8px"></div>
    <div class="skeleton sk-box"></div>
  </div>`;

  try {
    const res  = await fetch('/analyze-stock', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ symbol: sym, session_id: SID })
    });
    const d = await res.json();

    if (d.error) {
      res_div.innerHTML = `<div class="card">
        <div class="empty-state">
          <div class="empty-icon">❌</div>
          <h3>Stock not found</h3>
          <p>${d.error}</p>
        </div>
      </div>`;
      toast('Stock not found: ' + sym, 'error');
    } else {
      renderStockCard(d, res_div);
      toast(sym + ' analysis complete', 'success');
    }
  } catch (e) {
    res_div.innerHTML = `<div class="card"><div class="empty-state">
      <p>Error fetching data. Try again.</p></div></div>`;
    toast('Error fetching stock data', 'error');
  }

  btn.disabled = false;
  btn.textContent = '⚡ Analyse Live';
}

function renderStockCard(d, container) {
  const ind      = d.indicators || {};
  const isUp     = d.pct_change >= 0;
  const chgSign  = isUp ? '+' : '';
  const chgClass = isUp ? 'price-up' : 'price-down';

  const recMap = {
    'STRONG BUY':  'rec-strong-buy',
    'BUY':         'rec-buy',
    'HOLD':        'rec-hold',
    'SELL':        'rec-sell',
    'STRONG SELL': 'rec-strong-sell'
  };
  const recClass = recMap[d.recommendation] || 'rec-hold';

  const rsi   = ind.rsi || 50;
  const rsiCl = rsi < 30 ? 'rsi-oversold'
               : rsi > 70 ? 'rsi-overbought'
               : 'rsi-neutral';
  const rsiZone = rsi < 30 ? 'Oversold — Buy zone'
                : rsi > 70 ? 'Overbought — Caution'
                : 'Neutral zone';

  container.innerHTML = `
  <div class="stock-result-card">
    <div class="stock-header">
      <div>
        <div class="stock-name">${d.company_name}</div>
        <div class="stock-sym">${d.symbol} · NSE · ${d.analysis_time}</div>
      </div>
      <div>
        <div class="stock-price">₹${(d.current_price||0).toLocaleString('en-IN')}</div>
        <div class="stock-change ${chgClass}">
          ${chgSign}${d.pct_change}% today
        </div>
      </div>
    </div>

    <div class="rec-badge ${recClass}">
      ${d.recommendation === 'STRONG BUY' ? '🚀' :
        d.recommendation === 'BUY'  ? '✅' :
        d.recommendation === 'HOLD' ? '⏸️' : '⚠️'}
      ${d.recommendation}
    </div>

    <div class="targets-grid">
      <div class="target-item">
        <div class="target-label">Entry Price</div>
        <div class="target-value">₹${d.targets?.entry_price || '--'}</div>
      </div>
      <div class="target-item">
        <div class="target-label">Stop Loss</div>
        <div class="target-value t-red">₹${d.targets?.stop_loss || '--'}</div>
      </div>
      <div class="target-item">
        <div class="target-label">Target 1</div>
        <div class="target-value t-green">₹${d.targets?.target_1 || '--'}</div>
      </div>
      <div class="target-item">
        <div class="target-label">Target 2</div>
        <div class="target-value t-green">₹${d.targets?.target_2 || '--'}</div>
      </div>
    </div>

    <div class="indicators-row">
      <div class="ind-item">
        <div class="ind-label">RSI (14)</div>
        <div class="rsi-gauge-wrap">
          <div class="rsi-value" style="color:${
            rsi < 30 ? 'var(--green)' : rsi > 70 ? 'var(--red)' : 'var(--amber)'
          }">${rsi}</div>
          <div class="rsi-zone ${rsiCl}">${rsiZone}</div>
        </div>
      </div>
      <div class="ind-item">
        <div class="ind-label">MACD</div>
        <div class="ind-value" style="color:${
          (ind.macd||0) > (ind.macd_signal||0) ? 'var(--green)' : 'var(--red)'
        }">${ind.macd || '--'}</div>
        <div style="font-size:11px;color:var(--text-3);margin-top:2px">
          Signal: ${ind.macd_signal || '--'}
        </div>
      </div>
      <div class="ind-item">
        <div class="ind-label">52W Range</div>
        <div class="ind-value" style="font-size:13px">
          ₹${ind.week52_low || '--'} — ₹${ind.week52_high || '--'}
        </div>
      </div>
    </div>

    <div class="ai-analysis">${d.ai_analysis}</div>
  </div>`;
}

// ── SAVINGS ──────────────────────────────────────────────────
async function loadSavings() {
  const content = document.getElementById('savings-content');
  content.innerHTML = `<div class="card-header">
    <span class="card-title">💰 Savings Analysis</span>
  </div>
  <div class="skeleton sk-box" style="margin-bottom:10px"></div>
  <div class="skeleton sk-box"></div>`;

  try {
    const res  = await fetch('/savings-analysis', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ session_id: SID })
    });
    const data = await res.json();
    if (data.error) { toast(data.error, 'error'); return; }
    renderSavings(data, content);
    toast('Savings analysis complete', 'success');
  } catch (e) {
    toast('Error loading savings analysis', 'error');
  }
}

function renderSavings(data, container) {
  const s = data.savings_data;
  const b = s.breakdown;

  const needsColor  = s.expenses <= b.needs_target
    ? 'var(--green)' : 'var(--red)';
  const savingsColor = s.savings_rate >= 20
    ? 'var(--green)' : s.savings_rate >= 10
    ? 'var(--amber)' : 'var(--red)';

  container.innerHTML = `
  <div class="card-header">
    <span class="card-title">💰 Savings Analysis — ${s.name}</span>
    <button class="card-action" onclick="loadSavings()">↻ Refresh</button>
  </div>

  <div class="budget-visual">
    <div class="budget-chart-wrap">
      <canvas id="budget-chart" width="180" height="180"></canvas>
    </div>
    <div class="budget-legend">
      <div style="font-size:22px;font-weight:800;color:${savingsColor};margin-bottom:4px">
        ${s.savings_rate}% saved
      </div>
      <div style="font-size:13px;color:var(--text-2);margin-bottom:16px">
        ₹${fmt(s.actual_savings)}/month · ${s.health_label}
      </div>
      <div class="legend-item">
        <div class="legend-dot" style="background:var(--blue)"></div>
        <div class="legend-label">Needs (50%)</div>
        <div class="legend-value">₹${fmt(b.needs_target)}</div>
      </div>
      <div class="legend-item">
        <div class="legend-dot" style="background:var(--purple)"></div>
        <div class="legend-label">Wants (30%)</div>
        <div class="legend-value">₹${fmt(b.wants_target)}</div>
      </div>
      <div class="legend-item">
        <div class="legend-dot" style="background:var(--green)"></div>
        <div class="legend-label">Savings (20%)</div>
        <div class="legend-value">₹${fmt(b.savings_target)}</div>
      </div>
      <div style="margin-top:12px;padding:10px;background:var(--bg-2);
        border-radius:8px;font-size:12px;color:var(--text-2)">
        Emergency Fund Target:<br/>
        <strong style="font-size:16px;color:var(--amber)">
          ₹${fmt(s.emergency_fund.target)}
        </strong>
        <span> (save ₹${fmt(s.emergency_fund.monthly_needed)}/mo)</span>
      </div>
    </div>
  </div>

  <div style="margin-top:16px;padding:14px;background:var(--bg-2);
    border-radius:12px;font-size:13px;color:var(--text-2);line-height:1.7">
    ${data.ai_analysis}
  </div>`;

  // Draw doughnut
  setTimeout(() => {
    const ctx = document.getElementById('budget-chart');
    if (!ctx) return;
    new Chart(ctx.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['Needs', 'Wants', 'Savings'],
        datasets: [{
          data: [b.needs_target, b.wants_target, b.savings_target],
          backgroundColor: ['#4a8fff', '#a78bfa', '#00d084'],
          borderWidth: 0,
          hoverOffset: 4
        }]
      },
      options: {
        cutout: '72%',
        responsive: false,
        plugins: { legend: { display: false } }
      }
    });
  }, 100);
}

// ── TAX ───────────────────────────────────────────────────────
async function loadTax() {
  const content = document.getElementById('tax-content');
  content.innerHTML = `<div class="card-header">
    <span class="card-title">📋 Tax Optimizer</span>
  </div>
  <div class="skeleton sk-box" style="margin-bottom:10px"></div>
  <div class="skeleton sk-box"></div>`;

  try {
    const res  = await fetch('/tax-analysis', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ session_id: SID })
    });
    const data = await res.json();
    if (data.error) { toast(data.error, 'error'); return; }
    renderTax(data, content);
    toast('Tax analysis complete', 'success');
  } catch (e) {
    toast('Error loading tax analysis', 'error');
  }
}

function renderTax(data, container) {
  const t = data.tax_data;
  container.innerHTML = `
  <div class="card-header">
    <span class="card-title">📋 Tax Optimizer — ${t.name}</span>
    <button class="card-action" onclick="loadTax()">↻ Refresh</button>
  </div>

  <div class="tax-saved-badge">
    <div class="tax-saved-amount">₹${fmt(t.total_tax_saved)}</div>
    <div class="tax-saved-label">total tax you can save this year</div>
  </div>

  <div class="tax-compare">
    <div class="tax-box">
      <div class="tax-box-label">Without Planning</div>
      <div class="tax-box-amount t-red">₹${fmt(t.tax_without_deductions)}</div>
      <div style="font-size:11px;color:var(--text-3);margin-top:4px">
        ${t.tax_bracket}
      </div>
    </div>
    <div class="tax-arrow">→</div>
    <div class="tax-box">
      <div class="tax-box-label">After Planning</div>
      <div class="tax-box-amount t-green">₹${fmt(t.tax_after_deductions)}</div>
      <div style="font-size:11px;color:var(--green);margin-top:4px">
        optimised
      </div>
    </div>
  </div>

  <div style="margin-bottom:16px">
    ${t.recommendations.map(r => `
      <div style="display:flex;justify-content:space-between;
        align-items:center;padding:12px 14px;background:var(--bg-2);
        border-radius:10px;margin-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:600">${r.section}</div>
          <div style="font-size:11px;color:var(--text-2)">${r.instrument}</div>
        </div>
        <div style="text-align:right">
          <div style="font-size:13px;font-weight:700;color:var(--blue)">
            Invest ₹${fmt(r.invest)}
          </div>
          <div style="font-size:11px;color:var(--green)">
            Save ₹${fmt(r.tax_saved)} tax
          </div>
        </div>
      </div>`).join('')}
  </div>

  <div style="padding:14px;background:var(--bg-2);border-radius:12px;
    font-size:13px;color:var(--text-2);line-height:1.7">
    ${data.ai_analysis}
  </div>`;
}

// ── INSURANCE ─────────────────────────────────────────────────
async function loadInsurance() {
  const content = document.getElementById('insurance-content');
  content.innerHTML = `<div class="card-header">
    <span class="card-title">🛡️ Insurance Planner</span>
  </div>
  <div class="skeleton sk-box" style="margin-bottom:10px"></div>
  <div class="skeleton sk-box"></div>`;

  try {
    const res  = await fetch('/insurance-analysis', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ session_id: SID })
    });
    const data = await res.json();
    if (data.error) { toast(data.error, 'error'); return; }
    renderInsurance(data, content);
    toast('Insurance analysis complete', 'success');
  } catch (e) {
    toast('Error loading insurance analysis', 'error');
  }
}

function renderInsurance(data, container) {
  const ins  = data.insurance_data;
  const hlth = ins.health_insurance;
  const term = ins.term_insurance;

  const urgencyHTML = ins.urgency_flags.map(u =>
    `<div class="alert-item alert-crit" style="margin-bottom:8px">
      <div class="alert-icon">🚨</div>
      <div>
        <div class="alert-title">${u.flag}</div>
        <div class="alert-action">${u.action}</div>
      </div>
    </div>`
  ).join('');

  container.innerHTML = `
  <div class="card-header">
    <span class="card-title">🛡️ Insurance Planner — ${ins.name}</span>
    <button class="card-action" onclick="loadInsurance()">↻ Refresh</button>
  </div>

  ${urgencyHTML}

  <div class="coverage-grid">
    <div class="coverage-card">
      <div class="coverage-card-status ${ins.has_insurance ? 'status-ok' : 'status-missing'}"></div>
      <div class="coverage-card-icon">🏥</div>
      <div class="coverage-card-type">Health Insurance</div>
      <div class="coverage-card-amount">₹${fmt(hlth.cover)}</div>
      <div class="coverage-card-premium">
        ~₹${fmt(hlth.monthly_premium)}/month
      </div>
    </div>
    ${ins.dependents > 0 ? `
    <div class="coverage-card">
      <div class="coverage-card-status ${ins.has_insurance ? 'status-ok' : 'status-missing'}"></div>
      <div class="coverage-card-icon">🔒</div>
      <div class="coverage-card-type">Term Life Insurance</div>
      <div class="coverage-card-amount">${term.cover_display}</div>
      <div class="coverage-card-premium">
        ~₹${fmt(term.monthly_premium)}/month
      </div>
    </div>` : ''}
    ${ins.needs_critical ? `
    <div class="coverage-card">
      <div class="coverage-card-status status-missing"></div>
      <div class="coverage-card-icon">❤️</div>
      <div class="coverage-card-type">Critical Illness</div>
      <div class="coverage-card-amount">₹${fmt(ins.critical_illness.cover)}</div>
      <div class="coverage-card-premium">
        ~₹${Math.round(ins.critical_illness.annual_premium/12).toLocaleString('en-IN')}/month
      </div>
    </div>` : ''}
    <div class="coverage-card">
      <div class="coverage-card-icon">💰</div>
      <div class="coverage-card-type">Total Monthly Budget</div>
      <div class="coverage-card-amount" style="color:var(--blue)">
        ₹${fmt(ins.total_monthly_cost)}
      </div>
      <div class="coverage-card-premium">all insurance combined</div>
    </div>
  </div>

  <div style="padding:14px;background:var(--bg-2);border-radius:12px;
    font-size:13px;color:var(--text-2);line-height:1.7;margin-top:4px">
    ${data.ai_analysis}
  </div>`;
}

// ── ROADMAP ───────────────────────────────────────────────────
async function loadRoadmap() {
  const content = document.getElementById('roadmap-content');
  content.innerHTML = `<div class="card-header">
    <span class="card-title">🗺️ Investment Roadmap</span>
  </div>
  <div class="skeleton sk-box" style="margin-bottom:10px"></div>
  <div class="skeleton sk-box"></div>`;

  try {
    const res  = await fetch('/investment-roadmap', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ session_id: SID })
    });
    const data = await res.json();
    if (data.error) { toast(data.error, 'error'); return; }
    renderRoadmap(data, content);
    toast('Investment roadmap ready', 'success');
  } catch (e) {
    toast('Error loading roadmap', 'error');
  }
}

function renderRoadmap(data, container) {
  const rd = data.roadmap;
  const phaseColors = ['var(--red)', 'var(--amber)', 'var(--blue)',
                       'var(--green)', 'var(--purple)'];

  const phasesHTML = rd.phases.map((p, i) => {
    const col = phaseColors[i % phaseColors.length];
    const sipHTML = p.sip_plan ? p.sip_plan.map(s =>
      `<div style="display:flex;justify-content:space-between;
        padding:6px 0;border-bottom:1px solid var(--card-border);
        font-size:12px;">
        <span style="color:var(--text-2)">${s.fund}</span>
        <span style="font-weight:700;color:var(--blue)">
          ₹${fmt(s.amount)}/mo
        </span>
      </div>`
    ).join('') : '';

    const projHTML = p.projections ? `
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;
        gap:6px;margin-top:10px;">
        <div style="text-align:center;padding:8px;background:var(--bg-1);border-radius:8px">
          <div style="font-size:11px;color:var(--text-3)">10 Years</div>
          <div style="font-size:14px;font-weight:700;color:var(--green)">
            ₹${fmtCr(p.projections['10_years'])}
          </div>
        </div>
        <div style="text-align:center;padding:8px;background:var(--bg-1);border-radius:8px">
          <div style="font-size:11px;color:var(--text-3)">20 Years</div>
          <div style="font-size:14px;font-weight:700;color:var(--green)">
            ₹${fmtCr(p.projections['20_years'])}
          </div>
        </div>
        <div style="text-align:center;padding:8px;background:var(--bg-1);border-radius:8px">
          <div style="font-size:11px;color:var(--text-3)">Retirement</div>
          <div style="font-size:14px;font-weight:700;color:var(--green)">
            ₹${fmtCr(p.projections['at_retirement'])}
          </div>
        </div>
      </div>` : '';

    return `
    <div class="phase-item">
      <div class="phase-line-wrap">
        <div class="phase-dot" style="background:${col};color:#000">
          ${p.phase}
        </div>
        ${i < rd.phases.length - 1 ? '<div class="phase-line"></div>' : ''}
      </div>
      <div class="phase-content">
        <div class="phase-title">${p.title}</div>
        <div class="phase-amount" style="color:${col}">
          ₹${fmt(p.amount)}/month
        </div>
        <div class="phase-desc">${p.description}</div>
        ${sipHTML}
        ${projHTML}
      </div>
    </div>`;
  }).join('');

  container.innerHTML = `
  <div class="card-header">
    <span class="card-title">🗺️ Investment Roadmap — ${rd.name}</span>
    <button class="card-action" onclick="loadRoadmap()">↻ Refresh</button>
  </div>

  <div style="background:var(--bg-2);border-radius:10px;padding:12px 14px;
    margin-bottom:16px;display:flex;justify-content:space-between;
    align-items:center;">
    <div>
      <div style="font-size:11px;color:var(--text-3)">Monthly Investable</div>
      <div style="font-size:22px;font-weight:800;color:var(--blue)">
        ₹${fmt(rd.available)}</div>
    </div>
    <div style="text-align:right">
      <div style="font-size:11px;color:var(--text-3)">Risk Profile</div>
      <div style="font-size:14px;font-weight:600;color:var(--text-1)">
        ${rd.risk_tolerance.toUpperCase()}
      </div>
    </div>
  </div>

  <div class="roadmap-phases">${phasesHTML}</div>

  <div style="padding:14px;background:var(--bg-2);border-radius:12px;
    font-size:13px;color:var(--text-2);line-height:1.7;margin-top:8px">
    ${data.ai_analysis}
  </div>`;
}

// ── GOALS ────────────────────────────────────────────────────
async function loadGoals() {
  try {
    const res  = await fetch('/goals/' + SID);
    const data = await res.json();
    renderGoals(data.goals || []);
  } catch (e) {}
}

async function addGoal() {
  const name   = document.getElementById('g-name').value.trim();
  const target = parseFloat(document.getElementById('g-target').value);
  const saved  = parseFloat(document.getElementById('g-saved').value) || 0;
  const date   = document.getElementById('g-date').value;

  if (!name || !target) {
    toast('Enter goal name and target amount', 'warning');
    return;
  }

  try {
    const res  = await fetch('/goals/add', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        session_id: SID, title: name,
        target_amount: target, deadline: date
      })
    });
    const data = await res.json();

    if (saved > 0 && data.goal_id) {
      await fetch('/goals/update', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({
          session_id: SID,
          goal_id:    data.goal_id,
          saved_amount: saved
        })
      });
    }

    document.getElementById('g-name').value   = '';
    document.getElementById('g-target').value = '';
    document.getElementById('g-saved').value  = '';
    document.getElementById('g-date').value   = '';
    renderGoals(data.goals || []);
    toast('Goal added successfully 🎯', 'success');
  } catch (e) {
    toast('Error adding goal', 'error');
  }
}

function renderGoals(goals) {
  const list = document.getElementById('goals-list');
  if (!goals.length) {
    list.innerHTML = `<div class="empty-state">
      <div class="empty-icon">🎯</div>
      <h3>No goals yet</h3>
      <p>Add your first financial goal above</p>
    </div>`;
    return;
  }
  list.innerHTML = goals.map(g => {
    const pct  = Math.min(100, Math.round(
      (g.saved_amount || 0) / g.target_amount * 100
    ));
    const done = g.status === 'completed';
    return `<div class="goal-card">
      <div class="goal-top">
        <div class="goal-name">
          ${done ? '✅' : '🎯'} ${g.title}
        </div>
        <div class="goal-deadline">${g.deadline || 'No deadline'}</div>
      </div>
      <div class="goal-progress-bar">
        <div class="goal-progress-fill ${done ? 'complete' : ''}"
          style="width:${pct}%"></div>
      </div>
      <div class="goal-row">
        <span>₹${fmt(g.saved_amount || 0)} saved</span>
        <span class="goal-pct">${pct}%</span>
        <span>₹${fmt(g.target_amount)} target</span>
      </div>
    </div>`;
  }).join('');
}

// ── PORTFOLIO ─────────────────────────────────────────────────
async function loadPortfolio() {
  try {
    const res  = await fetch('/portfolio/' + SID);
    const data = await res.json();
    if (data.portfolio) renderPortfolio(data.portfolio);
  } catch (e) {}
}

async function addAsset() {
  const name = document.getElementById('a-name').value.trim();
  const inv  = parseFloat(document.getElementById('a-inv').value) || 0;
  const cur  = parseFloat(document.getElementById('a-cur').value) || inv;

  if (!name || !inv) {
    toast('Enter asset name and invested amount', 'warning');
    return;
  }

  try {
    const res  = await fetch('/portfolio/add', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        session_id:    SID,
        asset_type:    document.getElementById('a-type').value || 'other',
        asset_name:    name,
        invested:      inv,
        current_value: cur,
        monthly_sip:   parseFloat(document.getElementById('a-sip').value) || 0
      })
    });
    const data = await res.json();
    document.getElementById('a-name').value = '';
    document.getElementById('a-inv').value  = '';
    document.getElementById('a-cur').value  = '';
    document.getElementById('a-sip').value  = '';
    if (data.portfolio) renderPortfolio(data.portfolio);
    toast('Investment added 💼', 'success');
  } catch (e) {
    toast('Error adding investment', 'error');
  }
}

function renderPortfolio(p) {
  document.getElementById('pt-inv').textContent =
    '₹' + fmt(p.total_invested);
  document.getElementById('pt-cur').textContent =
    '₹' + fmt(p.total_current);

  const gainEl = document.getElementById('pt-gain');
  gainEl.textContent = '₹' + fmt(Math.abs(p.total_gain));
  gainEl.className   = 'metric-value ' +
    (p.total_gain >= 0 ? 't-green' : 't-red');

  const pctEl = document.getElementById('pt-pct');
  pctEl.textContent = p.gain_pct + '%';
  pctEl.className   = 'metric-value ' +
    (p.gain_pct >= 0 ? 't-green' : 't-red');

  const list = document.getElementById('assets-list');
  if (!p.items.length) {
    list.innerHTML = `<div class="empty-state">
      <div class="empty-icon">💼</div>
      <h3>No investments tracked</h3>
      <p>Add your SIPs, stocks, FDs above</p>
    </div>`;
    return;
  }

  list.innerHTML = p.items.map(item => {
    const gain    = item.current_value - item.invested;
    const gainPct = item.invested > 0
      ? ((gain / item.invested) * 100).toFixed(1) : 0;
    const isUp    = gain >= 0;
    return `<div class="asset-item">
      <div>
        <div class="asset-name">${item.asset_name}</div>
        <div class="asset-type">${item.asset_type}${
          item.monthly_sip > 0
            ? ' · SIP ₹' + fmt(item.monthly_sip) + '/mo'
            : ''
        }</div>
      </div>
      <div class="asset-value-right">
        <div class="asset-current">
          ₹${fmt(item.current_value)}
        </div>
        <div class="asset-gain ${isUp ? 't-green' : 't-red'}">
          ${isUp ? '+' : '-'}₹${fmt(Math.abs(gain))} (${gainPct}%)
        </div>
      </div>
    </div>`;
  }).join('');
}

// ── CHAT ─────────────────────────────────────────────────────
function setupChat() {
  const ta = document.getElementById('chat-input');
  if (!ta) return;
  ta.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendChatMessage();
    }
  });
  ta.addEventListener('input', function() {
    this.style.height = '40px';
    this.style.height = Math.min(this.scrollHeight, 100) + 'px';
  });
}

function toggleChat() {
  const panel = document.getElementById('chat-panel');
  chatOpen    = !chatOpen;
  panel.classList.toggle('open', chatOpen);
  if (chatOpen) {
    setTimeout(() => {
      document.getElementById('chat-input')?.focus();
    }, 320);
  }
}

function openChat() {
  if (!chatOpen) toggleChat();
}

function addChatMsg(text, role) {
  const msgs = document.getElementById('chat-messages');
  const w    = msgs.querySelector('.chat-welcome');
  if (w) w.remove();

  const div = document.createElement('div');
  div.className   = 'chat-msg ' + role;
  div.textContent = text;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
  return div;
}

function chatSend(msg) {
  openChat();
  document.getElementById('chat-input').value = msg;
  sendChatMessage();
}

async function sendChatMessage() {
  const ta  = document.getElementById('chat-input');
  const btn = document.getElementById('chat-send-btn');
  const txt = ta.value.trim();
  if (!txt) return;

  ta.value    = '';
  ta.style.height = '40px';
  btn.disabled = true;

  addChatMsg(txt, 'user');
  const thinking = addChatMsg('FinanceAI is thinking...', 'thinking');

  try {
    const res  = await fetch('/chat', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ session_id: SID, message: txt })
    });
    const data = await res.json();
    thinking.remove();
    addChatMsg(data.reply, 'ai');
  } catch (e) {
    thinking.remove();
    addChatMsg('Something went wrong. Please try again.', 'ai');
  }

  btn.disabled = false;
  ta.focus();
}

// ── UTILITIES ────────────────────────────────────────────────
function fmt(n) {
  return (n || 0).toLocaleString('en-IN');
}

function fmtCr(n) {
  if (!n) return '0';
  if (n >= 10000000) return (n / 10000000).toFixed(1) + 'Cr';
  if (n >= 100000)   return (n / 100000).toFixed(1)   + 'L';
  if (n >= 1000)     return (n / 1000).toFixed(1)     + 'K';
  return Math.round(n).toString();
}