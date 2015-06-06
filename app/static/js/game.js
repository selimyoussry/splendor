var MIN_NUMBER_OF_TOKENS_FOR_DOUBLE_PICK = 4;
var COLORS_NO_YELLOW = ['blue', 'black', 'green', 'red', 'white'];
var COLORS = ['blue', 'black', 'green', 'red', 'white', 'yellow'];
var MAX_N_RESERVED_CARDS = 3;
var BUY_CLASS = 'table-card-ready-to-buy';
var RESERVE_CLASS = 'table-card-ready-to-reserve';

// BUY TOKENS
//////////////////////////
//////////////////////////
//////////////////////////
//////////////////////////


function pick_token(color){

    var i_can_take_the_token = can_take_token(color);
    if(i_can_take_the_token){
        reset_table_cards();
        $('#table-token-' + color).html(get_n_tokens_picked(color) + 1);
    }

}

function get_n_tokens_on_table(color){
    var element = $('#table-token-' + color + '-n-on-table');
    return element.length ? parseInt(element.html()) : 0;
}

function get_n_tokens_picked(color){
    var element = $('#table-token-' + color);
    return element.length ? parseInt(element.html()) : 0;
}

function get_total_picked_tokens(){
    var total_picked = 0;
    for (var i = 0; i < COLORS_NO_YELLOW.length; i++) {
        total_picked += get_n_tokens_picked(COLORS_NO_YELLOW[i]);
    }
    return total_picked;
}

function game_rules_alert(msg){
    alert('Game Rules Reminder: '+ msg);
}

function can_take_token(color){
    var total_picked_tokens = get_total_picked_tokens();
    var n_picked_this_color = get_n_tokens_picked(color);
    var n_on_table_this_color = get_n_tokens_on_table(color);
    var msg = '';

    var ret = true;
    switch(total_picked_tokens){
        case 3:
            ret = false;
            msg = "You've already taken three different tokens.";
            break;
        case 2:
            switch(n_picked_this_color){
                case 2:
                    ret = false;
                    msg = "You've already taken two " + color + " tokens";
                    break;
                case 1:
                    ret = false;
                    msg = "You can't take twice the same color if you have already chosen two tokens of different colors";
                    break;
                case 0:
                    ret = n_on_table_this_color >= 0;
                    msg = "No " + color + " tokens on the table.";
                    if(ret){
                        for (var i = 0; i < COLORS_NO_YELLOW.length; i++) {
                            if(get_n_tokens_picked(COLORS_NO_YELLOW[i]) == 2){
                                ret = false;
                                msg = "You cannot take another token since two " + COLORS_NO_YELLOW[i] + " have already been picked";
                            }
                        }
                    }
                    break;
            }
            break;
        case 1:
            switch(n_picked_this_color){
                case 1:
                    ret = n_on_table_this_color >= MIN_NUMBER_OF_TOKENS_FOR_DOUBLE_PICK;
                    msg = "You can only take two tokens of the same color if there are more than " + MIN_NUMBER_OF_TOKENS_FOR_DOUBLE_PICK + " of this color on the table";
                    break;
                case 0:
                    ret = n_on_table_this_color >= 0;
                    msg = "No " + color + " tokens on the table.";
                    break;
        }
            break;
        case 0:
            ret = n_on_table_this_color >= 0;
            msg = "No " + color + " tokens on the table.";
            break;
    }

    if(!ret){
        game_rules_alert(msg);
    }
    return ret

}

function reset_tokens_picked(){
    for (var i = 0; i < COLORS_NO_YELLOW.length; i++) {
        $('#table-token-' + COLORS_NO_YELLOW[i]).html(0)
    }
}



// BUY OR RESERVE CARDS
//////////////////////////
//////////////////////////
//////////////////////////
//////////////////////////


function get_total_items(color){
    return parseInt($('#player-' + color + '-total').html());
}

function can_he_buy_card(card_info){
    var n_yellow_needed = 0;
    for(var i=0; i<COLORS_NO_YELLOW.length; i++){
        var d = card_info[COLORS_NO_YELLOW[i]] - get_total_items(COLORS_NO_YELLOW[i]);
        if(d > 0){
            n_yellow_needed += d;
        }
    }
    console.log('n_yellow_needed', n_yellow_needed);
    return n_yellow_needed <= get_total_items('yellow');
}

function get_card_info(table_card_id){
    var card_info = {};
    for(var i=0; i<COLORS_NO_YELLOW.length; i++){
        var element = $('#table-card-' + table_card_id + '-n' + COLORS_NO_YELLOW[i]);
        card_info[COLORS_NO_YELLOW[i]] = element.length ? parseInt(element.html()) : 0;
    }
    console.log(card_info);
    return card_info;
}

