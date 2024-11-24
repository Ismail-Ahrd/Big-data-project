const BASE_URL = 'https://fakestoreapi.com/products';

// Fetch all products
async function fetchProducts() {
    const response = await fetch(BASE_URL);
    return response.json();
}

// Fetch product by ID
async function fetchProductById(id) {
    const response = await fetch(`${BASE_URL}/${id}`);
    return response.json();
}
