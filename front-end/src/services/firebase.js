import { collection, getDocs, query, where } from 'firebase/firestore';
import { db } from '../lib/firebase'; // db = getFirestore(firebaseApp) 해야 함

export async function doesUsernameExist(username) {
  const q = query(
    collection(db, 'users'),
    where('username', '==', username)
  );

  const querySnapshot = await getDocs(q);
  return querySnapshot.docs.length > 0;
}
