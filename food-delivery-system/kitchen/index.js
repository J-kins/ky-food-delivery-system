/**
 * KY Food Delivery — Kitchen Portal Entry
 */
function render() {
  const app = document.getElementById('app');
  app.innerHTML = '';
  app.style.cssText = 'font-family:Poppins,sans-serif;min-height:100vh;background:#F7F4EF;';

  // Top bar
  const topbar = document.createElement('header');
  topbar.style.cssText = 'background:#005638;color:#fff;padding:16px 32px;display:flex;align-items:center;justify-content:space-between;';
  topbar.innerHTML = '<span style="font-family:\'Baloo 2\',sans-serif;font-size:20px;font-weight:700;color:#F0C019;">KY FOODS — KITCHEN</span><span style="font-size:14px;color:#E8D7B5;">Logged in as: Kitchen Staff</span>';

  // Content
  const content = document.createElement('main');
  content.style.cssText = 'padding:32px;';

  const h1 = document.createElement('h1');
  h1.textContent = 'Incoming Orders';
  h1.style.cssText = 'font-family:"Baloo 2",sans-serif;font-size:1.8rem;color:#3B2A1A;margin:0 0 24px;';

  const grid = document.createElement('div');
  grid.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;';

  const orders = [
    { id: '#ORD-001', items: 'Beef Burger x2, Fries x1', status: 'New', time: '2 min ago', color: '#DC4024' },
    { id: '#ORD-002', items: 'Chicken Pizza x1, Soda x2', status: 'Preparing', time: '8 min ago', color: '#F0C019' },
    { id: '#ORD-003', items: 'Pasta Bolognese x3', status: 'Ready', time: '15 min ago', color: '#005638' },
  ];

  orders.forEach(o => {
    const card = document.createElement('div');
    card.style.cssText = 'background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 12px rgba(59,42,26,0.07);border-top:4px solid ' + o.color;
    card.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
        <strong style="font-size:18px;color:#3B2A1A;">${o.id}</strong>
        <span style="background:${o.color};color:#fff;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;">${o.status}</span>
      </div>
      <p style="color:#A89F93;font-size:14px;margin:0 0 16px;">${o.items}</p>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span style="font-size:12px;color:#A89F93;">${o.time}</span>
        <button onclick="alert('Marked as done')" style="background:#005638;color:#fff;border:none;padding:8px 20px;border-radius:8px;cursor:pointer;font-weight:600;font-family:Poppins,sans-serif;">Mark Ready</button>
      </div>`;
    grid.appendChild(card);
  });

  content.appendChild(h1);
  content.appendChild(grid);
  app.appendChild(topbar);
  app.appendChild(content);
}

document.readyState === 'loading'
  ? document.addEventListener('DOMContentLoaded', render)
  : render();
