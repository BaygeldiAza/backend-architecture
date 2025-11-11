import { useState } from "react";
import logo from "./assets/react.svg";
import "./App.css"; // Import our custom CSS

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="container">
      <div className="content">
        <img
          src={logo}
          alt="React logo"
          className="logo"
        />

        <h1 className="count">{count}</h1>
        <p className="label">clicks</p>

        <div className="buttons">
          <button onClick={() => setCount(count + 1)} className="btn add">
            +1 count
          </button>
          <button onClick={() => setCount(0)} className="btn reset">
            RESET
          </button>
          <button onClick={() => setCount(count - 1)} className="btn sub">
            -1 count 
          </button>
        </div>
      </div>
    </div>
  );
}
