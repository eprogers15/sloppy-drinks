// ============================================================================
// SLOPPY DRINKS - Main JavaScript
// Vanilla JavaScript - No dependencies required (except HTMX for AJAX)
// 
// Table of Contents:
// 1. Search Bar Functionality
// 2. Sort Dropdown Functionality  
// 3. Filter Dropdown Functionality
// 4. Carousel Functionality (Drink Detail Page)
// 5. HTMX Error Handling
// 6. Utility Functions
// 7. Initialization
// ============================================================================

// ============================================================================
// 1. SEARCH BAR FUNCTIONALITY
// ============================================================================

/**
 * Prevent form submission on Enter key in search bar
 * This allows HTMX to handle the search via AJAX instead of page reload
 */
const searchBarForm = document.getElementById('search-bar-form');
if (searchBarForm) {
  searchBarForm.addEventListener('submit', (e) => {
    e.preventDefault();
  });
}

/**
 * Handle search bar clear button visibility
 * Shows clear button when user types, hides when empty
 */
const searchBar = document.getElementById('search-bar');
const clearButton = document.getElementById('clear-button');

if (searchBar && clearButton) {
  searchBar.addEventListener('input', () => {
    if (searchBar.value) {
      clearButton.style.display = 'block';
      searchBar.classList.add('clear-visible');
    } else {
      clearButton.style.display = 'none';
      searchBar.classList.remove('clear-visible');
    }
  });

  /**
   * Handle clear button click
   * Clears search, refocuses input, and triggers HTMX update
   */
  clearButton.addEventListener('click', () => {
    searchBar.value = '';
    searchBar.focus();
    clearButton.style.display = 'none';
    searchBar.classList.remove('clear-visible');
    
    // Trigger change event for HTMX
    const event = new Event('change', { bubbles: true });
    searchBar.dispatchEvent(event);
  });

  /**
   * Keyboard accessibility for clear button
   * Allows Enter/Space to activate the button
   */
  clearButton.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      clearButton.click();
    }
  });
}

// ============================================================================
// 2. SORT DROPDOWN FUNCTIONALITY
// ============================================================================

/**
 * Handle sort dropdown selection
 * Updates button text, active state, and hidden input value
 * @param {HTMLElement} element - The clicked sort dropdown item
 */
function handleSortSelection(element) {
  const newSortOrder = element.getAttribute('value');
  const sortButton = document.getElementById('sort-button');
  const sortHidden = document.getElementById('sort-hidden');
  
  if (sortButton && sortHidden) {
    sortButton.setAttribute('value', newSortOrder);
    sortButton.textContent = 'Sort: ' + element.textContent;
    
    // Remove active class from all items
    document.querySelectorAll('.dropdown-sort-item').forEach(item => {
      item.classList.remove('active');
    });
    
    // Add active class to selected item
    element.classList.add('active');
    sortHidden.setAttribute('value', newSortOrder);
  }
}

/**
 * Event delegation for sort dropdown items
 * Handles clicks on any sort item
 */
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('dropdown-sort-item')) {
    handleSortSelection(e.target);
  }
});

/**
 * Keyboard support for sort items
 * Allows Enter/Space to select sort options
 */
document.addEventListener('keydown', (e) => {
  if (e.target.classList.contains('dropdown-sort-item')) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleSortSelection(e.target);
      e.target.click();
    }
  }
});

// ============================================================================
// 3. FILTER DROPDOWN FUNCTIONALITY
// ============================================================================

/**
 * Update filter button text and state
 * Shows count of selected filters in button text
 */
function updateFilterButton() {
  const filterButton = document.getElementById('filter-button');
  const filterHidden = document.getElementById('filter-hidden');
  const checkedBoxes = document.querySelectorAll('.dropdown-filter-checkbox:checked');
  const checkedValues = Array.from(checkedBoxes).map(cb => cb.id);
  
  if (filterButton && filterHidden) {
    filterHidden.setAttribute('value', checkedValues.join(','));
    
    if (checkedValues.length > 0) {
      filterButton.textContent = `Ingredients (${checkedValues.length})`;
    } else {
      filterButton.textContent = 'Ingredients';
    }
  }
  
  /**
   * Show/hide clear filters button
   * Only shows when at least one filter is selected
   */
  const clearFilterDiv = document.getElementById('clearFilterButtonAndDivider');
  if (clearFilterDiv) {
    clearFilterDiv.style.display = checkedValues.length > 0 ? 'block' : 'none';
  }
}

/**
 * Event delegation for filter checkboxes
 * Updates filter button when any checkbox changes
 */
document.addEventListener('change', (e) => {
  if (e.target.classList.contains('dropdown-filter-checkbox')) {
    updateFilterButton();
  }
});

/**
 * Clear filters button handler
 * Unchecks all filter checkboxes and updates button state
 */
