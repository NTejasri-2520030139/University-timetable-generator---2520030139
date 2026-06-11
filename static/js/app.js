/**
 * Smart University Timetable Generator — app.js
 * Client-side logic: dark mode, modals, timetable rendering,
 * real-time search/filter, CSP generation, toast notifications.
 */

'use strict';

// ─── Dark Mode ───────────────────────────────────────────────────────────────

const themeToggle = document.getElementById('theme-toggle');
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
if (themeToggle) {
  if (savedTheme === 'dark') themeToggle.classList.add('dark');
  themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    themeToggle.classList.toggle('dark', next === 'dark');
  });
}

// ─── Toast Notifications ─────────────────────────────────────────────────────

function showToast(msg, type = 'info') {
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  const colors = { success: '#10b981', error: '#ef4444', info: '#6366f1', warning: '#f59e0b' };
  const toast = document.createElement('div');
  toast.style.cssText = `
    position:fixed; bottom:24px; right:24px; z-index:9999;
    background:var(--bg-card); border:1px solid ${colors[type]}44;
    border-left:3px solid ${colors[type]};
    border-radius:10px; padding:12px 18px;
    display:flex; align-items:center; gap:10px;
    font-size:.84rem; font-weight:500; color:var(--text-primary);
    box-shadow:0 8px 32px rgba(0,0,0,.3);
    min-width:280px; max-width:380px;
    animation:toastIn .4s cubic-bezier(.34,1.56,.64,1);
    backdrop-filter:blur(12px);
  `;
  toast.innerHTML = `<span>${icons[type]}</span><span>${msg}</span>`;

  const style = document.createElement('style');
  style.textContent = `@keyframes toastIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}
    @keyframes toastOut{from{transform:translateX(0);opacity:1}to{transform:translateX(100%);opacity:0}}`;
  document.head.appendChild(style);
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'toastOut .3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ─── Alert dismissal ─────────────────────────────────────────────────────────

document.querySelectorAll('.alert-close').forEach(btn => {
  btn.addEventListener('click', () => btn.closest('.alert').remove());
});

// ─── Modal System ─────────────────────────────────────────────────────────────

function openModal(id) {
  document.getElementById(id)?.classList.add('open');
}
function closeModal(id) {
  document.getElementById(id)?.classList.remove('open');
}
// Close on overlay click
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', e => {
    if (e.target === overlay) overlay.classList.remove('open');
  });
});
// Close on Escape
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open'));
  }
});

// ─── Edit modals: pre-fill form fields ───────────────────────────────────────

function fillEditModal(modalId, data) {
  const modal = document.getElementById(modalId);
  if (!modal) return;
  Object.entries(data).forEach(([key, val]) => {
    const el = modal.querySelector(`[name="${key}"]`);
    if (el) el.value = val;
  });
  openModal(modalId);
}

// ─── CSP Timetable Generation ─────────────────────────────────────────────────

const generateBtn = document.getElementById('btn-generate');
if (generateBtn) {
  generateBtn.addEventListener('click', async () => {
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<span class="spinner-inline"></span> Solving CSP...';

    // Show progress
    const progressEl = document.getElementById('csp-progress');
    if (progressEl) {
      progressEl.classList.remove('hidden');
      animateSteps();
    }

    try {
      const res = await fetch('/teacher/timetable/generate', { method: 'POST' });
      const data = await res.json();

      if (progressEl) progressEl.classList.add('hidden');

      if (data.success) {
        // Update metrics panel
        renderMetrics(data.metrics);
        showToast(`Timetable generated! ${data.metrics.backtracks} backtracks, solved in ${data.metrics.solve_time_ms}ms`, 'success');
        setTimeout(() => location.reload(), 1200);
      } else {
        showToast(data.error || 'Could not generate timetable.', 'error');
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<span class="shimmer"></span>🧠 Solve CSP & Generate';
      }
    } catch (err) {
      showToast('Network error: ' + err.message, 'error');
      generateBtn.disabled = false;
      generateBtn.innerHTML = '<span class="shimmer"></span>🧠 Solve CSP & Generate';
    }
  });
}

