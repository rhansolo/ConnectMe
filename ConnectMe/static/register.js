const readyButton = document.getElementById('readyButton')
readyButton.disabled = true;
const password = document.getElementById('password')
const confirmPassword = document.getElementById('confirmPassword')
confirmPassword.addEventListener('input', (value) => {
	console.log(confirmPassword.value)
	console.log(password.value)
	readyButton.disabled = !(confirmPassword.value == password.value);
})