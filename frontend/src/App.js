// frontend/src/App.js

import { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/summary/")
      .then(res => res.json())
      .then(setData);
  }, []);

  return (
    <div>
      <h2>Sales Summary</h2>

      <table border="1">
        <thead>
          <tr>
            <th>Category</th>
            <th>Total Revenue</th>
            <th>Top Product</th>
            <th>Quantity Sold</th>
          </tr>
        </thead>
        <tbody>
          {data.map(row => (
            <tr key={row.category}>
              <td>{row.category}</td>
              <td>{row.total_revenue}</td>
              <td>{row.top_product}</td>
              <td>{row.top_product_quantity_sold}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <br />

      <a href="http://localhost:8000/summary/download">
        <button>Download CSV</button>
      </a>
    </div>
  );
}

export default App;
