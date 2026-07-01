/**
 * KY Food Delivery System
 * Admin: Users Management
 */

export function UsersManagementView() {
  const container = document.createElement('div');
  container.className = 'users-management-view';
  container.style.padding = 'var(--spacing-xl)';

  const title = document.createElement('h1');
  title.textContent = 'Users Management';
  title.style.marginBottom = 'var(--spacing-xl)';
  container.appendChild(title);

  const table = document.createElement('table');
  table.style.width = '100%';
  table.style.borderCollapse = 'collapse';
  table.style.backgroundColor = 'var(--color-white)';

  const thead = table.createTHead();
  const headerRow = thead.insertRow();
  ['ID', 'Name', 'Email', 'Orders', 'Status', 'Action'].forEach(h => {
    const th = document.createElement('th');
    th.textContent = h;
    th.style.padding = 'var(--spacing-md)';
    th.style.borderBottom = '1.5px solid #D0C9BF';
    th.style.fontWeight = '600';
    th.style.textAlign = 'left';
    headerRow.appendChild(th);
  });

  const tbody = table.createTBody();
  const users = [
    { id: 'USR001', name: 'John Doe', email: 'john@email.com', orders: 12, status: 'Active' },
    { id: 'USR002', name: 'Jane Smith', email: 'jane@email.com', orders: 8, status: 'Active' },
    { id: 'USR003', name: 'Bob Wilson', email: 'bob@email.com', orders: 0, status: 'Inactive' }
  ];

  users.forEach(user => {
    const row = tbody.insertRow();
    [user.id, user.name, user.email, user.orders, user.status].forEach(text => {
      const td = row.insertCell();
      td.textContent = text;
      td.style.padding = 'var(--spacing-md)';
      td.style.borderBottom = '1px solid #E8D7B5';
    });

    const actionTd = row.insertCell();
    const editBtn = document.createElement('button');
    editBtn.textContent = 'Edit';
    editBtn.style.padding = '0.25rem 0.75rem';
    editBtn.style.backgroundColor = 'var(--color-primary-green)';
    editBtn.style.color = 'white';
    editBtn.style.border = 'none';
    editBtn.style.borderRadius = 'var(--radius-sm)';
    editBtn.style.cursor = 'pointer';
    actionTd.appendChild(editBtn);
  });

  container.appendChild(table);
  return container;
}
