/**
 * KY Food Delivery — Delivery Service
 */
import { api } from '../api.js';

export const deliveryService = {
  getActive()         { return api.get('/deliveries/active'); },
  getById(id)         { return api.get(`/deliveries/${id}`); },
  getLocation(id)     { return api.get(`/deliveries/${id}/location`); },
};
