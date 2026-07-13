import React, { useState } from 'react';
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
