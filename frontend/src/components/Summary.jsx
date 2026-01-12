import { useEffect, useState } from "react"

const API_URL = "http://localhost:8000"

export default function Summary() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const token = localStorage.getItem("token")

  // 🔐 Fetch summary with JWT
  useEffect(() => {
    const fetchSummary = async () => {
      const res = await fetch(`${API_URL}/summary`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      // 🔴 Token invalid / expired
      if (res.status === 401) {
        localStorage.removeItem("token")
        window.location.reload()
        return
      }

      const json = await res.json()
      setData(json)
      setLoading(false)
    }

    fetchSummary()
  }, [token])

  // ⏳ Loading state
  if (loading) {
    return <p>Loading summary...</p>
  }

  // 🚪 Logout
  const logout = () => {
    localStorage.removeItem("token")
    window.location.reload()
  }

  // 📥 Secure CSV download (JWT included)
  const downloadCSV = async () => {
    const res = await fetch(`${API_URL}/summary/download`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!res.ok) {
      alert("Unauthorized or session expired")
      return
    }

    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)

    const a = document.createElement("a")
    a.href = url
    a.download = "summary.csv"
    document.body.appendChild(a)
    a.click()

    document.body.removeChild(a)
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
