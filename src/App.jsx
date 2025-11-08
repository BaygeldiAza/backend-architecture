import { useState } from "react";

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <div style={{textAlign: "center", margin: "100px"}}>
      <h1>You clicked {count} times </h1>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  )
}