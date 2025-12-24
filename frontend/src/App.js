import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  // --- STATE TANIMLAMALARI ---
  const [currentUser, setCurrentUser] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [usernameInput, setUsernameInput] = useState("");
  const [passwordInput, setPasswordInput] = useState("");

  // Mesaj Gönderme Alanı
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

  // Gelen Kutusu
  const [inbox, setInbox] = useState([]);
  const [decryptedMessages, setDecryptedMessages] = useState({});

  // --- FONKSİYONLAR ---

  const handleRegister = async () => {
    if (!usernameInput || !passwordInput) { alert("Bilgileri giriniz"); return; }
    try {
      const res = await axios.post("http://localhost:5000/register", { username: usernameInput, password: passwordInput });
      alert(res.data.message);
    } catch (error) { alert(error.response?.data?.error || "Hata"); }
  };

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:5000/login", { username: usernameInput, password: passwordInput });
      setCurrentUser(res.data.username);
      setIsLoggedIn(true);
      fetchInbox(res.data.username);
    } catch (error) { alert("Giriş başarısız"); }
  };

  const handleLogout = () => {
    setIsLoggedIn(false); setCurrentUser(""); setInbox([]); setDecryptedMessages({});
  };

  const fetchInbox = async (user = currentUser) => {
    if (!user) return;
    try {
      const res = await axios.get(`http://localhost:5000/get_inbox/${user}`);
      setInbox(res.data);
    } catch (error) { console.error(error); }
  };

  const handleSend = async () => {
    if (!receiver || !text) { alert("Alıcı ve mesaj zorunlu!"); return; }

    const payload = {
      sender: currentUser,
      receiver: receiver,
      text: text,
      method: method,
      shift: Number(shift),
      key: key,
      a: Number(a), b: Number(b), x: Number(x), ro: Number(ro), kontrol: Boolean(kontrol)
    };

    try {
      await axios.post("http://localhost:5000/send_message", payload);
      alert("✅ Mesaj Gönderildi!");
      setText("");
    } catch (error) {
      alert("HATA: " + (error.response?.data?.error || "Gönderilemedi"));
    }
  };

  const handleDecryptRequest = async (msg) => {
    let userKeyInput = "";

    // RSA Hybrid dışındaki metodlar için anahtar soruyoruz
    // RSA'da sistem otomatik kendi private key'ini kullanacak
    if (msg.method !== "rsa_hybrid") {
       // Key gerektiren metodlar
       if (["vigenere", "columnar", "polybius", "pigpen", "playfair", "hill", "vernam", "aes_lib", "aes_manual", "des_manual"].includes(msg.method)) {
         userKeyInput = prompt(`'${msg.method}' çözmek için ANAHTAR giriniz:`);
         if (!userKeyInput) return;
       }
    }

    try {
      const res = await axios.post("http://localhost:5000/decrypt_message", {
        cipher_text: msg.content,
        method: msg.method,
        key: userKeyInput,
        params: msg.params,
        username: currentUser // RSA için gerekli (kimin private key'i kullanılacak?)
      });
      setDecryptedMessages(prev => ({ ...prev, [msg.id]: res.data.plaintext }));
    } catch (error) {
      alert("Şifre Çözülemedi! (Anahtar yanlış veya yetkiniz yok)");
    }
  };

  // --- EKRAN TASARIMI ---

  if (!isLoggedIn) {
    return (
      <div className="login-container">
        <h1>🔐 Kripto Projesi</h1>
        <div className="login-box">
          <input placeholder="Kullanıcı Adı" value={usernameInput} onChange={(e) => setUsernameInput(e.target.value)}/>
          <input type="password" placeholder="Şifre" value={passwordInput} onChange={(e) => setPasswordInput(e.target.value)}/>
          <div className="login-buttons">
            <button onClick={handleLogin} className="btn-primary">Giriş Yap</button>
            <button onClick={handleRegister} className="btn-secondary">Kayıt Ol</button>
          </div>
          <small style={{display:'block', marginTop:10, color:'#666'}}>*Kayıt olunca RSA anahtarlarınız otomatik üretilir.</small>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="header">
        <h2>👤 {currentUser}</h2>
        <div>
          <button className="refresh-btn" onClick={() => fetchInbox()}>↻ Yenile</button>
          <button className="logout-btn" onClick={handleLogout}>Çıkış</button>
        </div>
      </header>

      <div className="main-content">
        {/* SOL: GÖNDERME */}
        <div className="card send-card">
          <h3>Yeni Mesaj</h3>
          <div className="form-group">
            <label>Alıcı:</label>
            <input value={receiver} onChange={(e) => setReceiver(e.target.value)} placeholder="Kime?" />
          </div>
          <div className="form-group">
            <label>Mesaj:</label>
            <textarea value={text} onChange={(e) => setText(e.target.value)} rows={3} />
          </div>

          <div className="form-group">
            <label>Yöntem:</label>
            <select value={method} onChange={(e) => setMethod(e.target.value)}>
              <optgroup label="Modern & Hibrit (Ödev)">
                <option value="rsa_hybrid">RSA Hybrid (Otomatik Key)</option>
                <option value="aes_lib">AES-128 (Kütüphane)</option>
                <option value="aes_manual">AES (Manuel Simülasyon)</option>
                <option value="des_manual">DES (Manuel Simülasyon)</option>
              </optgroup>
              <optgroup label="Klasik Yöntemler">
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
                <option value="hill">Hill</option>
                <option value="vernam">Vernam</option>
              </optgroup>
            </select>
          </div>

          {/* Dinamik Parametreler */}
          <div className="params-area">
            {/* RSA İÇİN ÖZEL MESAJ */}
            {method === "rsa_hybrid" ? (
                <div style={{color: 'green', fontSize: '0.9rem', padding: '5px'}}>
                    ℹ️ <strong>Otomatik Şifreleme:</strong> Mesaj, alıcının Public Key'i ile şifrelenecek. Manuel anahtar gerekmez.
                </div>
            ) : (
                <>
                   {/* DİĞERLERİ İÇİN INPUTLAR */}
                   {method === "caesar" && <input type="number" placeholder="Shift" value={shift} onChange={e=>setShift(e.target.value)} />}
                   
                   {/* Key Gerektirenler */}
                   {["vigenere", "columnar", "playfair", "hill", "vernam", "aes_lib", "aes_manual", "des_manual"].includes(method) && (
                      <input type="text" placeholder="Gizli Anahtar (Key)" value={key} onChange={e=>setKey(e.target.value)} style={{flex:1}}/>
                   )}
                   
                   {method === "affine" && <><input type="number" placeholder="a" value={a} onChange={e=>setA(e.target.value)} /><input type="number" placeholder="b" value={b} onChange={e=>setB(e.target.value)} /></>}
                   {method === "railfence" && <input type="number" placeholder="x" value={x} onChange={e=>setX(e.target.value)} />}
                   {method === "route" && <input type="number" placeholder="ro" value={ro} onChange={e=>setRo(e.target.value)} />}
                </>
            )}
          </div>

          <button className="send-btn" onClick={handleSend}>Şifrele ve Gönder</button>
        </div>

        {/* SAĞ: GELEN KUTUSU */}
        <div className="card inbox-card">
          <h3>Gelen Kutusu</h3>
          <div className="messages-list">
            {inbox.length === 0 && <p className="no-msg">Mesaj yok.</p>}
            {inbox.map((msg) => (
              <div key={msg.id} className="message-item">
                <div className="msg-header">
                  <span className="sender-badge">{msg.sender}</span>
                  <span className="method-badge">{msg.method}</span>
                  <span className="time">{msg.timestamp}</span>
                </div>
                
                {decryptedMessages[msg.id] ? (
                   <div className="msg-content decrypted">✅ {decryptedMessages[msg.id]}</div>
                ) : (
                  <div className="msg-content encrypted">
                    🔒 {msg.content.substring(0, 40)}...
                  </div>
                )}

                {!decryptedMessages[msg.id] && (
                  <button className="decrypt-btn" onClick={() => handleDecryptRequest(msg)}>
                    {msg.method === "rsa_hybrid" ? "🔓 RSA ile Çöz (Otomatik)" : "🔑 Anahtar Gir ve Çöz"}
                  </button>
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