const firebaseConfig = {
    apiKey: "AIzaSyBnX1OvQlBpr7gVa7GOK9TDR7VZhJQAbCc",
    authDomain: "passwordmanager-335804.firebaseapp.com",
    projectId: "passwordmanager-335804",
    storageBucket: "passwordmanager-335804.appspot.com",
    messagingSenderId: "447082302868",
    appId: "1:447082302868:web:05d14c2a86b8878517d381",
    measurementId: "G-KS0QDPY0GL"
};

export function getFirebaseConfig() {
    if (!firebaseConfig || !firebaseConfig.apiKey) {
        throw new Error('No Firebase configuration object provided.' + '\n' +
            'Add your web app\'s configuration object to firebase-config.js');
    } else {
        return firebaseConfig;
    }
}