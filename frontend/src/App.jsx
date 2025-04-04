import { Outlet } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';

// Import CSS
import './index.css'

function App() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-xl font-bold text-gray-900">BankGen 360</h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <a
                href="/"
                className="text-gray-700 hover:text-gray-900"
              >
                Data Products
              </a>
              <a
                href="/dashboard"
                className="text-gray-700 hover:text-gray-900"
              >
                Dashboard
              </a>
              {user ? (
                <span className="text-gray-700">{user.email}</span>
              ) : (
                <a
                  href="/login"
                  className="text-gray-700 hover:text-gray-900"
                >
                  Login
                </a>
              )}
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <Outlet />
      </main>
    </div>
  );
}

export default App;
