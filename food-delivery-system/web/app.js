/**
 * KY Food Delivery System
 * Web App Entry Point & Router
 *
 * Served from: food-delivery-system/web/
 * Server root: food-delivery-system/ (python3 -m http.server 8000)
 * Access via:  http://localhost:8000/web/
 */

import { PublicLayout } from '../resources/views/components/layouts/PublicLayout.js';
import { HomeView }     from '../resources/views/public/HomeView.js';
import { MenuView }     from '../resources/views/public/MenuView.js';
import { LoginView }    from '../resources/views/public/LoginView.js';

// ─── Route Table ────────────────────────────────────────────────────────────
const routes = {
  '#/'       : HomeView,
  '#/menu'   : MenuView,
  '#/login'  : LoginView,
};

// ─── Router ──────────────────────────────────────────────────────────────────
function render() {
  const hash = window.location.hash || '#/';
  const ViewFn = routes[hash] || HomeView;

  const app = document.getElementById('app');
  if (!app) { console.error('[KY Router] #app mount point not found'); return; }

  // Clear previous view
  app.innerHTML = '';

  try {
    const content = ViewFn();
    const layout  = PublicLayout({ content });
    app.appendChild(layout);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } catch (err) {
    console.error('[KY Router] View render error:', err);
    // Fallback error UI
    app.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:center;height:100vh;flex-direction:column;gap:16px;font-family:Poppins,sans-serif;">
        <p style="font-size:1.2rem;color:#3B2A1A;font-weight:600;">Something went wrong loading this page.</p>
        <a href="#/" style="color:#005638;font-weight:600;">Go Home</a>
      </div>`;
  }
}

// ─── Event Listeners ─────────────────────────────────────────────────────────
window.addEventListener('hashchange', render);

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', render);
} else {
  render();
}

// Export router for programmatic navigation
export function navigate(hash) {
  window.location.hash = hash;
}
