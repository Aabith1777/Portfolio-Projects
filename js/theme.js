/**
 * Theme Manager for PromptVault
 * Coordinates dark/light modes and persists selections
 */
const ThemeManager = {
  currentTheme: 'dark',

  init() {
    // Load theme from StorageEngine, falling back to 'dark'
    this.currentTheme = StorageEngine.getTheme() || 'dark';
    this.applyTheme(this.currentTheme);
  },

  applyTheme(theme) {
    this.currentTheme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    StorageEngine.setTheme(theme);
    
    // Dispatch custom event to notify components
    const event = new CustomEvent('themechanged', { detail: { theme } });
    window.dispatchEvent(event);
  },

  toggle() {
    const nextTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
    this.applyTheme(nextTheme);
    return nextTheme;
  }
};
