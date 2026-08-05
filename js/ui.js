/**
 * UI Renderer for PromptVault
 * Builds and updates DOM components, manages modal overlays, toasts, and animations
 */
const UI = {
  // SVG Icon Paths dictionary (matches assets/icons for CORS-free inline rendering)
  iconPaths: {
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"></rect><rect x="14" y="3" width="7" height="7" rx="1"></rect><rect x="14" y="14" width="7" height="7" rx="1"></rect><rect x="3" y="14" width="7" height="7" rx="1"></rect>',
    "file-text": '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><line x1="10" y1="9" x2="8" y2="9"></line>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="15" x2="23" y2="15"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="15" x2="4" y2="15"></line>',
    "mail": '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline>',
    "mic": '<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path>',
    "dollar-sign": '<line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>',
    "trending-up": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline>',
    "send": '<line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>',
    "search": '<circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>',
    "sun": '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>',
    "moon": '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>',
    "settings": '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>',
    "copy": '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>',
    "info": '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>',
    "check": '<polyline points="20 6 9 17 4 12"></polyline>',
    "chevron-right": '<polyline points="9 18 15 12 9 6"></polyline>',
    "chevron-left": '<polyline points="15 18 9 12 15 6"></polyline>',
    "pin": '<line x1="12" y1="17" x2="12" y2="22"></line><path d="M5 17h14v-1.76a2 2 0 0 0-.44-1.24l-2.78-3.48A1 1 0 0 1 15 9.76V5a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v4.76a1 1 0 0 1-.22.68L5.44 14a2 2 0 0 0-.44 1.24z"></path>',
    "random": '<polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line>',
    "trash": '<polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line>',
    "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line>',
    "share": '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path><polyline points="16 6 12 2 8 6"></polyline><line x1="12" y1="2" x2="12" y2="15"></line>',
    "clock": '<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>',
    "sparkles": '<path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m11.314 11.314l.707.707M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"></path>',
    "refresh-cw": '<polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>',
    "external-link": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line>'
  },

  /**
   * Generates inline SVG HTML for CORS-safe loading
   */
  icon(name, className = '') {
    const path = this.iconPaths[name] || '';
    return `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-${name} ${className}">${path}</svg>`;
  },

  /**
   * Renders the left categories sidebar
   */
  renderSidebar(categories, counts, activeCategoryId) {
    const scrollContainer = document.getElementById('sidebar-categories');
    if (!scrollContainer) return;

    let html = '';

    // Add library category sections
    html += `<div class="sidebar-section-title">Library</div>`;
    categories.forEach(category => {
      const count = counts[category.id] || 0;
      const isActive = category.id === activeCategoryId ? 'active' : '';
      const iconMarkup = this.icon(category.icon, 'category-icon');

      html += `
        <a class="category-item ${isActive}" data-id="${category.id}">
          <div class="category-left">
            ${iconMarkup}
            <span>${category.name}</span>
          </div>
          <span class="category-count">${count}</span>
        </a>
      `;

      // Inject divider after 'All Prompts'
      if (category.id === 'all') {
        html += `<div class="sidebar-section-title">Categories</div>`;
      }
    });

    scrollContainer.innerHTML = html;
  },

  /**
   * Renders the stats widget in the dashboard
   */
  renderStats(totalCount, favoritesCount, categoriesCount, searchQueriesCount) {
    const totalEl = document.getElementById('stat-total');
    const favEl = document.getElementById('stat-favorites');
    const catEl = document.getElementById('stat-categories');
    const searchEl = document.getElementById('stat-search');

    if (totalEl) totalEl.innerText = totalCount;
    if (favEl) favEl.innerText = favoritesCount;
    if (catEl) catEl.innerText = categoriesCount;
    if (searchEl) searchEl.innerText = searchQueriesCount;
  },

  /**
   * Renders a random tip in the daily widget
   */
  renderDailyTip() {
    const widget = document.getElementById('daily-tip-container');
    if (!widget) return;

    const tips = [
      "Assign a specific role (e.g., 'Act as an ATS Parser') to set target vocabulary rules.",
      "Use delimiters like [YOUR_EXPERIENCE] to clearly demarcate parameters from prompt instructions.",
      "Provide negative constraints ('do not use corporate buzzwords') to keep AI responses clean.",
      "Integrate one-shot/few-shot examples in parameters to lock-in the output formats.",
      "Use prompt chaining for large files: first extract metrics, then rewrite descriptions.",
      "Enforce 'Chain of Thought' reasoning by asking AI to map out logic before giving options.",
      "Keep variables unique in your custom collections to build reusable personal prompt libraries."
    ];

    // Seed based on current date day of year (0-365)
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 0);
    const diff = now - start;
    const oneDay = 1000 * 60 * 60 * 24;
    const day = Math.floor(diff / oneDay);
    const tipText = tips[day % tips.length];

    widget.innerHTML = `
      <div class="daily-tip-widget">
        <div class="daily-tip-icon">${this.icon('sparkles')}</div>
        <div class="daily-tip-content">
          <span class="daily-tip-title">PROMPT TIP OF THE DAY</span>
          <span class="daily-tip-text">${tipText}</span>
        </div>
      </div>
    `;
  },

  /**
   * Renders loading skeletons inside the prompt cards container
   */
  renderSkeletons() {
    const listContainer = document.getElementById('prompt-cards-list');
    if (!listContainer) return;

    let html = '';
    for (let i = 0; i < 4; i++) {
      html += `
        <div class="skeleton-card">
          <div class="skeleton-text title"></div>
          <div class="skeleton-text desc-1"></div>
          <div class="skeleton-text desc-2"></div>
          <div class="skeleton-text meta"></div>
        </div>
      `;
    }
    listContainer.innerHTML = html;
  },

  /**
   * Renders the cards grid/list inside center pane
   */
  renderPromptList(prompts, selectedId, query = '') {
    const listContainer = document.getElementById('prompt-cards-list');
    if (!listContainer) return;

    if (prompts.length === 0) {
      listContainer.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">${this.icon('info', 'lucide-large')}</div>
          <span class="empty-state-title">No Prompts Found</span>
          <span class="empty-state-desc">Try clearing your filters or testing a different search query.</span>
        </div>
      `;
      return;
    }

    let html = '';
    prompts.forEach(prompt => {
      const isSelected = prompt.id === selectedId ? 'active' : '';
      const isFav = StorageEngine.isFavorite(prompt.id) ? 'favorited' : '';
      const isPinned = StorageEngine.isPinned(prompt.id) ? 'pinned' : '';

      const title = SearchEngine.highlightText(prompt.title, query);
      const desc = SearchEngine.highlightText(prompt.description, query);

      // Calculate category tag formatting
      const catObj = window.CATEGORIES_DATA.find(c => c.id === prompt.category);
      const catName = catObj ? catObj.name : prompt.category;

      const difficultyClass = `badge-difficulty-${prompt.difficulty.toLowerCase()}`;

      html += `
        <div class="prompt-card ${isSelected} ${isPinned ? 'pinned' : ''}" data-id="${prompt.id}">
          <div class="card-header">
            <h3 class="card-title">${title}</h3>
            <div class="card-actions">
              <button class="card-btn pin-toggle-btn ${isPinned ? 'pinned' : ''}" data-id="${prompt.id}" title="${isPinned ? 'Unpin' : 'Pin to top'}">
                ${this.icon('pin')}
              </button>
              <button class="card-btn fav-toggle-btn ${isFav ? 'favorited' : ''}" data-id="${prompt.id}" title="${isFav ? 'Remove from favorites' : 'Add to favorites'}">
                ${this.icon('star')}
              </button>
            </div>
          </div>
          <p class="card-description">${desc}</p>
          <div class="card-meta">
            <span class="badge ${difficultyClass}">${prompt.difficulty}</span>
            <span class="badge badge-category">${catName}</span>
            <div class="card-tags">
              ${(prompt.tags || []).slice(0, 2).map(tag => `<span class="card-tag">#${tag}</span>`).join('')}
            </div>
          </div>
        </div>
      `;
    });

    listContainer.innerHTML = html;
  },

  /**
   * Renders the details panel contents
   */
  renderPromptDetails(prompt) {
    const pane = document.getElementById('prompt-details-pane');
    if (!pane) return;

    if (!prompt) {
      pane.innerHTML = `
        <div class="empty-state" style="height: 100%;">
          <div class="empty-state-icon">${this.icon('file-text')}</div>
          <span class="empty-state-title">Select a Prompt</span>
          <span class="empty-state-desc">Choose a prompt card from the list to view template specifications and copy code.</span>
        </div>
      `;
      return;
    }

    // Mark variables like [VARIABLE] in prompt content
    const markedPrompt = prompt.prompt.replace(/(\[[A-Z0-9_]+\])/g, '<mark>$1</mark>');

    // Get category info
    const catObj = window.CATEGORIES_DATA.find(c => c.id === prompt.category);
    const catName = catObj ? catObj.name : prompt.category;

    // Check states
    const isFav = StorageEngine.isFavorite(prompt.id);
    const isPinned = StorageEngine.isPinned(prompt.id);
    const activeRating = StorageEngine.getRating(prompt.id);

    // Calculate reading time
    const words = (prompt.prompt || '').split(/\s+/).length;
    const readTime = Math.max(1, Math.round(words / 200));

    pane.innerHTML = `
      <div class="details-header">
        <div class="breadcrumbs">
          <span>PromptVault</span>
          <span class="breadcrumb-separator">${this.icon('chevron-right')}</span>
          <span>${catName}</span>
          <span class="breadcrumb-separator">${this.icon('chevron-right')}</span>
          <span class="details-meta-item" style="color: var(--text-primary); font-weight:700;">Details</span>
        </div>
        <div class="details-actions">
          <button class="btn-icon pin-detail-btn ${isPinned ? 'pinned' : ''}" data-id="${prompt.id}" title="${isPinned ? 'Unpin prompt' : 'Pin prompt'}">
            ${this.icon('pin')}
          </button>
          <button class="btn-icon fav-detail-btn ${isFav ? 'favorited' : ''}" data-id="${prompt.id}" title="${isFav ? 'Remove from favorites' : 'Add to favorites'}">
            ${this.icon('star')}
          </button>
          <button class="btn-icon print-btn" title="Print / Save as PDF">
            ${this.icon('share')}
          </button>
        </div>
      </div>
      
      <div class="details-scroll">
        <div class="details-title-section">
          <h2 class="details-title">${prompt.title}</h2>
          <div class="details-meta-row">
            <span class="details-meta-item">${this.icon('cpu')} v1.0.0</span>
            <span class="details-meta-item">${this.icon('clock')} ${readTime} min read</span>
            <span class="details-meta-item" style="color: var(--warning);">${this.icon('star')} Premium</span>
          </div>
        </div>

        <p class="details-description">${prompt.description}</p>

        <div class="prompt-block">
          <div class="prompt-block-header">
            <span class="prompt-block-title">${this.icon('file-text')} Prompt Template</span>
            <div style="display:flex; gap:6px;">
              <button class="btn-icon copy-btn" data-text="${prompt.prompt}" title="Copy template only" style="width:30px; height:30px;">
                ${this.icon('copy')}
              </button>
            </div>
          </div>
          <div class="prompt-block-body">${markedPrompt}</div>
        </div>

        <div class="response-quality-meter">
          <div class="quality-meter-header">
            <span>Estimated Response Quality</span>
            <span>92% (High Confidence)</span>
          </div>
          <div class="quality-meter-bar">
            <div class="quality-meter-fill"></div>
          </div>
        </div>

        <div>
          <span class="details-section-title">${this.icon('info')} Example Parameters</span>
          <pre class="example-box">${prompt.exampleInput}</pre>
        </div>

        <div>
          <span class="details-section-title">${this.icon('check')} Expected Output</span>
          <pre class="example-box">${prompt.exampleOutput}</pre>
        </div>

        <div>
          <span class="details-section-title">${this.icon('star')} Pro Tips & Guidelines</span>
          <ul class="tips-list">
            ${(prompt.tips || []).map(tip => `<li>${tip}</li>`).join('')}
          </ul>
        </div>
        
        <div class="rating-section">
          <span class="rating-title">Was this prompt useful?</span>
          <div class="rating-buttons">
            <button class="btn-rate up-rate-btn ${activeRating === 'up' ? 'active-up' : ''}" data-id="${prompt.id}">
              👍 Yes
            </button>
            <button class="btn-rate down-rate-btn ${activeRating === 'down' ? 'active-down' : ''}" data-id="${prompt.id}">
              👎 No
            </button>
          </div>
        </div>
      </div>

      <div class="details-footer">
        <button class="btn-secondary prev-prompt-btn" style="padding: 6px 12px; font-size: 0.8rem;">
          ${this.icon('chevron-left')} Prev
        </button>

        <button
          class="btn-secondary copy-prompt-btn"
          data-text="${prompt.prompt}"
          style="padding: 6px 12px; font-size: 0.8rem;">
          ${this.icon('copy')} Copy Prompt
        </button>

        <button class="btn-secondary next-prompt-btn" style="padding: 6px 12px; font-size: 0.8rem;">
          Next ${this.icon('chevron-right')}
        </button>
      </div>
    `;

    // Track recently viewed
    StorageEngine.addRecentlyViewed(prompt.id);
  },

  /**
   * Renders the Command Palette items list
   */
  renderCommandPaletteResults(results, selectedIndex) {
    const list = document.getElementById('command-palette-results');
    if (!list) return;

    if (results.length === 0) {
      list.innerHTML = `
        <div style="padding: 16px; text-align: center; color: var(--text-muted); font-size: 0.875rem;">
          No matching commands or prompts.
        </div>
      `;
      return;
    }

    let html = '';
    results.forEach((item, index) => {
      const isSelected = index === selectedIndex ? 'selected' : '';

      html += `
        <div class="command-item ${isSelected}" data-index="${index}" data-action="${item.type}" data-val="${item.value}">
          <div class="command-item-left">
            <span class="command-item-icon">${this.icon(item.icon)}</span>
            <span class="command-item-text">${item.name}</span>
          </div>
          <span class="command-item-badge">${item.type}</span>
        </div>
      `;
    });

    list.innerHTML = html;
  },

  /**
   * Injects visual button ripple animations
   */
  addRippleEffect(e) {
    const btn = e.currentTarget;
    const ripple = document.createElement('span');
    ripple.classList.add('ripple');

    const rect = btn.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);

    ripple.style.width = ripple.style.height = `${size}px`;
    ripple.style.left = `${e.clientX - rect.left - size / 2}px`;
    ripple.style.top = `${e.clientY - rect.top - size / 2}px`;

    btn.appendChild(ripple);

    setTimeout(() => {
      ripple.remove();
    }, 600);
  },

  /**
   * Triggers a toast alert notification
   */
  showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast`;

    const iconName = type === 'success' ? 'check' : 'info';
    toast.innerHTML = `
      <span class="toast-icon">${this.icon(iconName)}</span>
      <span>${message}</span>
    `;

    container.appendChild(toast);

    // Fade in
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);

    // Dismiss after 2.5s
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        toast.remove();
      }, 300);
    }, 2500);
  }
};
