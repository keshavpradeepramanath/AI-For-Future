import { useState } from "react"
import UploadForm from "../components/UploadForm"
import ResultTable from "../components/ResultTable"

export default function Home(){

  const [results,setResults] = useState([])

  return(

    <div style={{
      maxWidth:"1100px",
      margin:"40px auto",
      fontFamily:"Arial"
    }}>

      <h1 style={{marginBottom:10}}>
        AI Resume Screening
      </h1>

      <p style={{color:"#666"}}>
        Upload a job description and multiple resumes. The AI will evaluate candidates against the JD.
      </p>

      <UploadForm onResult={setResults}/>

      <ResultTable results={results}/>

    </div>
  )
}
