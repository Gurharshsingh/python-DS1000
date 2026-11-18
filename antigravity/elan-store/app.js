/* ============================================
   ÉLAN — Application Logic
   Cart · Auth · Products · Checkout
   ============================================ */

// ──── Product Data ────
const PRODUCTS = [
  {
    id: 1,
    name: 'Aria White Sneakers',
    category: 'shoes',
    subcategory: 'Sneakers',
    price: 129,
    originalPrice: null,
    image: 'images/shoe-white-sneakers.jpg',
    badge: null,
    sizes: ['38','39','40','41','42','43','44'],
    description: 'Crafted from premium full-grain leather, the Aria sneakers combine timeless design with everyday comfort. A clean silhouette with hand-stitched detailing and a cushioned insole make these your go-to pair for any occasion.',
    details: ['Full-grain Italian leather upper', 'Cushioned memory foam insole', 'Rubber outsole for traction', 'Handcrafted in Portugal']
  },
  {
    id: 2,
    name: 'Cognac Chelsea Boots',
    category: 'shoes',
    subcategory: 'Boots',
    price: 189,
    originalPrice: 229,
    image: 'images/shoe-chelsea-boots.jpg',
    badge: 'Sale',
    sizes: ['39','40','41','42','43','44'],
    description: 'The quintessential Chelsea boot reimagined. Rich cognac leather develops a beautiful patina over time, while the elastic side panels ensure an effortless on-and-off experience.',
    details: ['Hand-burnished leather upper', 'Goodyear welted construction', 'Leather lining & insole', 'Commando rubber sole']
  },
  {
    id: 3,
    name: 'Shadow Runner Trainers',
    category: 'shoes',
    subcategory: 'Athletic',
    price: 149,
    originalPrice: null,
    image: 'images/shoe-running.jpg',
    badge: 'New',
    sizes: ['38','39','40','41','42','43','44','45'],
    description: 'Engineered for performance and styled for the street. The Shadow Runner features a lightweight knit upper with responsive cushioning technology that adapts to your stride.',
    details: ['Breathable engineered mesh', 'Responsive foam midsole', 'Reflective accents', 'Weight: 245g per shoe']
  },
  {
    id: 4,
    name: 'Dune Suede Loafers',
    category: 'shoes',
    subcategory: 'Loafers',
    price: 159,
    originalPrice: null,
    image: 'images/shoe-loafers.jpg',
    badge: null,
    sizes: ['39','40','41','42','43','44'],
    description: 'Luxurious suede penny loafers that transition seamlessly from office to evening. The unlined construction keeps them light, while the leather sole provides elegant comfort.',
    details: ['Premium Italian suede', 'Blake stitched construction', 'Unlined for flexibility', 'Leather sole with rubber heel']
  },
  {
    id: 5,
    name: 'Natural Linen Shirt',
    category: 'clothing',
    subcategory: 'Shirts',
    price: 89,
    originalPrice: null,
    image: 'images/clothing-linen-shirt.jpg',
    badge: null,
    sizes: ['XS','S','M','L','XL'],
    description: 'A warm-weather essential in pure European linen. The relaxed fit and natural texture bring effortless sophistication to your summer wardrobe.',
    details: ['100% European flax linen', 'Relaxed regular fit', 'Mother-of-pearl buttons', 'Pre-washed for softness']
  },
  {
    id: 6,
    name: 'Heritage Navy Blazer',
    category: 'clothing',
    subcategory: 'Outerwear',
    price: 245,
    originalPrice: 289,
    image: 'images/clothing-navy-blazer.jpg',
    badge: 'Sale',
    sizes: ['S','M','L','XL'],
    description: 'A tailored navy blazer that anchors any wardrobe. Cut from fine merino wool with a half-canvas construction for a clean drape and structured silhouette.',
    details: ['Super 120s merino wool', 'Half-canvas construction', 'Gold-tone buttons', 'Fully lined in silk']
  },
  {
    id: 7,
    name: 'Cashmere Crew Sweater',
    category: 'clothing',
    subcategory: 'Knitwear',
    price: 195,
    originalPrice: null,
    image: 'images/clothing-wool-sweater.jpg',
    badge: 'New',
    sizes: ['XS','S','M','L','XL','XXL'],
    description: 'Pure Mongolian cashmere knitted into a perfectly weighted crew neck. The heather gray tone is endlessly versatile, pairing with everything from denim to tailoring.',
    details: ['100% Grade-A Mongolian cashmere', '12-gauge knit', 'Ribbed cuffs and hem', 'Whipstitch detailing']
  },
  {
    id: 8,
    name: 'Olive Stretch Chinos',
    category: 'clothing',
    subcategory: 'Trousers',
    price: 95,
    originalPrice: null,
    image: 'images/clothing-olive-chinos.jpg',
    badge: null,
    sizes: ['28','30','32','34','36'],
    description: 'Our signature chinos in a rich olive hue. A touch of stretch ensures all-day comfort, while the slim-tapered silhouette keeps things sharp.',
    details: ['98% cotton, 2% elastane', 'Slim tapered fit', 'YKK zip fly', 'Garment washed']
  },
  {
    id: 9,
    name: 'Essential Cotton Tee',
    category: 'clothing',
    subcategory: 'T-Shirts',
    price: 45,
    originalPrice: null,
    image: 'images/clothing-white-tee.jpg',
    badge: null,
    sizes: ['XS','S','M','L','XL','XXL'],
    description: 'The foundation of every great outfit. Heavyweight Supima cotton with a relaxed fit that drapes perfectly. A t-shirt worth building a wardrobe around.',
    details: ['220gsm Supima cotton', 'Relaxed fit', 'Reinforced collar', 'Side-seam construction']
  },
  {
    id: 10,
    name: 'Vintage Denim Jacket',
    category: 'clothing',
    subcategory: 'Outerwear',
    price: 165,
    originalPrice: null,
    image: 'images/clothing-linen-shirt.jpg',
    badge: 'New',
    sizes: ['XS','S','M','L','XL'],
    description: 'A modern take on the classic trucker jacket. Crafted from Japanese selvedge denim with a medium vintage wash that tells a story from day one.',
    details: ['14oz Japanese selvedge denim', 'Classic trucker fit', 'Copper rivets & buttons', 'Two chest pockets']
  }
];

