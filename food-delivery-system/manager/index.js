/**
 * KY Food Delivery — Manager Portal Entry
 */
function render() {
  const app = document.getElementById('app');
  app.innerHTML = '';
  app.style.cssText = 'font-family:Poppins,sans-serif;min-height:100vh;background:#F7F4EF;display:flex;';

  // Sidebar
  const sidebar = document.createElement('nav');
  sidebar.style.cssText = 'width:240px;background:#F03919;color:#fff;padding:24px 0;flex-shrink:0;';
  sidebar.innerHTML = `
    <div style="padding:0 24px 32px;font-family:'Baloo 2',sans-serif;font-size:20px;font-weight:700;color:#fff;">KY FOODS<br><span style="font-size:13px;font-weight:400;color:rgba(255,255,255,0.7);">Manager Portal</span></div>
  `;
  ['Menu', 'Orders', 'Staff', 'Promotions', 'Reports'].forEach((item, i) => {
    const a = document.createElement('a');
    a.href = '#';
    a.textContent = item;
    a.style.cssText = `display:block;padding:14px 24px;color:${i===0?'#F0C019':'rgba(255,255,255,0.85)'};text-decoration:none;font-weight:${i===0?'600':'400'};background:${i===0?'rgba(0,0,0,0.15)':'none'};`;
    sidebar.appendChild(a);
  });

  // Main
  const main = document.createElement('main');
  main.style.cssText = 'flex:1;padding:40px;';

  main.innerHTML = `
    <h1 style="font-family:'Baloo 2',sans-serif;font-size:2rem;color:#3B2A1A;margin:0 0 8px;">Restaurant Manager</h1>
    <p style="color:#A89F93;margin:0 0 40px;">Manage your restaurant, menu, and team.</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;">
      ${[['Today\'s Orders','48','#005638'],['Menu Items','32','#F03919'],['Staff On Duty','6','#F0C019'],['Avg. Rating','4.7','#3B2A1A']].map(([l,v,c])=>`
        <div style="background:#fff;border-radius:12px;padding:24px;box-shadow:0 2px 12px rgba(59,42,26,0.07);">
          <div style="font-size:13px;color:#A89F93;margin-bottom:8px;">${l}</div>
          <div style="font-size:2rem;font-weight:700;color:${c};font-family:'Baloo 2',sans-serif;">${v}</div>
        </div>`).join('')}
    </div>`;

  app.appendChild(sidebar);
  app.appendChild(main);
}

document.readyState === 'loading'
  ? document.addEventListener('DOMContentLoaded', render)
  : render();