function buy_or_reserve_card(table_card_id, already_reserved){
    var can_buy_card = can_he_buy_card(get_card_info(table_card_id));

    if(can_buy_card){
        if($('#table-card-' + table_card_id).hasClass(BUY_CLASS)){
            $('#table-card-' + table_card_id).removeClass(BUY_CLASS);
        }else{
            reset_table();
            $('#table-card-' + table_card_id).addClass(BUY_CLASS);
        }
        $('.buyable-card').removeClass(RESERVE_CLASS);
    }else if(get_n_reserved_cards() < MAX_N_RESERVED_CARDS && !already_reserved){
        if($('#table-card-' + table_card_id).hasClass(RESERVE_CLASS)){
            reset_table();
        }else{
            if(confirm("You can't buy that card. Do you want to reserve it?")){
                if(get_n_tokens_on_table('yellow') == 0){
                    if(confirm("There's no more yellow tokens on the table. Do you still want to reserve that card?")){
                        reset_table();
                        $('#table-card-' + table_card_id).addClass(RESERVE_CLASS);
                    }
                }else{
                    reset_table();
                    $('#table-card-' + table_card_id).addClass(RESERVE_CLASS);
                }
            }
        }

    }
}

function reset_table(){
    reset_tokens_picked();
    reset_table_cards();
}

function reset_table_cards(){
    $('.buyable-card').removeClass(RESERVE_CLASS);
    $('.buyable-card').removeClass(BUY_CLASS);
}


function get_n_reserved_cards(){
    return $('#player-yellow-card').length;
}

function can_he_reserve_card(){
    var n_yellow_needed = 0;
    for(var i=0; i<COLORS_NO_YELLOW.length; i++){
        var d = card_info[COLORS_NO_YELLOW[i]] - get_total_items(COLORS_NO_YELLOW[i]);
        if(d > 0){
            n_yellow_needed += d;
        }
    }
    console.log('n_yellow_needed', n_yellow_needed);
    return n_yellow_needed > get_total_items('yellow');
}


// PLAY
//////////////////////////
//////////////////////////
//////////////////////////
//////////////////////////

function want_to_reserve_a_card(){
    return $('.' + RESERVE_CLASS).length > 0;
}

function want_to_buy_a_reserved_card(){
    if($('.player-yellow-card').length > 0){
        console.log($('.player-yellow-card').hasClass(BUY_CLASS));
        return $('.player-yellow-card').hasClass(BUY_CLASS)
    }
}

function want_to_buy_a_card(){
    return $('.' + BUY_CLASS).length > 0;
}

function want_to_buy_tokens(){
    ret = false;
    if(get_total_picked_tokens() == 3){
        ret = true;
    }else{
        for (var i = 0; i < COLORS_NO_YELLOW.length; i++) {
            if(get_n_tokens_picked(COLORS_NO_YELLOW[i]) == 2){
                ret = true;
            }
        }
    }
    return ret;
}

function play_server(game_id, gameplayer_id){

    var play = {what: '?', game_id:game_id, gameplayer_id: gameplayer_id};
    if(want_to_reserve_a_card()){
        play.what = "reserve-a-card";
        play.table_card_id = parseInt($('.' + RESERVE_CLASS).attr('id').split('-').pop());
    }else if(want_to_buy_a_reserved_card()){
        play.what = "buy-a-reserved-card";
        play.player_card_id = parseInt($('.' + BUY_CLASS).attr('id').split('-').pop());
    }else if(want_to_buy_a_card()){
        play.what = "buy-a-card";
        play.table_card_id = parseInt($('.' + BUY_CLASS).attr('id').split('-').pop());
    }else if(want_to_buy_tokens()){
        play.what = "buy-tokens";
        play.tokens_to_buy = [];
        for (var i = 0; i < COLORS_NO_YELLOW.length; i++) {
            var n_tokens_for_that_color = get_n_tokens_picked(COLORS_NO_YELLOW[i]);
            if(n_tokens_for_that_color > 0){
                play.tokens_to_buy.push(COLORS_NO_YELLOW[i] + '-' + n_tokens_for_that_color)
            }
        }
        play.tokens_to_buy = play.tokens_to_buy.join('_');
        console.log('tok', play.tokens_to_buy);
    }

if(play.what == '?'){
    game_rules_alert('Your selection is not correct motherfucker!');
}else{
    $.post( "/play", play)
        .done(function( data ) {
        //location.reload();
    });

}


}