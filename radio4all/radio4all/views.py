from .models import Files, Locations, Programs, News, Faq, Types, License
from rest_framework import viewsets
from .serializers import FilesSerializer, LocationSerializer, ProgramsSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import DetailView
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render


class HomePageView(ListView):
    model = Programs
    context_object_name = 'latest_programs'  # Default: object_list
    paginate_by = 30
    queryset = Programs.objects.all().order_by('-date_created')  # Default: Model.objects.all()
    template_name = "radio4all/home.html"

class DashboardView(LoginRequiredMixin,ListView):
    model = Programs
    context_object_name = 'latest_programs'  # Default: object_list
    paginate_by = 30
#    queryset =
    template_name = "radio4all/dashboard.html"

    def get_queryset(self):
        return Programs.objects.filter(uid=self.request.user).order_by('-date_created')  # Default: Model.objects.all()

class ProgramView(DetailView):
    model = Files
    template_name = 'radio4all/program.html'

    def get_context_data(self, **kwargs):
        context = super(ProgramView, self).get_context_data(**kwargs)
        context['object'] = Files.objects.filter(program__program_id=self.kwargs.get('pk'))
        return context

class AboutPageView(ListView):
    model = Programs
    context_object_name = 'latest_programs'  # Default: object_list
    paginate_by = 30
    queryset = Programs.objects.all().order_by('-date_created')  # Default: Model.objects.all()
    template_name = "radio4all/about.html"

class FaqPageView(ListView):
    model = Faq
    context_object_name = 'latest_faq'  # Default: object_list
    paginate_by = 30
    queryset = Faq.objects.all().order_by('-sort_order')  # Default: Model.objects.all()
    template_name = "radio4all/faq.html"

class NewsPageView(ListView):
    model = News
    context_object_name = 'latest_news'  # Default: object_list
    paginate_by = 30
    queryset = News.objects.all().order_by('-pub_date')  # Default: Model.objects.all()
    template_name = "radio4all/news.html"

class ContactPageView(ListView):
    model = Programs
    context_object_name = 'latest_programs'  # Default: object_list
    paginate_by = 30
    queryset = Programs.objects.all().order_by('-date_created')  # Default: Model.objects.all()
    template_name = "radio4all/contact.html"

class ProgramsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Programs.objects.all().order_by('date_created')
    serializer_class = ProgramsSerializer

class FilesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Files.objects.all().order_by('program__date_created')
    serializer_class = FilesSerializer


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Locations.objects.all().order_by('file__program__date_created')
    serializer_class = LocationSerializer




def advisory(request):
    return render(request, 'radio4all/advisory.html')

def length(request):
    return render(request, 'radio4all/length.html')

def type(request):
    return render(request, 'radio4all/type.html')

def license(request):
    return render(request, 'radio4all/license.html')

def series(request):
    return render(request, 'radio4all/series.html')

def filter_popular(request):
    try:
        target = Files.objects.all().order_by('-downloads')[:300]
    except Files.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/popular.html', {
        'latest_programs': target,
    },)

def filter_series(request, letter):
    try:
        if letter == "0-9":
            programs_series = Programs.objects.filter(series__startswith='0') | Programs.objects.filter(series__startswith='1') | Programs.objects.filter(series__startswith ='2') | Programs.objects.filter(series__startswith='3') | Programs.objects.filter(series__startswith='4') | Programs.objects.filter(series__startswith='5') | Programs.objects.filter(series__startswith='6') | Programs.objects.filter(series__startswith='7') | Programs.objects.filter(series__startswith='8') | Programs.objects.filter(series__startswith='9')
        else:
            programs_series = Programs.objects.filter(series__startswith=letter.capitalize()) | Programs.objects.filter(series__startswith=letter)
        target = programs_series.values('series').distinct()
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/programs_by_series.html', {
        'all_series': target,
        'letter': letter,
    },)

def filter_license(request, abbrev):
    try:
        license = License.objects.get(cc_abbrev=abbrev)
    except License.DoesNotExist:
        return HttpResponse('<h1>No License Here</h1>')
    try:
        target = Programs.objects.filter(license=license)
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/dashboard.html', {
        'latest_programs': target,
    },)

def filter_type(request, pk):
    try:
        typer = Types.objects.get(pk=int(pk))
    except Types.DoesNotExist:
        return HttpResponse('<h1>No Type Here</h1>')
    try:
        target = Programs.objects.filter(type=typer.type)
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/dashboard.html', {
        'latest_programs': target,
    },)

def download(request, program, version,file):
    path="e"
    try:
        target = Files.objects.get(program_id=program, version_id=version, file_id=file)
    except Files.DoesNotExist:
        return HttpResponse('<h1>No Page Here</h1>')
    try:
        location = Locations.objects.get(file=target)
    except Locations.DoesNotExist:
        path="http://www.radio4all.net/files/"
    if path != "e":
        file_path = "http://www.radio4all.net/files/"+target.program.uid.email+"/"+target.filename
    else:
        file_path = location.file_location
    target.downloads=target.downloads+1
    target.save()
    return redirect(file_path)
