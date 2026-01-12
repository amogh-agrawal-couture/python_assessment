import { useState } from "react"
import { login } from "../api"

export default function Login({ setToken }) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const handleLogin = async () => {
    const data = await login(username, password)

    if (data.access_token) {
      localStorage.setItem("token", data.access_token)
      setToken(data.access_token)
    } else {
      alert("Invalid credentials")
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
    </>
  )
}
