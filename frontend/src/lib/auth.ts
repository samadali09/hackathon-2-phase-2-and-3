

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 1. User Type Definition
export interface User {
  id: string;
  email: string;
  name?: string;
}

// 2. getCurrentUser Function (Dashboard ki demand)
export async function getCurrentUser(): Promise<User | null> {
  const token = getToken();
  if (!token) return null;

  try {
    const response = await fetch(`${API_URL}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (!response.ok) return null;
    return await response.json();
  } catch (error) {
    return null;
  }
}

// 3. Sign Out Function
export function signOut() {
  localStorage.removeItem('token');
  if (typeof window !== 'undefined') {
    window.location.href = '/'; // Logout ke baad home par bhej dega
  }
}

// 4. API Login
export async function signInApi(email: string, password: string) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Sign in failed');
  }

  const data = await response.json();
  if (data.access_token) {
    localStorage.setItem('token', data.access_token);
  }
  return data;
}

// 5. API Register
export async function signUpApi(email: string, password: string, name: string) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Sign up failed');
  }

  const data = await response.json();
  if (data.access_token) {
    localStorage.setItem('token', data.access_token);
  }
  return data;
}

// 6. Helper functions
export function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
}