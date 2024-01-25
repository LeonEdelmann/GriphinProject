// Ist nur zum test 
// ignorieren!!

function send() {
    let account = {
        id: "id",
        username: "Linusderdepp",
        name: "Linus",
        email: "linus@idiot.de",
        password: "test123",
        age: 16,
        birthday: "7.7.2007", // i guess
        profile_pic: 'img/bild.jpg',
        info: 'Dumm'
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
                window.location.href = "/";
            } else {
                errorField.innerText = result;
            }
        })
}