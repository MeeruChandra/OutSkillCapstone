import api from './api'

/**
 * Cart service following Single Responsibility Principle
 * Handles all cart-related API calls
 */
class CartService {
  async getCart() {
    const response = await api.get('/api/cart')
    return response.data
  }

  async addToCart(productId, quantity = 1) {
    const response = await api.post('/api/cart/items', {
      product_id: productId,
      quantity
    })
    return response.data
  }

  async updateCartItem(cartItemId, quantity) {
    const response = await api.put(`/api/cart/items/${cartItemId}`, {
      quantity
    })
    return response.data
  }

  async removeFromCart(cartItemId) {
    await api.delete(`/api/cart/items/${cartItemId}`)
  }

  async clearCart() {
    await api.delete('/api/cart')
  }
}

export default new CartService()
