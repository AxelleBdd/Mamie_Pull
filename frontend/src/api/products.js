// Service pour gérer les appels API liés aux produits

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Récupère tous les produits depuis le backend
 * @returns {Promise<Array>} Liste des produits
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
 * Récupère un produit par son ID
 * @param {number} id - ID du produit
 * @returns {Promise<Object>} Détails du produit
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
 * Récupère les produits filtrés par catégorie
 * @param {number} categoryId - ID de la catégorie
 * @returns {Promise<Array>} Liste des produits filtrés
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