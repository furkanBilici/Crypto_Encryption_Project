import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  // Kullanıcı ve Login State'leri
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState("");
  const [usernameInput, setUsernameInput] = useState("");
  const [passwordInput, setPasswordInput] = useState("");

  // Mesajlaşma State'leri
  const [receiver, setReceiver] = useState("");
  const [text, setText] = useState("");
  const [method, setMethod] = useState("caesar");
  
  // Algoritma Parametreleri
  const [shift, setShift] = useState(3);
  const [key, setKey] = useState("KEY");
  const [a, setA] = useState(5);
  const [b, setB] = useState(8);
  const [x, setX] = useState(3);
  const [ro, setRo] = useState(5);
  const [kontrol, setKontrol] = useState(true);

  const [inbox, setInbox] = useState([]);
  const [decryptedMessages, setDecryptedMessages] = useState({});

  // --- LOGIN & REGISTER İŞLEMLERİ ---

  const handleRegister = async () => {
    if (!usernameInput || !passwordInput) {
      alert("Kullanıcı adı ve şifre giriniz!");
      return;
    }
    try {
      const res = await axios.post("http://localhost:5000/register", {
        username: usernameInput,
        password: passwordInput
      });
      alert(res.data.message); // "Kayıt başarılı" mesajı
    } catch (error) {
      alert(error.response?.data?.error || "Kayıt başarısız.");
    }
  };

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:5000/login", {
        username: usernameInput,
        password: passwordInput
      });
      setCurrentUser(res.data.username);
      setIsLoggedIn(true);
      fetchInbox(res.data.username); // Giriş yapınca mesajları çek
    } catch (error) {
      alert(error.response?.data?.error || "Giriş başarısız.");
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setCurrentUser("");
    setInbox([]);
    setDecryptedMessages({});
  };

  // --- MESAJLAŞMA İŞLEMLERİ ---

  const fetchInbox = async (user = currentUser) => {
    if (!user) return;
    try {
      const res = await axios.get(`http://localhost:5000/get_inbox/${user}`);
      setInbox(res.data);
    } catch (error) {
      console.error("Inbox hatası", error);
    }
  };

  const handleSend = async () => {
    if (!receiver || !text) {
      alert("Alıcı ve mesaj alanları boş olamaz!");
      return;
    }

    const payload = {
      sender: currentUser,
      receiver: receiver,
      text: text,
      method: method,
      shift: Number(shift),
      key: key,
      a: Number(a),
      b: Number(b),
      x: Number(x),
      ro: Number(ro),
      kontrol: Boolean(kontrol)
    };

    try {
      await axios.post("http://localhost:5000/send_message", payload);
      alert("✅ Mesaj başarıyla gönderildi!");
      setText(""); 
    } catch (error) {
      // BURADA Backend'den gelen hatayı (Kullanıcı yok) gösteriyoruz
      alert("❌ HATA: " + (error.response?.data?.error || "Bilinmeyen hata"));
    }
  };

  const handleDecryptRequest = async (msg) => {
    let userKeyInput = "";
    if (["vigenere", "columnar", "polybius", "pigpen"].includes(msg.method)) {
      userKeyInput = prompt(`'${msg.method}' için ANAHTARI giriniz:`);
      if (!userKeyInput) return;
    }

    try {
      const res = await axios.post("http://localhost:5000/decrypt_message", {
        cipher_text: msg.content,
        method: msg.method,
        key: userKeyInput,
        params: msg.params
      });
      setDecryptedMessages(prev => ({ ...prev, [msg.id]: res.data.plaintext }));
    } catch (error) {
      alert("Şifre Çözülemedi! Anahtar yanlış.");
    }
  };

  // --- ARAYÜZ ---

  if (!isLoggedIn) {
    return (
      <div className="login-container">
        <h1>🔐 Güvenli Mesajlaşma</h1>
        <div className="login-box">
          <input 
            placeholder="Kullanıcı Adı"
            value={usernameInput}
            onChange={(e) => setUsernameInput(e.target.value)}
          />
          <input 
            type="password"
            placeholder="Şifre"
            value={passwordInput}
            onChange={(e) => setPasswordInput(e.target.value)}
          />
          <div className="login-buttons">
            <button onClick={handleLogin} className="btn-primary">Giriş Yap</button>
            <button onClick={handleRegister} className="btn-secondary">Kayıt Ol</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="header">
        <div className="user-info">
          <h2>👤 {currentUser}</h2>
          <span className="status-dot"></span>
        </div>
        <div>
          <button className="refresh-btn" onClick={() => fetchInbox()}>↻ Yenile</button>
          <button className="logout-btn" onClick={handleLogout}>Çıkış</button>
        </div>
      </header>

      <div className="main-content">
        <div className="card send-card">
          <h3>Yeni Mesaj</h3>
          <div className="form-group">
            <label>Alıcı Kullanıcı Adı:</label>
            <input 
              value={receiver} 
              onChange={(e) => setReceiver(e.target.value)} 
              placeholder="Kullanıcı tam adını girin..." 
            />
          </div>
          
          <div className="form-group">
            <label>Mesaj:</label>
            <textarea value={text} onChange={(e) => setText(e.target.value)} rows={3} placeholder="Gizli mesaj..." />
          </div>

          <div className="form-group">
            <label>Şifreleme Yöntemi:</label>
            <select value={method} onChange={(e) => setMethod(e.target.value)}>
              <option value="caesar">Caesar</option>
              <option value="vigenere">Vigenere</option>
              <option value="substitution">Substitution</option>
              <option value="affine">Affine</option>
              <option value="railfence">Rail Fence</option>
              <option value="route">Route</option>
              <option value="columnar">Columnar</option>
              <option value="polybius">Polybius</option>
              <option value="pigpen">Pigpen</option>
              <option value="playfair">Playfair</option>
              <option value="hill">Hill (Key=4 harf örn: ABCD)</option>
              <option value="vernam">Vernam</option>
              <option value="aes_lib">AES (Lib)</option>
              <option value="aes_manual">AES (Manual Sim)</option>
              <option value="des_manual">DES (Manual Sim)</option>
            </select>
          </div>

          {/* Dinamik Parametreler */}
          <div className="params-area">
             {method === "caesar" && <input type="number" placeholder="Shift" value={shift} onChange={e=>setShift(e.target.value)} />}
             {(method === "vigenere" || method === "columnar") && <input type="text" placeholder="Gizli Anahtar" value={key} onChange={e=>setKey(e.target.value)} />}
             {method === "affine" && <><input type="number" placeholder="a" value={a} onChange={e=>setA(e.target.value)} /><input type="number" placeholder="b" value={b} onChange={e=>setB(e.target.value)} /></>}
             {method === "railfence" && <input type="number" placeholder="x" value={x} onChange={e=>setX(e.target.value)} />}
             {method === "route" && <input type="number" placeholder="ro" value={ro} onChange={e=>setRo(e.target.value)} />}
          </div>

          <button className="send-btn" onClick={handleSend}>Gönder</button>
        </div>

        <div className="card inbox-card">
          <h3>Gelen Kutusu ({inbox.length})</h3>
          <div className="messages-list">
            {inbox.length === 0 && <p className="no-msg">Henüz mesaj yok.</p>}
            {inbox.map((msg) => (
              <div key={msg.id} className="message-item">
                <div className="msg-header">
                  <span className="sender-badge">{msg.sender}</span>
                  <span className="time">{msg.timestamp}</span>
                </div>
                {decryptedMessages[msg.id] ? (
                   <div className="msg-content decrypted">✅ {decryptedMessages[msg.id]}</div>
                ) : (
                  <div className="msg-content encrypted">🔒 {msg.content} <br/><small>({msg.method})</small></div>
                )}
                {!decryptedMessages[msg.id] && (
                  <button className="decrypt-btn" onClick={() => handleDecryptRequest(msg)}>Çöz</button>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;