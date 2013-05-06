(function (jQuery) {
    
    Backbone.sync = function (method, model, success, error) {
    };
    
    String.prototype.capitalize = function() {
        return this.charAt(0).toUpperCase() + this.slice(1);
    }
    
    var TreatmentStep = Backbone.Model.extend({
        defaults: {
            'minimized': false,
            'decision': undefined,
            'initial': true
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
            this.model.bind("change:minimized", this.render);
            
            this.render();
            this.model.set('initial', false);
            
            var eltStep = jQuery(this.el).find("div.treatment-step");           
            jQuery(eltStep).fadeIn("slow");
        },
        render: function () {
            var eltStep = jQuery(this.el).find("div.treatment-step");
            
            this.template = _.template(jQuery("#treatment-step").html());
            this.el.innerHTML = this.template(this.model.toJSON());
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
            "click #select-patient-factors": "onContinue",
            "click .reset-state": "onResetState",
            "click .decision-point-button": "onDecisionPoint",
            "click .choose-again": "onChooseAgain",
            "click i.icon-question-sign": "onHelp"
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
                "onRemoveStep",
                "onHelp"
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
                    
                    // Minimize steps 0 - n-1
                    var week = 0;
                    self.treatmentSteps.forEach(function(step, idx) {
                        week += step.get('duration');
                        step.set('minimized', true);                
                    });
                    
                    // Appear the new treatment steps
                    for (var i = 0; i < json.steps.length; i++) {
                        var ts = new TreatmentStep(json.steps[i]);
                        ts.set('week', week);
                        self.treatmentSteps.add(ts);
                        week += ts.get('duration');
                    }    
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

            while ((model = self.treatmentSteps.first()) !== undefined) {
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
            
            var last = this.treatmentSteps.last();
            last.set({'decision': parseInt(jQuery(srcElement).attr('value'), 10)});
            this.activityState.set('node', last.get('id'));
            
            self.next();            
        },
        onChooseAgain: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var rollbackId = jQuery(srcElement).data('id');
            
            var prevId;
            var chosen;
            while ((step = this.treatmentSteps.last()) !== undefined) {
                if (prevId === rollbackId) {
                    step.set({
                        "minimized": false,
                        "decision": undefined
                    });
                    
                    if (step.get('type') === "DP") {
                        break;
                    }
                }
                prevId = step.get('id');
                step.destroy();
            }
            this.activityState.set('node', chosen);
        },
        onHelp: function(evt) {
            
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var parent = jQuery(srcElement).parents('div.treatment-step')[0];
            var helpText = jQuery(parent).find('div.treatment-step-help');
            
            jQuery("div.treatment-step-help:visible").not(helpText).hide();
            jQuery(helpText).toggle();
        }
    });
}(jQuery));    