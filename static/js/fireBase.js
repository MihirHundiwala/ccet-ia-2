// var firebaseConfig = {
//     apiKey: "AIzaSyBytnj22REer1KkXEh7hE3n-UEaWbd4Cko",
//     authDomain: "t-space-1616840866880.firebaseapp.com"
// };

// Initialize Firebase
// firebase.initializeApp(firebaseConfig);

// function googlelogin(){
//     let provider = new firebase.auth.GoogleAuthProvider()
//     firebase.auth().signInWithPopup(provider).then((response)=>{
//         let user = response.user
//         let email =  user.email
//         let provider = "google"
//         let token = user.xa
//         console.log(token)
//         if(token!=null || token!=undefined || token!=""){
//             window.location = "/signinwithgoogle?email="+email
//         }
//     }).catch((error)=>{
//         console.log(error)
//     })
// }

// <script src="https://www.gstatic.com/firebasejs/7.10.0/firebase-app.js"></script>
// <script src="https://www.gstatic.com/firebasejs/7.10.0/firebase-auth.js"></script>