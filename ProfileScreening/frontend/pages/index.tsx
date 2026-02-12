import { useState } from "react";
import ScreeningForm from "../components/ScreeningForm";
import ResultPanel from "../components/ResultPanel";

export default function Home() {
  const [result, setResult] = useState<any>(null);

  return (
    <div style={{ padding: 40 }}>
      <h1>📊 Resume Screening Agent</h1>
      <ScreeningForm onResult={setResult} />
      {result && <ResultPanel result={result} />}
    </div>
  );
}
