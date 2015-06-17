var MIN_NUMBER_OF_TOKENS_FOR_DOUBLE_PICK = 4;
var COLORS_NO_YELLOW = ['blue', 'black', 'green', 'red', 'white'];
var COLORS = ['blue', 'black', 'green', 'red', 'white', 'yellow'];
var MAX_N_RESERVED_CARDS = 3;
var BUY_CLASS = 'table-card-ready-to-buy';
var RESERVE_CLASS = 'table-card-ready-to-reserve';
var MAX_N_TOKENS_OWNED = 10;

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

function n_tokens_owned(){
    var total_tokens_owned = 0;
    for (var i = 0; i < COLORS.length; i++) {
        var element = $('#player-token-' + COLORS[i]);
        var n_of_that_color = element.length ? parseInt(element.html()) : 0;
        total_tokens_owned += n_of_that_color;
    }
    return total_tokens_owned;
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
    $('#game-alert-message').html(msg);
    $('#game-alert').fadeIn();
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

            bootbox.dialog({
              message: "You can't buy that card. Do you want to reserve it?",
              title: "Shall we reserve that card?",
              buttons: {
                success: {
                  label: "Yes!",
                  className: "btn-success",
                  callback: function() {
                    if(get_n_tokens_on_table('yellow') == 0){

                        bootbox.dialog({
                          message: "There's no more yellow tokens on the table. Do you still want to reserve that card?",
                          title: "Shall we reserve that card?",
                          buttons: {
                            success: {
                              label: "Yep",
                              className: "btn-success",
                              callback: function() {
                                reset_table();
                                $('#table-card-' + table_card_id).addClass(RESERVE_CLASS);
                                }
                            },
                            danger: {
                              label: "No, muchas gracias!",
                              className: "btn-danger",
                              callback: function() {
                                true;
                              }
                            },
                          }
                        });

                    }else{
                        reset_table();
                        $('#table-card-' + table_card_id).addClass(RESERVE_CLASS);
                    }
                  }
                },
                danger: {
                  label: "No thanks!",
                  className: "btn-danger",
                  callback: function() {
                    true;
                  }
                }
              }
            });

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
    return $('.player-yellow-card').length;
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

    // here check if the total after buying is not more than 10 tokens
    if(ret){
        if(get_total_picked_tokens() + n_tokens_owned() > MAX_N_TOKENS_OWNED){
            game_rules_alert('You cannot have more than 10 tokens.');
            reset_tokens_picked();
            ret=false;
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
            location.reload();
        });

    }

}

function get_game_id(){
    return($('#game-id').html());
};

function get_gameplayer_id(){
    return($('#gameplayer-id').html());
};

function start_game_post_emails(){

    var emails = [];
    $('.start-game-add-player .email').each(function(){
        emails.push($(this).html());
    });

    console.log(emails);
    $.post( "/start_game", {data: emails.join(',')})
    .done(function() {
      window.location = '/index';
    });;
}

function hack_reload_without_socket(){
    var is_not_my_turn_to_play = $('#play-server').prop('disabled');
    if(is_not_my_turn_to_play){
        window.setInterval(function(){
          location.reload();
        }, 10000);
    }
}

$(document).ready(function(){

    $('#play-server').click(function(){
        play_server(get_game_id(), get_gameplayer_id());
    });

    $('#reset-tokens-picked').click(function(){
        reset_tokens_picked();
    });

    $('#splendooor').click(function(){
        game_rules_alert('SPLENDOOOOOOOOOOOR', false);
    });

    $('.start-game-add-player').click(function(){
        $(this).toggleClass('btn-default');
        $(this).toggleClass('btn-primary');

        if($('.start-game-add-player.btn-primary').length >= 2){
            $( "#btn-start-game" ).prop( "disabled", false );
        }else{
            $( "#btn-start-game" ).prop( "disabled", true );
        }
    });

    $('#btn-start-game').click(function(){
        console.log('str');
        if($('.start-game-add-player.btn-primary').length >= 2){
            start_game_post_emails();
            console.log('str2');
        };
    });

    $('[data-toggle="tooltip"]').tooltip();


    var images_nyc = ['taxi17.png', 'theater3.png', 'burger9.png', 'hot62.png', 'new70.png', 'car105.png', 'shopping188.png', 'building47.png', 'new76.png', 'new71.png', 'new72.png', 'brindis2.png', 'shopping187.png', 'new73.png', 'business163.png', 'semaphore7.png', 'new74.png', 'bridge3.png', 'new77.png', 'new75.png'];
    var images_actions = ['cut51.png', 'exercise37.png', 'exercise19.png', 'celebrating.png', 'exercise45.png', 'exercise15.png', 'archery5.png', 'exercise41.png', 'soccer3.png', 'exercise20.png', 'suitcases6.png', 'canes.png', 'exercise16.png', 'exercise24.png', 'flutes.png', 'dumbbell7.png', 'exercise32.png', 'jump11.png', 'exercise42.png', 'women21.png', 'alcohol23.png', 'fork43.png', 'gym31.png', 'mountain8.png', 'exercise12.png', 'exercise33.png', 'exercise26.png', 'exercise28.png', 'couple5.png', 'think7.png', 'girl3.png', 'fisher.png', 'exercise29.png', 'ski23.png', 'exercise21.png', 'musical27.png', 'rain86.png', 'walker.png', 'musical26.png', 'balloon21.png', 'men41.png', 'exercise30.png', 'exercise43.png', 'exercise25.png', 'exercise23.png', 'basketball equipment6.png', 'exercise17.png', 'scooters.png', 'football game3.png', 'talk24.png', 'tennis ball2.png', 'exercise27.png', 'jumping4.png', 'girl4.png', 'boy3.png', 'exercise34.png', 'musical141.png', 'sports ball14.png', 'ring5.png', 'rope5.png', 'men39.png', 'men43.png', 'walk3.png', 'exercise39.png', 'boy2.png', 'exercise31.png', 'jump2.png', 'seat5.png', 'gym35.png', 'golfing3.png', 'greeting1.png', 'standing.png', 'exercise14.png', 'gym32.png', 'men40.png', 'exercise18.png', 'climb1.png', 'men42.png', 'exercise38.png', 'men38.png', 'ping pong8.png', 'exercise35.png', 'baseball6.png', 'basketball equipment5.png', 'tennis ball1.png', 'walk2.png', 'sing3.png', 'exercise40.png', 'exercise13.png', 'soccer player1.png', 'exercise44.png', 'gym34.png', 'exercise36.png', 'recycle8.png', 'chairs6.png', 'exercise22.png', 'gym36.png', 'gym33.png', 'knee.png', 'sport35.png', 'gymnast3.png', 'martial arts3.png', 'salute2.png'];
    var images = images_actions;
    var iconsdir = '../static/img/icons-actions/';

    $('.table-card').each(function(){
        $(this).css({'background-image': 'url(' + iconsdir + images[Math.floor(Math.random() * (images.length - 1))] + ')'});
    });
    $('.table-square').each(function(){
        $(this).css({'background-image': 'url(' + iconsdir + images[Math.floor(Math.random() * (images.length - 1))] + ')'});
    });
    $('.player-yellow-card').each(function(){
        $(this).css({'background-image': 'url(' + iconsdir + images[Math.floor(Math.random() * (images.length - 1))] + ')'});
    });

    hack_reload_without_socket();

});