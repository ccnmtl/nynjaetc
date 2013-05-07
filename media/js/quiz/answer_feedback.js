function hide_unchecked_rhetorical_answer_feedback (id, elem) {
    var corresponding_feedback_selector = 'div.one_per_answer_explanation.' + elem.id;
    if (elem.checked ) {
        jQuery (corresponding_feedback_selector).show();
        if(jQuery(elem).hasClass('is_correct')) {
            correct_answer_chosen();
        }
    }
    else {
        jQuery (corresponding_feedback_selector).hide();
    }
}

function correct_answer_chosen() {
    record_success();
    // prevent them from choosing any more wrong answers:
    jQuery('input:radio').each (disable_radio_buttons);
}

function disable_radio_buttons(id, elem) {
    elem.disabled=true;
}

function hide_all_unchecked_rhetorical_answer_feedback() {
    jQuery('input:radio').each (hide_unchecked_rhetorical_answer_feedback);
}

function the_init() {
    jQuery('input:radio').change (hide_all_unchecked_rhetorical_answer_feedback);
    
    if (jQuery ('.already_answered.true').length > 0) {
        // the user has already visited the page
        // and wants to review the correct answer he/she already chose:
        jQuery(jQuery ('.is_correct')[0]).prop('checked',true);
        jQuery('input:radio').each (hide_unchecked_rhetorical_answer_feedback);
    } else {
        jQuery('li.next').hide();
    }
}

function allow_to_proceed() {
    jQuery('li.next').show();
}



function record_success (){
    jQuery.ajax({
        data: {'section_id':jQuery('.section_id').html()},
        type: 'POST',
        url: '/record_section_as_answered_correctly/',
        success: allow_to_proceed
    });
    return false;
}

jQuery (the_init);

/*
Rules:

    A) New questions:
        Remove the show/hide answer toggle. Feedback should be hidden until the user chooses an answer ( any answer) and visible thereafter;
        On clicking an answer, show feedback for that answer only;
        Do not reveal which answer is correct until the user has chosen the correct answer;
        When a correct answer is chosen, user should no longer to be able to choose any incorrect answers;
        On page load, hide the next button;
        When the correct answer is chosen, show the next button;

    B) Old questions:
        When viewing a page that has already been answered correctly:
        Immediately show the correct answer on page load;
        Do not allow the incorrect answers to be selected;
        Do show the next button.
        
        
*/
