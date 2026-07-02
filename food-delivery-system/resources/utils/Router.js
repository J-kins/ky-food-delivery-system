/**
 * KY Food Delivery System
 * Utility: Router
 * 
 * Handles hash-based routing with lifecycle hooks for mounting and unmounting
 * interactive components like charts and maps.
 */

export class Router {
  constructor(routes, layoutComponent, appElementId = 'app') {
    this.routes = routes;
    this.layoutComponent = layoutComponent;
    this.appElement = document.getElementById(appElementId);
    this.currentView = null;
    
    // Bind the listener
    this.handleHashChange = this.handleHashChange.bind(this);
    window.addEventListener('hashchange', this.handleHashChange);
  }

  start() {
    this.handleHashChange();
  }

  handleHashChange() {
    const hash = window.location.hash || '#/';
    const route = this.routes[hash] || Object.values(this.routes)[0]; // default to first if not found
    
    // Unmount previous view
    if (this.currentView && typeof this.currentView.onUnmount === 'function') {
      this.currentView.onUnmount();
    }

    // Clear app container
    this.appElement.innerHTML = '';

    // Render new view
    const viewResult = route.component();
    
    let contentElement;
    if (viewResult instanceof HTMLElement) {
      contentElement = viewResult;
      this.currentView = { element: viewResult };
    } else {
      contentElement = viewResult.element;
      this.currentView = viewResult;
    }

    // Prepare nav items for layout
    const navItems = Object.entries(this.routes).map(([path, cfg]) => ({
      label: cfg.title,
      href: path,
      active: hash === path || (path === '#/' && hash === '')
    }));

    // Wrap in layout
    const layout = this.layoutComponent({
      content: contentElement,
      title: route.title,
      navItems: navItems
    });

    this.appElement.appendChild(layout);
    window.scrollTo(0, 0);

    // Call onMount after the element is in the DOM
    if (typeof this.currentView.onMount === 'function') {
      // Use requestAnimationFrame to ensure the browser has painted the DOM elements
      // so libraries like Chart.js or D3 can reliably calculate dimensions
      requestAnimationFrame(() => {
        this.currentView.onMount();
      });
    }
  }
}
