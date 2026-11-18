// NexusLogic Systems Interactive Logic

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initTechFilter();
  initCostEstimator();
  initContactForm();
});

// 1. Mobile Menu Drawer Toggle
function initMobileMenu() {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('mobile-menu');

  if (btn && menu) {
    btn.addEventListener('click', () => {
      menu.classList.toggle('hidden');
    });

    // Close on link click
    menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        menu.classList.add('hidden');
      });
    });
  }
}

// 2. Interactive Tech Stack Filter
function initTechFilter() {
  const buttons = document.querySelectorAll('.tech-tab-btn');
  const cards = document.querySelectorAll('.tech-card');

  if (!buttons.length || !cards.length) return;

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle button active styling
      buttons.forEach(b => {
        b.classList.remove('active', 'bg-indigo-600', 'text-white');
        b.classList.add('bg-slate-900', 'text-slate-400');
      });
      btn.classList.add('active', 'bg-indigo-600', 'text-white');
      btn.classList.remove('bg-slate-900', 'text-slate-400');

      const category = btn.getAttribute('data-category');

      cards.forEach(card => {
        const cardCat = card.getAttribute('data-cat');
        if (category === 'all' || cardCat === category) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

// 3. Project Cost & Timeline Calculator
function initCostEstimator() {
  const typeSelect = document.getElementById('est-type');
  const scaleBtns = document.querySelectorAll('.est-scale-btn');
  const addons = document.querySelectorAll('.est-addon');
  const totalCostEl = document.getElementById('est-total-cost');
  const totalWeeksEl = document.getElementById('est-total-weeks');

  if (!typeSelect || !totalCostEl || !totalWeeksEl) return;

  let currentScale = 1.0;

  function calculate() {
    const selectedOption = typeSelect.options[typeSelect.selectedIndex];
    const basePrice = parseFloat(selectedOption.getAttribute('data-price')) || 12000;
    const baseWeeks = parseInt(selectedOption.getAttribute('data-weeks')) || 6;

    let total = basePrice * currentScale;
    let weeks = Math.round(baseWeeks * (currentScale >= 1.4 ? 1.25 : 1.0));

    addons.forEach(addon => {
      if (addon.checked) {
        total += parseFloat(addon.getAttribute('data-cost')) || 0;
        weeks += parseInt(addon.getAttribute('data-addweeks')) || 0;
      }
    });

    totalCostEl.textContent = `$${Math.round(total).toLocaleString()}`;
    totalWeeksEl.textContent = `${weeks} Weeks`;
  }

  typeSelect.addEventListener('change', calculate);

  scaleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      scaleBtns.forEach(b => {
        b.classList.remove('active', 'border-indigo-500', 'bg-indigo-500/20', 'text-white');
        b.classList.add('border-slate-800', 'bg-slate-950', 'text-slate-400');
      });
      btn.classList.add('active', 'border-indigo-500', 'bg-indigo-500/20', 'text-white');
      btn.classList.remove('border-slate-800', 'bg-slate-950', 'text-slate-400');

      currentScale = parseFloat(btn.getAttribute('data-multiplier')) || 1.0;
      calculate();
    });
  });

  addons.forEach(addon => addon.addEventListener('change', calculate));

  // Initial calculation
  calculate();
}

// 4. Contact & Discovery Form Handler
function initContactForm() {
  const form = document.getElementById('contact-form');
  const statusMsg = document.getElementById('form-status');

  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn ? submitBtn.innerHTML : 'Submit';

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span>Dispatching Inquiry...</span>`;
    }

    const formData = {
      name: form.name ? form.name.value : '',
      email: form.email ? form.email.value : '',
      company: form.company ? form.company.value : '',
      service: form.service ? form.service.value : '',
      budget: form.budget ? form.budget.value : '',
      message: form.message ? form.message.value : '',
      timestamp: new Date().toISOString()
    };

    // Save lead in localStorage for verification
    const existingLeads = JSON.parse(localStorage.getItem('nexuslogic_leads') || '[]');
    existingLeads.push(formData);
    localStorage.setItem('nexuslogic_leads', JSON.stringify(existingLeads));

    setTimeout(() => {
      if (statusMsg) {
        statusMsg.classList.remove('hidden');
        statusMsg.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      form.reset();
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    }, 800);
  });
}