function animateSteps() {
  const steps = document.querySelectorAll('.csp-step');
  steps.forEach(s => s.className = 'csp-step');
  let i = 0;
  const interval = setInterval(() => {
    if (i > 0 && steps[i-1]) { steps[i-1].classList.add('done'); steps[i-1].classList.remove('active'); }
    if (i < steps.length) { steps[i].classList.add('active'); i++; }
    else clearInterval(interval);
  }, 320);
}

function renderMetrics(m) {
  const ids = {
    'met-time': m.solve_time_ms,
    'met-backtracks': m.backtracks,
    'met-checks': m.constraint_checks,
    'met-vars': m.variables,
    'met-constraints': m.constraints,
    'met-quality': m.quality_score,
  };
  Object.entries(ids).forEach(([id, val]) => {
    const el = document.getElementById(id);
    if (el) animateCounter(el, val, id === 'met-quality');
  });
}

function animateCounter(el, target, isFloat = false) {
  const dur = 1000, start = performance.now();
  const tick = now => {
    const p = Math.min((now - start) / dur, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = isFloat ? (eased * target).toFixed(1) : Math.round(eased * target).toLocaleString();
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

// ─── Timetable Grid Rendering ─────────────────────────────────────────────────

const colorMap = {};
let colorIdx = 0;
function getCourseColor(name) {
  if (!(name in colorMap)) colorMap[name] = colorIdx++ % 10;
  return colorMap[name];
}

function buildTimetableGrid(entries, days, timeslots, conflictIds = []) {
  const grid = document.getElementById('tt-grid');
  if (!grid) return;

  const slots = [...new Set(timeslots.map(ts => `${ts.start_time}|${ts.end_time}`))].sort();
  const numCols = days.length + 1;
  grid.style.gridTemplateColumns = `130px repeat(${days.length}, 1fr)`;
  grid.innerHTML = '';

  // Header row
  const cornerH = document.createElement('div');
  cornerH.className = 'tt-grid-header time-col';
  cornerH.textContent = 'Time';
  grid.appendChild(cornerH);
  days.forEach(day => {
    const h = document.createElement('div');
    h.className = 'tt-grid-header';
    h.textContent = day;
    grid.appendChild(h);
  });

  // Data rows
  slots.forEach(slotStr => {
    const [start, end] = slotStr.split('|');
    const timeCell = document.createElement('div');
    timeCell.className = 'tt-time-cell';
    timeCell.textContent = `${start}–${end}`;
    grid.appendChild(timeCell);

    days.forEach(day => {
      const cell = document.createElement('div');
      cell.className = 'tt-cell';

      const matching = entries.filter(e => e.day === day && e.start_time === start);
      matching.forEach(e => {
        const colorClass = `tt-c${getCourseColor(e.subject_name || e.course_name)}`;
        const isConflict = conflictIds.includes(e.id);
        const div = document.createElement('div');
        div.className = `tt-entry ${colorClass}${isConflict ? ' conflict' : ''}`;
        div.dataset.teacher = (e.teacher_name || '').toLowerCase();
        div.dataset.subject = (e.subject_name || '').toLowerCase();
        div.dataset.room = (e.room_number || '').toLowerCase();
        div.innerHTML = `
          <span class="entry-subject">${e.subject_name || ''}</span>
          <span class="entry-teacher">👨‍🏫 ${e.teacher_name || ''}</span>
          <span class="entry-room">🏫 ${e.room_number || ''}</span>
        `;
        div.title = `${e.subject_name}\n${e.teacher_name}\nRoom: ${e.room_number}\n${day} ${start}–${end}`;
        cell.appendChild(div);
      });
      grid.appendChild(cell);
    });
  });
}

// ─── Real-time Search & Filter ────────────────────────────────────────────────

function initFilters() {
  const searchInput  = document.getElementById('tt-search');
  const filterTeacher = document.getElementById('filter-teacher');
  const filterSubject = document.getElementById('filter-subject');
  const filterRoom    = document.getElementById('filter-room');
  const filterDay     = document.getElementById('filter-day');

  function applyFilters() {
    const search  = searchInput?.value.toLowerCase() || '';
    const teacher = filterTeacher?.value.toLowerCase() || '';
    const subject = filterSubject?.value.toLowerCase() || '';
    const room    = filterRoom?.value.toLowerCase() || '';
    const day     = filterDay?.value.toLowerCase() || '';

    document.querySelectorAll('.tt-entry').forEach(el => {
      const elTeacher = el.dataset.teacher || '';
      const elSubject = el.dataset.subject || '';
      const elRoom    = el.dataset.room || '';
      const elDay     = (el.closest('[data-day]')?.dataset.day || '').toLowerCase();

      const matches = (
        (!search  || elSubject.includes(search) || elTeacher.includes(search) || elRoom.includes(search)) &&
        (!teacher || elTeacher.includes(teacher)) &&
        (!subject || elSubject.includes(subject)) &&
        (!room    || elRoom.includes(room)) &&
        (!day     || elDay.includes(day))
      );
      el.style.opacity = matches ? '1' : '0.12';
      el.style.transform = matches ? '' : 'scale(.94)';
    });
  }

  [searchInput, filterTeacher, filterSubject, filterRoom, filterDay].forEach(el => {
    el?.addEventListener('input', applyFilters);
    el?.addEventListener('change', applyFilters);
  });
}

// ─── Bar Chart Renderer ──────────────────────────────────────────────────────

function renderBarChart(containerId, data, labelKey, valueKey) {
  const container = document.getElementById(containerId);
  if (!container || !data?.length) return;

  const maxVal = Math.max(...data.map(d => d[valueKey]), 1);
  container.innerHTML = data.map(d => `
    <div class="bar-row">
      <span class="bar-label" title="${d[labelKey]}">${d[labelKey]}</span>
      <div class="bar-track">
        <div class="bar-fill" style="width:0%" data-target="${Math.round(d[valueKey]/maxVal*100)}"></div>
      </div>
      <span class="bar-count">${d[valueKey]}</span>
    </div>
  `).join('');

  // Animate bar fills
  requestAnimationFrame(() => {
    container.querySelectorAll('.bar-fill').forEach(bar => {
      bar.style.width = bar.dataset.target + '%';
    });
  });
}

// ─── Conflict API Poll ────────────────────────────────────────────────────────

async function checkConflicts() {
  try {
    const res = await fetch('/api/conflicts');
    const data = await res.json();
    const el = document.getElementById('conflict-count');
    if (el) el.textContent = data.count;
    const badge = document.getElementById('conflict-badge');
    if (badge) {
      badge.textContent = data.count;
      badge.classList.toggle('hidden', data.count === 0);
    }
  } catch {}
}

// ─── Smooth Bar Chart Auto-animate on scroll ─────────────────────────────────

function observeCharts() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.querySelectorAll('.bar-fill').forEach(bar => {
          bar.style.width = bar.dataset.target + '%';
        });
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.bar-chart').forEach(c => observer.observe(c));
}

// ─── Mobile Sidebar Toggle ────────────────────────────────────────────────────

const menuToggle = document.getElementById('menu-toggle');
const sidebar = document.querySelector('.sidebar');
if (menuToggle && sidebar) {
  menuToggle.addEventListener('click', () => sidebar.classList.toggle('open'));
  document.addEventListener('click', e => {
    if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// ─── Table Search ────────────────────────────────────────────────────────────

function initTableSearch(searchId, tableId) {
  const input = document.getElementById(searchId);
  const table = document.getElementById(tableId);
  if (!input || !table) return;
  input.addEventListener('input', () => {
    const q = input.value.toLowerCase();
    table.querySelectorAll('tbody tr').forEach(row => {
      row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
}

// ─── Init ─────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  initFilters();
  observeCharts();
  initTableSearch('search-subjects', 'table-subjects');
  initTableSearch('search-teachers', 'table-teachers');
  initTableSearch('search-classrooms', 'table-classrooms');

  // Auto-check conflicts on timetable page
  if (document.getElementById('tt-grid')) {
    checkConflicts();
  }

  // Animate stat card numbers on landing
  document.querySelectorAll('.stat-animate').forEach(el => {
    const target = parseInt(el.dataset.target || '0');
    animateCounter(el, target);
  });

  // Inline spinner style
  const s = document.createElement('style');
  s.textContent = `.spinner-inline{display:inline-block;width:14px;height:14px;border:2px solid rgba(255,255,255,.3);border-top-color:#fff;border-radius:50%;animation:spin .7s linear infinite;vertical-align:middle;}@keyframes spin{to{transform:rotate(360deg)}}`;
  document.head.appendChild(s);
});
