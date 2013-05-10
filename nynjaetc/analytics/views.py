from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.contrib.auth.models import User
@login_required
@staff_member_required
@render_to('analytics/analytics_table.html')
def analytics_table(request):
    the_table = generate_the_table()
    return {'the_table': the_table}
    
    
    
def generate_the_table():
    return [ generate_row(u) for u in User.objects.all()]
    
    
    
def generate_row(the_user):
    return {'the_user': the_user}

