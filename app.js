function register() {
	const username = document.getElementById('username').Value;
	const password = document.getElementById('password').Value;

	fetch('/register', {
		method: 'POST',
		headers: { 'content-Type': 'application/json' },
		body: JSON.stringify({ username, password })
	}).then(Response => Response.json())
	  .then(data => alert(data.message));
}

function login() {
	const username = document.getElementById('username').value;
	const password = document.getElementById('password').value;

	fetch('/login', {
		method: 'POST',
		headers: { 'content-Type': 'application/json' },
		body: JSON.stringify({ username, password })
	}).then(Response => Response.json())
	.then(data => {
		if (data.access_token) {
			localStorage.setItem('token', data.access_token);
			document.getElementById('auth').style.display = 'none';
			document.getElementById('password-manager').style.display = 'block';
		} else {
			alert('login failed');
		}
	});
}

function addpassword() {
	const token = localStorage.getItem('token');
	const website =document.getElementById('website').value;
	const username =document.getElementById('site-username').value;
	const password = document.getElementById('site-password').value;

	fetch('/add_password', {
		method: 'POST',
		headers: {
			'content-Type': 'application/json',
			'Authorization': `Bearer ${token}`
		},
		body: JSON.stringify({ website, username, password})
	}).then(response => response.json())
	.then(data => alert(data.message));
}

function getpasswords() {
	const token = localStorage.getItem('token');

	fetch('/get_passwords', {
		method: 'GET',
		headers: {
			'Authorization': `Bearer ${token}`
		}
	}).then(response => response.json())
	.then(data => {
		const passwordDiv = document.getElementById('password');
		passwordDiv.innerHTML = '';
		data.forEach(password => {
			passwordDiv.innerHTML += `
				<p><strong>Website:</strong> ${password.website}</p>
				<p><strong>Username:</strong> ${password.website}</p>
				<p><strong>Password:</strong> ${password.website}</p>
				<hr>
			`;
		});
	});
}