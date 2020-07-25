

$(document).ready(function() {
	$("[id^='div_id_password'] a").on('click', function(event) {
		event.preventDefault();
		console.log("click test");
		if($("[id^='div_id_password'] input").attr("type") == "text"){
			$("[id^='div_id_password'] input").attr('type', 'password');
			$("[id^='div_id_password'] a").addClass( "mdi-eye-off" );
			$("[id^='div_id_password'] a").removeClass( "mdi-eye" );
		}else if($("[id^='div_id_password'] input").attr("type") == "password"){
			$("[id^='div_id_password'] input").attr('type', 'text');
			$("[id^='div_id_password'] a").removeClass( "mdi-eye-off" );
			$("[id^='div_id_password'] a").addClass( "mdi-eye" );
		}
	});
});