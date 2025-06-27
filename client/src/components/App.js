import React, { useState } from "react";
import Header from "./header";
import Footer from "./footer";
import "./app.css";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ProductsPage from "../pages/ProductsPage";
import AddProductPage from "../pages/AddProductPage"; // ✅ added this
import SignUpPage from "../pages/SignUpPage";
import HomePage from "../pages/HomePage";
import LoginPage from "../pages/LoginPage";
import Cart from "../components/Cart";

function App() {
  const [cart, setCart] = useState([]);

  const handleAddToCart = (product) => {
    setCart(prevCart => {
      const found = prevCart.find(item => item.id === product.id);
      if (found) {
        return prevCart.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prevCart, { ...product, quantity: 1 }];
    });
  };

  const handleRemoveFromCart = (id) => {
    setCart(prevCart => prevCart.filter(item => item.id !== id));
  };

  const handleCheckout = () => {
    alert("Checkout not implemented yet!");
  };

  const handleClearCart = () => setCart([]);

  return (
    <Router>
      <div className="flex-container">
        <div className="column left-column">
          <Header />
          <nav id="nav">
            <Link to="/"><button className="home-button">Home</button></Link>
            <Link to="/products"><button className="products-button">View Products</button></Link>
            <Link to="/sign-up"><button className="sign-up">Sign up</button></Link>
            <Link to="/login"><button className="login">Login</button></Link>
          </nav>
        </div>
        <div className="column right-column">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/products" element={<ProductsPage onAddToCart={handleAddToCart} />} />
            <Route path="/add-product" element={<AddProductPage />} /> {/* ✅ added route */}
            <Route path="/sign-up" element={<SignUpPage />} />
            <Route path="/login" element={<LoginPage />} />
          </Routes>

          <Cart
            cartItems={cart}
            onRemove={handleRemoveFromCart}
            onCheckout={handleCheckout}
            onClear={handleClearCart}
          />
        </div>
      </div>
    </Router>
  );
}

export default App;
