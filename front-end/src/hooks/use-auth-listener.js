import { useState, useEffect } from "react";

export default function useAuthListener() {
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('authUser');
    return storedUser ? JSON.parse(storedUser) : null;
  });

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setUser(null);
      localStorage.removeItem('authUser');
      return;
    }

    // 백엔드에 사용자 정보 요청할 API가 존재하지 않음.
    // 토큰만으로 인증 상태 유지하고, user 정보는 로그인 시 저장된 로컬 값을 사용함.

    // 🔒 나중에 /users/me 또는 /auth/me 생기면 복구
    /*
    const fetchUser = async () => {
      try {
        const res = await fetch('/api/users/me', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        if (res.ok) {
          const data = await res.json();
          setUser(data);
          localStorage.setItem('authUser', JSON.stringify(data));
        } else {
          setUser(null);
          localStorage.removeItem('authUser');
        }
      } catch (err) {
        console.error('Auth listener error:', err);
        setUser(null);
        localStorage.removeItem('authUser');
      }
    };

    fetchUser();
    */
  }, []);

  return { user };
}
