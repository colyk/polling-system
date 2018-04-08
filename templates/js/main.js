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
    $('#get-polls-btn').click(getPolls);
    $('#test-crt-btn').click(testAdd);
}

function createPollListItem(title) {
    const title_hash = title.hashCode();

    let li           = $('<li class="list-group-item" />'),
        c_btn        = $('<button class="btn btn-sm float-right collapse-btn" />'),
        title_span   = $('<span/>'),
        c_arrow      = $('<i id="l"class="arrow down" />'),
        title_head   = $('<div/>'),
        poll_content = $('<div class="container collapse poll-content" />'),
        poll_dsc_div = $('<div class="poll-description" />'),
        poll_dsc_p   = $('<p/>'),
        poll_stats   = $('<div class="poll-stats" />');

    let changeArrow = function() {
        if (c_arrow.hasClass('down')) {
            c_arrow.removeClass('down');
            c_arrow.addClass('up');
        } else {
            c_arrow.removeClass('up');
            c_arrow.addClass('down'); 
        }
    }
    c_btn.append(c_arrow)
         .click(changeArrow)
         .attr({'data-toggle': 'collapse', 'data-target': '#collapse'+title_hash});
    
    title_span.text(title)
              .attr({'data-toggle': 'collapse', 'data-target': '#collapse'+title_hash})
              .css('cursor', 'pointer')
              .click(changeArrow);

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

function getPolls() {
    $.getJSON(base_url+'getActivePolls/', {}, processGetPolls, 'json')
}


function getPollInfo(title) {

}

function createPoll(title, description, options) {
    //wip

    let poll_data = {
            'poll_name': title,
            'description': description,
            'options': options
        },
        str_poll_data = JSON.stringify(poll_data);
    

    $.ajax({url: base_url+'createPoll/', type: 'POST', data: str_poll_data, dataType: 'json', success: (data) => {console.log(data); getPolls();}, contentType: 'application/json'});
    console.log(poll_data);
    return poll_data
}

function genRandWord(len) {
    len = len ? len : randomInt(5,20);
    let a09 = 'qwertyuiopasdfghjklzxcvbnm 1234567890'.split(''),
        str = '';
    for (let i = 0; i < len; i++) {
        str += a09[randomInt(0, a09.length-1)]
    }
    return str
}

function testAdd() {
    let t = genRandWord(),
        d = genRandWord(75),
        o = [genRandWord(), genRandWord(), genRandWord()];
    createPoll(t, d, o);
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

function processGetPolls(data) {
    console.log(data);
    $('#polls-count').text(data['polls'].length);
    for (let n in data['polls']) {
        let t = data['polls'][n],
            h = t.hashCode();
        if (!$('li#'+h).length) {
            $('#polls-panel ul').append(createPollListItem(t));
        }
    }
}

initUI();
