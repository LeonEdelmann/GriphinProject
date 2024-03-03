let friend_request_button = document.getElementById('friendbutton');
let edit_profile_button = document.getElementById('editprofilebutton');
let message_send_button = document.getElementById('messagesendbutton');
let change_password_button = document.getElementById('changepasswordbutton');
let logout_button = document.getElementById('logoutbutton');
let image = document.getElementById('image');
let edit_profilepic_area = document.getElementById('profilepicarea');
let usernameh1 = document.getElementById('username');
let description = document.getElementById('description');
let friends = document.getElementById('friends');
let founded = document.getElementById('madeCom');
let member = document.getElementById('enteredCom');
let friendsN = document.getElementById('friendsN');
let foundedN = document.getElementById('madeComN');
let memberN = document.getElementById('enteredComN');
let title = document.getElementById('title');
let search_bar = document.getElementById('search-bar');
let content = document.getElementById('content');
let tap = document.getElementById('tap');
let change_pic = document.getElementById('change-pic');
let change = document.getElementById('change');
let edit = document.getElementById('edit');
let new_name = document.getElementById('new_username');
let new_description = document.getElementById('new_description');
let new_email = document.getElementById('new_email');

let currentURL = window.location.href;
let array = currentURL.split('/');
let username = array[array.length - 1];
let userstats = {};

function cancel_edit() {
    edit.style.display = 'none';
}

function cancel() {
    change_pic.setAttribute("hidden", true);
    change.style.display = 'block';
}

function submit() {

}

function edit_profile_pic() {
    change_pic.removeAttribute("hidden");
    change.style.display = 'none';
}

function add_friend() {

}

function send_message() {

}

function edit_profile() {
    edit.style.display = 'flex';
    new_name.value = userstats.username;
    new_description.value = userstats.info;
    new_email.value = userstats.email;
}

function changePassword() {

}

function search() {

}

function changeh3(topic) {
    title.innerText = topic + ':';
    search_bar.placeholder = 'In ' + topic + ' suchen...';
}

function logout() {
    window.location.href = '/logout';
}

function writeInfos() {
    usernameh1.innerText = userstats.username;
    description.innerText = userstats.info;
    friendsN.innerText = userstats.friends;
    foundedN.innerText = userstats.foundedcoms;
    memberN.innerText = userstats.membernum;
    image.src = "../static/imgs/" + userstats.profile_pic;
    tap.innerText += userstats.username;
}

function setRights() {
    if (userstats.rights == 'Yes') {
        friend_request_button.style.display = "none";
        message_send_button.style.display = "none";
    } else {
        edit_profile_button.style.display = "none";
        change_password_button.style.display = "none";
        logout_button.style.display = "none";
        edit_profilepic_area.style.display = "none";
    }
    writeInfos();
}

async function getAccount() {
    fetch('/getuser/' + username)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            userstats = data;
            console.log(userstats);
            setRights();
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}
getAccount();