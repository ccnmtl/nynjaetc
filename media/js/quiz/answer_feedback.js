function hide_unchecked_rhetorical_answer_feedback (id, elem) {
    var corresponding_feedback_selector = 'div.one_per_answer_explanation.' + elem.id;
    if (elem.checked ) {
        jQuery (corresponding_feedback_selector).show();
    }
    else {
        jQuery (corresponding_feedback_selector).hide();
    }
}
function hide_all_unchecked_rhetorical_answer_feedback() {
    jQuery('input:radio').each (hide_unchecked_rhetorical_answer_feedback);
}
jQuery('input:radio').change (hide_all_unchecked_rhetorical_answer_feedback);

