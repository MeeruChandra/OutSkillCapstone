import api from './api'

/**
 * Order service following Single Responsibility Principle
 * Handles all order-related API calls
 */
class OrderService {
  async createOrder(orderData) {
    const response = await api.post('/api/orders', orderData)
    return response.data
  }

  async getOrders() {
    const response = await api.get('/api/orders')
    return response.data
  }

  async getOrderById(id) {
    const response = await api.get(`/api/orders/${id}`)
    return response.data
  }
}

export default new OrderService()
