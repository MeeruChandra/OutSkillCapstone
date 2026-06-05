/**
 * Get the full URL for a product image
 * @param {string} imageFilename - The image filename from the product data
 * @returns {string} Full URL to fetch the image from the API
 */
export const getImageUrl = (imageFilename) => {
  if (!imageFilename) {
    return '/placeholder-image.jpg' // Fallback for missing images
  }
  return `http://localhost:8000/api/products/images/${imageFilename}`
}
