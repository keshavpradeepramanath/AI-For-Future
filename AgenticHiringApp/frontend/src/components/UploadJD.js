import React from "react";

function UploadJD({ setJds }) {
  const handleChange = (e) => {
    const files = Array.from(e.target.files);
    setJds(files);
  };

  return (
    <div>
      <h3>Upload Job Descriptions</h3>
      <input type="file" multiple onChange={handleChange} />
    </div>
  );
}

export default UploadJD;