// ──── State Management ────
const Store = {
  _cart: JSON.parse(localStorage.getItem('elan_cart') || '[]'),
  _user: JSON.parse(localStorage.getItem('elan_user') || 'null'),
  _listeners: [],

  get cart() { return this._cart; },
  get user() { return this._user; },

  subscribe(fn) { this._listeners.push(fn); },
  _notify() {
    this._listeners.forEach(fn => fn());
    this._saveCart();
  },

  _saveCart() {
    localStorage.setItem('elan_cart', JSON.stringify(this._cart));
  },

  addToCart(productId, size, qty = 1) {
    const existing = this._cart.find(i => i.productId === productId && i.size === size);
    if (existing) {
      existing.qty += qty;
    } else {
      this._cart.push({ productId, size, qty });
    }
    this._notify();
    showToast('Added to cart');
  },

  removeFromCart(productId, size) {
    this._cart = this._cart.filter(i => !(i.productId === productId && i.size === size));
    this._notify();
  },

  updateQty(productId, size, qty) {
    const item = this._cart.find(i => i.productId === productId && i.size === size);
    if (item) {
      item.qty = Math.max(1, qty);
      this._notify();
    }
  },

  clearCart() {
    this._cart = [];
    this._notify();
  },

  get cartCount() {
    return this._cart.reduce((sum, i) => sum + i.qty, 0);
  },

  get cartTotal() {
    return this._cart.reduce((sum, i) => {
      const product = PRODUCTS.find(p => p.id === i.productId);
      return sum + (product ? product.price * i.qty : 0);
    }, 0);
  },

  login(email, name) {
    this._user = { email, name };
    localStorage.setItem('elan_user', JSON.stringify(this._user));
    this._notify();
  },

  logout() {
    this._user = null;
    localStorage.removeItem('elan_user');
    this._notify();
  }
};

