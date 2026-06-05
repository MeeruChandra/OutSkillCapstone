import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import { useCart } from '../context/CartContext'
import productService from '../services/productService'
import { getImageUrl } from '../utils/imageUtils'
import './ProductDetail.css'

const ProductDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { addToCart } = useCart()
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [quantity, setQuantity] = useState(1)

  useEffect(() => {
    fetchProduct()
  }, [id])

  const fetchProduct = async () => {
    try {
      setLoading(true)
      const data = await productService.getProductById(id)
      setProduct(data)
    } catch (err) {
      setError('Failed to load product')
    } finally {
      setLoading(false)
    }
  }

  const handleAddToCart = async () => {
    try {
      await addToCart(product.id, quantity)
      navigate('/cart')
    } catch (error) {
      setError('Failed to add to cart')
    }
  }

  if (loading) return <div className="loading">Loading...</div>
  if (error) return <div className="error-message">{error}</div>
  if (!product) return <div>Product not found</div>

  return (
    <div>
      <Header />
      <div className="product-detail-page">
        <button onClick={() => navigate('/products')} className="back-btn">
          ← Back to Products
        </button>

        <div className="product-detail">
          <div className="product-detail-image">
            <img src={getImageUrl(product.image_url)} alt={product.name} />
          </div>

          <div className="product-detail-info">
            <h1>{product.name}</h1>
            <p className="product-detail-description">{product.description}</p>

            <div className="product-detail-price">${product.price.toFixed(2)}</div>

            <div className="product-detail-category">
              Category: <span>{product.category}</span>
            </div>

            <div className="product-detail-stock">
              {product.inventory_count > 0 ? (
                <span className="in-stock">In Stock ({product.inventory_count} available)</span>
              ) : (
                <span className="out-of-stock">Out of Stock</span>
              )}
            </div>

            <div className="product-detail-actions">
              <div className="quantity-selector">
                <label>Quantity:</label>
                <input
                  type="number"
                  min="1"
                  max={product.inventory_count}
                  value={quantity}
                  onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
                  className="quantity-input"
                />
              </div>

              <button
                onClick={handleAddToCart}
                disabled={product.inventory_count === 0}
                className="btn btn-primary add-to-cart-btn-large"
              >
                Add to Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProductDetail
