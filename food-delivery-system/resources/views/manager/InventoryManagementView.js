export function InventoryManagementView() {
  const container = document.createElement('div');
  container.style.padding = 'var(--spacing-xl)';
  const title = document.createElement('h1');
  title.textContent = 'Inventory Management';
  container.appendChild(title);
  return container;
}
