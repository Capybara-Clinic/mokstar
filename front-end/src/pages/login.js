import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import * as ROUTES from '../constants/routes';
import { apiFetch } from "../utils/api"; // ✅ 추가

export default function Login() {
  const navigate = useNavigate();

  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const isInvalid = password === '' || userId === '';

  const handleLogin = async (event) => {
    event.preventDefault();

    try {
      const res = await apiFetch('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          user_id: userId,
          pw: password
        })
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.message || '로그인 실패');
      }

      const data = await res.json();

      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('authUser', JSON.stringify(data.user));

      navigate(ROUTES.DASHBOARD);
    } catch (err) {
      setUserId('');
      setPassword('');
      setError(err.message);
    }
  };

  useEffect(() => {
    document.title = 'Login - Mokstagram';
  }, []);

  return (
    <div className="container flex mx-auto max-w-screen-md items-center h-screen">
      <div className="flex w-3/5 px-5">
        <img src="images/capybara-face-login.png" alt="the capybara" />
      </div>
      <div className="flex flex-col w-2/5">
        <div className="flex flex-col items-center bg-white p-4 border border-gray-primary mb-4 rounded">
          <h1 className="flex justify-center w-full">
            <img
              src="images/logo.png"
              alt="logo"
              className="mt-2 w-6/12 mb-4"
            />
          </h1>
          {error && <p className="mb-4 text-xs text-red-primary">{error}</p>}

          <form onSubmit={handleLogin} method="POST">
            <input
              aria-label="Enter your user ID"
              type="text"
              placeholder="User ID"
              className="text-sm text-gray-base w-full py-5 px-4 mb-2 border border-gray-primary rounded"
              onChange={({ target }) => setUserId(target.value)}
              value={userId}
            />
            <input
              aria-label="Enter your password"
              type="password"
              placeholder="Password"
              className="text-sm text-gray-base w-full py-5 px-4 mb-2 border border-gray-primary rounded"
              onChange={({ target }) => setPassword(target.value)}
              value={password}
            />
            <button
              disabled={isInvalid}
              type="submit"
              className={`bg-blue-medium text-white w-full rounded h-8 font-bold ${
                isInvalid && 'opacity-50'
              }`}
            >
              Log In
            </button>
          </form>
        </div>

        <div className="flex justify-center items-center flex-col w-full bg-white p-4 border border-gray-primary rounded">
          <p className="text-sm">
            Don't have an account?{' '}
            <Link to={ROUTES.SIGN_UP} className="font-bold text-blue-medium">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
