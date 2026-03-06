import { useState } from "react"
import { screenCandidates } from "../services/api"

export default function UploadForm({ onResult }) {

  const [jdFile,setJdFile] = useState<File|null>(null)
  const [resumes,setResumes] = useState<FileList|null>(null)

  async function handleSubmit(e:React.FormEvent){

    e.preventDefault()

    if(!jdFile || !resumes) return

    const formData = new FormData()

    formData.append("jd_file",jdFile)

    for(let i=0;i<resumes.length;i++){
      formData.append("resumes",resumes[i])
    }

    const data = await screenCandidates(formData)

    onResult(data.results)
  }

  return(

    <form onSubmit={handleSubmit}>

      <h3>Upload JD</h3>

      <input
        type="file"
        onChange={(e)=>setJdFile(e.target.files?.[0] || null)}
      />

      <h3>Upload Resumes</h3>

      <input
        type="file"
        multiple
        onChange={(e)=>setResumes(e.target.files)}
      />

      <button type="submit">
        Screen Candidates
      </button>

    </form>
  )
}
