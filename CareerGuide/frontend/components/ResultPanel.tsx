import { useState } from "react";
import ResumeUploader from "./ResumeUploader";
import RoadmapView from "./RoadmapView";

type ResultPanelProps = {
  result: {
    career_plan: string;
    learning_content: string;
  };
};

export default function ResultPanel({ result }: ResultPanelProps) {
  const [resumeResult, setResumeResult] = useState<any>(null);
  const [roadmap, setRoadmap] = useState<string | null>(null);

  const fullText = `
CAREER ROADMAP
==============
${result.career_plan}

LEARNING RESOURCES
==================
${result.learning_content}

RESUME GAP ANALYSIS
===================
${resumeResult?.gap_analysis ?? "Not generated"}

RESUME IMPROVEMENTS
===================
${resumeResult?.resume_improvements ?? "Not generated"}

60-DAY ROADMAP
==============
${roadmap ?? "Not generated"}
`;

  return (
    <div style={{ marginTop: 32 }}>
      {/* Career Plan */}
      <section>
        <h2>📌 Career Roadmap</h2>
        <pre>{result.career_plan}</pre>
      </section>

      {/* Learning Content */}
      <section>
        <h2>🎓 Learning Resources</h2>
        <pre>{result.learning_content}</pre>
      </section>

      {/* Resume Upload */}
      <section>
        <h2>📄 Resume Gap Analysis</h2>
        <ResumeUploader
          careerPlan={result.career_plan}
          onResult={setResumeResult}
        />

        {resumeResult && (
          <>
            <h3>🔍 Gap Analysis</h3>
            <pre>{resumeResult.gap_analysis}</pre>

            <h3>✍️ Resume Improvements</h3>
            <pre>{resumeResult.resume_improvements}</pre>
          </>
        )}
      </section>

      {/* Roadmap */}
      {resumeResult && (
        <section>
          <h2>🗓️ 60-Day Execution Roadmap</h2>
          <RoadmapView
            careerPlan={result.career_plan}
            gapAnalysis={resumeResult.gap_analysis}
            resumeImprovements={resumeResult.resume_improvements}
            onRoadmap={setRoadmap}
          />
        </section>
      )}

      {/* Copy Everything */}
      <section style={{ marginTop: 24 }}>
        <button
          onClick={() => navigator.clipboard.writeText(fullText)}
        >
          📋 Copy Full Plan
        </button>
      </section>
    </div>
  );
}
