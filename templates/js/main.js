'use strict'
const base_url = 'http://127.0.0.1:5000/'

function initUI() {
    $('#get-btn').click(handleGetBtn);
    $('#chk-btn').click(handleCheckBtn);
    $('#create-block-btn').click(handleCreateBtn);
}

function blockItem(index, blockdata) {
    let title = $('<span/>').text('Title: '+blockdata['title'])
                            .addClass('label label-primary'),
        vote = $('<span/>').text('Vote-for: '+blockdata['vote_for'])
                           .addClass('label label-primary'),
        li = $('<li/>').addClass('list-group-item')
                       .attr('id', 'block-'+index)
                       .append(title)
                       .append(vote)
                       .append($('<span/>').text(index).addClass('badge float-right'));
    return li
}

function handleGetBtn() {
    $.getJSON(base_url + 'getBlocks', processGet);
}

function handleCreateBtn() {
    let title = $('#input-title').val(),
        vote = $('#input-vote').val();
    if (title && vote) {
        $.post(base_url+'addBlock', {'title': title, 'vote': vote}, (data) => {
                        $('#input-title').val('');
                        $('#input-vote').val('');
                        handleGetBtn();
                        console.log('response: '+data)
                    });
    }

}

function handleCheckBtn() {
    alert('not available');
}

function processGet(data) {
    console.log(data);
    $('#blocks-count').text(data.blocks_count)
    let ptext = ''
    for (let b in data.blocks) {
        if (!$('#block-'+b).text()) {
            $('ul.list-group').append(blockItem(b, data.blocks[b]));
        }
    }
}

initUI();