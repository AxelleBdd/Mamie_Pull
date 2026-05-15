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

// Create product (staff only)
export const createProduct = async (productData, accessToken) => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
      credentials: 'include',
      body: JSON.stringify(productData),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || `Erreur HTTP: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error('Erreur lors de la création du produit:', error)
    throw error
  }
}

// Update product (staff only)
export const updateProduct = async (productId, productData, accessToken) => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/${productId}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
      credentials: 'include',
      body: JSON.stringify(productData),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || `Erreur HTTP: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error(
      `Erreur lors de la mise à jour du produit ${productId}:`,
      error,
    )
    throw error
  }
}

// Delete product (staff only)
export const deleteProduct = async (productId, accessToken) => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/${productId}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
      credentials: 'include',
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || `Erreur HTTP: ${response.status}`)
    }

    return true
  } catch (error) {
    console.error(
      `Erreur lors de la suppression du produit ${productId}:`,
      error,
    )
    throw error
  }
}
