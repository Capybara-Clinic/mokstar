import { useState, useEffect } from 'react';
import { apiFetch } from '../utils/api'; // ✅ apiFetch 임포트

export default function usePosts() {
  const [posts, setPosts] = useState(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const res = await apiFetch('/board'); // ✅ BASE_URL 적용
        if (!res.ok) throw new Error('Failed to fetch posts');
        const data = await res.json();
        setPosts(data);
      } catch (err) {
        console.error(err);
        setPosts([]);
      }
    };

    fetchPosts();
  }, []);

  return { posts };
}
