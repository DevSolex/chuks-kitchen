const API = "http://localhost:8000";

export const getToken = () => localStorage.getItem("ck_token");
export const setToken = (t) => localStorage.setItem("ck_token", t);
export const clearToken = () => localStorage.removeItem("ck_token");
export const isLoggedIn = () => !!getToken();

export async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { ...(options.headers || {}) };
  if (!(options.body instanceof FormData)) headers["Content-Type"] = "application/json";
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(`${API}${path}`, { ...options, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || "Request failed");
  return data;
}

export function showToast(msg, type = "success") {
  const icons = { success: "✓", error: "✕", info: "ℹ" };
  const t = document.createElement("div");
  t.className = `toast toast-${type}`;
  t.innerHTML = `<span>${icons[type] || "•"}</span><span>${msg}</span>`;
  document.body.appendChild(t);
  setTimeout(() => { t.style.opacity = "0"; t.style.transform = "translateY(1rem)"; t.style.transition = "all 0.3s"; setTimeout(() => t.remove(), 300); }, 3000);
}

export function setLoading(btn, loading) {
  if (loading) {
    btn.dataset.orig = btn.innerHTML;
    btn.innerHTML = `<span class="spinner"></span>`;
    btn.disabled = true;
  } else {
    btn.innerHTML = btn.dataset.orig || btn.innerHTML;
    btn.disabled = false;
  }
}

export function formatPrice(n) {
  return "₦" + Number(n).toLocaleString("en-NG", { minimumFractionDigits: 0 });
}

export function formatDate(d) {
  return new Date(d).toLocaleString("en-NG", { dateStyle: "medium", timeStyle: "short" });
}

// Cart count badge
export async function refreshCartBadge() {
  if (!isLoggedIn()) return;
  try {
    const items = await apiFetch("/cart/");
    const total = items.reduce((s, i) => s + i.quantity, 0);
    document.querySelectorAll(".cart-count-badge").forEach(el => {
      el.textContent = total;
      el.style.display = total > 0 ? "flex" : "none";
    });
  } catch {}
}

// Shared navbar injection
export function injectNavbar(activePage = "") {
  const logged = isLoggedIn();
  const nav = document.createElement("nav");
  nav.className = "navbar";
  nav.innerHTML = `
    <div class="navbar-inner">
      <a href="/index.html" class="navbar-brand">🍽️ <span>Chuks Kitchen</span></a>
      <div class="navbar-links">
        <a href="/pages/menu.html" class="btn btn-ghost btn-sm ${activePage==='menu'?'text-brand':''}">Menu</a>
        ${logged ? `
          <a href="/pages/orders.html" class="btn btn-ghost btn-sm ${activePage==='orders'?'text-brand':''}">Orders</a>
          <button id="cart-nav-btn" class="btn btn-ghost btn-sm" style="position:relative">
            🛒 Cart <span class="cart-count-badge" style="display:none;position:absolute;top:-4px;right:-4px;background:var(--brand);color:#fff;font-size:0.6rem;font-weight:700;width:16px;height:16px;border-radius:50%;align-items:center;justify-content:center;border:2px solid #fff"></span>
          </button>
          <button id="nav-logout" class="btn btn-outline btn-sm">Logout</button>
        ` : `
          <a href="/pages/login.html" class="btn btn-ghost btn-sm">Login</a>
          <a href="/pages/register.html" class="btn btn-primary btn-sm">Sign Up</a>
        `}
      </div>
    </div>`;
  document.body.prepend(nav);

  if (logged) {
    document.getElementById("nav-logout")?.addEventListener("click", () => {
      clearToken(); location.href = "/index.html";
    });
    refreshCartBadge();
  }
}
