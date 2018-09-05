let msgGetter = new LIB;
let users = new LIB;
const singleUser = new USERS;
const interface = new Interface;


msgGetter.get(`http://127.0.0.1:5000/user/msgs`)
	.then( data => console.log(data))
	.catch(err => console.log(err));

users.get('http://127.0.0.1:5000/users/all')
	.then( data => console.log(data))
	.catch(err => console.log(err));

let searchUser = document.getElementById('findUser');
searchUser.addEventListener('keyup', (e) => {
	searchValue = e.target.value;
	console.log(searchValue)

	if (searchValue !== '') {
		singleUser.get(searchValue)
			.then( data => {
				if (data.result.message === 'No User Found') {
					console.log('No user found');
				} else {
					interface.showFoundUser(data.result)
				}
			})
			.then( err => console.log(err));
	} else {
		interface.clearUserProf();
	}
});