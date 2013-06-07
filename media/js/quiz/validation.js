
  
(function () {

function validate_pretest_form ()  {
    var valid = true;
    jQuery(".quiz_feedbackbox").hide();
    
    
    if (jQuery("#input_for_question_17").length > 0 ) {
    
            
            var hrsa_id  = jQuery("#input_for_question_17")[0].value;
            
            var there_are_exactly_eight_digits =  (/^[0-9]{8}$/g.test(hrsa_id));
            if (!there_are_exactly_eight_digits ) {
            console.log ('ok there were not 8 chars');
            jQuery("#feedback_for_question_17").text("Please enter your 8-character HRSA ID.").show();
            valid = false;
            //return false;
          }
          else {
                console.log ('ok there were 8 chars');
            
          }

  }
  done_questions = []
    
    // How many radio button questions are there?
    radio_button_question_count = 0;
    jQuery ('.cases').each( function (a, b) {
        console.log (jQuery(b).find( 'input[type=radio]' ).length > 0)
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
    console.log ("there are " + radio_button_question_count + "questions.");
    console.log (" of which are clicked " + checked_radio_button_question_count);
     if  ( checked_radio_button_question_count < radio_button_question_count) {
        valid = false;
        jQuery("#quiz_general_feedback").text("Please answer all the questions.").show();
     
     }
    return valid; 
}

function init_pre_and_post_tests() {
    // if this is the pretest:
    jQuery(".quiz_feedbackbox").hide();
    jQuery('form').submit(validate_pretest_form);
}

jQuery(init_pre_and_post_tests);


})();

