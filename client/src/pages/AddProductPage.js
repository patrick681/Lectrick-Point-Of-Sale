import React, { useState } from 'react';

function AddProductPage() {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [stock, setStock] = useState('');
  const [message, setMessage] = useState('');
  const [image, setImage] = useState("");
  const [description, setDescription] = useState("");


  const handleSubmit = async (e) => {
    e.preventDefault();

    const product = {
      name,
      price: parseFloat(price),
      stock: parseInt(stock)
    };

    try {
      const response = await fetch('http://localhost:5555/products', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(product)
      });

      if (response.ok) {
        setMessage('✅ Product added successfully!');
        setName('');
        setPrice('');
        setStock('');
      } else {
        setMessage('❌ Failed to add product.');
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('⚠️ Server error');
    }
  };

  return (
    <div className="add-product-page">
    <form className="add-product-form" onSubmit={handleSubmit}>
      <h2>Add New Product</h2>
      <input
        type="text"
        placeholder="Product Name"
        value={name}
        onChange={e => setName(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Price"
        value={price}
        onChange={e => setPrice(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Stock"
        value={stock}
        onChange={e => setStock(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Image URL (optional)"
        value={image}
        onChange={e => setImage(e.target.value)}
      />
      <textarea
        placeholder="Description (optional)"
        value={description}
        onChange={e => setDescription(e.target.value)}
      />
      <button className="add-product-submit" type="submit">
        Add Product
      </button>
    </form>
  </div>
  );
}

export default AddProductPage;
