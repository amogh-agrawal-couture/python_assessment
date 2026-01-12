import { useState } from "react"
import { login } from "../api"

export default function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const handleLogin = async () => {
    try {
      await login(username, password)

      onLoginSuccess()
    } catch (err) {
      setError("Invalid credentials")
    }
  }

  return (
    <>
      <h2>Login</h2>

      <input
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>Login</button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </>
  )
}
