/**
 * KY Food Delivery — Order Service
 */
import { api } from '../api.js';

export const orderService = {
  getAll()         { return api.get('/orders'); },
  getById(id)      { return api.get(`/orders/${id}`); },
  place(data)      { return api.post('/orders', data); },
  cancel(id)       { return api.patch(`/orders/${id}/cancel`); },
  getHistory()     { return api.get('/orders/history'); },
  trackOrder(id)   { return api.get(`/orders/${id}/track`); },
};
