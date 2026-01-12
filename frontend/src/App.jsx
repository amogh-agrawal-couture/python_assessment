import { useState, useEffect } from "react"
import Login from "./components/Login"
import Summary from "./components/Summary"
import { fetchSummary } from "./api"

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false)
  const [checking, setChecking] = useState(true)

  // 🔄 On page refresh: check if cookie is valid
  useEffect(() => {
    fetchSummary()
      .then(() => setLoggedIn(true))
      .catch(() => setLoggedIn(false))
      .finally(() => setChecking(false))
  }, [])

  if (checking) {
    return <p>Checking session...</p>
  }

  return (
    <div style={{ padding: "40px" }}>
      {!loggedIn ? (
        <Login onLoginSuccess={() => setLoggedIn(true)} />
      ) : (
        <Summary onLogout={() => setLoggedIn(false)} />
      )}
    </div>
  )
}
