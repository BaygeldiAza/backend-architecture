import { useState } from "react";
import logo from './assets/react.svg';

export default function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to purple-50 flex items-center justify-center p-8">
      <div className="text-center">
        <img 
            src={logo}
            alt="React logo"
            className="w-32 h-32 mx-auto mb-8 anime-spin"
            style={{ animationDuration: '5s'}}            
        />

        <h1 className="text-6xl font-bold text-gray-800 mb-4">
          {count}
        </h1>

        <p className="text-xl text-gray-600 mb-8">clicks</p>

        <div className="space-x-4">
          <button 
            onClick={() => setCount(count+2)}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-8 rounded-lg shadow-lg transition"
            >
              RESET
          </button>

        </div>

      </div>

    </div>
  );
}
