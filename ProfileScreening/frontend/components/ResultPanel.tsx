import CopyButton from "./CopyButton";

export default function ResultPanel({ result }) {
  if (!result || typeof result !== "object") {
    return null;
  }

  return (
    <div style={{ marginTop: 30 }}>
      <h2>Screening Result</h2>

      <p><strong>Score:</strong> {result.score ?? "N/A"}</p>
      <p><strong>Decision:</strong> {result.decision ?? "N/A"}</p>

      <h3>Strong Matches</h3>
      <ul>
        {result.strong_matches?.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>

      <h3>Critical Gaps</h3>
      <ul>
        {result.critical_gaps?.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>

      <h3>Reasoning</h3>
      <p>{result.reasoning}</p>

      <CopyButton
        text={JSON.stringify(result, null, 2)}
        label="📋 Copy Evaluation"
      />
    </div>
  );
}
