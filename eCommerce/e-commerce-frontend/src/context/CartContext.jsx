import { createContext, useState, useContext, useEffect } from 'react'
import cartService from '../services/cartService'
import { useAuth } from './AuthContext'

const CartContext = createContext(null)

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState({ items: [], total_items: 0, total_amount: 0 })
  const [loading, setLoading] = useState(false)
  const { isAuthenticated } = useAuth()

  useEffect(() => {
    if (isAuthenticated) {
      fetchCart()
    }
  }, [isAuthenticated])

  const fetchCart = async () => {
    try {
      setLoading(true)
      const data = await cartService.getCart()
      setCart(data)
    } catch (error) {
      console.error('Failed to fetch cart:', error)
    } finally {
      setLoading(false)
    }
  }

  const addToCart = async (productId, quantity = 1) => {
    try {
      await cartService.addToCart(productId, quantity)
      await fetchCart()
    } catch (error) {
      console.error('Failed to add to cart:', error)
      throw error
    }
  }

  const updateCartItem = async (cartItemId, quantity) => {
    try {
      await cartService.updateCartItem(cartItemId, quantity)
      await fetchCart()
    } catch (error) {
      console.error('Failed to update cart item:', error)
      throw error
    }
  }

  const removeFromCart = async (cartItemId) => {
    try {
      await cartService.removeFromCart(cartItemId)
      await fetchCart()
    } catch (error) {
      console.error('Failed to remove from cart:', error)
      throw error
    }
  }

  const clearCart = async () => {
    try {
      await cartService.clearCart()
      setCart({ items: [], total_items: 0, total_amount: 0 })
    } catch (error) {
      console.error('Failed to clear cart:', error)
      throw error
    }
  }

  const value = {
    cart,
    loading,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart,
    fetchCart
  }

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

export const useCart = () => {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}
