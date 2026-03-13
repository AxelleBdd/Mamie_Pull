const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

// Get all products
export const getAllProducts = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Erreur lors de la récupération des produits:', error)
    throw error
  }
}

// Get product details
export const getProductById = async (id) => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/${id}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    })

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error(`Erreur lors de la récupération du produit ${id}:`, error)
    throw error
  }
}

// Get products by category
export const getProductsByCategory = async (categoryId) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/products/category/${categoryId}/`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      },
    )

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error(
      'Erreur lors de la récupération des produits par catégorie:',
      error,
    )
    throw error
  }
}
