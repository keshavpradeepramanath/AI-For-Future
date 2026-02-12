export async function evaluateCandidate(formData: FormData) {
    const res = await fetch("http://localhost:8000/api/screening/evaluate", {
      method: "POST",
      body: formData,
    });
  
    return res.json();
  }
  