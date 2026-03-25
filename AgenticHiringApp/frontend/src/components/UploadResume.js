import React from "react";

function UploadResume({ setResumes }) {
  const handleChange = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      setResumes(files);
    }
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <h3>Upload Resumes</h3>
      <input
        type="file"
        multiple
        accept=".txt,.pdf,.doc,.docx"
        onChange={handleChange}
      />
    </div>
  );
}

export default UploadResume;