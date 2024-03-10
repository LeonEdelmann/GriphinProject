let message_input = document.getElementById('message');
let h2 = document.getElementById('h2');
let own_profile_pic = document.getElementById('own_pic');
let chat_pic = document.getElementById('chat-pic');
let contact_list = document.getElementById('list');
let contact_base = '<div class="contact" onclick="loadchat()">' +
                    '<div class="profile-pic">' +
                    '<img src="" alt="">"' + 
                    '</div>' + 
                    '<div class="p-name">' +
                    '<font class="profile-name">Nutzername</font>' +
                    '</div>' +
                    '</div>';
let base_right = '<div class="right">' +
                '<div class="message a">' +
                '</div>' +
                '<div class="status">' +
                '<font>Gesendet: 10.3.2024 12:38</font>' +
                '<font>Gelesen</font>' +
                '</div>';
let base_left = '<div class="left">' +
                '<div class="message b">' + 
                '</div>' + 
                '<div class="status">' + 
                '<font>Gesendet: 10.3.2024 12:38</font>' +
                '</div>' + 
                '</div>';
let chatjson = {};


function loadOwnProfile() {
    window.location.href = '/user/' + chatjson.own_account.own_name;
}

function send() {

}

function loadName(username) {
    window.location.href = '/user/' + username;
}

function loadchat(contact) {

}

function buildPage() {
    own_profile_pic.src = "../static/imgs/" + chatjson.own_account.own_profile_pic;
    let chats = chatjson.chats;
    chats.forEach(element => {
        contact_list.innerHTML += '<div class="contact" onclick="loadchat(' + element[1] + ')">' +
        '<div class="profile-pic">' +
        '<img src="' + 'static/imgs/' + element[0] + '" alt="">"' + 
        '</div>' + 
        '<div class="p-name">' +
        '<font class="profile-name">' + element[1] + '</font>' +
        '</div>' +
        '</div>';
    });
    h2.innerText = chats[0][1];
    h2.setAttribute('onclick', "loadName('" + chats[0][1] + "')");
    chat_pic.src = "../static/imgs/" + chatjson.chats[0][0];
}

function scrollToBottom() {
    var container = document.getElementById('messages');
    container.scrollTop = container.scrollHeight;
}

window.onload = function() {
    scrollToBottom();
};
async function getJSON() {
    fetch('/chatjson')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        chatjson = data;
        console.log(chatjson);
        buildPage();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
getJSON()