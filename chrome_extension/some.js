// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCjcHuAZ1dcoNgsKt2_Kk9-wp7HEyP8Lds",
  authDomain: "passwordmanager-335804.firebaseapp.com",
  projectId: "passwordmanager-335804",
  storageBucket: "passwordmanager-335804.appspot.com",
  messagingSenderId: "447082302868",
  appId: "1:447082302868:web:547c420ced33fbcd17d381",
  measurementId: "G-V6QYZVESZF"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);