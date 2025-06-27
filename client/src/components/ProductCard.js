import "./app.css"
const ProductCard = ({ product, onAddToCart }) => {
  const image = product.image || "https://via.placeholder.com/160x160?text=No+Image";
  const description = product.description || "No description available.";

  return (
    <div className="product-card">
      <img
        src={image}
        alt={product.name}
        className="product-card-image"
      />
      <h2 className="product-card-title">{product.name}</h2>
      <p className="product-card-desc">{description}</p>
      <p className="product-card-price">
        {typeof product.price === "number"
          ? `$${product.price.toFixed(2)}`
          : "Price not available"}
      </p>
      <button className="add-to-cart-btn" onClick={() => onAddToCart(product)}>
        Add to Cart
      </button>
    </div>
  );
};

export default ProductCard;