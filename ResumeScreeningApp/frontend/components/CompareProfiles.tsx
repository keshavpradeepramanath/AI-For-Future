import { useState } from "react"

export default function CompareProfiles({results}){

const [selected,setSelected] = useState([])
const [comparison,setComparison] = useState([])

function toggle(name){

if(selected.includes(name)){
setSelected(selected.filter(x=>x!==name))
}else{
setSelected([...selected,name])
}

}

async function compare(){

const res = await fetch("http://localhost:8000/api/compare",{
method:"POST",
headers:{ "Content-Type":"application/json"},
body: JSON.stringify({candidates:selected})
})

const data = await res.json()

setComparison(data.comparison)

}

return(

<div style={{marginTop:40}}>

<h3>Compare Candidates</h3>

{results.map((r)=>(
<div key={r.candidate_name}>

<input
type="checkbox"
onChange={()=>toggle(r.candidate_name)}
/>

{r.candidate_name}

</div>
))}

<button
onClick={compare}
style={{marginTop:10}}
>

Compare

</button>


{comparison.length>0 && (

<table style={{marginTop:20,borderCollapse:"collapse"}}>

<thead>

<tr>

<th>Skill</th>

{selected.map(c=>(
<th key={c}>{c}</th>
))}

</tr>

</thead>

<tbody>

{comparison.map((row,i)=>(

<tr key={i}>

<td>{row.skill}</td>

{selected.map(c=>(
<td key={c}>{row[c]}</td>
))}

</tr>

))}

</tbody>

</table>

)}

</div>

)

}