/**
 * Favorites Manager for PromptVault
 * Coordinates bookmarking and collections logic
 */
const FavoritesManager = {
  toggle(id) {
    return StorageEngine.toggleFavorite(id);
  },

  isFavorite(id) {
    return StorageEngine.isFavorite(id);
  },

  getFavorites() {
    return StorageEngine.getFavorites();
  },

  /**
   * Filters the master prompts list to return only favorited items
   */
  getFavoritedPrompts(allPrompts) {
    const favorites = this.getFavorites();
    return allPrompts.filter(prompt => favorites.includes(prompt.id));
  }
};
