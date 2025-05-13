import Skeleton from "react-loading-skeleton";
import usePosts from "../hooks/use-posts";

export default function TimeLine() {
  const { posts } = usePosts();

  return (
    <div className="container col-span-2">
      {!posts ? (
        [...Array(4)].map((_, index) => (
          <Skeleton key={index} count={1} height={100} className="mb-4" />
        ))
      ) : posts.length > 0 ? (
        posts.map((post) => (
          <div key={post.bill_id} className="bg-white border rounded p-4 mb-4">
            <div className="flex justify-between mb-2">
              <span className="font-bold">{post.nickname}</span>
              <span className="text-xs text-gray-400">
                {new Date(post.created_at).toLocaleString()}
              </span>
            </div>
            <h2 className="text-lg font-semibold">{post.title}</h2>
            <div className="text-sm text-gray-600 mt-1">
              조회수 {post.view_cnt}회
            </div>
            {/* 나중에 상세 보기 링크로 연결할 수 있음 */}
          </div>
        ))
      ) : (
        <p className="text-center text-2xl">게시글이 없습니다.</p>
      )}
    </div>
  );
}
