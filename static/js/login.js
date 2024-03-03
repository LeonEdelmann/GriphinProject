let errorField = document.getElementById('error');

function login() {
    let usernameInput = document.getElementById('username');
    let passwordInput = document.getElementById('password');

    let username = usernameInput.value;
    let password = sha256(passwordInput.value);
    
    if (username == '' || password == '') {
        errorField.innerHTML += 'Nutzername oder Passwort eingeben';
    } else {

    let loginData = {
        username: username,
        password: password
    }

    let options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
    };

    fetch('/login', options)
        .then(response => response.json()) 
        .then(result => {
            if (result == 'Nutzername oder Passwort falsch.' || result == 'Zu viele Fehlversuche') {
                errorField.innerHTML = result;
            } else if (result == 'OK'){
                window.location.href = "/home";
            }
        });
    }
}