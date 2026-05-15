const API_URL = import.meta.env.VITE_API_BASE_URL

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

export async function signupRequest(signupData) {
  const url = `${API_URL}/auth/register/`
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(signupData),
    })

    if (!response.ok) {
      const text = await response.text()
      let errorMsg = "Erreur lors de l'inscription"
      try {
        const json = JSON.parse(text)
        errorMsg =
          json.detail ||
          json.non_field_errors?.[0] ||
          Object.values(json)?.flat?.()[0] ||
          errorMsg
      } catch {}
      throw new Error(errorMsg)
    }

    if (response.status === 204) return {}
    return await response.json()
  } catch (networkErr) {
    throw new Error(networkErr.message || 'Impossible de contacter le serveur')
  }
}

/**
 * Refresh access token using refresh token
 * @param {string} refreshToken
 * @returns {Promise<{access: string, refresh: string}>}
 */
export async function refreshTokenRequest(refreshToken) {
  const response = await fetch(`${API_URL}/token/refresh/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh: refreshToken }),
  })

  if (!response.ok) {
    throw new Error('Failed to refresh token')
  }

  return response.json()
}
