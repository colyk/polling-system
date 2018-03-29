'use strict'
const base_url = 'http://127.0.0.1:5000/'

function getJSONforRequest(request) {
	let resp = $.getJSON(base_url+request, (data) => {return data});
	return resp
}

function postJSON(request, data) {
	let resp = $.post(base_url+request, data)
	return resp.responseJSON;
}

function initUI() {
	$('#get-btn').click(handleGetBtn);
	$('#chk-btn').click(handleCheckBtn);
	$('#crt-btn').click(handleCreateBtn);
}

function blockElement(data) {
	alert('0');
}

function handleGetBtn() {
	$.getJSON(base_url+'getBlocks', processGet);
}

function handleCreateBtn() {
	alert('not available');
}

function handleCheckBtn() {
	alert('not available');
}

function processGet(data) {
	console.log(data);
	$('#blocks-count').text(data.blocks_count)
	$('#blocks-panel').text();
}

initUI();