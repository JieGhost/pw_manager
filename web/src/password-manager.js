import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged, signInWithPopup, GoogleAuthProvider, signOut, getIdToken } from "firebase/auth";
import { getFirebaseConfig } from './firebase-config.js';

// var base_url = 'https://passwordmanager-335804.uk.r.appspot.com/';
var base_url = 'http://127.0.0.1:8080/'

var store_url = base_url + 'store';
var retrieve_url = base_url + 'retrieve';
var list_url = base_url + 'list_domains';

// Adds a size to Google Profile pics URLs.
function addSizeToGoogleProfilePic(url) {
    if (url.indexOf('googleusercontent.com') !== -1 && url.indexOf('?') === -1) {
        return url + '?sz=150';
    }
    return url;
}

function handleSignIn() {
    if (!getAuth().currentUser) {
        const provider = new GoogleAuthProvider();
        // provider.addScope('https://www.googleapis.com/auth/contacts.readonly');
        signInWithPopup(getAuth(), provider).then((result) => {
            console.log('successfully signed in');
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
    }
}

function handleSignOut() {
    if (getAuth().currentUser) {
        signOut(getAuth());
    }
}

async function handleStore(e) {
    // TODO:
    // 1. encrypt password
    // 2. disable form and button while waiting for the response.
    e.preventDefault();
    if (domainInputElement.value && usernameInputElement.value && passwordInputElement.value) {
        var form_data = new FormData();
        form_data.append('domain', domainInputElement.value);
        form_data.append('username', usernameInputElement.value);
        form_data.append('encrypted_password', passwordInputElement.value);
        var idToken = await getIdToken(getAuth().currentUser);
        fetch(store_url, {
            method: 'POST',
            body: form_data,
            mode: 'cors',
            headers: {
                Authorization: 'Bearer ' + idToken
            }
        }).then(response => {
            if (!response.ok) {
                console.log('store failed');
            } else {
                console.log('successfully stored...');
            }
            domainInputElement.value = '';
            usernameInputElement.value = ''
            passwordInputElement.value = '';
            return response.text();
        }).then(response_text => {
            console.log(response_text);
        }).catch(err => { console.error(err); });
    } else {
        console.log('missing input...');
        domainInputElement.value = '';
        usernameInputElement.value = ''
        passwordInputElement.value = '';
    }
}

function handleRetrieve(e) {
    e.preventDefault();
}

async function handleList() {
    var idToken = await getIdToken(getAuth().currentUser);
    fetch(list_url, { mode: 'cors', headers: { Authorization: 'Bearer ' + idToken } }).then(response => {
        if (!response.ok) {
            console.log('list failed');
            console.log(response);
        } else {
            console.log('successfully listed...');
        }
        return response.text();
    }).then(response_text => {
        console.log(response_text);
    }).catch(err => { console.error(err); });
}

// async function getToken() {
//     var idToken = await getIdToken(getAuth().currentUser);
//     console.log(`the token type: ${typeof idToken}`);
//     document.cookie = 'token=' + idToken + '; SameSite=None; domain=127.0.0.1:8080; path=/; Secure';
//     console.log(document.cookie);
//     document.getElementById('quickstart-oauthtoken').textContent = idToken;
// }

function initApp() {
    // Listening for auth state changes.
    onAuthStateChanged(getAuth(), (user) => {
        if (user) {
            var profilePicUrl = (user.photoURL || '/profile_placeholder.png');
            var displayName = user.displayName;

            // Set the user's profile pic and name.
            userPicElement.style.backgroundImage = 'url(' + addSizeToGoogleProfilePic(profilePicUrl) + ')';
            userNameElement.textContent = displayName;

            // Show user's profile and sign-out button.
            userNameElement.removeAttribute('hidden');
            userPicElement.removeAttribute('hidden');
            signOutButtonElement.removeAttribute('hidden');

            // Hide sign-in button.
            signInButtonElement.setAttribute('hidden', 'true');

            // Show
            loginInfoFormElement.removeAttribute('hidden');
            retrieveFormElement.removeAttribute('hidden');
            listButtonElement.removeAttribute('hidden');

            // User is signed in.
            document.getElementById('quickstart-sign-in-status').textContent = 'Signed in';
            document.getElementById('quickstart-account-details').textContent = JSON.stringify(user, null, '  ');
        } else {
            // Hide user's profile and sign-out button.
            userNameElement.setAttribute('hidden', 'true');
            userPicElement.setAttribute('hidden', 'true');
            signOutButtonElement.setAttribute('hidden', 'true');

            // Show sign-in button.
            signInButtonElement.removeAttribute('hidden');

            // Hide
            loginInfoFormElement.setAttribute('hidden', 'true');
            retrieveFormElement.setAttribute('hidden', 'true');
            listButtonElement.setAttribute('hidden', 'true');

            // User is signed out.
            document.getElementById('quickstart-sign-in-status').textContent = 'Signed out';
            document.getElementById('quickstart-account-details').textContent = 'null';
            document.getElementById('quickstart-oauthtoken').textContent = 'null';
        }
    });
}

var userPicElement = document.getElementById('user-pic');
var userNameElement = document.getElementById('user-name');
var signInButtonElement = document.getElementById('sign-in');
var signOutButtonElement = document.getElementById('sign-out');

var loginInfoFormElement = document.getElementById('login-info-form');
var domainInputElement = document.getElementById('store-domain');
var usernameInputElement = document.getElementById('store-username');
var passwordInputElement = document.getElementById('store-password');

var retrieveFormElement = document.getElementById('retrieve-form');
var retrieveInfoElement = document.getElementById('get-domain');

var listButtonElement = document.getElementById('list-button')

signInButtonElement.addEventListener('click', handleSignIn, false);
signOutButtonElement.addEventListener('click', handleSignOut, false);

loginInfoFormElement.addEventListener('submit', handleStore, false);
retrieveFormElement.addEventListener('submit', handleRetrieve, false);

listButtonElement.addEventListener('click', handleList, false);

// Initialize Firebase App
const firebaseApp = initializeApp(getFirebaseConfig());

initApp();