/**
 * KY Food Delivery — Manager Portal Entry
 */
import { AdminLayout } from '../resources/views/components/layouts/AdminLayout.js';
import { ManagerDashboardView } from '../resources/views/manager/ManagerDashboardView.js';
import { MenuManagementView } from '../resources/views/manager/MenuManagementView.js';
import { OrdersManagementView } from '../resources/views/manager/OrdersManagementView.js';
import { StaffManagementView } from '../resources/views/manager/StaffManagementView.js';
import { PromotionsManagementView } from '../resources/views/manager/PromotionsManagementView.js';

import { Router } from '../resources/utils/Router.js';

const routes = {
  '#/': { title: 'Manager Dashboard', component: ManagerDashboardView },
  '#/menu': { title: 'Menu Management', component: MenuManagementView },
  '#/orders': { title: 'Orders Management', component: OrdersManagementView },
  '#/staff': { title: 'Staff Management', component: StaffManagementView },
  '#/promotions': { title: 'Promotions Management', component: PromotionsManagementView },
};

document.addEventListener('DOMContentLoaded', () => {
  const router = new Router(routes, AdminLayout);
  router.start();
});
