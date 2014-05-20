from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from nynjaetc.treatment_activity.models import TreatmentPath, TreatmentNode
import simplejson


@login_required
def get_next_steps(request, path_id, node_id):
    if not request.is_ajax():
        return HttpResponseForbidden()

    node = TreatmentNode.objects.get(id=node_id)

    next_steps = []
    prev = None
    if node.is_decisionpoint():
        steps = simplejson.loads(request.POST.get('steps'))
        decision = steps[len(steps) - 1]['decision']
        node = node.child_from_decision(decision)

        next_steps.append(node.to_json())
        prev = node

    for node in node.get_descendants():
        if prev and prev.is_decisionpoint():
            break
        else:
            next_steps.append(node.to_json())
            prev = node

    data = {'steps': next_steps,
            'path': path_id,
            'can_edit': request.user.is_superuser}
    if prev:
        data['node'] = prev.id

    return HttpResponse(simplejson.dumps(data, indent=2),
                        mimetype="application/json")


@login_required
def choose_treatment_path(request):
    if not request.is_ajax() or request.method != "POST":
        return HttpResponseForbidden()

    params = simplejson.loads(request.POST.get('state'))
    cirrhosis = params.get('cirrhosis', None)
    status = params.get('status', None)
    drug = params.get('drug', None)

    data = {}

    if cirrhosis is None or status is None or drug is None:
        data = {"error": "Missing required parameters"}

        return HttpResponse(simplejson.dumps(data, indent=2),
                            mimetype="application/json")
    try:
        path = TreatmentPath.objects.get(cirrhosis=cirrhosis,
                                         treatment_status=status,
                                         drug_choice=drug)

        return get_next_steps(request, path.id, path.tree.id)

    except TreatmentPath.DoesNotExist:
        msg = "Can't find a path. [cirrhosis: %s, status: %s, drug: %s]" \
            % (cirrhosis, status, drug)
        data = {"error": msg}

        return HttpResponse(simplejson.dumps(data, indent=2),
                            mimetype="application/json")
