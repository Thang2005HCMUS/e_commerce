import os

# Định nghĩa cấu trúc thư mục và nội dung file
files_structure = {
    # 1. Cấu hình API Axios
    "src/services/api.js": """import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8080',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default API;
""",

    # 2. Protected Route Component
    "src/components/ProtectedRoute.jsx": """import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

export default ProtectedRoute;
""",

    # 3. Trang Login
    "src/pages/Login.jsx": """import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await API.post('/auth/login', { username, password });
      if (response.data && response.data.accessToken) {
        localStorage.setItem('token', response.data.accessToken);
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Đăng nhập thất bại. Vui lòng kiểm tra lại!');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md space-y-6 rounded-lg bg-white p-8 shadow-md">
        <h2 className="text-center text-3xl font-bold tracking-tight text-gray-900">Đăng Nhập</h2>
        {error && <div className="rounded bg-red-100 p-3 text-sm text-red-700">{error}</div>}
        <form className="space-y-4" onSubmit={handleLogin}>
          <div>
            <label className="block text-sm font-medium text-gray-700">Username</label>
            <input
              type="text"
              required
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Mật khẩu</label>
            <input
              type="password"
              required
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="w-full rounded-md bg-indigo-600 px-4 py-2 font-semibold text-white hover:bg-indigo-700 focus:outline-none"
          >
            Đăng Nhập
          </button>
        </form>
        <p className="text-center text-sm text-gray-600">
          Chưa có tài khoản?{' '}
          <span onClick={() => navigate('/register')} className="cursor-pointer font-medium text-indigo-600 hover:text-indigo-500">
            Đăng ký ngay
          </span>
        </p>
      </div>
    </div>
  );
};

export default Login;
""",

    # 4. Trang Register
    "src/pages/Register.jsx": """import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../services/api';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    try {
      const response = await API.post('/auth/register', { username, email, password });
      setMessage(response.data || 'Đăng ký thành công!');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.message || 'Đăng ký thất bại. Dữ liệu không hợp lệ!');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md space-y-6 rounded-lg bg-white p-8 shadow-md">
        <h2 className="text-center text-3xl font-bold tracking-tight text-gray-900">Đăng Ký Tài Khoản</h2>
        {error && <div className="rounded bg-red-100 p-3 text-sm text-red-700">{error}</div>}
        {message && <div className="rounded bg-green-100 p-3 text-sm text-green-700">{message}</div>}
        <form className="space-y-4" onSubmit={handleRegister}>
          <div>
            <label className="block text-sm font-medium text-gray-700">Username (tối thiểu 4 ký tự)</label>
            <input
              type="text"
              required
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              required
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Mật khẩu (tối thiểu 6 ký tự)</label>
            <input
              type="password"
              required
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="w-full rounded-md bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700 focus:outline-none"
          >
            Đăng Ký
          </button>
        </form>
        <p className="text-center text-sm text-gray-600">
          Đã có tài khoản?{' '}
          <span onClick={() => navigate('/login')} className="cursor-pointer font-medium text-indigo-600 hover:text-indigo-500">
            Đăng nhập
          </span>
        </p>
      </div>
    </div>
  );
};

export default Register;
""",

    # 5. Trang Dashboard (Có Frame Youtube)
    "src/pages/Dashboard.jsx": """import React from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="flex items-center justify-between bg-white px-6 py-4 shadow-sm">
        <h1 className="text-xl font-bold text-gray-800">Hệ Thống Xác Thực</h1>
        <button
          onClick={handleLogout}
          className="rounded bg-red-500 px-4 py-2 text-sm font-medium text-white hover:bg-red-600"
        >
          Đăng xuất
        </button>
      </nav>

      <div className="mx-auto max-w-4xl p-6 text-center">
        <h2 className="mb-6 text-2xl font-semibold text-gray-800">Chào mừng bạn đã đăng nhập thành công!</h2>
        <p className="mb-4 text-gray-600">Dưới đây là khung phát video YouTube mẫu đặt trong ứng dụng:</p>
        
        <div className="relative overflow-hidden rounded-lg shadow-lg" style={{ paddingBottom: '56.25%', height: 0 }}>
          <iframe
            className="absolute top-0 left-0 h-full w-full"
            src="https://www.youtube.com/embed/dQw4w9WgXcQ"
            title="YouTube video player"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowFullScreen
          ></iframe>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
""",

    # 6. File điều phối Routing chính App.jsx
    "src/App.jsx": """import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element = {
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
"""
}

def create_structure():
    print("🚀 Bắt đầu khởi tạo cấu trúc thư mục và file cho src...")
    for file_path, content in files_structure.items():
        # Lấy đường dẫn thư mục cha
        dir_name = os.path.dirname(file_path)
        
        # Tạo thư mục nếu chưa tồn tại
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            print(f"📁 Đã tạo thư mục: {dir_name}")
            
        # Ghi nội dung vào file (sẽ ghi đè nếu file đã có sẵn)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Đã tạo file: {file_path}")
        
    print("✅ Hoàn thành! Toàn bộ cấu trúc src của bạn đã sẵn sàng.")

if __name__ == "__main__":
    create_structure()