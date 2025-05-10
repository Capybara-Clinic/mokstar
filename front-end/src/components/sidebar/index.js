import useUser from "../../hooks/use-user";
import User from './user';
import Suggestions from './suggestions';
import React from "react";

export default function Sidebar() {
  const { user } = useUser();

  if (!user) return null;

  const { user_id, nickname } = user;

  return (
    <div className="p-4">
      <User user_id={user_id} nickname={nickname} />
      <Suggestions userId={user_id} following={[]} /> {/* following은 현재 API에 없음 */}
    </div>
  );
}
