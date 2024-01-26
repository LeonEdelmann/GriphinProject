let errorField = document.getElementById('error');

function login() {
    let usernameInput = document.getElementById('username');
    let passwordInput = document.getElementById('password');

    let username = usernameInput.value;
    let password = passwordInput.value;
    
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
            if (result == 'Nutzername oder Passwort falsch.') {
                errorField.innerHTML += result;
            } else {
                console.log('OK');
            }
        });
    }
}