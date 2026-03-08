import { useState } from "react"

export default function UploadForm({ setResults }) {

  const [jd,setJd] = useState<File | null>(null)
  const [resumes,setResumes] = useState<FileList | null>(null)
  const [status,setStatus] = useState("")
  const [loading,setLoading] = useState(false)

  async function startScreening(){

    if(!jd || !resumes){
      alert("Please upload JD and resumes")
      return
    }

    const formData = new FormData()

    formData.append("jd_file",jd)

    for(let i=0;i<resumes.length;i++){
      formData.append("resumes",resumes[i])
    }

    setLoading(true)

    const response = await fetch(
      "http://localhost:8000/api/screen-stream",
      {
        method:"POST",
        body:formData
      }
    )

    const reader = response.body?.getReader()

    const decoder = new TextDecoder()

    if(!reader) return

    while(true){

      const {done,value} = await reader.read()

      if(done) break

      const chunk = decoder.decode(value)

      const lines = chunk.split("\n")

      for(const line of lines){

        if(line.startsWith("data:")){

          const data = JSON.parse(line.replace("data:",""))

          setStatus(data.status)

          if(data.results){
            setResults(data.results)
            setLoading(false)
          }

        }

      }

    }

  }


  return(

    <div style={{marginTop:"20px"}}>

      <h3>Upload Job Description</h3>

      <input
        type="file"
        onChange={(e)=>setJd(e.target.files?.[0] || null)}
      />

      <h3 style={{marginTop:"20px"}}>Upload Candidate Resumes</h3>

      <input
        type="file"
        multiple
        onChange={(e)=>setResumes(e.target.files)}
      />

      <br/>

      <button
        onClick={startScreening}
        disabled={loading}
        style={{
          marginTop:"20px",
          padding:"8px 16px",
          background: loading ? "#aaa" : "#2563eb",
          color:"white",
          border:"none",
          borderRadius:"6px",
          cursor: loading ? "not-allowed" : "pointer"
        }}
      >

        {loading ? "Screening..." : "Screen Candidates"}

      </button>


      {status && (

        <div style={{marginTop:"20px"}}>

          <p>{status}</p>

        </div>

      )}

    </div>

  )

}