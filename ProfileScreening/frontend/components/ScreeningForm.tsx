import { useState } from "react";
import { evaluateCandidate } from "../services/api";

export default function ScreeningForm({ onResult }) {
  const [jdFile, setJdFile] = useState<File | null>(null);
  const [resumeFile, setResumeFile] = useState<File | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!jdFile || !resumeFile) return;

    const formData = new FormData();
    formData.append("jd_file", jdFile);
    formData.append("resume_file", resumeFile);

    const data = await evaluateCandidate(formData);
    onResult(data);
  }

  return (
    <form onSubmit={handleSubmit}>
      <h3>Upload Job Description</h3>
      <input
        type="file"
        accept=".pdf,.docx,.txt"
        onChange={(e) => setJdFile(e.target.files?.[0] || null)}
      />

      <h3>Upload Resume</h3>
      <input
        type="file"
        accept=".pdf,.docx,.txt"
        onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
      />

      <button type="submit" style={{ marginTop: 20 }}>
        Evaluate Candidate
      </button>
    </form>
  );
}
