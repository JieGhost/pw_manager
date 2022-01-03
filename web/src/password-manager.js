import { initializeApp } from "firebase/app";
import { getAuth, onAuthStateChanged, signInWithPopup, GoogleAuthProvider, signOut, getIdToken } from "firebase/auth";
import { getFirebaseConfig } from './firebase-config.js';

var base_url = 'https://passwordmanager-335804.uk.r.appspot.com/';
// var base_url = 'http://127.0.0.1:8080/'

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

function handleSignIn(e) {
    e.preventDefault();
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

function handleSignOut(e) {
    e.preventDefault();
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
                needFetchDomains = true;
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

async function fetchDomainsList() {
    var idToken = await getIdToken(getAuth().currentUser);
    logToken(idToken);
    fetch(list_url, { mode: 'cors', headers: { Authorization: 'Bearer ' + idToken } }).then(response => {
        if (!response.ok) {
            console.log('list failed');
            console.log(response);
        } else {
            console.log('successfully listed...');
        }
        return response.text();
    }).then(response_text => {
        presentDomains(response_text);
        needFetchDomains = false;
    }).catch(err => { console.error(err); });
}

function presentDomains(domainsStr) {
    var domainsArray = domainsStr.split(';');
    // Clear old content.
    clearDomains();
    // List new content.
    domainsArray.forEach(domain => {
        var li = document.createElement("li");
        var a = document.createElement("button");
        a.textContent = domain;
        li.appendChild(a);
        domainsListElement.appendChild(li);
    });
}

function clearDomains() {
    while (domainsListElement.firstChild) {
        domainsListElement.removeChild(domainsListElement.lastChild);
    }
}

function logToken(idToken) {
    console.log(`the id token type: ${typeof idToken}`);
    console.log(`the id token: ${idToken}`);
}

function handleSidebarCollapse() {
    sidebarElement.classList.toggle('active');
}

function handleDomainsButton(e) {
    e.preventDefault();
    domainsListElement.removeAttribute('hidden');
    inputFormElement.setAttribute('hidden', true);
    if (!needFetchDomains) {
        return;
    }

    fetchDomainsList();
}

function handleStorePasswordButton(e) {
    e.preventDefault();
    domainsListElement.setAttribute('hidden', true);
    inputFormElement.removeAttribute('hidden');
}

function handleSupportButton(e) {
    e.preventDefault();
}

function initApp() {
    // Listening for auth state changes.
    onAuthStateChanged(getAuth(), (user) => {
        if (user) {
            console.log('user id: ' + user.uid);
            var profilePicUrl = (user.photoURL || '/profile_placeholder.png');
            var displayName = user.displayName;

            // // Set the user's profile pic and name.
            // userPicElement.style.backgroundImage = 'url(' + addSizeToGoogleProfilePic(profilePicUrl) + ')';
            // userNameElement.textContent = displayName;

            // // Show user's profile and sign-out button.
            // userNameElement.removeAttribute('hidden');
            // userPicElement.removeAttribute('hidden');
            // signOutButtonElement.removeAttribute('hidden');
            usernameElement.textContent = user.displayName;

            // Hide sign-in button.
            signInItemElement.setAttribute('hidden', 'true');

            // Show buttons
            domainsItemElement.removeAttribute('hidden');
            storePasswordItemElement.removeAttribute('hidden');
            supportItemElement.removeAttribute('hidden');
            signOutItemElement.removeAttribute('hidden');

            domainsListElement.removeAttribute('hidden');
            inputFormElement.setAttribute('hidden', true);
            fetchDomainsList();
        } else {
            // // Hide user's profile and sign-out button.
            // userNameElement.setAttribute('hidden', 'true');
            // userPicElement.setAttribute('hidden', 'true');
            // signOutButtonElement.setAttribute('hidden', 'true');
            usernameElement.textContent = 'Not Signed in';

            // Show sign-in button.
            signInItemElement.removeAttribute('hidden');

            // Hide buttons.
            domainsItemElement.setAttribute('hidden', 'true');
            storePasswordItemElement.setAttribute('hidden', 'true');
            supportItemElement.setAttribute('hidden', 'true');
            signOutItemElement.setAttribute('hidden', 'true');

            domainsListElement.setAttribute('hidden', true);
            inputFormElement.setAttribute('hidden', true);
            clearDomains();
        }
    });
}

// -------------------------------------------------------------------------------

// Declare module-level variables.
var needFetchDomains = false;

// Declare html tag elements.
var sidebarCollapseButtonElement = document.getElementById('sidebar-collapse');
var sidebarElement = document.getElementById('sidebar');

var usernameElement = document.getElementById('username');

var signInItemElement = document.getElementById('sign-in-item');
var signInButtonElement = document.getElementById('sign-in-button');
var domainsItemElement = document.getElementById('domains-item');
var domainsButtonElement = document.getElementById('domains-button');
var storePasswordItemElement = document.getElementById('store-password-item');
var storePasswordButtonElement = document.getElementById('store-password-button');
var supportItemElement = document.getElementById('support-item');
var supportButtonElement = document.getElementById('support-button');
var signOutItemElement = document.getElementById('sign-out-item');
var signOutButtonElement = document.getElementById('sign-out-button');

var domainsListElement = document.getElementById('domains-list');

var inputFormElement = document.getElementById('input-form');
var domainInputElement = document.getElementById('input-domain');
var usernameInputElement = document.getElementById('input-username');
var passwordInputElement = document.getElementById('input-password');

// -------------------------------------------------------------------------------

// Register event listners
sidebarCollapseButtonElement.addEventListener('click', handleSidebarCollapse, false);

signInButtonElement.addEventListener('click', handleSignIn, false);
signOutButtonElement.addEventListener('click', handleSignOut, false);

domainsButtonElement.addEventListener('click', handleDomainsButton, false);
storePasswordButtonElement.addEventListener('click', handleStorePasswordButton, false);

supportButtonElement.addEventListener('click', handleSupportButton, false);

inputFormElement.addEventListener('submit', handleStore, false);

// -------------------------------------------------------------------------------

// // Declare old elements



// var retrieveFormElement = document.getElementById('retrieve-form');
// var retrieveInfoElement = document.getElementById('get-domain');

// var listButtonElement = document.getElementById('list-button')

// //
// retrieveFormElement.addEventListener('submit', handleRetrieve, false);

// -------------------------------------------------------------------------------

// Initialize Firebase App
const firebaseApp = initializeApp(getFirebaseConfig());

initApp();