const sendButton = document.getElementById('messageBox')
const messagesDiv = document.getElementById('messages')
const messageInput = document.getElementById('messageBox')

sendButton.addEventListener('click', () => {
	messagesDiv.innerHTML += createMessageHTML(messageInput.value)
	messageInput.value = ""
})

const createMessageHTML = (message) => `
	<div class="container darker">
		  <img src="https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2017/05/12/104466932-PE_Color.240x240.jpg?v=1494613853" alt="Avatar" class="right">
		  <p>${message}</p>
		  <span class="time-left">11:01</span>
		</div>
`

