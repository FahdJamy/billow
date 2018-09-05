let msgGetter = new apiLIB;
recepient = document.getElementById('receiver');

msgs = '';


msgGetter.get(`http://127.0.0.1:5000/messages/wow`).then( data => {
	console.log(data);
});