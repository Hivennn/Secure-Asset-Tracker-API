// --- CENTRAL CONFIGURATION ---
const BASE_URL = "http://127.0.0.1:8000";

// --- DOM ELEMENTS HOOK SELECTION ---
const authBox = document.getElementById("auth-box");
const dashboardBox = document.getElementById("dashboard-box");
const sessionStatus = document.getElementById("session-status");
const authMessage = document.getElementById("auth-message");
const dashboardMessage = document.getElementById("dashboard-message");
const assetTableBody = document.getElementById("asset-table-body");

// --- PHASE 1: APPLICATION STATE MANAGEMENT ---

// Check if a token exists in local storage and update the UI immediately on page load
function initializeApp() {
  const token = localStorage.getItem("access_token");
  if (token) {
    showDashboardView();
    fetchAndRenderAssets();
  } else {
    showAuthView();
  }
}

function showDashboardView() {
  authBox.classList.add("hidden");
  dashboardBox.classList.remove("hidden");
  sessionStatus.textContent = "Status: Authenticated Connection";
  sessionStatus.className = "status-logged-in";
}

function showAuthView() {
  authBox.classList.remove("hidden");
  dashboardBox.classList.add("hidden");
  sessionStatus.textContent = "Status: Unauthorized Connection";
  sessionStatus.className = "status-logged-out";
  assetTableBody.innerHTML = ""; // Clear confidential data states
}

// --- PHASE 2: AUTHENTICATION NETWORKING OPERATIONS ---

// Handle User Account Registrations
async function handleRegistration() {
  const userField = document.getElementById("username").value;
  const passField = document.getElementById("password").value;

  if (!userField || !passField) {
    displayMessage(authMessage, "Please enter both credentials.", "red");
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: userField, password: passField }),
    });

    const data = await response.json();

    if (response.ok) {
      displayMessage(
        authMessage,
        "Account created! You can sign in now.",
        "green",
      );
    } else {
      displayMessage(authMessage, data.detail || "Registration failed.", "red");
    }
  } catch (error) {
    displayMessage(authMessage, "Could not connect to backend server.", "red");
  }
}

// Handle User Session Login Operations
async function handleLogin() {
  const userField = document.getElementById("username").value;
  const passField = document.getElementById("password").value;

  if (!userField || !passField) {
    displayMessage(authMessage, "Please enter both credentials.", "red");
    return;
  }

  // Form-Data encoding scheme matching OAuth2 constraints natively
  const formData = new URLSearchParams();
  formData.append("username", userField);
  formData.append("password", passField);

  try {
    const response = await fetch(`${BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("access_token", data.access_token);
      displayMessage(authMessage, "", "");
      showDashboardView();
      fetchAndRenderAssets();
    } else {
      displayMessage(authMessage, data.detail || "Invalid credentials.", "red");
    }
  } catch (error) {
    displayMessage(authMessage, "Could not connect to backend server.", "red");
  }
}

// Clear Session Token State
function handleLogout() {
  localStorage.removeItem("access_token");
  showAuthView();
}

// --- PHASE 3: ASSET INVENTORY NETWORKING OPERATIONS ---

// Fetch and render the full list of tracked hardware assets
async function fetchAndRenderAssets() {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(`${BASE_URL}/assets`, {
      method: "GET",
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await response.json();

    if (response.ok) {
      renderTableRows(data.assets);
    } else if (response.status === 401) {
      handleLogout(); // Automatic logout if the token expires
    }
  } catch (error) {
    console.error("Failed to extract repository metrics:", error);
  }
}

// Save a brand new structural asset logging record
async function handleSaveAsset() {
  const token = localStorage.getItem("access_token");
  const name = document.getElementById("asset-name").value;
  const type = document.getElementById("asset-type").value;
  const ip = document.getElementById("asset-ip").value;
  const port = parseInt(document.getElementById("asset-port").value);

  if (!name || !type || !ip || !port) {
    displayMessage(
      dashboardMessage,
      "All configuration tracking fields are mandatory.",
      "red",
    );
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/assets`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name, asset_type: type, ip_address: ip, port }),
    });

    if (response.ok) {
      displayMessage(dashboardMessage, "Asset recorded successfully!", "green");
      clearAssetFormInputs();
      fetchAndRenderAssets();
    } else {
      const data = await response.json();
      displayMessage(
        dashboardMessage,
        data.detail || "Failed to log configuration.",
        "red",
      );
    }
  } catch (error) {
    displayMessage(
      dashboardMessage,
      "Network connection fault detected.",
      "red",
    );
  }
}

// Delete an asset entry safely by its unique ID
async function handleDeleteAsset(assetId) {
  const token = localStorage.getItem("access_token");

  try {
    const response = await fetch(`${BASE_URL}/assets/${assetId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.ok) {
      fetchAndRenderAssets();
    }
  } catch (error) {
    console.error("Failed to drop database asset entry row:", error);
  }
}

// --- PHASE 4: UTILITY INJECTION HELPERS ---

function renderTableRows(assetsList) {
  assetTableBody.innerHTML = "";

  if (assetsList.length === 0) {
    assetTableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted);">No infrastructure records active.</td></tr>`;
    return;
  }

  assetsList.forEach((asset) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${asset.id}</td>
      <td><strong>${asset.name}</strong></td>
      <td>${asset.asset_type}</td>
      <td><code>${asset.ip_address}</code></td>
      <td>${asset.port}</td>
      <td><button class="btn-delete-action" onclick="handleDeleteAsset(${asset.id})">Delete</button></td>
    `;
    assetTableBody.appendChild(tr);
  });
}

function displayMessage(elementHook, textContent, colorValue) {
  elementHook.textContent = textContent;
  elementHook.style.color =
    colorValue === "green" ? "var(--success)" : "var(--danger)";
}

function clearAssetFormInputs() {
  document.getElementById("asset-name").value = "";
  document.getElementById("asset-type").value = "";
  document.getElementById("asset-ip").value = "";
  document.getElementById("asset-port").value = "";
}

// --- PHASE 5: MASTER EVENT LISTENER ATTACHMENTS ---
document.getElementById("btn-login").addEventListener("click", handleLogin);
document
  .getElementById("btn-register")
  .addEventListener("click", handleRegistration);
document.getElementById("btn-logout").addEventListener("click", handleLogout);
document
  .getElementById("btn-save-asset")
  .addEventListener("click", handleSaveAsset);
document
  .getElementById("btn-refresh")
  .addEventListener("click", fetchAndRenderAssets);

// Launch the system engine initialization cycle
initializeApp();
