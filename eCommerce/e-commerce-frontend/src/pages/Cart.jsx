import { useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import { useCart } from '../context/CartContext'
import { getImageUrl } from '../utils/imageUtils'
import './Cart.css'

const Cart = () => {
  const navigate = useNavigate()
  const { cart, updateCartItem, removeFromCart } = useCart()

  const handleQuantityChange = async (cartItemId, newQuantity) => {
    if (newQuantity < 1) return
    try {
      await updateCartItem(cartItemId, newQuantity)
    } catch (error) {
      console.error('Failed to update quantity:', error)
    }
  }

  const handleRemove = async (cartItemId) => {
    try {
      await removeFromCart(cartItemId)
    } catch (error) {
      console.error('Failed to remove item:', error)
    }
  }

  const handleCheckout = () => {
    if (cart.items.length > 0) {
      navigate('/checkout')
    }
  }

  return (
    <div>
      <Header />
      <div className="cart-page">
        <h1>Shopping Cart</h1>

        {cart.items.length === 0 ? (
          <div className="empty-cart">
            <p>Your cart is empty</p>
            <button onClick={() => navigate('/products')} className="btn btn-primary">
              Continue Shopping
            </button>
          </div>
        ) : (
          <div className="cart-content">
            <div className="cart-items">
              {cart.items.map((item) => (
                <div key={item.id} className="cart-item">
                  <img
                    src={getImageUrl(item.product.image_url)}
                    alt={item.product.name}
                    className="cart-item-image"
                  />

                  <div className="cart-item-info">
                    <h3>{item.product.name}</h3>
                    <p className="cart-item-price">${item.product.price.toFixed(2)}</p>
                  </div>

                  <div className="cart-item-actions">
                    <div className="quantity-controls">
                      <button
                        onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                        className="quantity-btn"
                        disabled={item.quantity <= 1}
                      >
                        -
                      </button>
                      <span className="quantity-value">{item.quantity}</span>
                      <button
                        onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                        className="quantity-btn"
                      >
                        +
                      </button>
                    </div>

                    <div className="cart-item-total">
                      ${(item.product.price * item.quantity).toFixed(2)}
                    </div>

                    <button
                      onClick={() => handleRemove(item.id)}
                      className="btn btn-danger remove-btn"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="cart-summary">
              <h2>Order Summary</h2>

              <div className="summary-row">
                <span>Items ({cart.total_items}):</span>
                <span>${cart.total_amount.toFixed(2)}</span>
              </div>

              <div className="summary-row summary-total">
                <span>Total:</span>
                <span>${cart.total_amount.toFixed(2)}</span>
              </div>

              <button onClick={handleCheckout} className="btn btn-primary checkout-btn">
                Proceed to Checkout
              </button>

              <button
                onClick={() => navigate('/products')}
                className="btn btn-secondary continue-btn"
              >
                Continue Shopping
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Cart
