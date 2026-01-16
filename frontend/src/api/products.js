const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Get all products from the API
 * @returns {Promise<Array>} Products list
 */
export const getAllProducts = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erreur lors de la récupération des produits:', error);
    throw error;
  }
};

/**
 * Get product details by ID
 * @param {number} id - Product ID
 * @returns {Promise<Object>} - Product details
 */
export const getProductById = async (id) => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/${id}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Erreur lors de la récupération du produit ${id}:`, error);
    throw error;
  }
};

/**
 * Get products by category ID
 * @param {number} categoryId - Category ID
 * @returns {Promise<Array>} Filtered products list
 * (?) Is this route needed (?)
 */
export const getProductsByCategory = async (categoryId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/products/?category=${categoryId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erreur lors de la récupération des produits par catégorie:', error);
    throw error;
  }
};