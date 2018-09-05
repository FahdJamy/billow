class Interface {
	constructor () {
		this.user = document.getElementById('profile')
	}

	showFoundUser (user) {
		console.log(user);
		this.user.innerHTML = `
			<div class="form-group">
				<img src="../static/profilePics/profile.PNG" alt="profile" class="rounded-circle" style="width : 50px; height : 50px;">
				<span class="text-center text-primary">${user.user}</span>
			</div>
		`
	}

	clearUserProf () {
		this.user.innerHTML = '';
	}
}