/* ═══════════════════════════════════════════════════════════════════════════
   iOS Interview Study Guide — script.js
   Features: Accordion · Search · Difficulty Filter · Scrollspy · FAB · KB shortcuts
   ═══════════════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Syntax highlighting ──────────────────────────────────────────────────────
  if (typeof hljs !== 'undefined') {
    hljs.configure({ ignoreUnescapedHTML: true });
    hljs.highlightAll();
  }

  // ── DOM refs ─────────────────────────────────────────────────────────────────
  const allItems    = document.querySelectorAll('.accordion-item');
  const allSections = document.querySelectorAll('.cat-section');
  const navItems    = document.querySelectorAll('.nav-item');
  const searchInput = document.getElementById('search-input');
  const banner      = document.getElementById('search-banner');
  const bannerTerm  = document.getElementById('search-term');
  const bannerClear = document.getElementById('search-clear');
  const pills       = document.querySelectorAll('.pill');
  const fab         = document.getElementById('fab');
  const main        = document.getElementById('main');

  // ═══════════════════════════════════════════════════════════════════════════
  //  ACCORDION
  // ═══════════════════════════════════════════════════════════════════════════
  function openItem(item) {
    const body = item.querySelector('.accordion-body');
    const btn  = item.querySelector('.accordion-btn');
    item.classList.add('open');
    btn.setAttribute('aria-expanded', 'true');
    body.style.maxHeight = body.scrollHeight + 'px';
  }

  function closeItem(item) {
    const body = item.querySelector('.accordion-body');
    const btn  = item.querySelector('.accordion-btn');
    item.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    body.style.maxHeight = '0px';
  }

  function toggleItem(item) {
    if (item.classList.contains('open')) {
      closeItem(item);
    } else {
      // Close siblings in the same accordion group
      const group = item.closest('.accordion-group');
      group.querySelectorAll('.accordion-item.open').forEach(sibling => {
        if (sibling !== item) closeItem(sibling);
      });
      openItem(item);
      // Smooth scroll into view after transition starts
      setTimeout(() => {
        const rect = item.getBoundingClientRect();
        if (rect.top < 80 || rect.bottom > window.innerHeight - 40) {
          item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      }, 120);
    }
  }

  // After accordion closes, ensure max-height is truly '0px'
  // After accordion fully opens, remove max-height limit (allows dynamic content)
  document.querySelectorAll('.accordion-body').forEach(body => {
    body.addEventListener('transitionend', () => {
      const item = body.closest('.accordion-item');
      if (item.classList.contains('open')) {
        body.style.maxHeight = 'none'; // Prevents clipping if inner content changes height
      }
    });
  });

  // Bind clicks
  document.querySelectorAll('.accordion-btn').forEach(btn => {
    btn.addEventListener('click', () => toggleItem(btn.closest('.accordion-item')));
  });

  // ═══════════════════════════════════════════════════════════════════════════
  //  SEARCH
  // ═══════════════════════════════════════════════════════════════════════════
  let searchTimeout = null;

  function runSearch(rawQuery) {
    const q = rawQuery.trim().toLowerCase();

    if (!q) {
      clearSearch();
      return;
    }

    banner.classList.remove('hidden');
    bannerTerm.textContent = rawQuery.trim();

    // Filter items
    allItems.forEach(item => {
      const qText  = item.querySelector('.q-text')?.textContent.toLowerCase() || '';
      const aText  = item.querySelector('.accordion-inner')?.textContent.toLowerCase() || '';
      const match  = qText.includes(q) || aText.includes(q);

      item.classList.toggle('hidden', !match);

      if (match) {
        // Auto-open matching items so user can see context
        if (!item.classList.contains('open')) openItem(item);
      } else {
        if (item.classList.contains('open')) closeItem(item);
      }
    });

    // Hide empty sections
    allSections.forEach(sec => {
      const visible = sec.querySelectorAll('.accordion-item:not(.hidden):not(.filtered)');
      sec.classList.toggle('hidden', visible.length === 0);
    });
  }

  function clearSearch() {
    searchInput.value = '';
    banner.classList.add('hidden');
    allItems.forEach(item => {
      item.classList.remove('hidden');
      if (item.classList.contains('open') && !item.classList.contains('filtered')) {
        closeItem(item);  // Collapse auto-opened items
      }
    });
    // Re-apply difficulty filter visibility
    reapplyFilter();
  }

  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => runSearch(searchInput.value), 180);
  });

  bannerClear.addEventListener('click', () => {
    clearSearch();
    searchInput.focus();
  });

  // ═══════════════════════════════════════════════════════════════════════════
  //  DIFFICULTY FILTER
  // ═══════════════════════════════════════════════════════════════════════════
  let activeDiff = 'all';

  function reapplyFilter() {
    allItems.forEach(item => {
      if (item.classList.contains('hidden')) return; // Don't undo search hiding
      const d = item.dataset.difficulty || '';
      const shouldFilter = activeDiff !== 'all' && d !== activeDiff;
      item.classList.toggle('filtered', shouldFilter);
      if (shouldFilter && item.classList.contains('open')) closeItem(item);
    });
    allSections.forEach(sec => {
      const visible = sec.querySelectorAll('.accordion-item:not(.hidden):not(.filtered)');
      sec.classList.toggle('hidden', visible.length === 0);
    });
  }

  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      activeDiff = pill.dataset.diff;
      reapplyFilter();
    });
  });

  // ═══════════════════════════════════════════════════════════════════════════
  //  SCROLLSPY
  // ═══════════════════════════════════════════════════════════════════════════
  const sectionObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navItems.forEach(ni => {
          const active = ni.dataset.target === id;
          ni.classList.toggle('active', active);
          if (active) {
            // Scroll nav item into view within the sidebar
            ni.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
          }
        });
      }
    });
  }, {
    root: main,
    rootMargin: '-5% 0px -60% 0px',
    threshold: 0,
  });

  allSections.forEach(sec => sectionObserver.observe(sec));

  // Nav click → smooth scroll
  navItems.forEach(ni => {
    ni.addEventListener('click', e => {
      e.preventDefault();
      const target = document.getElementById(ni.dataset.target);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  // ═══════════════════════════════════════════════════════════════════════════
  //  FAB (Back to Top)
  // ═══════════════════════════════════════════════════════════════════════════
  main.addEventListener('scroll', () => {
    fab.classList.toggle('visible', main.scrollTop > 500);
  }, { passive: true });

  fab.addEventListener('click', () => {
    main.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // ═══════════════════════════════════════════════════════════════════════════
  //  KEYBOARD SHORTCUTS
  // ═══════════════════════════════════════════════════════════════════════════
  document.addEventListener('keydown', e => {
    // ⌘K / Ctrl+K — focus search
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    }

    // Escape — clear search or blur
    if (e.key === 'Escape') {
      if (document.activeElement === searchInput) {
        if (searchInput.value) {
          clearSearch();
        } else {
          searchInput.blur();
        }
      }
    }

    // Arrow keys for navigating between open accordion items (when not in input)
    if (!['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)) {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        const visibleBtns = [...document.querySelectorAll(
          '.accordion-item:not(.hidden):not(.filtered) .accordion-btn'
        )];
        if (!visibleBtns.length) return;
        const focused = visibleBtns.indexOf(document.activeElement);
        let next = e.key === 'ArrowDown' ? focused + 1 : focused - 1;
        next = Math.max(0, Math.min(next, visibleBtns.length - 1));
        visibleBtns[next]?.focus();
        e.preventDefault();
      }
    }
  });

  // ═══════════════════════════════════════════════════════════════════════════
  //  MOBILE SIDEBAR TOGGLE
  // ═══════════════════════════════════════════════════════════════════════════
  const sidebar       = document.getElementById('sidebar');
  const mobileToggle  = document.getElementById('mobile-toggle');
  const mobileOverlay = document.getElementById('mobile-overlay');

  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      mobileOverlay.classList.toggle('hidden');
    });
    mobileOverlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      mobileOverlay.classList.add('hidden');
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  //  STATS — count per difficulty
  // ═══════════════════════════════════════════════════════════════════════════
  const counts = { easy: 0, mid: 0, expert: 0, '': 0 };
  allItems.forEach(item => { counts[item.dataset.difficulty || ''] = (counts[item.dataset.difficulty || ''] || 0) + 1; });

  ['easy', 'mid', 'expert'].forEach(d => {
    const el = document.querySelector(`.hp.${d}`);
    if (el) el.title = `${counts[d] || 0} questions`;
  });

  console.log(
    `%ciOS Study Guide loaded\n` +
    `%c${allItems.length} questions · ${allSections.length} categories\n` +
    `%c⌘K to search · Arrow keys to navigate`,
    'color: #0A84FF; font-size: 16px; font-weight: bold;',
    'color: #F5F5F7; font-size: 12px;',
    'color: #636366; font-size: 11px;'
  );
});
