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
  })

  return res.json()
}

export async function fetchSummary(token) {
  const res = await fetch(`${API_URL}/summary`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return res.json()
}
