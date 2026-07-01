import { PublicLayout } from '../resources/views/components/layouts/PublicLayout.js';
import { HomeView } from '../resources/views/public/HomeView.js';
import { MenuView } from '../resources/views/public/MenuView.js';
import { LoginView } from '../resources/views/public/LoginView.js';

// Simple Hash Router
const routes = {
  '#/': HomeView,
  '#/menu': MenuView,
  '#/login': LoginView,
};

function render() {
  const hash = window.location.hash || '#/';
  const ViewComponent = routes[hash] || HomeView;

  const app = document.getElementById('app');
  app.innerHTML = '';

  const content = ViewComponent();
  const layout = PublicLayout({ content });
  
  app.appendChild(layout);
  window.scrollTo(0, 0);
}

// Listen for hash changes
window.addEventListener('hashchange', render);

// Initial render
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', render);
} else {
  render();
}