// ──── Toast Notifications ────
function showToast(message) {
  const container = document.querySelector('.toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
    ${message}
  `;
  container.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.add('show');
  });

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 400);
  }, 2800);
}

// ──── Header Logic ────
function initHeader() {
  const header = document.querySelector('.site-header');
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('.nav-links');

  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 10);
    }, { passive: true });
  }

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      navLinks.classList.toggle('mobile-open');
    });
  }

  updateCartBadge();
  updateAuthNav();
}

function updateCartBadge() {
  const badges = document.querySelectorAll('.cart-badge');
  const count = Store.cartCount;
  badges.forEach(badge => {
    badge.textContent = count;
    badge.classList.toggle('visible', count > 0);
  });
}

function updateAuthNav() {
  const authLinks = document.querySelectorAll('[data-auth-link]');
  authLinks.forEach(link => {
    if (Store.user) {
      link.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
      `;
      link.title = Store.user.name;
    }
  });
}

// ──── Scroll Reveal ────
function initScrollReveal() {
  const reveals = document.querySelectorAll('.reveal');
  if (!reveals.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  reveals.forEach(el => observer.observe(el));
}

// ──── Product Card Renderer ────
function renderProductCard(product) {
  return `
    <div class="product-card" data-product-id="${product.id}" onclick="goToProduct(${product.id})">
      <div class="product-card-image">
        <img src="${product.image}" alt="${product.name}" loading="lazy">
        ${product.badge ? `<span class="product-badge">${product.badge}</span>` : ''}
        <div class="product-card-actions">
          <button onclick="event.stopPropagation(); quickAdd(${product.id})" title="Add to cart">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
              <line x1="3" y1="6" x2="21" y2="6"></line>
              <path d="M16 10a4 4 0 0 1-8 0"></path>
            </svg>
          </button>
          <button onclick="event.stopPropagation(); goToProduct(${product.id})" title="View details">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="M21 21l-4.35-4.35"></path>
            </svg>
          </button>
        </div>
      </div>
      <div class="product-card-info">
        <span class="product-category">${product.subcategory}</span>
        <h4>${product.name}</h4>
        <span class="product-price">
          $${product.price}
          ${product.originalPrice ? `<span class="original-price">$${product.originalPrice}</span>` : ''}
        </span>
      </div>
    </div>
  `;
}

function quickAdd(productId) {
  const product = PRODUCTS.find(p => p.id === productId);
  if (product) {
    Store.addToCart(productId, product.sizes[Math.floor(product.sizes.length / 2)]);
  }
}

function goToProduct(productId) {
  window.location.href = `product.html?id=${productId}`;
}

// ──── Home Page Init ────
function initHomePage() {
  // Featured products
  const featuredGrid = document.getElementById('featured-products');
  if (featuredGrid) {
    const featured = PRODUCTS.filter(p => p.badge === 'New' || p.badge === 'Sale').slice(0, 4);
    if (featured.length < 4) {
      const remaining = PRODUCTS.filter(p => !featured.includes(p)).slice(0, 4 - featured.length);
      featured.push(...remaining);
    }
    featuredGrid.innerHTML = featured.map(renderProductCard).join('');
  }

  // Best sellers
  const bestGrid = document.getElementById('best-sellers');
  if (bestGrid) {
    const best = PRODUCTS.slice(0, 4);
    bestGrid.innerHTML = best.map(renderProductCard).join('');
  }
}

// ──── Shop Page Init ────
function initShopPage() {
  const grid = document.getElementById('shop-products');
  const filterBtns = document.querySelectorAll('.filter-btn');
  const sortSelect = document.querySelector('.sort-select');
  const resultCount = document.getElementById('result-count');

  let currentFilter = 'all';
  let currentSort = 'featured';

  function render() {
    let filtered = currentFilter === 'all'
      ? [...PRODUCTS]
      : PRODUCTS.filter(p => p.category === currentFilter);

    switch (currentSort) {
      case 'price-low':  filtered.sort((a, b) => a.price - b.price); break;
      case 'price-high': filtered.sort((a, b) => b.price - a.price); break;
      case 'name':       filtered.sort((a, b) => a.name.localeCompare(b.name)); break;
      default: break; // featured = default order
    }

    if (grid) grid.innerHTML = filtered.map(renderProductCard).join('');
    if (resultCount) resultCount.textContent = `${filtered.length} products`;
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.filter;
      render();
    });
  });

  if (sortSelect) {
    sortSelect.addEventListener('change', () => {
      currentSort = sortSelect.value;
      render();
    });
  }

  render();
}

