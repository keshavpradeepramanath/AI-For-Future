import React from "react"

type Candidate = {
  rank: number
  candidate_name: string
  score: number
  decision: string
  reason: string
  strength: string
  skill_gap: string
}

type Props = {
  results: Candidate[]
}

export default function ResultTable({ results }: Props) {

  if (!results || results.length === 0) {
    return null
  }

  const tableStyle = {
    width: "100%",
    borderCollapse: "collapse" as const,
    marginTop: "30px"
  }

  const th = {
    textAlign: "left" as const,
    padding: "10px",
    background: "#f3f4f6",
    borderBottom: "1px solid #ddd",
    fontSize: "14px"
  }

  const td = {
    padding: "10px",
    borderBottom: "1px solid #eee",
    fontSize: "14px"
  }

  const scoreBarContainer = {
    width: "120px",
    height: "8px",
    background: "#e5e7eb",
    borderRadius: "5px"
  }

  return (

    <div>

      <h3 style={{marginTop:"40px"}}>Candidate Ranking</h3>

      <table style={tableStyle}>

        <thead>

          <tr>

            <th style={th}>Rank</th>

            <th style={th}>Candidate</th>

            <th style={th}>Score</th>

            <th style={th}>Decision</th>

            <th style={th}>Reason</th>

            <th style={th}>Strength</th>

            <th style={th}>Skill Gap</th>

          </tr>

        </thead>

        <tbody>

          {results.map((r, index) => (

            <tr key={index}>

              <td style={td}>{r.rank}</td>

              <td style={td}>{r.candidate_name}</td>

              <td style={td}>

                <div style={scoreBarContainer}>

                  <div
                    style={{
                      width: `${r.score}%`,
                      height: "8px",
                      background: "#2563eb",
                      borderRadius: "5px"
                    }}
                  />

                </div>

                <div style={{fontSize:"12px",marginTop:"4px"}}>

                  {r.score}%

                </div>

              </td>

              <td style={td}>

                <span
                  style={{
                    padding: "4px 8px",
                    borderRadius: "6px",
                    background:
                      r.decision === "Selected"
                        ? "#dcfce7"
                        : "#fee2e2",
                    color:
                      r.decision === "Selected"
                        ? "#166534"
                        : "#991b1b"
                  }}
                >

                  {r.decision}

                </span>

              </td>

              <td style={td}>{r.reason}</td>

              <td style={td}>{r.strength}</td>

              <td style={td}>{r.skill_gap}</td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  )
}