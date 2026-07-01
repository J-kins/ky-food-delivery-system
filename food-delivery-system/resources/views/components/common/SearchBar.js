/**
 * KY Food Delivery System
 * Component: SearchBar
 *
 * A search input with a submit button and optional clear button.
 *
 * @param {Object}   options
 * @param {string}   [options.placeholder]  - Placeholder text (default: 'Search...')
 * @param {string}   [options.value]        - Initial value
 * @param {boolean}  [options.expandable]   - Collapses to icon on desktop, expands on focus
 * @param {string}   [options.id]           - HTML id on the input
 * @param {string}   [options.className]    - Extra CSS classes on wrapper
 * @param {Function} [options.onSearch]     - Called with query string on submit/enter
 * @param {Function} [options.onInput]      - Called on each keystroke
 * @param {Function} [options.onClear]      - Called when clear button is pressed
 * @returns {HTMLFormElement}
 *
 * Usage:
 *   import { SearchBar } from './components/common/SearchBar.js';
 *   header.appendChild(SearchBar({ onSearch: (q) => loadResults(q) }));
 */

const SEARCH_ICON = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>`;
const CLEAR_ICON  = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`;

export function SearchBar({
  placeholder = 'Search...',
  value = '',
  expandable = false,
  id = 'search-input',
  className = '',
  onSearch = null,
  onInput = null,
  onClear = null,
} = {}) {
  const form = document.createElement('form');
  form.className = ['searchbar', expandable ? 'searchbar--expandable' : '', className].filter(Boolean).join(' ');
  form.setAttribute('role', 'search');
  form.setAttribute('aria-label', 'Site search');

  // Leading search icon (decorative)
  const iconWrap = document.createElement('span');
  iconWrap.className = 'searchbar__icon';
  iconWrap.innerHTML = SEARCH_ICON;
  form.appendChild(iconWrap);

  // Input
  const input = document.createElement('input');
  input.type = 'search';
  input.id = id;
  input.name = 'q';
  input.className = 'searchbar__input';
  input.placeholder = placeholder;
  input.value = value;
  input.setAttribute('aria-label', placeholder);
  input.setAttribute('autocomplete', 'off');

  input.addEventListener('input', (e) => {
    clearBtn.style.display = input.value ? 'flex' : 'none';
    if (onInput) onInput(e.target.value);
  });

  form.appendChild(input);

  // Clear button
  const clearBtn = document.createElement('button');
  clearBtn.type = 'button';
  clearBtn.className = 'searchbar__clear';
  clearBtn.setAttribute('aria-label', 'Clear search');
  clearBtn.innerHTML = CLEAR_ICON;
  clearBtn.style.display = value ? 'flex' : 'none';
  clearBtn.addEventListener('click', () => {
    input.value = '';
    clearBtn.style.display = 'none';
    input.focus();
    if (onClear) onClear();
  });
  form.appendChild(clearBtn);

  // Submit
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (onSearch) onSearch(input.value.trim());
  });

  return form;
}
