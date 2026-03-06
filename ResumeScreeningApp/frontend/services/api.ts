export async function screenCandidates(formData: FormData) {
    const res = await fetch("http://localhost:8000/api/screen", {
      method: "POST",
      body: formData
    });
  
    return res.json();
  }
  