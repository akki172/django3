from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from results.models import DeclareResult
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core import serializers
import json

from student_classes.models import StudentClass
from results.models import DeclareResult
from subjects.models import Subject
from students.models import Student
from django.http import Http404

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def index(request):
    if request.method == "POST":
        # Extract username and password from the form data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # If authentication is successful, log in the user and redirect to the dashboard
            login(request, user)
            return redirect('dashboard:dashboard')
        else:
            # If authentication fails, render the index.html template with an error message
            context = {'message': 'Invalid User Name and Password'}
            return render(request, 'index.html', context)

    # If the request method is GET (i.e., accessing the page for the first time),
    # render the index.html template with some initial data (if needed)
    return render(request, 'index.html')

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"

    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['cls'] = StudentClass.objects.count()
        context['results'] = DeclareResult.objects.count()
        context['students'] = Student.objects.count()
        context['subjects'] = Subject.objects.count()
        return context
    

def find_result_view(request):
    student_class = DeclareResult.objects.all()
    if request.method == "POST":
        data = request.POST
        # data = json.loads(form)
        roll = int(data['rollid'])
        pk = int(data['class'])
        clss = get_object_or_404(DeclareResult, pk=pk)
        if clss.select_student.student_roll == roll:
            data = {
                    'pk': data['class']
            }
            return JsonResponse(data)
        else:
            pk = '0'
            data = {
                'pk': pk
            }
            return JsonResponse(data)
    return render(request, 'find_result.html', {'class':student_class})

def result(request, pk):
    obj = get_object_or_404(DeclareResult, pk=pk)
    marks = []
    for i in range(int(len(obj.marks) / 2)):
        subject_key = f'subject_{i}'
        mark_key = f'subject_{i}_mark'
        if subject_key in obj.marks and mark_key in obj.marks:
            marks.append([obj.marks[subject_key], obj.marks[mark_key]])
    return render(request, 'result.html', {'object': obj, 'pk': pk, 'marks': marks})


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('dashboard:dashboard')
    template_name = 'password_change_form.html'

    
    def get_context_data(self, **kwargs):
        context = super(PasswordChangeView, self).get_context_data(**kwargs)
        context['main_page_title'] = 'Admin Change Password'
        context['panel_title'] = 'Admin Change Password'
        return context


def renderPdf(template, content={}):
    t = get_template(template)
    send_data = t.render(content)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(send_data.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error rendering PDF: {}'.format(pdf.err), status=500)


class pdf(View):
    def get(self, request, id):
        try:
            query = get_object_or_404(DeclareResult, id=id)
        except:
          raise Http404('Content Not Found')
        marks = []
        lst = []
        for i in range(int(len(query.marks)/2)):
            lst.append(query.marks['subject_'+str(i)])
            lst.append(query.marks['subject_'+str(i)+'_mark'])
            marks.append(lst)
            lst = []
        article_pdf = renderPdf('result.html', {'object': query, 'marks':marks})
        return HttpResponse(article_pdf, content_type='application/pdf')


# dashboard/views.py
  # Assuming you have a Feedback model



