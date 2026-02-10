export default function ResumeUploader({ careerPlan, onResult }) {
    async function upload(e) {
      const form = new FormData();
      form.append("career_plan", careerPlan);
      form.append("file", e.target.files[0]);
  
      const res = await analyzeResume(form);
      onResult(res);
    }
  
    return <input type="file" onChange={upload} />;
  }
  