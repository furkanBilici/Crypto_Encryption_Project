import React, { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [method, setMethod] = useState("caesar");
  const [shift, setShift] = useState(3);
  const [key, setKey] = useState("KEY");
  const [a, setA] = useState(5);
  const [b, setB] = useState(8);
  const [x, setX] = useState(3);
  const [ro, setRo] = useState(5);
  const [kontrol, setKontrol] = useState(true);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const handleEncrypt = async () => {
    setError("");
    setResult("");
    try {
      const body = { text, method };
      if (method === "caesar") body.shift = Number(shift);
      if (method === "vigenere") body.key = key;
      if (method === "columnar") body.key = key;
      if (method === "railfence") body.x = Number(x);
      if (method === "affine") {
        body.a = Number(a);
        body.b = Number(b);
      }
      if (method === "route") {
        body.ro = Number(ro);
        body.kontrol = Boolean(kontrol);
      }

      const res = await fetch("http://127.0.0.1:5000/encrypt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        setError(err.error || `Server returned ${res.status}`);
        return;
      }

      const data = await res.json();
      setResult(data.encrypted ?? JSON.stringify(data));
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div style={{ padding: 30, fontFamily: "sans-serif" }}>
      <h1>🔐 Crypto Encryption Project</h1>

      <textarea
        rows={4}
        cols={50}
        placeholder="Enter text..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <div style={{ marginTop: 10 }}>
        <label>Algorithm: </label>
        <select value={method} onChange={(e) => setMethod(e.target.value)}>
          <option value="caesar">Caesar</option>
          <option value="vigenere">Vigenere</option>
          <option value="substitution">Substitution</option>
          <option value="railfence">Rail Fence</option>
          <option value="affine">Affine</option>
          <option value="route">Route</option>
          <option value="columnar">Columnar</option>
          <option value="polybius">Polybius</option>
          <option value="pigpen">Pigpen</option>
        </select>
      </div>

      {method === "caesar" && (
        <div style={{ marginTop: 8 }}>
          <label>Shift: </label>
          <input
            type="number"
            value={shift}
            onChange={(e) => setShift(e.target.value)}
            style={{ width: 80 }}
          />
        </div>
      )}

      {(method === "vigenere" || method === "columnar") && (
        <div style={{ marginTop: 8 }}>
          <label>Key: </label>
          <input
            type="text"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            style={{ width: 120 }}
          />
        </div>
      )}

      {method === "railfence" && (
        <div style={{ marginTop: 8 }}>
          <label>x: </label>
          <input
            type="number"
            value={x}
            onChange={(e) => setX(e.target.value)}
            style={{ width: 60 }}
          />
        </div>
      )}

      {method === "affine" && (
        <div style={{ marginTop: 8 }}>
          <label>a: </label>
          <input
            type="number"
            value={a}
            onChange={(e) => setA(e.target.value)}
            style={{ width: 60, marginRight: 8 }}
          />
          <label>b: </label>
          <input
            type="number"
            value={b}
            onChange={(e) => setB(e.target.value)}
            style={{ width: 60 }}
          />
        </div>
      )}

      {method === "route" && (
        <div style={{ marginTop: 8 }}>
          <label>ro: </label>
          <input
            type="number"
            value={ro}
            onChange={(e) => setRo(e.target.value)}
            style={{ width: 60, marginRight: 8 }}
          />
          <label>Saat Yönü: </label>
          <input
            type="checkbox"
            checked={kontrol}
            onChange={(e) => setKontrol(e.target.checked)}
          />
        </div>
      )}

      <div style={{ marginTop: 12 }}>
        <button onClick={handleEncrypt}>Encrypt</button>
      </div>

      {error && (
        <div style={{ marginTop: 12, color: "red" }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: 12 }}>
          <h3>Encrypted Result:</h3>
          <pre>{result}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
