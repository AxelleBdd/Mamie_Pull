const API_URL = import.meta.env.VITE_API_BASE_URL

export async function getCurrentUser(accessToken) {
  const response = await fetch(`${API_URL}/auth/me/`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
  })

  if (!response.ok) {
    throw new Error('Impossible de charger le profil utilisateur')
  }

  return response.json()
}

export async function updateUser(accessToken, userData) {
  const response = await fetch(`${API_URL}/auth/me/`, {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Impossible de mettre à jour le profil')
  }

  return response.json()
}
