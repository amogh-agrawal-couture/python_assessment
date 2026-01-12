import { useState } from "react"
import Login from "./components/Login.jsx"
import Summary from "./components/Summary.jsx"

export default function App() {
  const [token, setToken] = useState(
    localStorage.getItem("token")
  )

  return (
    <div style={{ padding: "40px" }}>
      {!token ? (
        <Login setToken={setToken} />
      ) : (
        <Summary />
      )}
    </div>
  )
}
