export default function RoadmapView({ roadmap }) {
    return (
      <>
        <pre>{roadmap}</pre>
        <button
          onClick={() => navigator.clipboard.writeText(roadmap)}
        >
          Copy Roadmap
        </button>
      </>
    );
  }
  