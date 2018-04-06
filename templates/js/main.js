'use strict'

//Simple string hashing
//Source: http://werxltd.com/wp/2010/05/13/javascript-implementation-of-javas-string-hashcode-method/
String.prototype.hashCode = function() {
  let hash = 0, i, chr;
  if (this.length === 0) return hash;
  for (i = 0; i < this.length; i++) {
    chr   = this.charCodeAt(i);
    hash  = ((hash << 5) - hash) + chr;
    hash |= 0;
  }
  return hash;
};

const base_url = 'http://127.0.0.1:5000/'

function initUI() {

}

function createPollListItem(title) {
    const title_hash = title.hashCode();

    let li           = $('<li class="list-group-item" />'),
        c_btn        = $('<button class="btn btn-sm float-right collapse-btn" />'),
        title_span   = $('<span/>'),
        c_arrow      = $('<i class="arrow down" />'),
        title_head   = $('<div/>'),
        poll_content = $('<div class="container collapse poll-content" />'),
        poll_dsc_div = $('<div class="poll-description" />'),
        poll_dsc_p   = $('<p/>'),
        poll_stats   = $('<div class="poll-stats" />');

    c_btn.append(c_arrow)
         .click(() => {
            if (c_arrow.hasClass('down')) {
                c_arrow.removeClass('down');
                c_arrow.addClass('up');
            } else {
                c_arrow.removeClass('up');
                c_arrow.addClass('down'); 
            }
         })
         .attr({'data-toggle': 'collapse', 'data-target': '#collapse'+title_hash});
    
    title_span.text(title);

    title_head.append(title_span)
              .append(c_btn);

    poll_dsc_p.text('No description');
    poll_dsc_div.append(poll_dsc_p);
    poll_content.append(poll_dsc_div)
                .append(poll_stats)
                .attr('id', 'collapse'+title_hash);
    li.attr('id', title_hash)
      .append(title_head)
      .append(poll_content);

    return li
}

function genRandWord() {
    let len = randomInt(8,20),
        a09 = 'qwertyuiopasdfghjklzxcvbnm1234567890'.split(''),
        str = '';
    for (let i = 0; i < len; i++) {
        str += a09[randomInt(0, a09.length-1)]
    }
    return str
}

function testAdd() {
    let t = genRandWord();
    $('ul').append(createPollListItem(t));
}


function randomInt(min, max) {
    var rand = Math.round((min - 0.5 + Math.random() * (max - min + 1)));
    return rand;
}

function handleGetBtn() {
    $.getJSON(base_url + 'getBlocks', processGet);
}

function handleCreateBtn() {
    let title = $('#input-title').val(),
        vote  = $('#input-vote').val();
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
    $('#blocks-count').text(data.blocks_count);
    for (let b in data.blocks) {
        if (!$('#block-'+b).text()) {
            $('ul.list-group').append(blockItem(b, data.blocks[b]));
        }
    }
}

initUI();