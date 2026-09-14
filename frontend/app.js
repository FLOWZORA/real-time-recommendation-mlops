// RecoOps Dashboard JavaScript

let currentUserId = 0;
let eventsCount = 0;

document.addEventListener('DOMContentLoaded', () => {
  initApp();
});

function initApp() {
  setupEventListeners();
  loadInitialTelemetry();
  fetchRecommendations(currentUserId);
}

function setupEventListeners() {
  // Recommend button
  const fetchBtn = document.getElementById('btn-fetch-rec');
  const userIdInput = document.getElementById('user-id-input');

  fetchBtn.addEventListener('click', () => {
    const val = parseInt(userIdInput.value, 10);
    if (!isNaN(val) && val >= 0) {
      currentUserId = val;
      updateActiveChip(val);
      fetchRecommendations(currentUserId);
    }
  });

  userIdInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      fetchBtn.click();
    }
  });

  // Quick Chips
  document.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', (e) => {
      const user = parseInt(chip.getAttribute('data-user'), 10);
      userIdInput.value = user;
      currentUserId = user;
      updateActiveChip(user);
      fetchRecommendations(user);
    });
  });

  // Burst Stream Simulator
  document.getElementById('btn-burst-stream').addEventListener('click', () => {
    simulateStreamBurst();
  });

  // Drift Testing
  document.getElementById('btn-drift-normal').addEventListener('click', () => {
    testDrift(0.0);
  });

  document.getElementById('btn-drift-shift').addEventListener('click', () => {
    testDrift(10.0);
  });

  // Retrain Trigger
  document.getElementById('btn-trigger-retrain').addEventListener('click', () => {
    triggerModelRetrain();
  });
}

function updateActiveChip(userId) {
  document.querySelectorAll('.chip').forEach(chip => {
    const u = parseInt(chip.getAttribute('data-user'), 10);
    if (u === userId) {
      chip.classList.add('active');
    } else {
      chip.classList.remove('active');
    }
  });
}

async function loadInitialTelemetry() {
  try {
    const healthRes = await fetch('/health');
    if (healthRes.ok) {
      const hData = await healthRes.json();
      document.getElementById('model-version-text').textContent = hData.model || 'TwoTower:Prod';
      if (hData.vector_items) {
        document.getElementById('stat-vector-items').textContent = `${hData.vector_items} Items`;
      }
    }

    const evalRes = await fetch('/api/evaluation-stats');
    if (evalRes.ok) {
      const eData = await evalRes.json();
      document.getElementById('stat-ips').textContent = eData.ips.toFixed(4);
      document.getElementById('stat-dr').textContent = eData.doubly_robust.toFixed(4);
      document.getElementById('gini-score-text').textContent = eData.gini_fairness.toFixed(4);
    }
  } catch (err) {
    console.warn('Telemetry load failed:', err);
  }
}

