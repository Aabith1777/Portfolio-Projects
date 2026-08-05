/**
 * Main Application Orchestrator for PromptVault
 * Registers event listeners, coordinates filtering/sorting, maps keyboard shortcuts,
 * and maintains reactive visual updates.
 */
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});

const App = {
  // Global State
  state: {
    prompts: [],
    categories: [],
    filteredPrompts: [],
    selectedCategoryId: 'all',
    selectedPromptId: null,
    searchQuery: '',
    difficultyFilter: 'all',
    sortBy: 'alphabetical',
    searchCount: 0,

    // Command Palette state
    commandPaletteOpen: false,
    activeCommandIndex: 0,
    matchingCommands: []
  },

  /**
   * Initializes state, applies styling configs, renders widgets, and binds events
   */
  init() {
    // 1. Check offline fallback data exists
    if (!window.PROMPTS_DATA || !window.CATEGORIES_DATA) {
      console.error("Missing configuration database arrays window.PROMPTS_DATA or window.CATEGORIES_DATA.");
      return;
    }

    this.state.prompts = window.PROMPTS_DATA;
    this.state.categories = window.CATEGORIES_DATA;

    // 2. Initialize logical subsystems
    StorageEngine.getFavorites(); // Ensure initialization
    ThemeManager.init();

    // 3. Apply preferences
    const prefs = StorageEngine.getPreferences();
    if (prefs.sidebarCollapsed) {
      document.getElementById('app-sidebar').classList.add('collapsed');
    }

    // 4. Render initial elements
    UI.renderDailyTip();
    this.refreshUI();

    // Select first prompt on launch if list is not empty
    if (this.state.filteredPrompts.length > 0) {
      this.selectPrompt(this.state.filteredPrompts[0].id);
    } else {
      this.selectPrompt(null);
    }

    // 5. Setup Listeners
    this.bindEvents();
  },

  /**
   * Performs filtering, sorting, calculations, and triggers DOM renders
   */
  refreshUI() {
    // A. Filter prompts based on Category and Difficulty
    let result = [...this.state.prompts];

    // Filter by category
    if (this.state.selectedCategoryId === 'favorites') {
      result = FavoritesManager.getFavoritedPrompts(result);
    } else if (this.state.selectedCategoryId !== 'all') {
      result = result.filter(p => p.category === this.state.selectedCategoryId);
    }

    // Filter by difficulty
    if (this.state.difficultyFilter !== 'all') {
      result = result.filter(p => p.difficulty.toLowerCase() === this.state.difficultyFilter);
    }

    // B. Apply search matching if query is active
    if (this.state.searchQuery.trim()) {
      result = SearchEngine.search(result, this.state.searchQuery);
    }

    // C. Sort results
    // Pinned items are always sorted to the absolute top
    const pinnedIds = StorageEngine.getPinned();
    const pinnedPrompts = [];
    const regularPrompts = [];

    result.forEach(prompt => {
      if (pinnedIds.includes(prompt.id)) {
        pinnedPrompts.push(prompt);
      } else {
        regularPrompts.push(prompt);
      }
    });

    const sortFn = (a, b) => {
      if (this.state.sortBy === 'alphabetical') {
        return a.title.localeCompare(b.title);
      } else if (this.state.sortBy === 'newest') {
        return new Date(b.createdDate || 0) - new Date(a.createdDate || 0);
      } else if (this.state.sortBy === 'difficulty') {
        const diffWeight = { 'Beginner': 1, 'Intermediate': 2, 'Advanced': 3 };
        return (diffWeight[a.difficulty] || 0) - (diffWeight[b.difficulty] || 0);
      }
      return 0;
    };

    pinnedPrompts.sort(sortFn);
    regularPrompts.sort(sortFn);

    this.state.filteredPrompts = [...pinnedPrompts, ...regularPrompts];

    // D. Re-render UI Elements
    // Render list
    UI.renderPromptList(this.state.filteredPrompts, this.state.selectedPromptId, this.state.searchQuery);

    // Calculate category counts dynamically
    const counts = { all: this.state.prompts.length };
    counts['favorites'] = FavoritesManager.getFavorites().length;

    this.state.categories.forEach(cat => {
      if (cat.id !== 'all') {
        counts[cat.id] = this.state.prompts.filter(p => p.category === cat.id).length;
      }
    });

    // Render Sidebar categories
    UI.renderSidebar(this.state.categories, counts, this.state.selectedCategoryId);

    // Render Stats dashboard
    UI.renderStats(
      this.state.prompts.length,
      FavoritesManager.getFavorites().length,
      this.state.categories.length - 1, // minus 'All Prompts' placeholder
      this.state.searchCount
    );

    // If active prompt is no longer visible, auto-select first of filtered
    if (this.state.selectedPromptId) {
      const activeExists = this.state.filteredPrompts.some(p => p.id === this.state.selectedPromptId);
      if (!activeExists && this.state.filteredPrompts.length > 0) {
        this.selectPrompt(this.state.filteredPrompts[0].id);
      } else if (!activeExists) {
        this.selectPrompt(null);
      }
    }
  },

  /**
   * Selects a prompt and renders the right pane details
   */
  selectPrompt(id) {
    this.state.selectedPromptId = id;
    const prompt = this.state.prompts.find(p => p.id === id);
    UI.renderPromptDetails(prompt);

    // Mark card as active
    document.querySelectorAll('.prompt-card').forEach(card => {
      card.classList.remove('active');
      if (card.getAttribute('data-id') === id) {
        card.classList.add('active');
        // Scroll into view if needed
        card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  },

  /**
   * Registers DOM event listeners, modal controllers, and keyboard macros
   */
  bindEvents() {
    // 1. Sidebar Category Clicks (using event delegation)
    const sidebar = document.getElementById('sidebar-categories');
    if (sidebar) {
      sidebar.addEventListener('click', (e) => {
        const item = e.target.closest('.category-item');
        if (item) {
          const categoryId = item.getAttribute('data-id');
          this.state.selectedCategoryId = categoryId;
          this.refreshUI();

          // On mobile, close sidebar after choosing category
          document.getElementById('app-sidebar').classList.remove('open-mobile');
        }
      });
    }

    // 2. Card selection and card buttons (using event delegation)
    const list = document.getElementById('prompt-cards-list');
    if (list) {
      list.addEventListener('click', (e) => {
        const card = e.target.closest('.prompt-card');
        const favBtn = e.target.closest('.fav-toggle-btn');
        const pinBtn = e.target.closest('.pin-toggle-btn');

        if (favBtn) {
          e.stopPropagation();
          const id = favBtn.getAttribute('data-id');
          const res = StorageEngine.toggleFavorite(id);
          UI.showToast(res.added ? 'Added to favorites' : 'Removed from favorites');
          this.refreshUI();
        } else if (pinBtn) {
          e.stopPropagation();
          const id = pinBtn.getAttribute('data-id');
          const res = StorageEngine.togglePin(id);
          UI.showToast(res.added ? 'Prompt pinned to top' : 'Prompt unpinned');
          this.refreshUI();
        } else if (card) {
          const id = card.getAttribute('data-id');
          this.selectPrompt(id);

          // On small viewports, open detail pane overlay
          if (window.innerWidth <= 1024) {
            document.getElementById('prompt-details-pane').classList.add('active-overlay');
          }
        }
      });
    }

    // 3. Search Inputs
    const searchInput = document.getElementById('main-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.state.searchQuery = e.target.value;
        if (e.target.value.trim() && e.target.value.length === 3) {
          // Increment search stat on typing beginning
          this.state.searchCount++;
        }
        this.refreshUI();
      });
    }

    // 4. Filtering and Sorting Dropdowns
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
      sortSelect.addEventListener('change', (e) => {
        this.state.sortBy = e.target.value;
        this.refreshUI();
      });
    }

    const diffSelect = document.getElementById('difficulty-select');
    if (diffSelect) {
      diffSelect.addEventListener('change', (e) => {
        this.state.difficultyFilter = e.target.value;
        this.refreshUI();
      });
    }

    // 5. Detail Pane Event Handlers (delegated)
    const detailPane = document.getElementById('prompt-details-pane');
    if (detailPane) {
      detailPane.addEventListener('click', (e) => {
        const copyBtn = e.target.closest('.copy-btn');
        const copyAllBtn = e.target.closest('.copy-all-btn');
        const copyPromptBtn = e.target.closest('.copy-prompt-btn');
        const printBtn = e.target.closest('.print-btn');
        const favBtn = e.target.closest('.fav-detail-btn');
        const pinBtn = e.target.closest('.pin-detail-btn');
        const upBtn = e.target.closest('.up-rate-btn');
        const downBtn = e.target.closest('.down-rate-btn');
        const prevBtn = e.target.closest('.prev-prompt-btn');
        const nextBtn = e.target.closest('.next-prompt-btn');

        if (copyBtn) {
          const text = copyBtn.getAttribute('data-text');
          navigator.clipboard.writeText(text).then(() => {
            UI.showToast('Copied Prompt Template!');
          });
        } else if (copyPromptBtn) {
          const text = copyPromptBtn.getAttribute('data-text');
          navigator.clipboard.writeText(text).then(() => {
            UI.showToast('Prompt copied successfully!');
          });
        } else if (printBtn) {
          window.print();
        } else if (favBtn) {
          const id = favBtn.getAttribute('data-id');
          const res = StorageEngine.toggleFavorite(id);
          UI.showToast(res.added ? 'Added to favorites' : 'Removed from favorites');
          this.refreshUI();
          this.selectPrompt(id); // Force render updates
        } else if (pinBtn) {
          const id = pinBtn.getAttribute('data-id');
          const res = StorageEngine.togglePin(id);
          UI.showToast(res.added ? 'Prompt pinned' : 'Prompt unpinned');
          this.refreshUI();
          this.selectPrompt(id);
        } else if (upBtn) {
          const id = upBtn.getAttribute('data-id');
          StorageEngine.setRating(id, 'up');
          this.selectPrompt(id);
        } else if (downBtn) {
          const id = downBtn.getAttribute('data-id');
          StorageEngine.setRating(id, 'down');
          this.selectPrompt(id);
        } else if (prevBtn) {
          this.navigatePrompt(-1);
        } else if (nextBtn) {
          this.navigatePrompt(1);
        }
      });
    }

    // 6. Header Buttons
    const themeToggle = document.getElementById('btn-toggle-theme');
    if (themeToggle) {
      themeToggle.addEventListener('click', (e) => {
        UI.addRippleEffect(e);
        const nextTheme = ThemeManager.toggle();
        UI.showToast(`Switched to ${nextTheme === 'dark' ? 'Dark' : 'Light'} Mode`);
      });
    }

    const settingsToggle = document.getElementById('btn-settings');
    if (settingsToggle) {
      settingsToggle.addEventListener('click', (e) => {
        UI.addRippleEffect(e);
        this.toggleModal('settings-modal-overlay', true);
      });
    }

    const randomBtn = document.getElementById('btn-random');
    if (randomBtn) {
      randomBtn.addEventListener('click', (e) => {
        UI.addRippleEffect(e);
        if (this.state.filteredPrompts.length > 0) {
          const randomIndex = Math.floor(Math.random() * this.state.filteredPrompts.length);
          const chosen = this.state.filteredPrompts[randomIndex];
          this.selectPrompt(chosen.id);
          UI.showToast(`Opened random prompt: ${chosen.title}`);
        } else {
          UI.showToast('No visible prompts to pick from.', 'error');
        }
      });
    }

    const sidebarToggle = document.getElementById('btn-toggle-sidebar');
    if (sidebarToggle) {
      sidebarToggle.addEventListener('click', (e) => {
        UI.addRippleEffect(e);

        if (window.innerWidth <= 768) {
          // Mobile: slide drawer in/out
          document.getElementById('app-sidebar').classList.toggle('open-mobile');
        } else {
          // Desktop: collapse sidebar
          const sidebar = document.getElementById('app-sidebar');
          const isCollapsed = sidebar.classList.toggle('collapsed');
          StorageEngine.setPreference('sidebarCollapsed', isCollapsed);
        }
      });
    }

    // Mobile Back Button inside Details Overlay
    const backDetailsBtn = document.getElementById('btn-details-back');
    if (backDetailsBtn) {
      backDetailsBtn.addEventListener('click', () => {
        document.getElementById('prompt-details-pane').classList.remove('active-overlay');
      });
    }

    // Scroll to top implementation
    const scrollContainer = document.getElementById('prompt-cards-scroll-container');
    const scrollBtn = document.getElementById('scroll-to-top-btn');
    if (scrollContainer && scrollBtn) {
      scrollContainer.addEventListener('scroll', () => {
        if (scrollContainer.scrollTop > 300) {
          scrollBtn.classList.add('visible');
        } else {
          scrollBtn.classList.remove('visible');
        }
      });

      scrollBtn.addEventListener('click', () => {
        scrollContainer.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }

    // Modal close handlers (clicks outside or close button)
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          this.toggleModal(overlay.id, false);
        }
      });
    });

    const closeSettings = document.getElementById('btn-close-settings');
    if (closeSettings) {
      closeSettings.addEventListener('click', () => {
        this.toggleModal('settings-modal-overlay', false);
      });
    }

    // 7. Settings Operations
    const btnResetFav = document.getElementById('btn-reset-favorites');
    if (btnResetFav) {
      btnResetFav.addEventListener('click', () => {
        if (confirm('Are you sure you want to reset all favorites?')) {
          StorageEngine.resetFavorites();
          UI.showToast('All Favorites Reset');
          this.refreshUI();
        }
      });
    }

    const btnResetAll = document.getElementById('btn-reset-all');
    if (btnResetAll) {
      btnResetAll.addEventListener('click', () => {
        if (confirm('This will wipe all favorites, ratings, and return preferences to default. Proceed?')) {
          StorageEngine.resetAllSettings();
          ThemeManager.init();
          UI.showToast('All Settings Restored to Default');
          this.refreshUI();
          if (this.state.filteredPrompts.length > 0) {
            this.selectPrompt(this.state.filteredPrompts[0].id);
          }
          this.toggleModal('settings-modal-overlay', false);
        }
      });
    }

    const btnExport = document.getElementById('btn-export-backup');
    if (btnExport) {
      btnExport.addEventListener('click', () => {
        StorageEngine.exportBackup();
        UI.showToast('Backup File Downloaded');
      });
    }

    const fileImport = document.getElementById('file-import-backup');
    if (fileImport) {
      fileImport.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
          const success = StorageEngine.importBackup(event.target.result);
          if (success) {
            UI.showToast('Settings & Favorites Restored!');
            ThemeManager.init();
            this.refreshUI();
            this.toggleModal('settings-modal-overlay', false);
          } else {
            UI.showToast('Invalid backup file formatting.', 'error');
          }
        };
        reader.readAsText(file);
      });
    }

    // 8. Command Palette Event Listeners
    const commandInput = document.getElementById('command-palette-input');
    if (commandInput) {
      commandInput.addEventListener('input', (e) => {
        this.filterCommandPalette(e.target.value);
      });

      commandInput.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          this.navigateCommandSelection(1);
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          this.navigateCommandSelection(-1);
        } else if (e.key === 'Enter') {
          e.preventDefault();
          this.executeSelectedCommand();
        }
      });
    }

    const cmdList = document.getElementById('command-palette-results');
    if (cmdList) {
      cmdList.addEventListener('click', (e) => {
        const item = e.target.closest('.command-item');
        if (item) {
          const idx = parseInt(item.getAttribute('data-index'), 10);
          this.state.activeCommandIndex = idx;
          this.executeSelectedCommand();
        }
      });
    }

    // 9. Global Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      // Ctrl + F (Focus Search)
      if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        const input = document.getElementById('main-search-input');
        if (input) {
          input.focus();
          input.select();
        }
      }

      // Ctrl + D (Toggle Theme)
      if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        const nextTheme = ThemeManager.toggle();
        UI.showToast(`Switched to ${nextTheme === 'dark' ? 'Dark' : 'Light'} Mode`);
      }

      // Ctrl + K (Command Palette)
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.toggleCommandPalette(!this.state.commandPaletteOpen);
      }

      // Esc (Dismiss overlays / focus out)
      if (e.key === 'Escape') {
        if (this.state.commandPaletteOpen) {
          this.toggleCommandPalette(false);
        } else {
          // Close settings modal
          this.toggleModal('settings-modal-overlay', false);
          // Blur active elements
          document.activeElement.blur();
        }
      }

      // Arrow Keys navigation on prompt list
      if (!this.state.commandPaletteOpen && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          this.navigatePromptList(1);
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          this.navigatePromptList(-1);
        }
      }
    });
  },

  /**
   * Toggles modal visibilities
   */
  toggleModal(id, isOpen) {
    const el = document.getElementById(id);
    if (el) {
      if (isOpen) {
        el.classList.add('open');
      } else {
        el.classList.remove('open');
      }
    }
  },

  /**
   * Cycles prompt details selection (Prev/Next)
   */
  navigatePrompt(direction) {
    if (this.state.filteredPrompts.length === 0) return;

    const currentIndex = this.state.filteredPrompts.findIndex(p => p.id === this.state.selectedPromptId);
    let nextIndex = currentIndex + direction;

    if (nextIndex < 0) nextIndex = this.state.filteredPrompts.length - 1;
    if (nextIndex >= this.state.filteredPrompts.length) nextIndex = 0;

    const nextPrompt = this.state.filteredPrompts[nextIndex];
    this.selectPrompt(nextPrompt.id);
  },

  /**
   * Navigation on prompt card list via Arrow Keys
   */
  navigatePromptList(direction) {
    if (this.state.filteredPrompts.length === 0) return;

    const currentIndex = this.state.filteredPrompts.findIndex(p => p.id === this.state.selectedPromptId);
    let nextIndex = currentIndex + direction;

    if (nextIndex >= 0 && nextIndex < this.state.filteredPrompts.length) {
      this.selectPrompt(this.state.filteredPrompts[nextIndex].id);
    }
  },

  /**
   * Toggles the central command palette overlay
   */
  toggleCommandPalette(isOpen) {
    this.state.commandPaletteOpen = isOpen;
    this.toggleModal('command-palette-overlay', isOpen);

    if (isOpen) {
      const input = document.getElementById('command-palette-input');
      if (input) {
        input.value = '';
        input.focus();
      }
      this.filterCommandPalette('');
    }
  },

  /**
   * Builds matching actions based on query inside command palette
   */
  filterCommandPalette(query) {
    const cleanQuery = query.toLowerCase().trim();
    const cmdList = [];

    // Add static operational commands
    const staticCommands = [
      { name: "Toggle Dark / Light Theme", icon: "sun", type: "system", value: "theme" },
      { name: "Open Settings Page Panel", icon: "settings", type: "system", value: "settings" },
      { name: "Export Favorites Backup JSON", icon: "download", type: "system", value: "export" },
      { name: "Open Random Prompt", icon: "random", type: "system", value: "random" }
    ];

    staticCommands.forEach(cmd => {
      if (!cleanQuery || cmd.name.toLowerCase().includes(cleanQuery)) {
        cmdList.push(cmd);
      }
    });

    // Add prompt matches
    this.state.prompts.forEach(p => {
      if (p.title.toLowerCase().includes(cleanQuery) || p.description.toLowerCase().includes(cleanQuery)) {
        cmdList.push({
          name: `View Prompt: ${p.title}`,
          icon: "file-text",
          type: "prompt",
          value: p.id
        });
      }
    });

    this.state.matchingCommands = cmdList.slice(0, 10); // Limit to top 10 items
    this.state.activeCommandIndex = 0;

    UI.renderCommandPaletteResults(this.state.matchingCommands, this.state.activeCommandIndex);
  },

  /**
   * Navigates command list selection index
   */
  navigateCommandSelection(direction) {
    const total = this.state.matchingCommands.length;
    if (total === 0) return;

    let index = this.state.activeCommandIndex + direction;
    if (index < 0) index = total - 1;
    if (index >= total) index = 0;

    this.state.activeCommandIndex = index;
    UI.renderCommandPaletteResults(this.state.matchingCommands, this.state.activeCommandIndex);

    // Auto-scroll selected command item
    const container = document.getElementById('command-palette-results');
    const selected = container.querySelector('.command-item.selected');
    if (selected) {
      selected.scrollIntoView({ block: 'nearest' });
    }
  },

  /**
   * Triggers the action of the active selected command item
   */
  executeSelectedCommand() {
    const item = this.state.matchingCommands[this.state.activeCommandIndex];
    if (!item) return;

    this.toggleCommandPalette(false); // Close first

    if (item.type === 'system') {
      if (item.value === 'theme') {
        const nextTheme = ThemeManager.toggle();
        UI.showToast(`Switched to ${nextTheme === 'dark' ? 'Dark' : 'Light'} Mode`);
      } else if (item.value === 'settings') {
        this.toggleModal('settings-modal-overlay', true);
      } else if (item.value === 'export') {
        StorageEngine.exportBackup();
        UI.showToast('Backup File Downloaded');
      } else if (item.value === 'random') {
        if (this.state.filteredPrompts.length > 0) {
          const randomIndex = Math.floor(Math.random() * this.state.filteredPrompts.length);
          const chosen = this.state.filteredPrompts[randomIndex];
          this.selectPrompt(chosen.id);
        }
      }
    } else if (item.type === 'prompt') {
      this.selectPrompt(item.value);
    }
  }
};
