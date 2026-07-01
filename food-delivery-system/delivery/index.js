/**
 * KY Food Delivery — Delivery Portal Entry
 */
function render() {
  const app = document.getElementById('app');
  app.innerHTML = '';
  app.style.cssText = 'font-family:Poppins,sans-serif;min-height:100vh;background:#F7F4EF;';

  const topbar = document.createElement('header');
  topbar.style.cssText = 'background:#3B2A1A;color:#fff;padding:16px 32px;display:flex;align-items:center;justify-content:space-between;';
  topbar.innerHTML = '<span style="font-family:\'Baloo 2\',sans-serif;font-size:20px;font-weight:700;color:#F0C019;">KY FOODS — DELIVERY</span><span style="font-size:14px;color:#E8D7B5;">Rider: John D.</span>';

  const content = document.createElement('main');
  content.style.cssText = 'padding:32px;';

  const h1 = document.createElement('h1');
  h1.textContent = 'My Deliveries';
  h1.style.cssText = 'font-family:"Baloo 2",sans-serif;font-size:1.8rem;color:#3B2A1A;margin:0 0 24px;';

  const deliveries = [
    { id: '#DLV-011', customer: 'Alice Namukasa', address: '14 Kampala Rd, Kampala', status: 'Picked Up', statusColor: '#F03919' },
    { id: '#DLV-012', customer: 'Brian Otieno',   address: '7 Entebbe Rd, Entebbe',  status: 'Delivered',  statusColor: '#005638' },
  ];

  const list = document.createElement('div');
  list.style.cssText = 'display:flex;flex-direction:column;gap:16px;max-width:700px;';

  deliveries.forEach(d => {
    const card = document.createElement('div');
    card.style.cssText = 'background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 12px rgba(59,42,26,0.07);display:flex;justify-content:space-between;align-items:center;';
    card.innerHTML = `
      <div>
        <strong style="font-size:16px;color:#3B2A1A;">${d.id}</strong>
        <p style="margin:4px 0;color:#A89F93;font-size:14px;">${d.customer}</p>
        <p style="margin:0;color:#A89F93;font-size:13px;">${d.address}</p>
      </div>
      <span style="background:${d.statusColor};color:#fff;padding:6px 16px;border-radius:20px;font-size:13px;font-weight:600;white-space:nowrap;">${d.status}</span>`;
    list.appendChild(card);
  });

  content.appendChild(h1);
  content.appendChild(list);
  app.appendChild(topbar);
  app.appendChild(content);
}

document.readyState === 'loading'
  ? document.addEventListener('DOMContentLoaded', render)
  : render();
