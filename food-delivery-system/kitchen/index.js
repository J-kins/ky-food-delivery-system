/**
 * KY Food Delivery — Kitchen Portal Entry
 */
import { KitchenLayout } from '../resources/views/components/layouts/KitchenLayout.js';
import { KitchenDashboardView } from '../resources/views/kitchen/KitchenDashboardView.js';
import { IncomingOrdersView } from '../resources/views/kitchen/IncomingOrdersView.js';
import { OrderPreparationView } from '../resources/views/kitchen/OrderPreparationView.js';
import { KitchenQueueView } from '../resources/views/kitchen/KitchenQueueView.js';
import { KitchenSettingsView } from '../resources/views/kitchen/KitchenSettingsView.js';

import { Router } from '../resources/utils/Router.js';

const routes = {
  '#/': { title: 'Kitchen Dashboard', component: KitchenDashboardView },
  '#/incoming': { title: 'Incoming Orders', component: IncomingOrdersView },
  '#/preparation': { title: 'Order Preparation', component: OrderPreparationView },
  '#/queue': { title: 'Kitchen Queue', component: KitchenQueueView },
  '#/settings': { title: 'Kitchen Settings', component: KitchenSettingsView },
};

document.addEventListener('DOMContentLoaded', () => {
  const router = new Router(routes, KitchenLayout);
  router.start();
});
