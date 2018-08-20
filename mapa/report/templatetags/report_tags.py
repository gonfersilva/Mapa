from django import template
from report.forms import ReportCreateForm
from report.models import Report

register = template.Library()

@register.inclusion_tag('report/report_form.html')
def report_form(self):
    form = ReportCreateForm()
    return {'form': form }


