import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import * as ROUTES from '../constants/routes';
// import { doesUsernameExist } from "../services/api";
import { apiFetch } from "../utils/api"; // ✅ 추가

export default function SignUp() {
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [nickname, setNickname] = useState('');
  const [emailAddress, setEmailAddress] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const isInvalid = password === '' || emailAddress === '';

  const handleSignUp = async (event) => {
    event.preventDefault();

    // Todo
    // make this shit.
    // const usernameExists = await doesUsernameExist(username);
    const usernameExists = false;
    if (usernameExists) {
      setError('That username is already taken, please try another.');
      return;
    }

    try {
      const res = await apiFetch('/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: username,
          pw: password,
          email: emailAddress,
          nickname: nickname
        })
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.message || '회원가입 실패');
      }

      const data = await res.json();
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('authUser', JSON.stringify(data.user));

      navigate(ROUTES.DASHBOARD);
    } catch (err) {
      setNickname('');
      setEmailAddress('');
      setPassword('');
      setError(err.message);
    }
  };

  useEffect(() => {
    document.title = 'Sign Up - Mokstagram';
  }, []);

  return (
    <div className="container flex mx-auto max-w-screen-md items-center h-screen">
      <div className="flex w-3/5 px-5">
        <img src="images/capybara-face-login.png" alt="the capybara" />
      </div>
      <div className="flex flex-col w-2/5">
        <div className="flex flex-col items-center bg-white p-4 border border-gray-primary mb-4 rounded">
          <h1 className="flex justify-center w-full">
            <img src="images/logo.png" alt="logo" className="mt-2 w-6/12 mb-4" />
          </h1>
          {error && <p className="mb-4 text-xs text-red-primary">{error}</p>}

          <form onSubmit={handleSignUp} method="POST">
            <input
              aria-label="Enter your username"
              type="text"
              placeholder="User ID"
              className="text-sm text-gray-base w-full py-5 px-4 mb-2 border border-gray-primary rounded"
              onChange={({ target }) => setUsername(target.value)}
              value={username}
            />
            <input
              aria-label="Enter your nickname"
              type="text"
              placeholder="Nickname"
              className="text-sm text-gray-base w-full py-5 px-4 mb-2 border border-gray-primary rounded"
              onChange={({ target }) => setNickname(target.value)}
              value={nickname}
            />
            <input
              aria-label="Enter your email address"
              type="text"
              placeholder="Email address"
              className="text-sm text-gray-base w-full py-5 px-4 mb-2 border border-gray-primary rounded"
              onChange={({ target }) => setEmailAddress(target.value)}
              value={emailAddress}
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
              Sign Up
            </button>
          </form>
        </div>

        <div className="flex justify-center items-center flex-col w-full bg-white p-4 border border-gray-primary rounded">
          <p className="text-sm">
            Have an account?{" "}
            <Link to={ROUTES.LOGIN} className="font-bold text-blue-medium">
              Log in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
