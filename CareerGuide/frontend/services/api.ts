const API = "http://localhost:8000/api";

export async function generateCareer(data: any) {
  const res = await fetch(`${API}/career/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function analyzeResume(form: FormData) {
  const res = await fetch(`${API}/resume/analyze`, {
    method: "POST",
    body: form,
  });
  return res.json();
}

export async function generateRoadmap(data: any) {
  const res = await fetch(`${API}/roadmap/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}
