export default function ResultTable({ results }) {

    if (!results || results.length === 0) return null;
  
    return (
  
      <div style={{marginTop:40}}>
  
        <h2 style={{marginBottom:20}}>Candidate Ranking</h2>
  
        <table style={{
          width:"100%",
          borderCollapse:"collapse",
          fontFamily:"Arial"
        }}>
  
          <thead style={{background:"#f5f7fa"}}>
            <tr>
              <th style={th}>Candidate</th>
              <th style={th}>Score</th>
              <th style={th}>Status</th>
              <th style={th}>Reason</th>
            </tr>
          </thead>
  
          <tbody>
  
          {results.map((r,index)=>{
  
            const statusColor =
              r.decision === "Selected"
              ? "#16a34a"
              : "#dc2626"
  
            return(
  
            <tr key={index} style={{borderBottom:"1px solid #eee"}}>
  
              <td style={td}>{r.candidate_name}</td>
  
              <td style={td}>
  
                <div style={{
                  background:"#eee",
                  width:"120px",
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
  
                <div style={{fontSize:"12px",marginTop:"4px"}}>
                  {r.score}
                </div>
  
              </td>
  
              <td style={td}>
                <span style={{
                  background:statusColor,
                  color:"white",
                  padding:"6px 12px",
                  borderRadius:"6px"
                }}>
                  {r.decision}
                </span>
              </td>
  
              <td style={td}>{r.reason}</td>
  
            </tr>
  
            )
  
          })}
  
          </tbody>
  
        </table>
  
      </div>
    );
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
  