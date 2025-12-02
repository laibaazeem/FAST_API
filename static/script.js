const API_BASE_URL = "http://127.0.0.1:8000";

// Store logged-in user data
let currentUser = null;
let authToken = null;

// Load user from localStorage on page load
document.addEventListener('DOMContentLoaded', function() {
    const savedUser = localStorage.getItem('currentUser');
    const savedToken = localStorage.getItem('authToken');
    
    if (savedUser && savedToken) {
        currentUser = JSON.parse(savedUser);
        authToken = savedToken;
        updateAuthButtons();
    }
    
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchProducts();
            }
        });
    }
});

// Update auth buttons based on login status
function updateAuthButtons() {
    const authButtons = document.querySelector('.auth-buttons');
    if (!authButtons) return;
    
    if (currentUser && authToken) {
        authButtons.innerHTML = `
            <span style="color: white; margin-right: 1rem;">Welcome, ${currentUser.email}</span>
            <button class="btn register-btn" onclick="logout()">Logout</button>
        `;
    }
}

// Logout function
function logout() {
    currentUser = null;
    authToken = null;
    localStorage.removeItem('currentUser');
    localStorage.removeItem('authToken');
    window.location.href = '/';
}

// ===== REGISTER FUNCTION =====
async function handleRegister(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password,
                role: "user"
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || 'Registration failed');
            return;
        }

        alert('Account created successfully! Please login.');
        window.location.href = '/login';
        
    } catch (error) {
        console.error('Registration error:', error);
        alert('Error during registration');
    }
}

// ===== LOGIN FUNCTION =====
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || 'Login failed');
            return;
        }

        // Store token and user info
        authToken = data.access_token;
        localStorage.setItem('authToken', authToken);
        
        // Store user info from response
        currentUser = { 
            email: data.email || email, 
            id: data.user_id 
        };
        localStorage.setItem('currentUser', JSON.stringify(currentUser));

        alert('Login successful!');
        window.location.href = '/';
        
    } catch (error) {
        console.error('Login error:', error);
        alert('Error during login');
    }
}

// Fetch all products from backend
async function fetchProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products/`);
        if (!response.ok) throw new Error('Failed to fetch products');
        const products = await response.json();
        return products;
    } catch (error) {
        console.error('Error fetching products:', error);
        return [];
    }
}

// Display products
async function displayProducts(productsToShow = null) {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;
    
    grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">Loading products...</p>';
    
    let products = productsToShow;
    if (!products) {
        products = await fetchProducts();
    }
    
    grid.innerHTML = '';
    
    if (products.length === 0) {
        grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; font-size: 1.2rem; color: #7f8c8d;">No products found</p>';
        return;
    }
    
    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <div class="product-image">📦</div>
            <div class="product-name">${product.name}</div>
            <div class="product-description" style="color: #7f8c8d; font-size: 0.9rem; margin-bottom: 0.5rem;">${product.description || 'No description'}</div>
            <div class="product-price">₨ ${product.price.toLocaleString()}</div>
            <div style="color: ${product.stock_status === 'Available' ? '#27ae60' : '#e74c3c'}; font-size: 0.9rem; margin-bottom: 0.5rem;">
                ${product.stock_status}
            </div>
            <button class="add-to-cart" onclick="addToCart(${product.id}, '${product.name}', ${product.price})">Add to Cart</button>
        `;
        grid.appendChild(card);
    });
}

// Add to cart function
async function addToCart(productId, productName, productPrice) {
    if (!currentUser || !authToken) {
        alert('Please login first to add items to cart!');
        window.location.href = '/login';
        return;
    }

    const payload = {
        user_id: currentUser.id,
        products: [
            {
                product_id: productId,
                quantity: 1
            }
        ]
    };

    try {
        const response = await fetch(`${API_BASE_URL}/cart/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${authToken}`
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Failed to add to cart");
            return;
        }

        alert(`${productName} added to cart!`);
        
    } catch (error) {
        console.error("Cart error:", error);
        alert("Error adding to cart");
    }
}

// Search products from navigation bar
function searchProducts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    if (searchTerm.trim() === '') {
        alert('Please enter a search term');
        return;
    }
    window.location.href = `/search?q=${encodeURIComponent(searchTerm)}`;
}

// Change page function
function changePage(page) {
    const buttons = document.querySelectorAll('.page-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    if (typeof page === 'number') {
        buttons[page].classList.add('active');
        alert(`Loading page ${page}...`);
    } else if (page === 'prev') {
        alert('Loading previous page...');
    } else if (page === 'next') {
        alert('Loading next page...');
    }
}

// Fetch all categories from backend
async function fetchCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories/`);
        if (!response.ok) throw new Error('Failed to fetch categories');
        const categories = await response.json();
        return categories;
    } catch (error) {
        console.error('Error fetching categories:', error);
        return [];
    }
}

// Filter by category
async function filterByCategory(categoryName) {
    const allProducts = await fetchProducts();
    const filtered = allProducts.filter(p => p.category.name === categoryName);
    displayProducts(filtered);
}