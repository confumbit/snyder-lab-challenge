import express from "express";
import cors from "cors";
import pool from "./db.js";

const app = express();
app.use(cors());

app.get("/api/data", async (req, res) => {
  const { start_date, end_date, user_id, metric } = req.query;

  if (!start_date || !end_date || !metric) {
    return res.status(400).json({ error: "Missing required query parameters" });
  }

  try {
    const result = await pool.query(
      `SELECT timestamp, value
       FROM raw_data
       WHERE timestamp BETWEEN $1 AND $2
       ORDER BY timestamp`,
      [start_date, end_date]
    );

    console.log(result.rows);

    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal server error" });
  }
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
