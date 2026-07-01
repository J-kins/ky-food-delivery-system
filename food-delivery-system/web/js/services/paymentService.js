/**
 * KY Food Delivery — Payment Service
 */
import { api } from '../api.js';

export const paymentService = {
  initiate(data)       { return api.post('/payments/initiate', data); },
  verify(reference)    { return api.get(`/payments/verify/${reference}`); },
  getMethods()         { return api.get('/payments/methods'); },
  addMethod(data)      { return api.post('/payments/methods', data); },
};
