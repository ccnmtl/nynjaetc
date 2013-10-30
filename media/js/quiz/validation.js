/*

Note: this code runs on ALL non-rhetorical quizzes;
e.g. the pre- and post-test,
as well as the disclaimer

*/
  
(function () {

function validate_pre_and_post_test_forms (e)  {

    e.preventDefault(); // don't submit multiple times
    var valid = true;
    jQuery(".quiz_feedbackbox").hide();
    
    if (jQuery("#input_for_question_17").length > 0 ) {
            // special hrsa ID validation.
            var hrsa_id  = jQuery("#input_for_question_17")[0].value;
            var there_are_exactly_eight_digits =  (/^[0-9]{8}$/g.test(hrsa_id));
            if (!there_are_exactly_eight_digits ) {
            //console.log ('ok there were not 8 chars');
            jQuery("#feedback_for_question_17").text("Please enter your 8-character HRSA ID.").show();
            valid = false;
            //return false;
          }
          else {
                // console.log ('ok there were 8 chars');
          }
  }
  done_questions = []
    // How many radio button questions are there?
    radio_button_question_count = 0;
    jQuery ('.cases').each( function (a, b) {
            //console.log (jQuery(b).find( 'input[type=radio]' ).length > 0)
            if (jQuery(b).find( 'input[type=radio]' ).length > 0) {
                radio_button_question_count ++
            }
        }
    )
    // how many are clicked?
    jQuery('input:radio').each (
    function(a, b) {
          if ( b.checked) { done_questions.push (b.name); }
       }
    );
    checked_radio_button_question_count = done_questions.length
    //console.log ("there are " + radio_button_question_count + "questions.");
    //console.log (" of which the user answered " + checked_radio_button_question_count);
     if  ( checked_radio_button_question_count < radio_button_question_count) {
        valid = false;
        jQuery("#quiz_general_feedback").text("Please answer all the questions.").show();
    }
    if (valid) {
        submit_quiz_via_ajax_then_go_to_next_page();
    }
}


function submit_quiz_via_ajax_then_go_to_next_page (){
    jQuery.ajax({
        data: jQuery('form').serialize(),
        type: 'POST',
        url: '.',
        success: go_to_next_page
    });
    return false;
}



function go_to_next_page () {

    jQuery('li.next a')[0].click();    
}


function checkbox_changed() {
    if (the_checkbox[0].checked) {
        record_success_on_disclaimer ()
    }
    else {
        jQuery ('#continue_button').hide();
    
    }
}

function init_disclaimer () {
    jQuery('#primarynav').hide();
    jQuery ('#continue_button').hide();
    the_checkbox = jQuery('input[name=pageblock-116-question50]');
    the_checkbox.change (checkbox_changed);
    jQuery('input[type=submit]').hide()
}

function allow_to_proceed () {
        jQuery ('#continue_button').show();
}

function record_success_on_disclaimer (){
    jQuery.ajax({
        data: {'section_id':jQuery('.section_id').html()},
        type: 'POST',
        url: '/record_section_as_answered_correctly/',
        success: allow_to_proceed
    });
    return false;
}


function init_disclaimer_and_pre_and_post_tests() {
    jQuery ('#quiz_general_feedback').hide()
    
    // pre and post tests:
    if (jQuery('.section_id').html() == '35' || jQuery('.section_id').html() == '51') {
        jQuery(".quiz_feedbackbox").hide();
        jQuery('form').submit(validate_pre_and_post_test_forms);
        
        // don't allow users to leave the page unless they submit a response.
        if ( typeof (the_user_submitted_a_response) ==="undefined" || (!the_user_submitted_a_response) ) {
            jQuery ('.next').hide()
        }
    }
    // if this is the disclaimer page:
    
    if (jQuery('input[name=pageblock-116-question50]').length) {
        init_disclaimer();
    }
    
}

jQuery(init_disclaimer_and_pre_and_post_tests);


})();

