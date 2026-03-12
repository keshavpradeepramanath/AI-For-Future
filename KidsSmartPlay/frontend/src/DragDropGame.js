import React, { useState } from "react";
import { DndContext } from "@dnd-kit/core";

function DragDropGame({ objects, answer, onCorrect }) {

const [items, setItems] = useState(objects);

function handleDragEnd(result) {

```
if (!result.destination) return;

const newItems = Array.from(items);

const [moved] = newItems.splice(result.source.index, 1);

newItems.splice(result.destination.index, 0, moved);

setItems(newItems);

if (newItems.join("") === answer.join("")) {
  onCorrect();
}
```

}

return (

```
<DragDropContext onDragEnd={handleDragEnd}>

  <Droppable droppableId="row" direction="horizontal">

    {(provided) => (
      <div
        {...provided.droppableProps}
        ref={provided.innerRef}
        style={{display:"flex",justifyContent:"center",fontSize:"80px"}}
      >

        {items.map((item,index)=>(
          <Draggable key={index} draggableId={index.toString()} index={index}>

            {(provided)=>(
              <div
                ref={provided.innerRef}
                {...provided.draggableProps}
                {...provided.dragHandleProps}
                style={{margin:"15px",cursor:"grab"}}
              >
                {item}
              </div>
            )}

          </Draggable>
        ))}

        {provided.placeholder}

      </div>
    )}

  </Droppable>

</DragDropContext>
```

);

}

export default DragDropGame;
