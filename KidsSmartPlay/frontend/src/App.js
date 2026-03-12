import React, { useState, useEffect } from "react";
import DragDropGame from "./DragDropGame";

function App() {

const [exercise, setExercise] = useState(null);
const [exerciseNumber, setExerciseNumber] = useState(1);
const [feedback, setFeedback] = useState("");
const [showNext, setShowNext] = useState(false);
const [completed, setCompleted] = useState(false);

function speak(text) {


if (!text) return;

const speech = new SpeechSynthesisUtterance(text);

speech.lang = "en-US";
speech.rate = 0.9;
speech.pitch = 1.2;

window.speechSynthesis.speak(speech);


}

useEffect(() => {


loadExercise(exerciseNumber);


}, [exerciseNumber]);

async function loadExercise(num) {


setFeedback("");
setShowNext(false);

try {

  const response = await fetch(`http://127.0.0.1:8000/game/${num}`);

  const data = await response.json();

  if (data.message === "All exercises completed") {

    setCompleted(true);

    speak("Great job! You finished all the exercises!");

    return;

  }

  setExercise(data);

  speak(data.instruction);

} catch (error) {

  console.error("Failed to load exercise", error);

}


}

function checkAnswer(option) {


if (!exercise) return;

if (String(option) === String(exercise.answer)) {

  setFeedback("🎉 Correct!");

  speak("Correct! Great job!");

} else {

  setFeedback("❌ Try again");

  speak("Try again");

}

setShowNext(true);


}

function nextExercise() {


setExerciseNumber(prev => prev + 1);


}

if (completed) {


return (
  <div style={{ textAlign:"center", padding:40 }}>
    <h1>🎉 All Exercises Completed!</h1>
    <p>Come back tomorrow for more fun learning.</p>
  </div>
);


}

if (!exercise) {


return (
  <div style={{ padding:40 }}>
    <h2>Loading exercise...</h2>
  </div>
);


}

return (


<div style={{ padding:40, textAlign:"center" }}>

  <h1>SmartPlay Kids 🎮</h1>

  <h2>Exercise {exerciseNumber} / 100</h2>

  <button
    onClick={() => speak(exercise.instruction)}
    style={{
      fontSize:"30px",
      marginBottom:"20px",
      cursor:"pointer"
    }}
  >
    🔊
  </button>

  {/* Drag-drop exercise */}

  {exercise.game_name && exercise.game_name.includes("Arrange") ? (

    <DragDropGame
      objects={exercise.objects}
      answer={exercise.answer}
      onCorrect={() => {

        setFeedback("🎉 Correct!");

        speak("Great job!");

        setShowNext(true);

      }}
    />

  ) : (

    <div style={{ fontSize:"80px", margin:"30px 0" }}>

      {exercise.objects && exercise.objects.map((obj,i)=>(
        <span key={i} style={{ margin:"15px" }}>
          {obj}
        </span>
      ))}

    </div>

  )}

  {/* Tap answer exercises */}

  {!showNext && exercise.options && exercise.options.length > 0 && (

    <div>

      {exercise.options.map((opt,i)=>(

        <button
          key={i}
          onClick={()=>checkAnswer(opt)}
          style={{
            margin:"15px",
            padding:"20px",
            fontSize:"40px",
            borderRadius:"20px",
            cursor:"pointer"
          }}
        >
          {opt}
        </button>

      ))}

    </div>

  )}

  <h2 style={{ marginTop:20 }}>{feedback}</h2>

  {showNext && (

    <button
      onClick={nextExercise}
      style={{
        marginTop:20,
        padding:"12px 25px",
        fontSize:"18px",
        background:"#4CAF50",
        color:"white",
        border:"none",
        cursor:"pointer"
      }}
    >
      Next Exercise →
    </button>

  )}

</div>


);

}

export default App;
