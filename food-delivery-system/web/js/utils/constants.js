/** KY Food Delivery — Shared Constants */
export const APP_NAME    = 'KY Food Delivery';
export const CURRENCY    = 'UGX';
export const API_BASE    = '/api';

export const ORDER_STATUS = {
  PENDING    : 'pending',
  CONFIRMED  : 'confirmed',
  PREPARING  : 'preparing',
  READY      : 'ready',
  PICKED_UP  : 'picked_up',
  DELIVERED  : 'delivered',
  CANCELLED  : 'cancelled',
};

export const PAYMENT_METHODS = {
  MOBILE_MONEY : 'mobile_money',
  CARD         : 'card',
  CASH         : 'cash',
};
