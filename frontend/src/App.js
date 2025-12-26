import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [currentUser, setCurrentUser] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [usernameInput, setUsernameInput] = useState("");
  const [passwordInput, setPasswordInput] = useState("");

  // Mesaj & Dosya State'leri
  const [receiver, setReceiver] = useState("");
  const [text, setText] = useState("");
  const [file, setFile] = useState(null); // Dosya objesi
  const [method, setMethod] = useState("caesar");
  
  // Parametreler
  const [shift, setShift] = useState(3);
  const [key, setKey] = useState("KEY");
  const [a, setA] = useState(5);
  const [b, setB] = useState(8);
  const [x, setX] = useState(3);
  const [ro, setRo] = useState(5);
  const [kontrol, setKontrol] = useState(true);

  const [inbox, setInbox] = useState([]);
  const [decryptedMessages, setDecryptedMessages] = useState({});
  const [lastProcessTime, setLastProcessTime] = useState(null); // Son işlem süresi

  // --- YARDIMCI: RANDOM ANAHTAR OLUŞTURUCU ---
  const generateRandomKey = () => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%";
    let result = "";
    for (let i = 0; i < 16; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setKey(result);
  };

  // --- YARDIMCI: DOSYAYI BASE64'E ÇEVİR ---
  const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
    });
  };

  // --- API FONKSİYONLARI ---

  const handleRegister = async () => {
    if (!usernameInput || !passwordInput) return alert("Bilgileri giriniz");
    try {
      const res = await axios.post("http://localhost:5000/register", { username: usernameInput, password: passwordInput });
      alert(res.data.message);
    } catch (error) { alert("Hata oluştu"); }
  };

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:5000/login", { username: usernameInput, password: passwordInput });
      setCurrentUser(res.data.username); setIsLoggedIn(true); fetchInbox(res.data.username);
    } catch (error) { alert("Giriş başarısız"); }
  };

  const fetchInbox = async (user = currentUser) => {
    if (!user) return;
    try {
      const res = await axios.get(`http://localhost:5000/get_inbox/${user}`);
      setInbox(res.data);
    } catch (error) { console.error(error); }
  };

  const handleSend = async () => {
    if (!receiver) return alert("Alıcı giriniz!");
    if (!text && !file) return alert("Mesaj veya Dosya seçiniz!");

    let contentToSend = text;
    let isFileToSend = false;
    let filenameToSend = null;

    if (file) {
      try {
        contentToSend = await fileToBase64(file);
        isFileToSend = true;
        filenameToSend = file.name;
      } catch (err) {
        alert("Dosya okunamadı!");
        return;
      }
    }

    const payload = {
      sender: currentUser, receiver: receiver,
      text: contentToSend,
      method: method,
      is_file: isFileToSend,
      filename: filenameToSend,
      shift: Number(shift), key: key, a: Number(a), b: Number(b), x: Number(x), ro: Number(ro), kontrol: Boolean(kontrol)
    };

    try {
      const res = await axios.post("http://localhost:5000/send_message", payload);
      setLastProcessTime(res.data.time);
      alert(`✅ Gönderildi! (Süre: ${res.data.time.toFixed(4)} sn)`);
      setText(""); setFile(null);
    } catch (error) {
      alert("HATA: " + (error.response?.data?.error || "Gönderilemedi"));
    }
  };

  const handleDecryptRequest = async (msg) => {
    let userKeyInput = "";
    
    // Key istemesi gereken metodlar listesi
    const methodsRequiringKey = ["vigenere", "columnar", "playfair", "hill", "vernam", "aes_lib", "aes_manual", "des_manual"];

    if (msg.method !== "rsa_hybrid") {
       if (methodsRequiringKey.includes(msg.method)) {
         userKeyInput = prompt(`'${msg.method}' için ANAHTAR giriniz:`);
         if (userKeyInput === null) return;
       }
    }

    try {
      const res = await axios.post("http://localhost:5000/decrypt_message", {
        cipher_text: msg.content,
        method: msg.method,
        key: userKeyInput,
        params: msg.params,
        username: currentUser
      });

      let content = res.data.plaintext;
      if (msg.is_file) {
        content = (
          <div>
            <p>✅ Dosya Çözüldü!</p>
            <a href={res.data.plaintext} download={msg.filename || "cozulmus_dosya"}>
              📥 İndirmek İçin Tıkla: {msg.filename}
            </a>
            <br/>
            <small>Süre: {res.data.time.toFixed(4)}s</small>
          </div>
        );
      } else {
        content = <span>{res.data.plaintext} <small style={{color:'#888', fontSize:'0.7em'}}>({res.data.time.toFixed(4)}s)</small></span>;
      }
      
      setDecryptedMessages(prev => ({ ...prev, [msg.id]: content }));
    } catch (error) {
      alert("Şifre Çözülemedi!");
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="login-container">
        <h1>🔐 Kriptoloji Ödevi 🔐</h1>
        <div className="login-box">
          <input placeholder="Kullanıcı Adı" value={usernameInput} onChange={(e) => setUsernameInput(e.target.value)}/>
          <input type="password" placeholder="Şifre" value={passwordInput} onChange={(e) => setPasswordInput(e.target.value)}/>
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
        <h2>👤 {currentUser}</h2>
        <div>
          <button className="refresh-btn" onClick={() => fetchInbox()}>↻ Yenile</button>
          <button className="logout-btn" onClick={() => window.location.reload()}>Çıkış</button>
        </div>
      </header>

      <div className="main-content">
        {/* SOL: GÖNDERME */}
        <div className="card send-card">
          <h3>Yeni İleti</h3>
          
          <div className="form-group">
             <input value={receiver} onChange={(e) => setReceiver(e.target.value)} placeholder="Alıcı Kullanıcı Adı" />
          </div>

          <div className="form-group" style={{border:'1px dashed #ccc', padding:10, borderRadius:5}}>
            <label>Mesaj VEYA Dosya:</label>
            <textarea 
              value={text} 
              onChange={(e) => setText(e.target.value)} 
              disabled={file !== null} 
              placeholder={file ? "Dosya seçildi, metin kilitli." : "Metin giriniz..."} 
              rows={3} 
            />
            <div style={{marginTop:5, display:'flex', alignItems:'center', gap:10}}>
              <input type="file" onChange={(e) => setFile(e.target.files[0])} />
              {file && <button onClick={()=>setFile(null)} style={{background:'red', color:'white', border:'none', cursor:'pointer'}}>X İptal</button>}
            </div>
          </div>

          <div className="form-group">
            <label>Yöntem Seçiniz:</label>
            {/* BURASI DÜZELTİLDİ: TÜM LİSTE EKLENDİ */}
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

          <div className="params-area">
             {/* Key Gerektirenler İçin RANDOM Butonu */}
             {["vigenere", "columnar", "playfair", "hill", "vernam", "aes_lib", "aes_manual", "des_manual"].includes(method) && (
                <div style={{display:'flex', width:'100%', gap:5}}>
                  <input type="text" placeholder="Anahtar" value={key} onChange={e=>setKey(e.target.value)} style={{flex:1}}/>
                  <button onClick={generateRandomKey} style={{background:'#6f42c1', color:'white', border:'none', cursor:'pointer', borderRadius:3}}>🎲 Random</button>
                </div>
             )}
             
             {/* Diğer Parametreler */}
             {method === "caesar" && <input type="number" value={shift} onChange={e=>setShift(e.target.value)} placeholder="Shift"/>}
             {method === "affine" && <><input type="number" placeholder="a" value={a} onChange={e=>setA(e.target.value)} /><input type="number" placeholder="b" value={b} onChange={e=>setB(e.target.value)} /></>}
             {method === "railfence" && <input type="number" placeholder="x" value={x} onChange={e=>setX(e.target.value)} />}
             {method === "route" && <input type="number" placeholder="ro" value={ro} onChange={e=>setRo(e.target.value)} />}
          </div>

          <button className="send-btn" onClick={handleSend}>
            {file ? "📁 Dosyayı Şifrele ve Gönder" : "✉️ Mesajı Şifrele ve Gönder"}
          </button>
          
          {lastProcessTime && <p style={{textAlign:'center', fontSize:'0.8em', color:'green'}}>Son işlem: {lastProcessTime.toFixed(5)} saniye</p>}
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
                   <span style={{fontSize:'0.7em', color:'#555', marginLeft:5}}>⏱ {msg.process_time.toFixed(4)}s</span>
                 </div>
                 
                 {decryptedMessages[msg.id] ? (
                    <div className="msg-content decrypted">{decryptedMessages[msg.id]}</div>
                 ) : (
                   <div className="msg-content encrypted">
                     {msg.is_file ? <span>📎 <strong>ŞİFRELİ DOSYA:</strong> {msg.filename}</span> : <span>🔒 {msg.content.substring(0,30)}...</span>}
                   </div>
                 )}

                 {!decryptedMessages[msg.id] && (
                   <button className="decrypt-btn" onClick={() => handleDecryptRequest(msg)}>
                     {msg.method === "rsa_hybrid" ? "🔓 Çöz" : "🔑 Anahtar Gir & Çöz"}
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