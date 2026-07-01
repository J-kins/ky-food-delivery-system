/**
 * KY Food Delivery — Auth Module
 * Manages login state, token storage, and session helpers.
 */

const TOKEN_KEY = 'ky_token';
const USER_KEY  = 'ky_user';

export const Auth = {
  /** Save auth session after login */
  setSession(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  /** Get the stored JWT token */
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  /** Get the current user object */
  getUser() {
    try {
      return JSON.parse(localStorage.getItem(USER_KEY));
    } catch {
      return null;
    }
  },

  /** Check if user is authenticated */
  isLoggedIn() {
    return !!this.getToken();
  },

  /** Clear the session (logout) */
  clearSession() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },
};
