/**
 * KY Food Delivery — Auth Service
 */
import { api }  from '../api.js';
import { Auth } from '../auth.js';

export const authService = {
  async login(email, password) {
    const res = await api.post('/auth/login', { email, password });
    Auth.setSession(res.token, res.user);
    return res.user;
  },

  async register(data) {
    const res = await api.post('/auth/register', data);
    Auth.setSession(res.token, res.user);
    return res.user;
  },

  logout() {
    Auth.clearSession();
    window.location.hash = '#/login';
  },

  currentUser() {
    return Auth.getUser();
  },

  isLoggedIn() {
    return Auth.isLoggedIn();
  }
};
