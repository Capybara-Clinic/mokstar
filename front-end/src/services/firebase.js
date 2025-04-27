import { collection, getDocs, limit, query, where } from 'firebase/firestore';
import { db } from '../lib/firebase'; // db = getFirestore(firebaseApp) 해야 함

export async function doesUsernameExist(username) {
  const q = query(
    collection(db, 'users'),
    where('username', '==', username)
  );

  const querySnapshot = await getDocs(q);
  return querySnapshot.docs.length > 0;
}

export async function getUserByUserId(userId) {
  const q = query(
    collection(db, 'users'),
    where('userId', '==', userId)
  );
  const snapshot = await getDocs(q);

  const user = snapshot.docs.map((item) => ({
    ... item.data(),
    docId: item.id
  }));

  return user;
}

export async function getSuggestedProfiles(userId, following = []) {
  const q = query(
    collection(db, 'users'),
    limit(10)
  );

  const snapshot = await getDocs(q);
  return snapshot.docs.map((user) => ({
    ... user.data(),
    docId: user.id
  }))
  .filter((profile) =>
  profile.userId !== userId && !following.includes(profile.userId));
  // const result = await coll
}

export async function getPhotos(userId, following) {
  const q = query(
    collection(db, 'photos'),
    where('userid', 'in', following)
  );
  const snapshot = await getDocs(q);
  const photos = snapshot.docs.map((item) => ({
    ... item.data(),
    docId: item.id
  }));

  const photosWithUserDetails = await Promise.all(
    photos.map(async (photo) => {
      let userLikedPhoto = false;
      if (photo.likes.includes(userId)) {
        userLikedPhoto = true;
      }
      const user = await getUserByUserId(photo.userId);
      const {username} = user[0];
      return {username, ...photo, userLikedPhoto };
    })
  );
  return photosWithUserDetails;
}