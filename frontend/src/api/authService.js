const API_URL = 'http://localhost:8000/api'

/**
 * Send Django login details to get JWT tokens
 * @param {string} email
 * @param {string} password
 * @returns {Promise<{access: string, refresh: string}>}
 */

export async function loginRequest(email, password) {
  const response = await fetch(`${API_URL}/token/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  })

  if (!response.ok) {
    // Return the error message from the backend if login fails
    const error = await response.json()
    throw new Error(error.detail || 'Identifiants invalides')
  }

  return response.json() // { access, refresh }
}
