import { useEffect, useState } from "react"

const API_URL = "http://localhost:8000"

export default function Summary() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSummary = async () => {
      const res = await fetch(`${API_URL}/summary`, {
        credentials: "include", // 🔥 SEND COOKIE
      })

      if (res.status === 401) {
        alert("Session expired. Please login again.")
        window.location.reload()
        return
      }

      const json = await res.json()
      setData(json)
      setLoading(false)
    }

    fetchSummary()
  }, [])

  if (loading) {
    return <p>Loading summary...</p>
  }

  // 🚪 Logout
const logout = async () => {
  await fetch("http://localhost:8000/auth/logout", {
    method: "POST",
    credentials: "include", // 🔥 REQUIRED
  })

  window.location.reload()
}

  // 📥 CSV download (cookie included automatically)
  const downloadCSV = async () => {
    const res = await fetch(`${API_URL}/summary/download`, {
      credentials: "include", // 🔥 REQUIRED
    })

    if (!res.ok) {
      alert("Unauthorized")
      return
    }

    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)

    const a = document.createElement("a")
    a.href = url
    a.download = "summary.csv"
    a.click()

    window.URL.revokeObjectURL(url)
  }

  return (
    <>
      <h2>Sales Summary</h2>

      <button onClick={logout}>Logout</button>

      <table border="1" cellPadding="8" style={{ marginTop: "20px" }}>
        <thead>
          <tr>
            <th>Category</th>
            <th>Total Revenue</th>
            <th>Top Product</th>
            <th>Quantity Sold</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              <td>{row.category}</td>
              <td>{row.total_revenue}</td>
              <td>{row.top_product}</td>
              <td>{row.top_product_quantity_sold}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <br />

      <button onClick={downloadCSV}>Download CSV</button>
    </>
  )
}
