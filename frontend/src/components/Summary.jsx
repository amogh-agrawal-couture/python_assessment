import { useEffect, useState } from "react"
import { fetchSummary } from "../api"

export default function Summary() {
  const [data, setData] = useState([])
  const token = localStorage.getItem("token")

  useEffect(() => {
    fetchSummary(token).then(setData)
  }, [])

  return (
    <>
      <h2>Sales Summary</h2>

      <table border="1" cellPadding="8">
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

      <button
        onClick={() =>
          window.open(
            "http://localhost:8000/summary/download",
            "_blank"
          )
        }
      >
        Download CSV
      </button>
    </>
  )
}
