import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged, signInWithPopup, GoogleAuthProvider, signOut, getIdToken } from "firebase/auth";
import { getFirebaseConfig } from './firebase-config.js';

function toggleSignIn() {
    const auth = getAuth();
    if (!auth.currentUser) {
        const provider = new GoogleAuthProvider();
        // provider.addScope('https://www.googleapis.com/auth/contacts.readonly');
        signInWithPopup(auth, provider).then((result) => {
            // // This gives you a Google Access Token. You can use it to access the Google API.
            // var token = result.credential.accessToken;
            // // The signed-in user info.
            // var user = result.user;
            // document.getElementById('quickstart-oauthtoken').textContent = user.email;
            // user.getIdToken().then((id_token) => { document.getElementById('quickstart-oauthtoken').textContent = id_token; })
        }).catch((error) => {
            // Handle Errors here.
            var errorCode = error.code;
            var errorMessage = error.message;
            // The email of the user's account used.
            var email = error.email;
            // The firebase.auth.AuthCredential type that was used.
            var credential = error.credential;
            if (errorCode === 'auth/account-exists-with-different-credential') {
                alert('You have already signed up with a different auth provider for that email.');
                // If you are using multiple auth providers on your app you should handle linking
                // the user's accounts here.
            } else {
                console.error(error);
            }
        });
    } else {
        signOut(auth);
    }
    document.getElementById('quickstart-sign-in').disabled = true;
}

async function getToken() {
    document.getElementById('quickstart-oauthtoken').textContent = await getIdToken(getAuth().currentUser);
}

function initApp() {
    // Listening for auth state changes.
    onAuthStateChanged(getAuth(), (user) => {
        if (user) {
            // User is signed in.
            var displayName = user.displayName;
            var email = user.email;
            var emailVerified = user.emailVerified;
            var photoURL = user.photoURL;
            var isAnonymous = user.isAnonymous;
            var uid = user.uid;
            var providerData = user.providerData;
            document.getElementById('quickstart-sign-in-status').textContent = 'Signed in';
            document.getElementById('quickstart-sign-in').textContent = 'Sign out';
            document.getElementById('quickstart-account-details').textContent = JSON.stringify(user, null, '  ');
            getToken();
            // user.getIdToken().then((id_token) => { document.getElementById('quickstart-oauthtoken').textContent = id_token; });
        } else {
            // User is signed out.
            document.getElementById('quickstart-sign-in-status').textContent = 'Signed out';
            document.getElementById('quickstart-sign-in').textContent = 'Sign in with Google:)';
            document.getElementById('quickstart-account-details').textContent = 'null';
            document.getElementById('quickstart-oauthtoken').textContent = 'null';
        }
        document.getElementById('quickstart-sign-in').disabled = false;
    });

    document.getElementById('quickstart-sign-in').addEventListener('click', toggleSignIn, false);
}

// Initialize Firebase App
const firebaseApp = initializeApp(getFirebaseConfig());

initApp();