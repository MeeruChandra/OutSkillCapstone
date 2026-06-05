import { useState, useEffect } from 'react'
import Header from '../components/Header'
import orderService from '../services/orderService'
import { getImageUrl } from '../utils/imageUtils'
import './Orders.css'

const Orders = () => {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [expandedOrder, setExpandedOrder] = useState(null)

  useEffect(() => {
    fetchOrders()
  }, [])

  const fetchOrders = async () => {
    try {
      setLoading(true)
      const data = await orderService.getOrders()
      setOrders(data)
    } catch (err) {
      setError('Failed to load orders')
    } finally {
      setLoading(false)
    }
  }

  const toggleOrder = (orderId) => {
    setExpandedOrder(expandedOrder === orderId ? null : orderId)
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div>
      <Header />
      <div className="orders-page">
        <h1>My Orders</h1>

        {error && <div className="error-message">{error}</div>}

        {loading ? (
          <div className="loading">Loading orders...</div>
        ) : orders.length === 0 ? (
          <div className="no-orders">
            <p>You haven't placed any orders yet.</p>
          </div>
        ) : (
          <div className="orders-list">
            {orders.map((order) => (
              <div key={order.id} className="order-card">
                <div className="order-header" onClick={() => toggleOrder(order.id)}>
                  <div className="order-header-info">
                    <h3>Order #{order.id}</h3>
                    <p className="order-date">{formatDate(order.created_at)}</p>
                  </div>

                  <div className="order-header-details">
                    <span className={`order-status status-${order.status}`}>
                      {order.status}
                    </span>
                    <span className="order-total">${order.total_amount.toFixed(2)}</span>
                    <button className="toggle-btn">
                      {expandedOrder === order.id ? '−' : '+'}
                    </button>
                  </div>
                </div>

                {expandedOrder === order.id && (
                  <div className="order-details">
                    <div className="order-section">
                      <h4>Shipping Address</h4>
                      <p>{order.shipping_address}</p>
                    </div>

                    <div className="order-section">
                      <h4>Payment Method</h4>
                      <p className="payment-method">{order.payment_method.replace('_', ' ')}</p>
                    </div>

                    <div className="order-section">
                      <h4>Order Items</h4>
                      <div className="order-items">
                        {order.order_items.map((item) => (
                          <div key={item.id} className="order-item">
                            <img
                              src={getImageUrl(item.product.image_url)}
                              alt={item.product.name}
                              className="order-item-image"
                            />
                            <div className="order-item-info">
                              <h5>{item.product.name}</h5>
                              <p>
                                ${item.price_at_purchase.toFixed(2)} x {item.quantity}
                              </p>
                            </div>
                            <div className="order-item-total">
                              ${(item.price_at_purchase * item.quantity).toFixed(2)}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Orders
