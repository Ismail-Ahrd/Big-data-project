document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname;
    if (currentPage.includes('/products.html')) {
        renderProducts();
    } else if (currentPage.includes('/product-details.html')) {
        renderProductDetails();
    }
});

async function renderProducts() {
    const productList = document.getElementById('product-list');
    const products = await fetchProducts();

    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.innerHTML = `
            <img src="${product.image}" alt="${product.title}">
            <h3>${product.title}</h3>
            <p>Price: $${product.price}</p>
            <div>
                <button class="view-details-btn" data-id="${product.id}" data-title="${product.title}" data-price="${product.price}">View Details</button>
                <button class="buy-now-btn" data-id="${product.id}" data-title="${product.title}" data-price="${product.price}">Buy Now</button>
            </div>
        `;
        productList.appendChild(productCard);
    });

    document.querySelectorAll('.view-details-btn').forEach((button) => {
        button.addEventListener('click', (event) => {
            const productId = event.target.dataset.id;
            const productTitle = event.target.dataset.title;
            const productPrice = event.target.dataset.price;
            sendEvent(productTitle, productPrice, 'ENTER_PRODUCT_DETAILS');
            window.location.href = `product-details.html?id=${productId}`;
        });
    });

    document.querySelectorAll('.buy-now-btn').forEach((button) => {
        button.addEventListener('click', async (event) => {
            const productId = event.target.dataset.id;
            const productTitle = event.target.dataset.title;
            const productPrice = event.target.dataset.price;

            // Log the purchase event
            sendEvent(productTitle, productPrice, 'BUY');
        });
    });
}

function viewProduct(productId) {
    window.location.href = `product-details.html?id=${productId}`;
}

async function renderProductDetails() {
    const queryParams = new URLSearchParams(window.location.search);
    const productId = queryParams.get('id');
    const product = await fetchProductById(productId);

    const detailsContainer = document.getElementById('product-details');
    detailsContainer.innerHTML = `
        <img src="${product.image}" alt="${product.title}" width="250px">
        <h2>${product.title}</h2>
        <p>${product.description}</p>
        <p>Price: $${product.price}</p>
        <button onclick="sendEvent('${product.title}', ${product.price}, 'BUY')">Buy</button>
    `;
}

function sendEvent(product, price, action) {
    const payload = {
        timestamp: Date.now(),
        action: action,
        product,
        quantity: 1,
        price,
        route: window.location.pathname,
        agent: navigator.userAgent
    };

    fetch('http://localhost:3000/api/event-log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(() => {})
        .catch(err => console.error('Error logging purchase:', err));
}