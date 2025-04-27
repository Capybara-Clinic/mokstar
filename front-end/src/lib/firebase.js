// firebase v9 이상 부터는 다음과 같이 named import 방식을 사용해야 함.
import { initializeApp } from 'firebase/app';
import { getFirestore, serverTimestamp } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

// here i want to import the seed file
// import { seedDatabase } from '../seed';

const config = {
    apiKey: process.env.REACT_APP_API_KEY,
    projectId: process.env.REACT_APP_PROJECT_ID,
    authDomain: process.env.REACT_APP_AUTH_DOMAIN,
    storageBucket: process.env.REACT_APP_STORAGE_BUCKET,
    messagingSenderId: process.env.REACT_APP_MESSAGING_SENDER_ID,
    appId: process.env.REACT_APP_APP_ID,
  };
  

// Firebase 초기화
const firebase = initializeApp(config);
const db = getFirestore(firebase);
const auth = getAuth(firebase);
// FieldValue 유틸
const FieldValue = { serverTimestamp };
console.log('TEST_USER_ID:', process.env.REACT_APP_TEST_USER_ID);

// here is where i want to call the seed file (only once)
// seed 데이터 삽입 (개발 환경일 때만)

// seedDatabase(db); // 또는 seedDatabase(firebase) → 내부에서 getFirestore() 해도 OK

export { firebase, FieldValue, db, auth };