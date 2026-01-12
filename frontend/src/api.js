const API_URL = "http://localhost:8000"

/**
 * LOGIN
 * JWT is stored automatically in HttpOnly cookie
 */
export async function login(username, password) {
  const formData = new URLSearchParams()
  formData.append("username", username)
  formData.append("password", password)

  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
    credentials: "include", // 🔥 REQUIRED
  })

  if (!res.ok) {
    throw new Error("Login failed")
  }

  return res.json() // { message: "Login successful" }
}

/**
 * FETCH SUMMARY (JWT REQUIRED)
 */
export async function fetchSummary() {
  const res = await fetch(`${API_URL}/summary`, {
    credentials: "include", // 🔥 REQUIRED
  })

  if (!res.ok) {
    throw new Error("Unauthorized")
  }

  return res.json()
}

/**
 * DOWNLOAD CSV (JWT REQUIRED)
 */
export async function downloadSummary() {
  const res = await fetch(`${API_URL}/summary/download`, {
    credentials: "include", // 🔥 REQUIRED
  })

  if (!res.ok) {
    throw new Error("Unauthorized")
  }

  return res.blob()
}

/**
 * LOGOUT
 */
export async function logout() {
  await fetch(`${API_URL}/auth/logout`, {
    method: "POST",
    credentials: "include",
  })
}
