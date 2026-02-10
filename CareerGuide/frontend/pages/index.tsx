import { useState } from "react";
import { generateCareer } from "../services/api";
import CareerForm from "../components/CareerForm";
import ResultPanel from "../components/ResultPanel";

export default function Home() {
  const [result, setResult] = useState<any>(null);

  return (
    <>
      <CareerForm onSubmit={setResult} />
      {result && <ResultPanel result={result} />}
    </>
  );
}
