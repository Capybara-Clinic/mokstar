import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import Skeleton from 'react-loading-skeleton';

export default function User({ user_id, nickname }) {
  return !user_id || !nickname ? (
    <Skeleton count={1} height={61} />
  ) : (
    <Link to={`/p/${user_id}`} className="grid grid-cols-4 gap-4 mb-6 items-center">
      <div className="flex items-center justify-between col-span-1">
        <img 
          className="rounded-full w-16 flex mr-3"
          src={`/images/avatars/${user_id}.jpg`}
          alt={`${nickname} profile`}
        />
      </div>
      <div className="col-span-3">
        <p className="font-bold text-sm">{user_id}</p>
        <p className="text-sm">{nickname}</p>
      </div>
    </Link>
  );
}

User.propTypes = {
  user_id: PropTypes.string,
  nickname: PropTypes.string.isRequired
};
