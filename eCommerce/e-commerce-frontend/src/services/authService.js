import api from './api'

/**
 * Authentication service following Single Responsibility Principle
 * Handles all authentication-related API calls
 */
class AuthService {
  async login(username, password) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await api.post('/api/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  }

  async register(userData) {
    const response = await api.post('/api/auth/register', userData)
    return response.data
  }

  async getCurrentUser() {
    const response = await api.get('/api/auth/me')
    return response.data
  }

  logout() {
    localStorage.removeItem('token')
  }

  saveToken(token) {
    localStorage.setItem('token', token)
  }

  getToken() {
    return localStorage.getItem('token')
  }

  isAuthenticated() {
    return !!this.getToken()
  }
}

export default new AuthService()
