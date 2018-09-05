class LIB {
	async get (url) {
		const response = await fetch (url);
		const responseData = await response.json();
		return responseData;
	}
}

class USERS {

	async get(user_n) {
		const user = await fetch (`http://127.0.0.1:5000/user/sing/${user_n}`)
		const result = await user.json();

		return {
			result  
		}
	}
}