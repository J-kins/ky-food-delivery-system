/**
 * KY Food Delivery — API Client
 * Centralised fetch wrapper with auth headers.
 */

const BASE_URL = '/api'; // Update when backend is live

async function request(method, endpoint, body = null) {
  const token = localStorage.getItem('ky_token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);

  const res = await fetch(`${BASE_URL}${endpoint}`, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: 'Unknown error' }));
    throw new Error(err.message || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  get:    (url)         => request('GET',    url),
  post:   (url, data)   => request('POST',   url, data),
  put:    (url, data)   => request('PUT',    url, data),
  patch:  (url, data)   => request('PATCH',  url, data),
  delete: (url)         => request('DELETE', url),
};
