const BASE_URL = process.env.REACT_APP_API_BASE_URL;

export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem("access_token");

  const headers = {
    ...(options.headers || {}),
    ...(token && { Authorization: `Bearer ${token}` }),
    'Content-Type': 'application/json'
  };

  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers
  });

  return res;
}

/* ❌ 미구현: 사용자 중복 확인 API 없음 (e.g. /auth/exists 등)
export async function doesUsernameExist(username) {
  const res = await apiFetch(`/api/users/exists?username=${encodeURIComponent(username)}`);
  if (!res.ok) return false;

  const data = await res.json();
  return data.exists === true;
}
*/

/* ❌ 미구현: 사용자 정보 조회 API 없음 (e.g. /api/users/:id)
export async function getUserByUserId(userId) {
  const res = await apiFetch(`/api/users/${userId}`);
  if (!res.ok) return [];

  const data = await res.json();
  return [data];
}
*/

// ✅ 추천 사용자 목록 (정식 API 명세에 포함)
export async function getSuggestedProfiles(userId) {
  const res = await apiFetch(`/users/${userId}/suggestions`);
  if (!res.ok) return [];

  return await res.json();
}

// ✅ 사용자 팔로우
export async function followUser(userId, targetUserId) {
  const res = await apiFetch(`/users/${userId}/follow`, {
    method: 'POST',
    body: JSON.stringify({ target_id: targetUserId })
  });

  return res.ok;
}

/* ❌ 미구현: 사진 리스트 API 없음 (/api/photos?user_id=...&following=...)
export async function getPhotos(userId, following) {
  const res = await apiFetch(`/api/photos?user_id=${encodeURIComponent(userId)}&following=${encodeURIComponent(following.join(','))}`);
  if (!res.ok) return [];

  const photos = await res.json();

  return photos.map((photo) => ({
    ...photo,
    userLikedPhoto: photo.likes?.includes(userId) ?? false
  }));
}
*/
