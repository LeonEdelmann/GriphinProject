let email_answer = document.getElementById('email');
let username_answer = document.getElementById('username');
let name_answer = document.getElementById('name');
let birthday_answer = document.getElementById('birthday');
let info_answer = document.getElementById('info');
let password_answer = document.getElementById('password');
let password2_answer = document.getElementById('password2');
let errorField = document.getElementById('error');

function signup() {
    let email = email_answer.value;
    let username = username_answer.value;
    let name = name_answer.value;
    let birthday = birthday_answer.value;
    let info = info_answer.value;
    let password = password_answer.value;
    let password2 = password2_answer.value;

    if (email == '' || username == '' || name == '' || birthday == '' || password == '' || password2 == '') {
        console.log(email, username, name, birthday, password, password2);
        errorField.innerText = 'Es sind nicht alle Felder ausgefüllt.';
        return;
    }

    if (password != password2) {
        errorField.innerText = 'Passwort ist falsch wiederholt worden.';
        return;
    }

    let account = {
        username: username,
        name: name,
        email: email,
        password: sha256(password),
        birthday: birthday,
        info: info
    }
    let options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(account)
    };

    fetch('/signup', options)
        .then(response => response.json()) 
        .then(result => {
            if (result == "Account written") {
                window.location.href = "/login";
            } else {
                errorField.innerText = result;
            }
        })
}