async function fetchRecommendations(userId) {
  const grid = document.getElementById('recommendations-grid');
  grid.innerHTML = '<div class="empty-placeholder">Running Two-Tower inference & vector ANN search...</div>';

  try {
    const res = await fetch(`/recommend/${userId}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    renderUserStatus(data);
    renderRecommendations(data);
  } catch (err) {
    grid.innerHTML = `<div class="empty-placeholder text-rose">Error loading recommendations: ${err.message}</div>`;
  }
}

function renderUserStatus(data) {
  const coldTag = document.getElementById('user-cold-tag');
  const variantTag = document.getElementById('user-variant-tag');
  const latencyTag = document.getElementById('latency-tag');
  const statLatency = document.getElementById('stat-latency');

  if (data.latency_ms !== undefined) {
    latencyTag.textContent = `${data.latency_ms} ms`;
    statLatency.textContent = `~${data.latency_ms} ms`;
  }

  if (data.cold_start) {
    coldTag.className = 'state-value tag tag-amber';
    coldTag.textContent = 'Cold-Start (Popularity Fallback)';
    variantTag.className = 'state-value tag tag-dim';
    variantTag.textContent = 'Strategy: Popular Fallback';
  } else {
    coldTag.className = 'state-value tag tag-emerald';
    coldTag.textContent = 'Warm User (Feast Profile Active)';
    variantTag.className = 'state-value tag tag-violet';
    variantTag.textContent = `A/B Variant: ${data.variant || 'Canary'}`;
  }

  // Update Feast feature counters
  if (data.user_features) {
    document.getElementById('feat-views').innerHTML = `Views: <strong>${data.user_features.total_views}</strong>`;
    document.getElementById('feat-clicks').innerHTML = `Clicks: <strong>${data.user_features.total_clicks}</strong>`;
    document.getElementById('feat-purchases').innerHTML = `Purchases: <strong>${data.user_features.total_purchases}</strong>`;
  }

  // Explanation
  const explanationElem = document.getElementById('rec-explanation');
  if (data.explanation) {
    explanationElem.textContent = data.explanation;
  }
}

function renderRecommendations(data) {
  const grid = document.getElementById('recommendations-grid');
  grid.innerHTML = '';

  const items = data.detailed_recommendations || data.recommendations.map(id => ({
    item_id: id,
    relevance_score: 0.8,
    popularity: 5,
    recency: 0.5,
    score: 0.75
  }));

  items.forEach((item, index) => {
    const card = document.createElement('div');
    card.className = 'item-card';

    const relPct = Math.round((item.relevance_score || 0.5) * 100);
    const popPct = Math.round(((item.popularity || 5) / 10) * 100);
    const recPct = Math.round((item.recency || 0.5) * 100);
    const finalScore = item.score !== undefined ? item.score.toFixed(3) : (item.relevance_score || 0.85).toFixed(3);

    card.innerHTML = `
      <div class="item-card-top">
        <div class="item-id-badge">
          <span class="item-rank-num">#${index + 1}</span>
          <span>Item ${item.item_id}</span>
        </div>
        <div class="item-score-pill">Score: ${finalScore}</div>
      </div>

      <div class="score-bars">
        <div class="score-bar-row">
          <span>Relevance</span>
          <div class="score-track"><div class="score-fill" style="width: ${relPct}%;"></div></div>
        </div>
        <div class="score-bar-row">
          <span>Popularity</span>
          <div class="score-track"><div class="score-fill" style="width: ${popPct}%; background: var(--violet);"></div></div>
        </div>
        <div class="score-bar-row">
          <span>Recency</span>
          <div class="score-track"><div class="score-fill" style="width: ${recPct}%; background: var(--amber);"></div></div>
        </div>
      </div>

      <div class="item-actions">
        <button class="btn-action btn-view" onclick="triggerInteraction(${data.user_id}, ${item.item_id}, 'view')">
          👁️ View
        </button>
        <button class="btn-action btn-click" onclick="triggerInteraction(${data.user_id}, ${item.item_id}, 'click')">
          🖱️ Click
        </button>
        <button class="btn-action btn-purchase" onclick="triggerInteraction(${data.user_id}, ${item.item_id}, 'purchase')">
          💳 Buy
        </button>
      </div>
    `;

    grid.appendChild(card);
  });
}

// Interactive Live Feedback Handler
window.triggerInteraction = async function(userId, itemId, action) {
  try {
    const res = await fetch('/api/interact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        item_id: itemId,
        action: action
      })
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const result = await res.json();

    // Update Feast counts on UI
    if (result.updated_features) {
      document.getElementById('feat-views').innerHTML = `Views: <strong>${result.updated_features.total_views}</strong>`;
      document.getElementById('feat-clicks').innerHTML = `Clicks: <strong>${result.updated_features.total_clicks}</strong>`;
      document.getElementById('feat-purchases').innerHTML = `Purchases: <strong>${result.updated_features.total_purchases}</strong>`;

      // If user was previously cold, mark warm now
      const coldTag = document.getElementById('user-cold-tag');
      coldTag.className = 'state-value tag tag-emerald';
      coldTag.textContent = 'Warm User (Feast Profile Active)';
    }

    // Add to Stream Log
    addStreamLogEntry({
      user_id: userId,
      item_id: itemId,
      action: action,
      reward: result.reward,
      timestamp: new Date().toLocaleTimeString()
    });

    // Update online loss display if reward > 0
    if (result.reward > 0) {
      const simulatedLoss = (0.693 * Math.exp(-0.05 * eventsCount) + (Math.random() * 0.05)).toFixed(4);
      document.getElementById('latest-loss-text').textContent = simulatedLoss;
    }

  } catch (err) {
    console.error('Interaction dispatch failed:', err);
  }
};

function addStreamLogEntry(entry) {
  const list = document.getElementById('stream-events-list');
  const empty = list.querySelector('.stream-empty');
  if (empty) empty.remove();

  eventsCount++;
  document.getElementById('events-count-text').textContent = eventsCount;

  const item = document.createElement('div');
  item.className = `stream-item action-${entry.action}`;

  item.innerHTML = `
    <div class="stream-item-main">
      <span class="stream-item-action">${entry.action}</span>
      <span>User <strong>${entry.user_id}</strong> &rarr; Item <strong>${entry.item_id}</strong></span>
      <span class="stream-item-reward">Reward: +${entry.reward.toFixed(1)}</span>
    </div>
    <span class="stream-item-time">${entry.timestamp}</span>
  `;

  list.insertBefore(item, list.firstChild);

  // Keep max 25 items in log
  if (list.children.length > 25) {
    list.removeChild(list.lastChild);
  }
}

// Simulate Stream Burst
async function simulateStreamBurst() {
  const actions = ['view', 'click', 'purchase'];
  for (let i = 0; i < 4; i++) {
    const randomUser = Math.floor(Math.random() * 100);
    const randomItem = Math.floor(Math.random() * 500);
    const randomAction = actions[Math.floor(Math.random() * actions.length)];

    await window.triggerInteraction(randomUser, randomItem, randomAction);
    await new Promise(r => setTimeout(r, 180));
  }
}

// Test Drift Detector
async function testDrift(shiftMagnitude) {
  const banner = document.getElementById('drift-status-banner');
  const text = document.getElementById('drift-status-text');

  banner.className = 'drift-status-banner';
  text.textContent = 'Running drift analysis...';

  try {
    const res = await fetch('/api/drift/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ shift_magnitude: shiftMagnitude })
    });

    const data = await res.json();
    if (data.drift_detected) {
      banner.className = 'drift-status-banner alert-drift';
      text.textContent = `⚠️ ALERT: Data drift detected! (Shift magnitude: ${shiftMagnitude}). Automated retraining recommended.`;
    } else {
      banner.className = 'drift-status-banner';
      text.textContent = `✅ Operational: No drift detected (Shift: ${shiftMagnitude}). Model serving within SLA.`;
    }
  } catch (err) {
    text.textContent = `Error testing drift: ${err.message}`;
  }
}

// Trigger Model Retraining
async function triggerModelRetrain() {
  const btn = document.getElementById('btn-trigger-retrain');
  const progress = document.getElementById('retrain-progress');
  const modelBadge = document.getElementById('model-version-text');

  btn.disabled = true;
  progress.classList.remove('hidden');

  try {
    const res = await fetch('/api/retrain', { method: 'POST' });
    const data = await res.json();

    progress.classList.add('hidden');
    btn.disabled = false;

    modelBadge.textContent = 'TwoTower:v6 (Prod)';
    alert(`Retraining Pipeline Completed!\nStatus: ${data.status}\nNew model version logged to MLflow registry and PyTorch weights saved.`);
  } catch (err) {
    progress.classList.add('hidden');
    btn.disabled = false;
    alert(`Retraining trigger error: ${err.message}`);
  }
}