// ──── Product Detail Page ────
function initProductPage() {
  const params = new URLSearchParams(window.location.search);
  const productId = parseInt(params.get('id'));
  const product = PRODUCTS.find(p => p.id === productId);

  if (!product) {
    document.querySelector('.container').innerHTML = `
      <div class="cart-empty">
        <h2>Product not found</h2>
        <p>The product you're looking for doesn't exist.</p>
        <a href="shop.html" class="btn btn-primary">Browse Shop</a>
      </div>
    `;
    return;
  }

  // Fill in product data
  document.title = `${product.name} — ÉLAN`;
  document.getElementById('product-name').textContent = product.name;
  document.getElementById('product-category-crumb').textContent = product.subcategory;
  document.getElementById('product-price').innerHTML = `$${product.price}${product.originalPrice ? ` <span class="original-price" style="font-weight:400;color:var(--color-text-light);text-decoration:line-through;margin-left:8px;font-size:var(--text-sm);">$${product.originalPrice}</span>` : ''}`;
  document.getElementById('product-description').textContent = product.description;

  const mainImg = document.getElementById('main-product-image');
  mainImg.src = product.image;
  mainImg.alt = product.name;

  // Sizes
  const sizeContainer = document.getElementById('size-options');
  let selectedSize = null;
  sizeContainer.innerHTML = product.sizes.map(s => `<button data-size="${s}">${s}</button>`).join('');
  sizeContainer.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
      sizeContainer.querySelectorAll('button').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      selectedSize = btn.dataset.size;
    });
  });

  // Quantity
  let qty = 1;
  const qtyDisplay = document.getElementById('qty-value');
  document.getElementById('qty-minus').addEventListener('click', () => {
    qty = Math.max(1, qty - 1);
    qtyDisplay.textContent = qty;
  });
  document.getElementById('qty-plus').addEventListener('click', () => {
    qty++;
    qtyDisplay.textContent = qty;
  });

  // Add to cart
  document.getElementById('add-to-cart-btn').addEventListener('click', () => {
    if (!selectedSize) {
      showToast('Please select a size');
      return;
    }
    Store.addToCart(product.id, selectedSize, qty);
  });

  // Details list
  const detailsList = document.getElementById('product-details-list');
  if (detailsList && product.details) {
    detailsList.innerHTML = product.details.map(d => `<li style="margin-bottom:6px;font-size:var(--text-sm);color:var(--color-text-muted);">— ${d}</li>`).join('');
  }

  // Related products
  const relatedGrid = document.getElementById('related-products');
  if (relatedGrid) {
    const related = PRODUCTS.filter(p => p.id !== product.id && p.category === product.category).slice(0, 4);
    relatedGrid.innerHTML = related.map(renderProductCard).join('');
  }
}

// ──── Cart Page ────
function initCartPage() {
  renderCart();
  Store.subscribe(renderCart);
}

