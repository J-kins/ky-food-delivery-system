/**
 * KY Food Delivery System
 * Component: SearchFilter
 *
 * Filtering component for restaurant/food search results.
 *
 * @param {Object} options
 * @param {Array} [options.filters] - Available filter options
 * @param {Function} [options.onFilterChange] - Callback when filters change
 * @returns {HTMLDivElement}
 */

export function SearchFilter({ filters = [], onFilterChange = null } = {}) {
  const container = document.createElement('div');
  container.className = 'search-filter';

  const filtersMap = new Map();

  const filterGroups = [
    {
      label: 'Sort By',
      type: 'radio',
      options: [
        { value: 'relevance', label: 'Relevance' },
        { value: 'rating', label: 'Rating' },
        { value: 'delivery-time', label: 'Delivery Time' },
        { value: 'price-low', label: 'Price: Low to High' },
      ],
    },
    {
      label: 'Cuisine',
      type: 'checkbox',
      options: [
        { value: 'italian', label: 'Italian' },
        { value: 'asian', label: 'Asian' },
        { value: 'mexican', label: 'Mexican' },
        { value: 'american', label: 'American' },
      ],
    },
    {
      label: 'Price Range',
      type: 'checkbox',
      options: [
        { value: 'budget', label: 'Budget' },
        { value: 'moderate', label: 'Moderate' },
        { value: 'premium', label: 'Premium' },
      ],
    },
  ];

  filterGroups.forEach((group) => {
    const groupEl = document.createElement('div');
    groupEl.className = 'search-filter__group';

    const label = document.createElement('h4');
    label.className = 'search-filter__group-label';
    label.textContent = group.label;
    groupEl.appendChild(label);

    const options = document.createElement('div');
    options.className = 'search-filter__options';

    group.options.forEach((option) => {
      const wrapper = document.createElement('label');
      wrapper.className = 'search-filter__option';

      const input = document.createElement('input');
      input.type = group.type;
      input.name = group.label.toLowerCase();
      input.value = option.value;
      input.className = 'search-filter__input';

      const text = document.createElement('span');
      text.className = 'search-filter__option-label';
      text.textContent = option.label;

      wrapper.appendChild(input);
      wrapper.appendChild(text);
      options.appendChild(wrapper);

      input.addEventListener('change', () => {
        if (onFilterChange) {
          const active = Array.from(container.querySelectorAll('input:checked')).map(
            (el) => ({ group: el.name, value: el.value })
          );
          onFilterChange(active);
        }
      });
    });

    groupEl.appendChild(options);
    container.appendChild(groupEl);
  });

  const resetBtn = document.createElement('button');
  resetBtn.className = 'search-filter__reset';
  resetBtn.textContent = 'Clear Filters';
  resetBtn.type = 'button';
  resetBtn.addEventListener('click', () => {
    container.querySelectorAll('input:checked').forEach((el) => {
      el.checked = false;
    });
    if (onFilterChange) onFilterChange([]);
  });
  container.appendChild(resetBtn);

  return container;
}
