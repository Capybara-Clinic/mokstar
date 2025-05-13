import PropTypes from "prop-types";
import { useState } from "react";
import { Link } from "react-router-dom";

export default function SuggestedProfile({ userId, targetId, nickname }) {
  const [followed, setFollowed] = useState(false);

  // Todo : 구현 안됨.
  // const handleFollow = async () => {
  //   const token = localStorage.getItem('access_token');
  //   try {
  //     const res = await fetch(`/api/users/${userId}/follow`, {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //         Authorization: `Bearer ${token}`
  //       },
  //       body: JSON.stringify({ target_id: targetId })
  //     });

  //     if (res.ok) {
  //       setFollowed(true);
  //     } else {
  //       console.error('팔로우 실패');
  //     }
  //   } catch (err) {
  //     console.error('팔로우 에러:', err);
  //   }
  // };

  return !followed ? (
    <div className="flex flex-row items-center justify-between">
      <div className="flex items-center justify-between">
        <img
          className="rounded-full w-8 flex mr-3"
          src={`/images/avatars/${targetId}.jpg`}
          alt={`${nickname} avatar`}
        />
      </div>
      <Link to={`/p/${targetId}`}>
        <p className="font-bold text-sm">{nickname}</p>
      </Link>
      <div>
        <button
          className="text-xs font-bold text-blue-medium"
          type="button"
          // onClick={handleFollow}
        >
          Follow
        </button>
      </div>
    </div>
  ) : null;
}

SuggestedProfile.propTypes = {
  userId: PropTypes.string.isRequired,    // 로그인한 사용자 ID
  targetId: PropTypes.string.isRequired,  // 팔로우할 대상 사용자 ID
  nickname: PropTypes.string.isRequired   // 대상 사용자 닉네임
};
