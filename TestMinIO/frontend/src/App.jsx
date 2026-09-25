import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

export default function App() {
  const [usernameInput, setUsernameInput] = useState('');
  const [currentUser, setCurrentUser] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState('');

  // Lấy danh sách file khi đã đăng nhập
  const fetchFiles = async (user) => {
    try {
      const res = await axios.get(`${API_BASE}/files/${user}`);
      setFiles(res.data.files || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (currentUser) {
      fetchFiles(currentUser);
    }
  }, [currentUser]);

  // Xử lý Login
  const handleLogin = (e) => {
    e.preventDefault();
    if (usernameInput.trim()) {
      setCurrentUser(usernameInput.trim());
      setMsg('');
    }
  };

  // Xử lý Logout
  const handleLogout = () => {
    setCurrentUser('');
    setUsernameInput('');
    setFiles([]);
    setSelectedFile(null);
    setMsg('');
  };

  // Xử lý Upload File
  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setMsg('Vui lòng chọn file');
      return;
    }

    const formData = new FormData();
    formData.append('username', currentUser);
    formData.append('file', selectedFile);

    setLoading(true);
    setMsg('');
    try {
      await axios.post(`${API_BASE}/upload`, formData);
      setMsg('Upload thành công!');
      setSelectedFile(null);
      document.getElementById('fileInput').value = '';
      fetchFiles(currentUser); // Refresh danh sách
    } catch (err) {
      console.error(err);
      setMsg('Upload thất bại!');
    } finally {
      setLoading(false);
    }
  };

  // Chưa đăng nhập
  if (!currentUser) {
    return (
      <div style={{ maxWidth: 400, margin: '50px auto', fontFamily: 'sans-serif', padding: 20, border: '1px solid #ccc', borderRadius: 8 }}>
        <h2>Đăng Nhập Test</h2>
        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Nhập username..."
            value={usernameInput}
            onChange={(e) => setUsernameInput(e.target.value)}
            style={{ width: '90%', padding: '8px', marginBottom: '10px' }}
            required
          />
          <button type="submit" style={{ padding: '8px 16px', cursor: 'pointer' }}>Vào hệ thống</button>
        </form>
      </div>
    );
  }

  // Đã đăng nhập
  return (
    <div style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'sans-serif', padding: 20 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #ddd', paddingBottom: 10 }}>
        <h3>Xin chào: <span style={{ color: 'blue' }}>{currentUser}</span></h3>
        <button onClick={handleLogout} style={{ padding: '6px 12px', cursor: 'pointer' }}>Đăng xuất</button>
      </div>

      <div style={{ marginTop: 20, padding: 15, background: '#f9f9f9', borderRadius: 6 }}>
        <h4>Upload File lên MinIO</h4>
        <form onSubmit={handleUpload}>
          <input
            id="fileInput"
            type="file"
            onChange={(e) => setSelectedFile(e.target.files[0])}
            style={{ marginBottom: 10 }}
          />
          <br />
          <button type="submit" disabled={loading} style={{ padding: '8px 16px', cursor: 'pointer' }}>
            {loading ? 'Đang tải lên...' : 'Upload'}
          </button>
        </form>
        {msg && <p style={{ color: msg.includes('thành công') ? 'green' : 'red', marginTop: 10 }}>{msg}</p>}
      </div>

      <div style={{ marginTop: 25 }}>
        <h4>Danh sách link file đã upload:</h4>
        {files.length === 0 ? (
          <p style={{ color: '#888' }}>Chưa có file nào.</p>
        ) : (
          <ul style={{ paddingLeft: 20 }}>
            {files.map((url, idx) => (
              <li key={idx} style={{ marginBottom: 8 }}>
                <a href={url} target="_blank" rel="noreferrer" style={{ wordBreak: 'break-all' }}>
                  {url}
                </a>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}