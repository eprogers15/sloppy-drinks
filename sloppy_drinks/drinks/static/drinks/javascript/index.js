// ============================================================================
// SLOPPY DRINKS - Main JavaScript
// Vanilla JavaScript - No dependencies required (except HTMX for AJAX)
// ============================================================================

// ============================================================================
// SEARCH BAR FUNCTIONALITY
// ============================================================================

// Prevent form submission on Enter key
const searchBarForm = document.getElementById('search-bar-form');
if (searchBarForm) {
  searchBarForm.addEventListener('submit', (e) => {
    e.preventDefault();
  });
}

// Handle search bar clear button visibility
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

  // Handle clear button click
  clearButton.addEventListener('click', () => {
    searchBar.value = '';
    searchBar.focus();
    clearButton.style.display = 'none';
    searchBar.classList.remove('clear-visible');
    
    // Trigger change event for HTMX
    const event = new Event('change', { bubbles: true });
    searchBar.dispatchEvent(event);
  });

  // Keyboard accessibility for clear button
  clearButton.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      clearButton.click();
    }
  });
}

// ============================================================================
// SORT DROPDOWN FUNCTIONALITY
// ============================================================================

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

// Event delegation for sort dropdown items
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('dropdown-sort-item')) {
    handleSortSelection(e.target);
  }
});

// Keyboard support for sort items
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
// FILTER DROPDOWN FUNCTIONALITY
// ============================================================================

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
  
  // Show/hide clear filters button
  const clearFilterDiv = document.getElementById('clearFilterButtonAndDivider');
  if (clearFilterDiv) {
    clearFilterDiv.style.display = checkedValues.length > 0 ? 'block' : 'none';
  }
}

// Event delegation for filter checkboxes
document.addEventListener('change', (e) => {
  if (e.target.classList.contains('dropdown-filter-checkbox')) {
    updateFilterButton();
  }
});

// Clear filters button
const clearFilterButton = document.getElementById('clearFilterButton');
if (clearFilterButton) {
  clearFilterButton.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-filter-checkbox:checked').forEach(checkbox => {
      checkbox.checked = false;
    });
    updateFilterButton();
  });
  
  // Keyboard support
  clearFilterButton.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      clearFilterButton.click();
    }
  });
}

// Prevent dropdown from closing when clicking inside
const ingredientsList = document.querySelector('.ingredients-dropdown-list');
if (ingredientsList) {
  ingredientsList.addEventListener('click', (e) => {
    e.stopPropagation();
  });
}

// ============================================================================
// CAROUSEL FUNCTIONALITY (Drink Detail Page)
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
  const carousel = document.querySelector('#carouselExampleIndicators');
  
  // Only run if carousel exists on the page
  if (!carousel) return;
  
  const imageSourceText = document.getElementById('image-source-text');
  
  if (!imageSourceText) return;
  
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
// HTMX ERROR HANDLING
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
  // Handle HTMX errors
  document.body.addEventListener('htmx:responseError', (event) => {
    console.error('HTMX request failed:', event.detail);
    
    // Optional: Show user-friendly error message
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
  
  // Handle HTMX timeouts
  document.body.addEventListener('htmx:timeout', (event) => {
    console.error('HTMX request timed out:', event.detail);
  });
  
  // Optional: Show loading indicator for HTMX requests
  document.body.addEventListener('htmx:beforeRequest', (event) => {
    const target = event.target;
    if (target.id === 'results') {
      target.style.opacity = '0.6';
      target.style.pointerEvents = 'none';
    }
  });
  
  document.body.addEventListener('htmx:afterRequest', (event) => {
    const target = event.target;
    if (target.id === 'results') {
      target.style.opacity = '1';
      target.style.pointerEvents = 'auto';
    }
  });
});

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

// Helper function to safely query elements
function safeQuerySelector(selector) {
  try {
    return document.querySelector(selector);
  } catch (e) {
    console.error('Invalid selector:', selector, e);
    return null;
  }
}

// Helper function to safely query multiple elements
function safeQuerySelectorAll(selector) {
  try {
    return document.querySelectorAll(selector);
  } catch (e) {
    console.error('Invalid selector:', selector, e);
    return [];
  }
}

// ============================================================================
// INITIALIZATION
// ============================================================================

// Log that JavaScript has loaded successfully
if (console && console.log) {
  console.log('Sloppy Drinks JS initialized');
}
