/**
 * KY Food Delivery — Notification Service
 */
import { api } from '../api.js';

export const notificationService = {
  getAll()        { return api.get('/notifications'); },
  markRead(id)    { return api.patch(`/notifications/${id}/read`); },
  markAllRead()   { return api.patch('/notifications/read-all'); },
};
