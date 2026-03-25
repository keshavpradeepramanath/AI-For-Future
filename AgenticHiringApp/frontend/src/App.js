import React, { useState } from "react";
import axios from "axios";
import UploadJD from "./components/UploadJD";
import UploadResume from "./components/UploadResume";
import Results from "./components/Results";
import Dashboard from "./components/Dashboard";

function App() {
  
  const [resumes, setResumes] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [bgResults, setBgResults] = useState([]);
  const [jds, setJds] = useState([]);  // instead of single jd

  const runBackgroundCheck = async () => {
    const formData = new FormData();
  
    resumes.forEach((file) => {
      formData.append("resumes", file);
    });
  
    const res = await axios.post(
      "http://localhost:8000/background-check",
      formData
    );
  
    setBgResults(res.data.background_results);
  };



  const handleSubmit = async () => {
    if (jds.length === 0 || resumes.length === 0) {
      alert("Upload JDs and resumes first!");
      return;
    }
  
    setLoading(true);
  
    const formData = new FormData();
  
    // ✅ MULTIPLE JDs
    jds.forEach((file) => {
      formData.append("jds", file);
    });
  
    // ✅ MULTIPLE RESUMES
    resumes.forEach((file) => {
      formData.append("resumes", file);
    });
  
    try {
      const res = await axios.post("http://localhost:8000/screen", formData);
      setResults(res.data.ranked_candidates);
    } catch (err) {
      console.error(err);
      alert("Error calling backend");
    }
  
    setLoading(false);
  };
  return (
    <div style={{ padding: 20 }}>
      <h2>AI Resume Screener</h2>
  
      <UploadJD setJds={setJds} />
      <UploadResume setResumes={setResumes} />
  
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Processing..." : "Screen Candidates"}
      </button>

      <button
        onClick={runBackgroundCheck}
        style={{
            marginLeft: "10px",
            padding: "8px",
            backgroundColor: "#2196F3",
            color: "white",
            border: "none",
            cursor: "pointer"
        }}
        >
        🔍 Run Background Check
      </button>
  
      {loading && (
        <div style={{ marginTop: "20px", color: "blue", fontWeight: "bold" }}>
          ⏳ Screening candidates... please wait
        </div>
      )}
  
      {/* ✅ Results Table */}
      <Results results={results} />
  
      {/* ✅ STEP 5: ADD DASHBOARD HERE */}
      <Dashboard results={results} />

      {bgResults.length > 0 && (
        <div style={{ marginTop: "30px" }}>
            <h3>🔍 Background Check Results</h3>

            {bgResults.map((r, i) => (
            <div key={i} style={{ marginBottom: "15px" }}>
                <strong>{r.resume}</strong>
                <pre>{r.result}</pre>
        </div>
    ))}
  </div>
)}
  
    </div>
  );
    
}

export default App;