function renderCart() {
  const list = document.getElementById('cart-items');
  const summary = document.getElementById('cart-summary');
  const emptyState = document.getElementById('cart-empty');

  if (!list) return;

  if (Store.cart.length === 0) {
    list.style.display = 'none';
    if (summary) summary.style.display = 'none';
    if (emptyState) emptyState.style.display = 'block';
    return;
  }

  list.style.display = 'flex';
  if (summary) summary.style.display = 'block';
  if (emptyState) emptyState.style.display = 'none';

  list.innerHTML = Store.cart.map(item => {
    const product = PRODUCTS.find(p => p.id === item.productId);
    if (!product) return '';
    const itemTotal = product.price * item.qty;
    return `
      <div class="cart-item">
        <div class="cart-item-image">
          <a href="product.html?id=${product.id}"><img src="${product.image}" alt="${product.name}"></a>
        </div>
        <div class="cart-item-details">
          <h4><a href="product.html?id=${product.id}">${product.name}</a></h4>
          <div class="cart-item-meta">Size: ${item.size}</div>
          <div class="qty-control">
            <button onclick="Store.updateQty(${product.id}, '${item.size}', ${item.qty - 1})">−</button>
            <span class="qty-value">${item.qty}</span>
            <button onclick="Store.updateQty(${product.id}, '${item.size}', ${item.qty + 1})">+</button>
          </div>
        </div>
        <div class="cart-item-right">
          <span class="cart-item-price">$${itemTotal}</span>
          <button class="cart-item-remove" onclick="Store.removeFromCart(${product.id}, '${item.size}')">Remove</button>
        </div>
      </div>
    `;
  }).join('');

  // Update summary
  const subtotal = Store.cartTotal;
  const shipping = subtotal > 150 ? 0 : 12;
  const total = subtotal + shipping;

  document.getElementById('summary-subtotal').textContent = `$${subtotal}`;
  document.getElementById('summary-shipping').textContent = shipping === 0 ? 'Free' : `$${shipping}`;
  document.getElementById('summary-total').textContent = `$${total}`;
}

// ──── Auth Page ────
function initAuthPage() {
  const loginTab = document.getElementById('login-tab');
  const registerTab = document.getElementById('register-tab');
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  if (loginTab && registerTab) {
    loginTab.addEventListener('click', () => {
      loginTab.classList.add('active');
      registerTab.classList.remove('active');
      loginForm.style.display = 'block';
      registerForm.style.display = 'none';
    });

    registerTab.addEventListener('click', () => {
      registerTab.classList.add('active');
      loginTab.classList.remove('active');
      registerForm.style.display = 'block';
      loginForm.style.display = 'none';
    });
  }

  // Login form
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = loginForm.querySelector('[name="email"]').value;
      const password = loginForm.querySelector('[name="password"]').value;
      if (email && password) {
        Store.login(email, email.split('@')[0]);
        showToast('Welcome back!');
        setTimeout(() => window.location.href = 'index.html', 1200);
      }
    });
  }

  // Register form
  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = registerForm.querySelector('[name="fullname"]').value;
      const email = registerForm.querySelector('[name="email"]').value;
      const password = registerForm.querySelector('[name="password"]').value;
      if (name && email && password) {
        Store.login(email, name);
        showToast('Account created successfully!');
        setTimeout(() => window.location.href = 'index.html', 1200);
      }
    });
  }

  // If user is already logged in, show option to go to account
  if (Store.user) {
    const container = document.querySelector('.auth-form-container');
    if (container) {
      container.innerHTML = `
        <p class="section-label">Welcome back</p>
        <h1>Hello, ${Store.user.name}</h1>
        <p class="auth-subtitle">You are already signed in.</p>
        <div style="display:flex;flex-direction:column;gap:var(--space-md);">
          <a href="index.html" class="btn btn-primary btn-wide">Continue Shopping</a>
          <button class="btn btn-outline btn-wide" onclick="Store.logout(); location.reload();">Sign Out</button>
        </div>
      `;
    }
  }
}

