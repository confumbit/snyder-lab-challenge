import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

function App() {
  const [data, setData] = useState([]);
  const [startDate, setStartDate] = useState("2024-01-01");
  const [endDate, setEndDate] = useState("2024-01-10");
  const [metric, setMetric] = useState("heart_rate");

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/data", {
        params: {
          start_date: startDate,
          end_date: endDate,
          metric,
        },
      })
      .then((res) => {
        setData(res.data);
      })
      .catch(console.error);
  }, [startDate, endDate, metric]);

  return (
    <div style={{ padding: 20 }}>
      <h2>Fitbit Time-Series Dashboard</h2>
      <label>
        Start Date:{" "}
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
      </label>
      <label>
        End Date:{" "}
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </label>
      <LineChart width={900} height={400} data={data}>
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
      </LineChart>
    </div>
  );
}

export default App;
