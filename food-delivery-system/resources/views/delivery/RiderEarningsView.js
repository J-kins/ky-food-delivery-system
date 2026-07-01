/**
 * KY Food Delivery System
 * View: Rider Earnings
 */
import { Card } from '../components/common/Card.js';

export function RiderEarningsView() {
  const container = document.createElement('div');
  container.className = 'rider-earnings-view';
  container.style.padding = 'var(--spacing-xl)';
  container.style.maxWidth = '1000px';
  container.style.margin = '0 auto';

  const title = document.createElement('h1');
  title.textContent = 'Earnings';
  title.style.marginBottom = 'var(--spacing-xl)';

  container.appendChild(title);

  const summary = document.createElement('div');
  summary.style.display = 'grid';
  summary.style.gridTemplateColumns = 'repeat(auto-fit, minmax(200px, 1fr))';
  summary.style.gap = 'var(--spacing-lg)';
  summary.style.marginBottom = 'var(--spacing-xl)';

  const earnings = [
    { label: 'Today', amount: 'UGX 84,000' },
    { label: 'This Week', amount: 'UGX 420,000' },
    { label: 'This Month', amount: 'UGX 1,680,000' }
  ];

  earnings.forEach(earn => {
    const content = document.createElement('div');

    const label = document.createElement('p');
    label.textContent = earn.label;
    label.style.margin = '0 0 var(--spacing-sm) 0';

    const amount = document.createElement('h3');
    amount.textContent = earn.amount;
    amount.style.margin = '0';
    amount.style.color = 'var(--color-primary-green)';

    content.appendChild(label);
    content.appendChild(amount);

    const card = Card({ children: content, padding: 'lg' });
    summary.appendChild(card);
  });

  container.appendChild(summary);

  const transactions = document.createElement('section');
  transactions.style.marginTop = 'var(--spacing-xl)';

  const transTitle = document.createElement('h2');
  transTitle.textContent = 'Recent Earnings';
  transTitle.style.marginBottom = 'var(--spacing-lg)';

  const transTable = document.createElement('table');
  transTable.style.width = '100%';
  transTable.style.borderCollapse = 'collapse';

  const header = transTable.createTHead();
  const headerRow = header.insertRow();
  headerRow.innerHTML = '<th style="text-align:left;padding:var(--spacing-md);border-bottom:1.5px solid #D0C9BF;">Date</th><th style="text-align:left;padding:var(--spacing-md);border-bottom:1.5px solid #D0C9BF;">Orders</th><th style="text-align:right;padding:var(--spacing-md);border-bottom:1.5px solid #D0C9BF;">Amount</th>';

  const body = transTable.createTBody();
  [
    { date: '1 Dec 2024', orders: 15, amount: 'UGX 84,000' },
    { date: '30 Nov 2024', orders: 12, amount: 'UGX 72,000' },
    { date: '29 Nov 2024', orders: 14, amount: 'UGX 78,000' }
  ].forEach(row => {
    const tr = body.insertRow();
    tr.innerHTML = `<td style="padding:var(--spacing-md);border-bottom:1px solid #E8D7B5;">${row.date}</td><td style="padding:var(--spacing-md);border-bottom:1px solid #E8D7B5;">${row.orders}</td><td style="text-align:right;padding:var(--spacing-md);border-bottom:1px solid #E8D7B5;font-weight:600;color:var(--color-primary-green);">${row.amount}</td>`;
  });

  transactions.appendChild(transTitle);
  transactions.appendChild(transTable);
  container.appendChild(transactions);

  return container;
}
