/**
 * KY Food Delivery — Admin Portal Entry
 */
import { AdminLayout } from '../resources/views/components/layouts/AdminLayout.js';
import { AdminDashboardView } from '../resources/views/admin/AdminDashboardView.js';
import { UsersManagementView } from '../resources/views/admin/UsersManagementView.js';
import { RestaurantsManagementView } from '../resources/views/admin/RestaurantsManagementView.js';
import { OrdersMonitoringView } from '../resources/views/admin/OrdersMonitoringView.js';
import { SystemSettingsView } from '../resources/views/admin/SystemSettingsView.js';

import { Router } from '../resources/utils/Router.js';

const routes = {
  '#/': { title: 'Dashboard', component: AdminDashboardView },
  '#/orders': { title: 'Orders Monitoring', component: OrdersMonitoringView },
  '#/users': { title: 'Users Management', component: UsersManagementView },
  '#/restaurants': { title: 'Restaurants Management', component: RestaurantsManagementView },
  '#/settings': { title: 'System Settings', component: SystemSettingsView },
};

document.addEventListener('DOMContentLoaded', () => {
  const router = new Router(routes, AdminLayout);
  router.start();
});
