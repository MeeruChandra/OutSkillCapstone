import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useCart } from '../context/CartContext'
import './Header.css'

const Header = () => {
  const { user, logout } = useAuth()
  const { cart } = useCart()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="header">
      <div className="header-container">
        <Link to="/products" className="logo">
          Swag Labs
        </Link>

        <nav className="nav">
          <Link to="/products" className="nav-link">
            Products
          </Link>
          <Link to="/orders" className="nav-link">
            Orders
          </Link>
          <Link to="/cart" className="nav-link cart-link">
            Cart
            {cart.total_items > 0 && (
              <span className="cart-badge">{cart.total_items}</span>
            )}
          </Link>
        </nav>

        <div className="user-section">
          <span className="username">{user?.username}</span>
          <button onClick={handleLogout} className="btn btn-secondary">
            Logout
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