// ──── Checkout Page ────
function initCheckoutPage() {
  // Redirect if cart is empty
  if (Store.cart.length === 0) {
    window.location.href = 'cart.html';
    return;
  }

  // Populate order summary
  const orderItems = document.getElementById('order-items');
  if (orderItems) {
    orderItems.innerHTML = Store.cart.map(item => {
      const product = PRODUCTS.find(p => p.id === item.productId);
      if (!product) return '';
      return `
        <div class="order-item">
          <div class="order-item-thumb">
            <img src="${product.image}" alt="${product.name}">
          </div>
          <div>
            <div class="order-item-name">${product.name}</div>
            <div class="order-item-qty">Size ${item.size} × ${item.qty}</div>
          </div>
          <div class="order-item-price">$${product.price * item.qty}</div>
        </div>
      `;
    }).join('');
  }

  const subtotal = Store.cartTotal;
  const shipping = subtotal > 150 ? 0 : 12;
  const tax = Math.round(subtotal * 0.08);
  const total = subtotal + shipping + tax;

  const setEl = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
  setEl('checkout-subtotal', `$${subtotal}`);
  setEl('checkout-shipping', shipping === 0 ? 'Free' : `$${shipping}`);
  setEl('checkout-tax', `$${tax}`);
  setEl('checkout-total', `$${total}`);

  // Payment method toggle
  const paymentOptions = document.querySelectorAll('.payment-option');
  const cardForm = document.querySelector('.card-form');
  paymentOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      paymentOptions.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      opt.querySelector('input[type="radio"]').checked = true;
      if (cardForm) {
        cardForm.classList.toggle('visible', opt.dataset.method === 'card');
      }
    });
  });

  // Steps
  const steps = document.querySelectorAll('.checkout-step');
  const sections = document.querySelectorAll('.checkout-section');
  let currentStep = 0;

  function updateSteps() {
    steps.forEach((step, i) => {
      step.classList.remove('active', 'completed');
      if (i < currentStep) step.classList.add('completed');
      if (i === currentStep) step.classList.add('active');
    });
  }
  updateSteps();

  // Place order
  const placeOrderBtn = document.getElementById('place-order-btn');
  if (placeOrderBtn) {
    placeOrderBtn.addEventListener('click', (e) => {
      e.preventDefault();
      placeOrderBtn.textContent = 'Processing...';
      placeOrderBtn.disabled = true;

      setTimeout(() => {
        Store.clearCart();
        showOrderConfirmation();
      }, 1800);
    });
  }

  // Card number formatting
  const cardInput = document.getElementById('card-number');
  if (cardInput) {
    cardInput.addEventListener('input', (e) => {
      let val = e.target.value.replace(/\D/g, '').substring(0, 16);
      val = val.replace(/(.{4})/g, '$1 ').trim();
      e.target.value = val;
    });
  }

  const expiryInput = document.getElementById('card-expiry');
  if (expiryInput) {
    expiryInput.addEventListener('input', (e) => {
      let val = e.target.value.replace(/\D/g, '').substring(0, 4);
      if (val.length > 2) val = val.substring(0, 2) + '/' + val.substring(2);
      e.target.value = val;
    });
  }
}

function showOrderConfirmation() {
  const overlay = document.getElementById('order-confirm-modal');
  if (overlay) {
    overlay.classList.add('active');
  } else {
    // Fallback: create modal dynamically
    const modal = document.createElement('div');
    modal.className = 'modal-overlay active';
    modal.innerHTML = `
      <div class="modal" style="text-align:center;">
        <div style="width:56px;height:56px;border-radius:50%;background:var(--color-success);color:#fff;display:flex;align-items:center;justify-content:center;margin:0 auto var(--space-lg);">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
        <h3>Order Confirmed</h3>
        <p>Thank you for your purchase! Your order has been placed and a confirmation email will be sent shortly.</p>
        <p style="font-family:var(--font-nav);font-size:var(--text-xs);color:var(--color-text-light);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:var(--space-xl);">Order #ÉL${Date.now().toString().slice(-6)}</p>
        <a href="index.html" class="btn btn-primary btn-wide">Continue Shopping</a>
      </div>
    `;
    document.body.appendChild(modal);
  }
}

// ──── Newsletter ────
function initNewsletter() {
  const form = document.querySelector('.newsletter-form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = form.querySelector('input');
      if (input && input.value) {
        showToast('Subscribed successfully!');
        input.value = '';
      }
    });
  }
}

// ──── Global Init ────
document.addEventListener('DOMContentLoaded', () => {
  initHeader();
  initScrollReveal();
  initNewsletter();

  Store.subscribe(updateCartBadge);
  Store.subscribe(updateAuthNav);

  // Page-specific init
  const page = document.body.dataset.page;
  switch (page) {
    case 'home':     initHomePage(); break;
    case 'shop':     initShopPage(); break;
    case 'product':  initProductPage(); break;
    case 'cart':     initCartPage(); break;
    case 'auth':     initAuthPage(); break;
    case 'checkout': initCheckoutPage(); break;
  }
});
