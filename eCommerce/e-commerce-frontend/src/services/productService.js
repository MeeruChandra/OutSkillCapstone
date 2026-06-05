import api from './api'

/**
 * Product service following Single Responsibility Principle
 * Handles all product-related API calls
 */
class ProductService {
  async getProducts(params = {}) {
    const response = await api.get('/api/products', { params })
    return response.data
  }

  async getProductById(id) {
    const response = await api.get(`/api/products/${id}`)
    return response.data
  }

  async searchProducts(search) {
    const response = await api.get('/api/products', {
      params: { search }
    })
    return response.data
  }

  async getProductsByCategory(category) {
    const response = await api.get('/api/products', {
      params: { category }
    })
    return response.data
  }
}

export default new ProductService()
