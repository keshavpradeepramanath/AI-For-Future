import React, { useState, useEffect } from "react";

function App() {

const [game, setGame] = useState(null);
const [day, setDay] = useState(1);
const [result, setResult] = useState("");
const [showNext, setShowNext] = useState(false);
const [loading, setLoading] = useState(true);

useEffect(() => {
fetchGame();
}, [day]);

async function fetchGame() {


setLoading(true);
setResult("");
setShowNext(false);

try {

  const response = await fetch(`http://127.0.0.1:8000/game/${day}`);
  const data = await response.json();

  setGame(data);

} catch (error) {

  console.error("Error loading game:", error);

}

setLoading(false);


}

function checkAnswer(option) {


if (!game) return;

if (String(option) === String(game.answer)) {

  setResult("🎉 Correct!");

} else {

  setResult(`❌ Wrong! Correct answer is ${game.answer}`);

}

setShowNext(true);


}

function nextExercise() {


setDay(prev => prev + 1);


}

if (loading || !game) {


return (
  <div style={{ padding: 40 }}>
    <h2>Loading exercise...</h2>
  </div>
);


}

return (


<div style={{ padding: 40, textAlign: "center" }}>

  <h1>SmartPlay Kids 🎮</h1>

  <h2>Exercise {day} / 100</h2>

  <h3>{game.game_name}</h3>

  <p>{game.instruction}</p>

  <h3>{game.question}</h3>

  <div style={{ fontSize: "60px", margin: "20px 0" }}>

    {game.objects && game.objects.map((obj, i) => (
      <span key={i} style={{ margin: "10px" }}>
        {obj}
      </span>
    ))}

  </div>

  {!showNext && game.options && (

    <div>

      {game.options.map((opt, i) => (

        <button
          key={i}
          onClick={() => checkAnswer(opt)}
          style={{
            margin: "10px",
            padding: "10px 20px",
            fontSize: "18px",
            cursor: "pointer"
          }}
        >
          {opt}
        </button>

      ))}

    </div>

  )}

  <h2 style={{ marginTop: 20 }}>{result}</h2>

  {showNext && (

    <button
      onClick={nextExercise}
      style={{
        marginTop: 20,
        padding: "12px 25px",
        fontSize: "18px",
        background: "#4CAF50",
        color: "white",
        border: "none",
        cursor: "pointer"
      }}
    >
      Next Exercise →
    </button>

  )}

</div>


);

}

export default App;
