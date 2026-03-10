import React, { useState, useEffect } from "react";

function App() {

const [exercise, setExercise] = useState(null);
const [exerciseNumber, setExerciseNumber] = useState(1);
const [feedback, setFeedback] = useState("");
const [showNext, setShowNext] = useState(false);
const [completed, setCompleted] = useState(false);

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
    return;
  }

  setExercise(data);

} catch (error) {

  console.error("Failed to load exercise", error);

}


}

function checkAnswer(option) {


if (!exercise) return;

if (String(option) === String(exercise.answer)) {

  setFeedback("🎉 Correct!");

} else {

  setFeedback(`❌ Wrong! Correct answer: ${exercise.answer}`);

}

setShowNext(true);


}

function nextExercise() {


setExerciseNumber(prev => prev + 1);


}

if (completed) {


return (

  <div style={{textAlign:"center",padding:40}}>

    <h1>🎉 All 100 Exercises Completed!</h1>

    <p>Great job! Come back tomorrow for more learning.</p>

  </div>

);


}

if (!exercise) {


return (

  <div style={{padding:40}}>

    <h2>Loading exercise...</h2>

  </div>

);


}

return (


<div style={{padding:40,textAlign:"center"}}>

  <h1>SmartPlay Kids 🎮</h1>

  <h2>Exercise {exerciseNumber} / 100</h2>

  <h3>{exercise.game_name}</h3>

  <p>{exercise.instruction}</p>

  <h3>{exercise.question}</h3>

  <div style={{fontSize:"60px",margin:"20px 0"}}>

    {exercise.objects && exercise.objects.map((obj,i)=>(
      <span key={i} style={{margin:"10px"}}>
        {obj}
      </span>
    ))}

  </div>

  {!showNext && (

    <div>

      {exercise.options && exercise.options.map((opt,i)=>(

        <button
          key={i}
          onClick={()=>checkAnswer(opt)}
          style={{
            margin:"10px",
            padding:"10px 20px",
            fontSize:"18px",
            cursor:"pointer"
          }}
        >
          {opt}
        </button>

      ))}

    </div>

  )}

  <h2 style={{marginTop:20}}>{feedback}</h2>

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
