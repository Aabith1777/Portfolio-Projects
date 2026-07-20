/**
 * Storage Engine for PromptVault
 * Handles offline persistence using localStorage
 */
const StorageEngine = {
  PREFIX: 'promptvault_',

  // Base methods
  get(key, defaultValue = null) {
    try {
      const value = localStorage.getItem(this.PREFIX + key);
      return value ? JSON.parse(value) : defaultValue;
    } catch (e) {
      console.error('Error reading from localStorage', e);
      return defaultValue;
    }
  },

  set(key, value) {
    try {
      localStorage.setItem(this.PREFIX + key, JSON.stringify(value));
      return true;
    } catch (e) {
      console.error('Error writing to localStorage', e);
      return false;
    }
  },

  remove(key) {
    try {
      localStorage.removeItem(this.PREFIX + key);
      return true;
    } catch (e) {
      console.error('Error removing from localStorage', e);
      return false;
    }
  },

  // Favorites management
  getFavorites() {
    return this.get('favorites', []);
  },

  isFavorite(id) {
    const favorites = this.getFavorites();
    return favorites.includes(id);
  },

  toggleFavorite(id) {
    let favorites = this.getFavorites();
    const index = favorites.indexOf(id);
    let added = false;
    
    if (index === -1) {
      favorites.push(id);
      added = true;
    } else {
      favorites.splice(index, 1);
    }
    
    this.set('favorites', favorites);
    return { favorites, added };
  },

  resetFavorites() {
    return this.set('favorites', []);
  },

  // Pinned prompts management
  getPinned() {
    return this.get('pinned', []);
  },

  isPinned(id) {
    const pinned = this.getPinned();
    return pinned.includes(id);
  },

  togglePin(id) {
    let pinned = this.getPinned();
    const index = pinned.indexOf(id);
    let added = false;
    
    if (index === -1) {
      pinned.push(id);
      added = true;
    } else {
      pinned.splice(index, 1);
    }
    
    this.set('pinned', pinned);
    return { pinned, added };
  },

  // Recently Viewed management (keeps last 5 unique prompts)
  getRecentlyViewed() {
    return this.get('recently_viewed', []);
  },

  addRecentlyViewed(id) {
    let list = this.getRecentlyViewed();
    // Remove if already exists to push it to the top/front
    list = list.filter(item => item !== id);
    list.unshift(id);
    // Limit to 5
    if (list.length > 5) {
      list.pop();
    }
    this.set('recently_viewed', list);
    return list;
  },

  resetRecentlyViewed() {
    return this.set('recently_viewed', []);
  },

  // Theme settings
  getTheme() {
    return this.get('theme', 'dark'); // Default to dark first
  },

  setTheme(theme) {
    return this.set('theme', theme);
  },

  // Ratings (up/down vote persistence)
  getRatings() {
    return this.get('ratings', {});
  },

  getRating(id) {
    const ratings = this.getRatings();
    return ratings[id] || null;
  },

  setRating(id, ratingType) {
    const ratings = this.getRatings();
    if (ratings[id] === ratingType) {
      delete ratings[id]; // Toggle off
    } else {
      ratings[id] = ratingType; // Up or Down
    }
    this.set('ratings', ratings);
    return ratings[id] || null;
  },

  // Window Preferences
  getPreferences() {
    return this.get('preferences', {
      sidebarCollapsed: false,
      detailPaneCollapsed: false
    });
  },

  setPreference(key, value) {
    const prefs = this.getPreferences();
    prefs[key] = value;
    return this.set('preferences', prefs);
  },

  // Import/Export Tools
  exportBackup() {
    const data = {
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      favorites: this.getFavorites(),
      pinned: this.getPinned(),
      ratings: this.getRatings(),
      recently_viewed: this.getRecentlyViewed(),
      theme: this.getTheme(),
      preferences: this.getPreferences()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `promptvault_backup_${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },

  importBackup(jsonString) {
    try {
      const data = JSON.parse(jsonString);
      
      // Basic validation
      if (typeof data !== 'object' || data === null) return false;
      
      if (Array.isArray(data.favorites)) {
        this.set('favorites', data.favorites);
      }
      if (Array.isArray(data.pinned)) {
        this.set('pinned', data.pinned);
      }
      if (typeof data.ratings === 'object') {
        this.set('ratings', data.ratings);
      }
      if (Array.isArray(data.recently_viewed)) {
        this.set('recently_viewed', data.recently_viewed);
      }
      if (data.theme === 'dark' || data.theme === 'light') {
        this.set('theme', data.theme);
      }
      if (typeof data.preferences === 'object') {
        this.set('preferences', data.preferences);
      }
      
      return true;
    } catch (e) {
      console.error('Failed to parse backup JSON file', e);
      return false;
    }
  },

  resetAllSettings() {
    this.set('favorites', []);
    this.set('pinned', []);
    this.set('ratings', {});
    this.set('recently_viewed', []);
    this.set('theme', 'dark');
    this.set('preferences', {
      sidebarCollapsed: false,
      detailPaneCollapsed: false
    });
    return true;
  }
};
