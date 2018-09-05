// $(document).ready(function() {

// 	$('form').on('submit', function(e) {
// 		console.log('x: number');
// 		$.ajax({
// 			data : {message : $('#msgInput').val()},
// 			type : 'POST',
// 			url : '/messages'
// 		}).done(function(data) {
// 			if (data.error) {
// 				$('#errorAlert').text(data.error).show();
// 				$('#successAlert').hide();
// 			} else {
// 				$('#successAlert').text(data.message).show();
// 				$('#errorAlert').hide();
// 			}
// 		});
// 		e.preventDefault();
// 	});

// });

// let socket = io.connect('http://127.0.0.1:5000/messages')
// socket.on('connect', () => {
// 	socket.emit('my_event', {
// 		connected_user : 'User connected'
// 	});
// });

// var form = $('form').on('submit', (e) => {
// 	let msg = $('#msgInput').val();
// 	let username = $('#nameinput').val();
// 	console.log(msg, username);
// 	e.preventDefault();
// });

// const messageGetter = new apiLIB;
// recepient = document.getElementById('receiver')

// messageGetter.get(`http://127.0.0.1:5000/messages/${recepient}`).then( data => {
// 	console.log(data);
// })