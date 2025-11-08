import { useState } from "react";
import logo from './assets/logo.svg';

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <img
        src={logo}
        alt="React logo"
        style={{ width: "100px", height: "100px", animation: "spin 5s linear infinite" }}
      />
      <h1>You clicked {count} times</h1>
      <button onClick={() => setCount(count + 1)}>Click Me</button>
    </div>
  );
}
