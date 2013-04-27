(function (jQuery) {
        
    StateMachine = Backbone.Model.extend({
        states: [
            'patient-factors',
            'zero-four-weeks'
        ],
        defaults: {
            state: 0
        },
        context: function() {
            if (this.get('state') === 0) {
                return {
                    'complete': this.get('cirrhosis') !== undefined &&
                                this.get('naive') !== undefined &&
                                this.get('drug') !== undefined,
                    'cirrhosis': this.get('cirrhosis'),
                    'naive': this.get('naive'),
                    'drug': this.get('drug')
                };
            }
        },
        next: function() {
            this.set('state', this.get('state') + 1);
        },
        reset: function() {
            this.set('state', 0);
            this.set('cirrhosis', undefined);
            this.set('naive', undefined);
            this.set('drug', undefined);
        }
    });

    window.TreatmentActivityView = Backbone.View.extend({
        events: {
            "click div.treatment-activity-container input[type='radio']":
                "onSelectPatientFactor",
            "click input[type='button'].continue":
                "onContinue",
            "click #reset-state": "onResetState"                
        },
        initialize: function(options) {
            _.bindAll(this,
                "render",
                "onSelectPatientFactor",
                "onContinue",
                "onResetState"
            );
            
            jQuery('li.previous').hide();
            jQuery('li.next').hide();
            
            this.stateMachine = new StateMachine();
            this.stateMachine.bind("change", this.render);
            
            this.templates = [];
            for (var i = 0; i < this.stateMachine.states.length; i++) {
                this.templates.push(_.template(
                    jQuery("#" + this.stateMachine.states[i]).html()));
            }
            
            this.render();
        },
        render: function() {
            var self = this;
            var state = this.stateMachine.get('state');
            var context = this.stateMachine.context();
            
            var markup = this.templates[state](context);
            jQuery("div.treatment-activity-view").html(markup);            
            jQuery("div.treatment-activity-view").fadeIn("slow");
        },
        onSelectPatientFactor: function() {
            this.stateMachine.set({
                'cirrhosis': jQuery("input:radio[name=cirrhosis]:checked").attr("value"),
                'naive': jQuery("input:radio[name=naive]:checked").attr("value"),
                'drug':  jQuery("input:radio[name=drug]:checked").attr("value")
            });
        },
        onContinue: function() {
            this.stateMachine.next();
        },
        onResetState: function() {
            this.stateMachine.reset();
        }
    });
}(jQuery));    