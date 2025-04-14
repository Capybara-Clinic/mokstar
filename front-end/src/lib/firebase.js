// firebase v9 이상 부터는 다음과 같이 named import 방식을 사용해야 함.
import { initializeApp } from 'firebase/app';
import { getFirestore, serverTimestamp } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

// here i want to import the seed file

const config = {
    apiKey: process.env.REACT_APP_API_KEY,
    projectId: process.env.REACT_APP_PROJECT_ID,
    authDomain: process.env.REACT_APP_AUTH_DOMAIN,
    storageBucket: process.env.REACT_APP_STORAGE_BUCKET,
    messagingSenderId: process.env.REACT_APP_MESSAGING_SENDER_ID,
    appId: process.env.REACT_APP_APP_ID,
  };
  

const firebase = initializeApp(config);
const { FieldValue } = getFirestore(firebase);

// here is where i want to call the seed file (only once)
// seedDatabase(firebase);

export { firebase, FieldValue };