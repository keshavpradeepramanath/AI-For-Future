export default function ResultTable({ results }) {

    if (!results || results.length === 0) return null
  
    return (
  
      <div style={{marginTop:40}}>
  
        <h2 style={{marginBottom:20}}>Candidate Screening Results</h2>
  
        <table style={{
          width:"100%",
          borderCollapse:"collapse",
          fontFamily:"Arial"
        }}>
  
          <thead style={{background:"#f4f6f8"}}>
            <tr>
            <th style={th}>Rank</th>
            <th style={th}>Candidate</th>
            <th style={th}>Match Score</th>
            <th style={th}>Status</th>
            <th style={th}>Risk</th>
            <th style={th}>Reason</th>
            </tr>
          </thead>
  
          <tbody>
  
          {results.map((r,index)=>{
  
            const statusColor =
              r.decision === "Selected" ? "#16a34a" : "#dc2626"
  
            const riskColor =
              r.risk_level === "Low Risk"
                ? "#16a34a"
                : r.risk_level === "Medium Risk"
                ? "#f59e0b"
                : "#dc2626"
  
            return(
  
                <tr key={index} style={{borderBottom:"1px solid #eee"}}>

                <td style={td}>{r.rank}</td>
                
                <td style={td}>{r.candidate_name}</td>
                
                <td style={td}>
                  <div style={{
                    background:"#e5e7eb",
                    width:"140px",
                    height:"10px",
                    borderRadius:"6px"
                  }}>
                    <div style={{
                      width:`${r.score}%`,
                      background:"#2563eb",
                      height:"10px",
                      borderRadius:"6px"
                    }}/>
                  </div>
                
                  <div style={{fontSize:"12px"}}>{r.score}/100</div>
                </td>
                
                <td style={td}>{r.decision}</td>
                
                <td style={td}>{r.risk_level}</td>
                
                <td style={td}>{r.strength}</td>
                
                <td style={td}>{r.skill_gap}</td>
                
                <td style={td}>
                  <details>
                    <summary>View Question</summary>
                    {r.interview_question}
                  </details>
                </td>
                
                </tr>
  
            )
          })}
  
          </tbody>
  
        </table>
  
      </div>
    )
  }
  
  const th = {
    padding:"12px",
    textAlign:"left",
    fontWeight:"600"
  }
  
  const td = {
    padding:"12px",
    verticalAlign:"top"
  }
  

  function getScoreColor(score:number){

    if(score >= 80) return "#16a34a"  // green
    if(score >= 60) return "#2563eb"  // blue
    if(score >= 40) return "#f59e0b"  // yellow
    return "#dc2626"                  // red
  }
 
  
  function getStatusStyle(status:string){

    if(status === "Selected"){
      return {
        background:"#ecfdf5",
        color:"#065f46",
        border:"1px solid #a7f3d0"
      }
    }
  
    return {
      background:"#f3f4f6",
      color:"#374151",
      border:"1px solid #d1d5db"
    }
  }
  
  
  function getRiskStyle(risk:string){
  
    if(risk === "Low Risk"){
      return {
        background:"#ecfdf5",
        color:"#065f46",
        border:"1px solid #a7f3d0"
      }
    }
  
    if(risk === "Medium Risk"){
      return {
        background:"#fffbeb",
        color:"#92400e",
        border:"1px solid #fde68a"
      }
    }
  
    return {
      background:"#fef2f2",
      color:"#991b1b",
      border:"1px solid #fecaca"
    }
  }
  