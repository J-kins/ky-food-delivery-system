export function AuditLogsView() {
  const container = document.createElement('div');
  container.style.padding = 'var(--spacing-xl)';
  const title = document.createElement('h1');
  title.textContent = 'Audit Logs';
  container.appendChild(title);
  return container;
}
