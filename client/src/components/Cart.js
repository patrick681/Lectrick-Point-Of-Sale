// src/components/Cart.js

import React from "react";
import "./app.css";

const Cart = ({ cartItems, onRemove, onCheckout, onClear }) => {
  const total = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  return (
    <div className="cart-floating">
      <h3>Cart</h3>
      {cartItems.length === 0 ? (
        <p>No items in cart.</p>
      ) : (
        <>
          <ul>
            {cartItems.map(item => (
              <li key={item.id} className="cart-item">
                <span>
                  {item.name} x{item.quantity}
                </span>
                <span>
                  ${item.price.toFixed(2)}
                  <button onClick={() => onRemove(item.id)}>Remove</button>
                </span>
              </li>
            ))}
          </ul>
          <button className="clear-cart-btn" onClick={onClear}>
            Clear Cart
          </button>
        </>
      )}
      <div className="cart-total">Total: ${total.toFixed(2)}</div>
      <button
        className="checkout-btn"
        onClick={onCheckout}
        disabled={cartItems.length === 0}
      >
        Checkout
      </button>
    </div>
  );
};

export default Cart;