var MIN_NUMBER_OF_TOKENS_FOR_DOUBLE_PICK = 4;
var COLORS_NO_YELLOW = ['blue', 'black', 'green', 'red', 'white'];
var COLORS = ['blue', 'black', 'green', 'red', 'white', 'yellow'];


function pick_token(color){

    var i_can_take_the_token = can_take_token(color);
    if(i_can_take_the_token){
        $('#table-token-' + color).html(get_n_tokens_picked(color) + 1);
    }

}

function get_n_tokens_on_table(color){
    return parseInt($('#table-token-' + color + '-n-on-table').html());
}

function get_n_tokens_picked(color){
    return parseInt($('#table-token-' + color).html());
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