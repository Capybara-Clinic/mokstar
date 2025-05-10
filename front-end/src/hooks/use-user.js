import { useEffect, useState } from 'react';

export default function useUser() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // 현재는 토큰 기반 사용자 정보 조회 API가 없음.
    const storedUser = localStorage.getItem('authUser');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  return { user };
}
