import React from 'react';
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
