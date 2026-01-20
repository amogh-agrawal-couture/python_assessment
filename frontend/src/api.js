const API_URL = "http://localhost:8000"

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

export async function fetchSummary() {
  const res = await fetch(`${API_URL}/summary`, {
    credentials: "include", // 🔥 REQUIRED
  })

  if (!res.ok) {
    throw new Error("Unauthorized")
  }

  return res.json()
}

export async function downloadSummary() {
  const res = await fetch(`${API_URL}/summary/download`, {
    credentials: "include", // 🔥 REQUIRED
  })

  if (!res.ok) {
    throw new Error("Unauthorized")
  }

  return res.blob()
}

export async function logout() {
  await fetch(`${API_URL}/auth/logout`, {
    method: "POST",
    credentials: "include",
  })
}
