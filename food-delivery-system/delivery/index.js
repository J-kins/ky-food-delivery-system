/**
 * KY Food Delivery — Delivery Portal Entry
 */
import { DeliveryLayout } from '../resources/views/components/layouts/DeliveryLayout.js';
import { DeliveryDashboardView } from '../resources/views/delivery/DeliveryDashboardView.js';
import { DeliveryRequestsView } from '../resources/views/delivery/DeliveryRequestsView.js';
import { DeliveryStatusView } from '../resources/views/delivery/DeliveryStatusView.js';
import { RiderEarningsView } from '../resources/views/delivery/RiderEarningsView.js';
import { RiderProfileView } from '../resources/views/delivery/RiderProfileView.js';

import { Router } from '../resources/utils/Router.js';

const routes = {
  '#/': { title: 'Delivery Dashboard', component: DeliveryDashboardView },
  '#/requests': { title: 'Delivery Requests', component: DeliveryRequestsView },
  '#/status': { title: 'Delivery Status', component: DeliveryStatusView },
  '#/earnings': { title: 'Earnings', component: RiderEarningsView },
  '#/profile': { title: 'Rider Profile', component: RiderProfileView },
};

document.addEventListener('DOMContentLoaded', () => {
  const router = new Router(routes, DeliveryLayout);
  router.start();
});
