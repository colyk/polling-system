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

    let li           = $('<li class="list-group-item" loaded="false" />'),
        c_btn        = $('<button class="btn btn-sm float-right collapse-btn" />'),
        title_span   = $('<span/>'),
        c_arrow      = $('<i class="arrow down" />'),
        title_head   = $('<div/>'),
        poll_content = $('<div class="container collapse poll-content" />'),
        poll_dsc_div = $('<div class="poll-description" />'),
        poll_dsc_p   = $('<p/>'),
        poll_stats   = $('<div class="poll-stats" />');

    let pollUpd = () => {
        if (c_arrow.hasClass('down')) {
            c_arrow.removeClass('down');
            c_arrow.addClass('up');
            getPollData(title)
        } else {
            c_arrow.removeClass('up');
            c_arrow.addClass('down'); 
        }
    };
    c_btn.append(c_arrow)
         .click(pollUpd)
         .attr({'data-toggle': 'collapse', 'data-target': '#collapse'+title_hash});
    
    title_span.text(title)
              .attr({'data-toggle': 'collapse', 'data-target': '#collapse'+title_hash})
              .css('cursor', 'pointer')
              .click(pollUpd);

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

function createPollOptions(title, option, count, total_sum) {
    let row      = $('<div class="row poll-ctrl"/>').attr('id', option.hashCode()),
        col_btn  = $('<div class="col-3"/>'),
        col_prog = $('<div class="col"/>'),
        prog_div = $('<div class="progress"/>'),
        prog_bar = $('<div role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" class="progress-bar bg-dark">'),
        vote_btn = $('<button class="btn btn-sm btn-dark"/>').text(option);
    let percent = ((count * 100.0) / total_sum).toFixed(3);

    vote_btn.click(() => {
            let data = JSON.stringify({
                'poll_name': title,
                'vote_for': option
            });
            $.post(base_url+'addVote/', data, (data) => {getPollData(title)}, 'json');
        })
        .appendTo(col_btn);

    prog_bar.attr('aria-valuenow', percent)
            .css('width', percent+'%')
            .text(percent+'%')
            .appendTo(prog_div);

    col_btn.appendTo(row);

    col_prog.append(prog_div)
            .appendTo(row);
    return row
}

function getPolls() {
    $.getJSON(base_url+'getActivePolls/', {}, processGetPolls, 'json')
}

function getPollData(title) {
    let data = JSON.stringify({'poll_name': title});
    $.post(base_url+'getPollInfo/', data, setPollData, 'json')
}

function setPollData(data) {
    console.log(data);
    let h          = data['title'].hashCode(), 
        descr      = data['description'],
        elem       = $('#'+h),
        stats_elem = $('#'+h+' div.poll-content div.poll-stats'),
        descr_elem = $('#'+h+' div.poll-content div.poll-description p'),
        total_sum  = 0;
    for (let c in data['vote_state']) {
        total_sum += data['vote_state'][c];
    }
    if (elem.attr('loaded') === 'false') {
        descr_elem.text(descr);
        for (let opt in data['vote_state']) {
            let option = createPollOptions(data['title'], opt,  data['vote_state'][opt], total_sum);
            stats_elem.append(option);
        }
        elem.attr('loaded', 'true')
    } else {
        for (let opt in data['vote_state']) {

            let opt_hash = opt.hashCode(),
                percent = ((data['vote_state'][opt] * 100.0) / total_sum).toFixed(3),
                progress_elem = $('#'+h+' #'+opt_hash+' .progress-bar');
            progress_elem.css('width', percent+'%')
                         .text(percent+'%');
        }
    }
}



function createPoll(title, description, options) {
    //wip

    let poll_data = {
            'poll_name': title,
            'description': description,
            'options': options
        },
        str_poll_data = JSON.stringify(poll_data);

    $.ajax({
        url: base_url+'createPoll/', 
        type: 'POST', data: str_poll_data, 
        dataType: 'json', 
        success: (data) => {console.log(data); getPolls(); /*process errors in response*/}
    });
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