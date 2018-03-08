function verify() {
	document.getElementById("verify_loading").style.visibility = "visible";
	var form = document.getElementById('verify'),
		data = new FormData(form);
	$.ajax
	({
		url: 'http://localhost:2333/verify',
		type: 'post',
		data: data,
		processData: false,
		contentType: false,
		success:
			async function(response){
				document.getElementById("verify_loading").style.visibility = "hidden";
				if (response == "0") {
					var data = {message: '验证成功'};
				}
				else {
					var data = {message: '验证不成功'};
				}
				var snackbarContainer = document.querySelector('#toast');
				var showToastButton = document.querySelector('#verify_button');
				snackbarContainer.MaterialSnackbar.showSnackbar(data);
				if (response == "0") {
					await sleep(1000);
					location.reload();
				}
				else {
					document.getElementById("cookie").select();
				}
			},
		error:
			function(error){
				document.getElementById("verify_loading").style.visibility = "hidden";
				var data = {message: '未知错误'};
				var snackbarContainer = document.querySelector('#toast');
				var showToastButton = document.querySelector('#verify_button');
				snackbarContainer.MaterialSnackbar.showSnackbar(data);
			}
	})
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

async function expand() {
	await sleep(500);
	$("div.mdl-layout__drawer-button").click();
}

function set() {
	var form = document.getElementById('settings'),
		data = new FormData(form);
	var snackbarContainer = document.querySelector('#set_toast');
	var showToastButton = document.querySelector('#set_button');
	$.ajax
	({
		url: 'http://localhost:2333/set',
		type: 'post',
		data: data,
		processData: false,
		contentType: false,
		success:
			function(response){
				if (response == "0") {
					var data = {message: '设定成功'};
					snackbarContainer.MaterialSnackbar.showSnackbar(data);
					document.getElementById('uc_sent').disabled = "disabled";
					document.getElementById('message').disabled = "disabled";
					document.getElementById('set_button').innerHTML = "修改";
					document.getElementById('set_button').setAttribute("onclick", "revert();")
				}
			},
		error:
			function(error){
				var data = {message: '未知错误'};
				snackbarContainer.MaterialSnackbar.showSnackbar(data);
			}
	})
}

function revert() {
	document.getElementById('uc_sent').disabled = "";
	document.getElementById('message').disabled = "";
	document.getElementById('set_button').innerHTML = "设定";
	document.getElementById('set_button').setAttribute("onclick", "set();")
}

function start() {
	var form = document.getElementById('chain'),
		data = new FormData(form);
	var snackbarContainer = document.querySelector('#start_toast');
	var showToastButton = document.querySelector('#start_button');
	$.ajax
	({
		url: 'http://localhost:2333/start',
		type: 'post',
		data: data,
		processData: false,
		contentType: false,
		success:
			function(response){
				if (response == "0") {
					var data = {message: '设定成功'};
					snackbarContainer.MaterialSnackbar.showSnackbar(data);
					document.getElementById('uc_sent').disabled = "disabled";
					document.getElementById('message').disabled = "disabled";
					document.getElementById('set_button').innerHTML = "修改";
					document.getElementById('set_button').setAttribute("onclick", "revert();")
				}
			},
		error:
			function(error){
				var data = {message: '未知错误'};
				snackbarContainer.MaterialSnackbar.showSnackbar(data);
			}
	})
}