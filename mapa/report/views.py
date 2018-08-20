from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report
from .forms import ReportCreateForm
from django.views.generic import ListView, CreateView
from django.utils import timezone
from django.contrib.auth.decorators import login_required

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'report/report_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ReportCreateView(LoginRequiredMixin, CreateView):
    template_name = 'report/report_create.html'
    form_class = ReportCreateForm
    success_url = '/report/'
     
    
@login_required
def report_detail(request, pk):
    report = Report.objects.get(pk=pk)
    
    template_name = 'report/report_detail.html'
    context = {
        'report': report,
        
    }
    return render(request, template_name, context)