const clearFilterButton = document.getElementById('clearFilterButton');
if (clearFilterButton) {
  clearFilterButton.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-filter-checkbox:checked').forEach(checkbox => {
      checkbox.checked = false;
    });
    updateFilterButton();
  });
  
  /**
   * Keyboard support for clear filters button
   * Allows Enter/Space to activate
   */
  clearFilterButton.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      clearFilterButton.click();
    }
  });
}

/**
 * Prevent dropdown from closing when clicking inside
 * Allows users to select multiple filters without dropdown closing
 */
const ingredientsList = document.querySelector('.ingredients-dropdown-list');
if (ingredientsList) {
  ingredientsList.addEventListener('click', (e) => {
    e.stopPropagation();
  });
}

// ============================================================================
// 4. CAROUSEL FUNCTIONALITY (Drink Detail Page)
// ============================================================================

/**
 * Update carousel image source attribution
 * Changes the attribution text when user slides to a different image
 */
document.addEventListener('DOMContentLoaded', () => {
  const carousel = document.querySelector('#carouselExampleIndicators');
  
  // Only run if carousel exists on the page
  if (!carousel) return;
  
  const imageSourceText = document.getElementById('image-source-text');
  
  if (!imageSourceText) return;
  
  /**
   * Updates image source attribution text based on active carousel item
   */
  function updateImageSource() {
    const activeItem = carousel.querySelector('.carousel-item.active');
    if (!activeItem) return;
    
    const imageSourceName = activeItem.getAttribute('image-source-name') || 'Unknown';
    const imageSourceUrl = activeItem.getAttribute('image-source-url') || '';
    
    let htmlContent;
    if (imageSourceUrl) {
      htmlContent = `Image by <a class="image-source-link" href="${imageSourceUrl}" target="_blank">${imageSourceName}</a>`;
    } else {
      htmlContent = `Image by ${imageSourceName}`;
    }
    imageSourceText.innerHTML = htmlContent;
  }
  
  // Update on initial load
  updateImageSource();
  
  // Update when carousel slides
  carousel.addEventListener('slid.bs.carousel', updateImageSource);
});

// ============================================================================
// 5. HTMX ERROR HANDLING
// ============================================================================

/**
 * HTMX error handling and loading states
 * Provides user feedback when AJAX requests fail or time out
 */
document.addEventListener('DOMContentLoaded', () => {
  /**
   * Handle HTMX response errors
   * Shows user-friendly error message that auto-dismisses
   */
  document.body.addEventListener('htmx:responseError', (event) => {
    console.error('HTMX request failed:', event.detail);
    
    // Show user-friendly error message
    const errorMessage = document.createElement('div');
    errorMessage.className = 'alert alert-danger alert-dismissible fade show';
    errorMessage.style.position = 'fixed';
    errorMessage.style.top = '70px';
    errorMessage.style.right = '20px';
    errorMessage.style.zIndex = '9999';
    errorMessage.innerHTML = `
      <strong>Error:</strong> Failed to load content. Please try again.
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(errorMessage);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (errorMessage.parentNode) {
        errorMessage.remove();
      }
    }, 5000);
  });
  
  /**
   * Handle HTMX timeouts
   * Logs timeout for debugging
   */
  document.body.addEventListener('htmx:timeout', (event) => {
    console.error('HTMX request timed out:', event.detail);
  });
  
  /**
   * Show loading indicator for HTMX requests
   * Dims results area and prevents interaction during load
   */
  document.body.addEventListener('htmx:beforeRequest', (event) => {
    const target = event.target;
    if (target.id === 'results') {
      target.style.opacity = '0.6';
      target.style.pointerEvents = 'none';
    }
  });
  
  /**
   * Remove loading indicator after HTMX request completes
   */
  document.body.addEventListener('htmx:afterRequest', (event) => {
    const target = event.target;
    if (target.id === 'results') {
      target.style.opacity = '1';
      target.style.pointerEvents = 'auto';
    }
  });
});

// ============================================================================
// 6. UTILITY FUNCTIONS
// ============================================================================

/**
 * Safely query a single element
 * @param {string} selector - CSS selector
 * @returns {Element|null} - Found element or null
 */
function safeQuerySelector(selector) {
  try {
    return document.querySelector(selector);
  } catch (e) {
    console.error('Invalid selector:', selector, e);
    return null;
  }
}

/**
 * Safely query multiple elements
 * @param {string} selector - CSS selector
 * @returns {NodeList|Array} - Found elements or empty array
 */
function safeQuerySelectorAll(selector) {
  try {
    return document.querySelectorAll(selector);
  } catch (e) {
    console.error('Invalid selector:', selector, e);
    return [];
  }
}

// ============================================================================
// 7. INITIALIZATION
// ============================================================================

/**
 * Log successful JavaScript initialization
 * Useful for debugging and confirming script load
 */
if (console && console.log) {
  console.log('Sloppy Drinks JS initialized');
  console.log('Features: Search, Sort, Filter, Carousel, HTMX Error Handling');
}
