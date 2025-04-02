import { useEffect, useState } from "react";

function Table({ selectedCategory }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!selectedCategory) return;

    setLoading(true);
    setError(null);

    fetch(`http://127.0.0.1:5000/${selectedCategory}`)
      .then((response) => response.json())
      .then((json) => setData(json))
      .catch((error) => setError(error.message))
      .finally(() => setLoading(false));
  }, [selectedCategory]);

  return (
    <div>
      <h2 style={{ fontSize: "2rem", marginBottom: "20px" }}>Music Dataset</h2>

      {/* Display loading state */}
      {loading && <p>Loading...</p>}

      {/* Display error */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Display Table */}
      {data.length > 0 ? (
        <table border="1" style={{ margin: "auto", width: "80%", borderCollapse: "collapse", backgroundColor: "#222", color: "white" }}>
          <thead>
            <tr style={{ backgroundColor: "#1DB954" }}>
              {Object.keys(data[0]).map((key) => (
                <th key={key} style={{ padding: "10px", border: "1px solid black" }}>
                  {key.toUpperCase()}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                {Object.values(row).map((value, i) => (
                  <td key={i} style={{ padding: "10px", border: "1px solid black" }}>
                    {value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        !loading && <p>No data available. Click a button above.</p>
      )}
    </div>
  );
}

export default Table;