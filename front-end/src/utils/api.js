
const BASE_URL = process.env.REACT_APP_API_BASE_URL;

export async function apiFetch(path, options = {}) {
    const token = localStorage.getItem("access_token");
  
    const headers = {
      ...(options.headers || {}),
      ...(token && { Authorization: `Bearer ${token}` }),
      'Content-Type': 'application/json'
    };
  
    const res = await fetch(`${BASE_URL}${path}`, {
      ...options,
      headers
    });
  
    return res;
  }