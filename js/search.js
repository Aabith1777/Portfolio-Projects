/**
 * Search Engine for PromptVault
 * Performs local keyword matching, scoring, and text highlighting
 */
const SearchEngine = {
  /**
   * Escapes regex special characters in a search term
   */
  escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  },

  /**
   * Highlights matching text segments using <mark> tags
   */
  highlightText(text, query) {
    if (!query || !text) return text || '';
    
    // Convert text to string if it isn't
    const textStr = String(text);
    const escapedQuery = this.escapeRegExp(query.trim());
    
    if (!escapedQuery) return textStr;
    
    // Find all occurrences and wrap them in a mark tag
    const regex = new RegExp(`(${escapedQuery})`, 'gi');
    return textStr.replace(regex, '<mark class="search-highlight">$1</mark>');
  },

  /**
   * Searches a prompts collection and scores them by relevance
   */
  search(prompts, query) {
    if (!query || !query.trim()) {
      return prompts.map(p => ({ ...p, score: 0 }));
    }

    const terms = query.toLowerCase().trim().split(/\s+/);
    
    const results = prompts.map(prompt => {
      let score = 0;
      const title = (prompt.title || '').toLowerCase();
      const category = (prompt.category || '').toLowerCase();
      const description = (prompt.description || '').toLowerCase();
      const content = (prompt.prompt || '').toLowerCase();
      const tags = (prompt.tags || []).map(t => t.toLowerCase());
      const tips = (prompt.tips || []).map(t => t.toLowerCase());
      
      // Check each term against fields
      terms.forEach(term => {
        // Exact Title Match (highest weight)
        if (title === term) {
          score += 15;
        } else if (title.includes(term)) {
          score += 8;
        }
        
        // Category Match
        if (category === term) {
          score += 8;
        } else if (category.includes(term)) {
          score += 4;
        }
        
        // Tags Match
        if (tags.includes(term)) {
          score += 6;
        } else if (tags.some(t => t.includes(term))) {
          score += 3;
        }
        
        // Description Match
        if (description.includes(term)) {
          score += 4;
        }
        
        // Prompt Content Match
        if (content.includes(term)) {
          score += 2;
        }
        
        // Tips Match
        if (tips.some(t => t.includes(term))) {
          score += 1;
        }
      });
      
      return {
        ...prompt,
        score
      };
    });
    
    // Filter out items with 0 score and sort by score descending
    return results
      .filter(item => item.score > 0)
      .sort((a, b) => b.score - a.score);
  }
};
