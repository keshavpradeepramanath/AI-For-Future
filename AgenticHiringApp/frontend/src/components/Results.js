import React from "react";
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

function Results({ results }) {
  if (!results || results.length === 0) {
    return <p>No results yet.</p>;
  }

  // ✅ Excel download function
  const downloadExcel = () => {
    const data = results.map((r, index) => ({
      Rank: index + 1,
      Resume: r.resume,
      Score: r.score,
      Decision: r.decision,
      Reason: r.reason,
      Summary: r.summary,
    }));

    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();

    XLSX.utils.book_append_sheet(workbook, worksheet, "Results");

    const excelBuffer = XLSX.write(workbook, {
      bookType: "xlsx",
      type: "array",
    });

    const fileData = new Blob([excelBuffer], {
      type: "application/octet-stream",
    });

    saveAs(fileData, "Screening_Results.xlsx");
  };

  return (
    <div style={{ marginTop: "30px" }}>
      <h3>Screening Results</h3>

      {/* ✅ Download Button */}
      <button
        onClick={downloadExcel}
        style={{
          marginBottom: "15px",
          padding: "10px",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          cursor: "pointer",
        }}
      >
        📥 Download Excel
      </button>

      {/* ✅ Table */}
      <table
        border="1"
        cellPadding="10"
        style={{ width: "100%", borderCollapse: "collapse" }}
      >
        <thead>
          <tr>
            <th>Rank</th>
            <th>Resume</th>
            <th>Score</th>
            <th>Decision</th>
            <th>Reason</th>
            <th>Summary</th>
          </tr>
        </thead>

        <tbody>
          {results.map((r, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{r.resume}</td>
              <td>{r.score}</td>
              <td style={{ color: r.decision === "SELECT" ? "green" : "red" }}>
                {r.decision}
              </td>
              <td>{r.reason}</td>
              <td>{r.summary}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Results;