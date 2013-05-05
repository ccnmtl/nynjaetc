(function (jQuery) {
    
    Backbone.sync = function (method, model, success, error) {
    };
    
    var TreatmentStep = Backbone.Model.extend({
        defaults: {
            'minimized': false,
            'decision': undefined,
            'visible': true
        },
        url: function() {
            
        }
    });
    
    var TreatmentStepCollection = Backbone.Collection.extend({
        model: TreatmentStep
    });
    
    var TreatmentStepView = Backbone.View.extend({
        events: {
        },
        initialize: function (options, render) {
            _.bindAll(this, "render", "unrender");
            this.model.bind("destroy", this.unrender);
            this.template = _.template(jQuery("#treatment-step").html());

            this.el.innerHTML = this.template(this.model.toJSON());
            var eltStep = jQuery(this.el).find("div.treatment-step");
            jQuery(eltStep).fadeIn("slow");
            
            this.render();
            
            this.model.bind("change:visible", this.render);
            this.model.bind("change:minimized", this.render);
        },
        render: function () {
            var eltStep = jQuery(this.el).find("div.treatment-step");
            if (this.model.get('visible') === false) {
                jQuery(this.el).fadeOut("slow");
            } else if (this.model.get('visible') === true) {
                jQuery(this.el).fadeIn("slow");
            }
            
            if (this.model.get("minimized") === true &&
                !jQuery(eltStep).hasClass("minimzed")) {
                // @todo -- create a visual transition
                // between the minimized & maximized state
                //
                /**
                jQuery(eltStep).animate({height: '60px'}, 200, function() {
                    jQuery(eltStep)
                        .find("div.height-0,div.height-4, div.height-8,div.height-12,div.height-24")
                        .removeClass("height-0 height-4 height-8 height-12 height-24");
                    jQuery(eltStep).removeClass("height-0 height-4 height-8 height-12 height-24");
                    jQuery(eltStep).addClass("minimized");
                });
                **/
                
                jQuery(eltStep)
                    .find("div.height-0,div.height-4, div.height-8,div.height-12,div.height-24")
                    .removeClass("height-0 height-4 height-8 height-12 height-24");
                jQuery(eltStep).removeClass("height-0 height-4 height-8 height-12 height-24");
                jQuery(eltStep).addClass("minimized");
            }
        },
        unrender: function () {
            jQuery(this.el).fadeOut('slow', function() {
                jQuery(this.el).remove();
            });            
        }
    });
        
    var ActivityState = Backbone.Model.extend({
        templates: [
            'patient-factors',
            'treatment-flow'
        ],
        defaults: {
            template: 0,
            path: '',
            node: '',
            cirrhosis: undefined,
            status: undefined,
            drug: undefined
        },
        statusDescription: function() {
            switch(this.get('status')) {
                case '0': return 'treatment-naive';
                case '1': return 'prior null responder';
                case '2': return 'prior relapser';
                case '3': return 'prior partial';
                default: return '';
            }
        },
        cirrhosisDescription: function() {
            if (this.get('cirrhosis') === '1') {
                return 'with cirrhosis';
            } else {
                return 'without known cirrhosis';
            }
        },
        toTemplate: function() {
            var ctx = _(this.attributes).clone();
            ctx.patient_factors_complete =
                this.get('cirrhosis') !== undefined &&
                this.get('status') !== undefined &&
                this.get('drug') !== undefined;
            ctx.status_description = this.statusDescription();
            ctx.cirrhosis_description = this.cirrhosisDescription();
            return ctx;
        },
        getNextUrl: function() {
            var url = '/_rgt/';
            if (this.get('path')) {
                url += this.get('path') + '/' + this.get('node') + '/';
            }
            return url;  
        },        
        reset: function() {
            this.set('template', 0);
            this.set('cirrhosis', undefined);
            this.set('status', undefined);
            this.set('drug', undefined);
            this.set('path', '');
            this.set('node', '');
        }
    });

    window.TreatmentActivityView = Backbone.View.extend({
        events: {
            "click div.treatment-activity-container input[type='radio']":
                "onSelectPatientFactor",
            "click input[type='button'].continue":
                "onContinue",
            "click .reset-state": "onResetState",
            "click .decision-point-button": "onDecisionPoint",
            "click .choose-again": "onChooseAgain"
        },
        initialize: function(options) {
            _.bindAll(this,
                "render",
                "onSelectPatientFactor",
                "onContinue",
                "onResetState",
                "onDecisionPoint",
                "onChooseAgain",
                "onAddStep",
                "onRemoveStep"
            );
            
            jQuery('li.previous').hide();
            jQuery('li.next').hide();
            
            this.activityState = new ActivityState();
            this.activityState.reset();
            this.activityState.bind("change", this.render);
            
            this.treatmentSteps = new TreatmentStepCollection();
            this.treatmentSteps.bind("add", this.onAddStep);
            this.treatmentSteps.bind("remove", this.onRemoveStep);
            
            this.templates = [];
            for (var i = 0; i < this.activityState.templates.length; i++) {
                this.templates.push(_.template(
                    jQuery("#" + this.activityState.templates[i]).html()));
            }
            
            this.render();
        },
        render: function() {
            var self = this;
            var templateIdx = this.activityState.get('template');
            var context = this.activityState.toTemplate();
            var markup = this.templates[templateIdx](context);
            
            jQuery("div.treatment-activity-view").html(markup);            
            jQuery("div.treatment-activity-view, div.treatment-steps").fadeIn("slow");
        },
        next: function() {
            var self = this;
            
            jQuery.ajax({
                type: 'POST',
                url: self.activityState.getNextUrl(),
                data: {
                    'state': JSON.stringify(this.activityState.toJSON()),
                    'steps': JSON.stringify(this.treatmentSteps.toJSON())
                },
                dataType: 'json',
                error: function () {
                    alert('There was an error.');
                },
                success: function (json, textStatus, xhr) {
                    self.activityState.set({'template': 1,
                                            'path': json.path,
                                            'node': json.node});
                    
                    var week = 0;
                    self.treatmentSteps.initial().forEach(function(step, idx) {
                        week += step.get('duration');
                        step.set('minimized', true);                
                    });
                    
                    setTimeout(function() {
                        var last = self.treatmentSteps.last();
                        if (last) {
                            last.set('visible', false);
                        }
                        setTimeout(function() {
                            for (var i = 0; i < json.steps.length; i++) {
                                var ts = new TreatmentStep(json.steps[i]);
                                ts.set('week', week);
                                self.treatmentSteps.add(ts);
                                week += ts.get('duration');
                            }    
                        }, 1000);                            
                    }, 1000);
                }
            });
        },
        onAddStep: function(step) {
            var view = new TreatmentStepView({model: step, parentView: this});
            jQuery("div.treatment-steps").append(view.el);    
        },
        onRemoveStep: function(step) {
            step.destroy();
        },
        onSelectPatientFactor: function() {
            this.activityState.set({
                'cirrhosis': jQuery("input:radio[name=cirrhosis]:checked").attr("value"),
                'status': jQuery("input:radio[name=status]:checked").attr("value"),
                'drug':  jQuery("input:radio[name=drug]:checked").attr("value")
            });
        },
        onContinue: function() {
            var self = this;
            jQuery("div.treatment-activity-view").fadeOut("slow", function() {
                self.next();
            });            
        },
        onResetState: function(evt) {
            var self = this;
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).button("loading");

            while (model = self.treatmentSteps.first()) {
                model.destroy();
            }
            self.treatmentSteps.reset();            
            jQuery("div.treatment-steps,div.treatment-activity-view").fadeOut("slow", function() {
                self.activityState.reset();                
            });
        },
        onDecisionPoint: function(evt) {
            var self = this;
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).button("loading");
            
            var decision = jQuery(srcElement).attr('value') === 'Yes'? 1: 0;
            
            var last = this.treatmentSteps.last();
            last.set({'decision': decision});
            this.activityState.set('node', last.get('id'));
            
            self.next();            
        },
        onChooseAgain: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var rollbackTo = jQuery(srcElement).data('id');
            
            var use_previous;
            var chosen;
            while (step = this.treatmentSteps.last()) {
                if (chosen !== undefined) {
                    if (step.get('type') === "DP") {
                        break;
                    }
                    step.set("minimized", false);
                    step.set("visible", true);
                }
                if (use_previous) {
                    chosen = step.get("id");
                } else {
                    use_previous = step.get('id') === rollbackTo;
                    step.destroy();
                }
            }
            this.activityState.set('node', chosen);
        }
    });
}(jQuery));    