from .models import Files, Locations, Programs, News, Faq, Types, License, Users, Topics, TopicAssignment, Restrictions, Advisories, Lang, Formats, Versions
from rest_framework import viewsets
from .serializers import FilesSerializer, LocationSerializer, ProgramsSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import DetailView
import os
import datetime
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, BadHeaderError, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.db import connection
from django.utils import feedgenerator
from math import ceil

class HomePageView(ListView):
    model = Programs
    context_object_name = 'latest_programs'  # Default: object_list
    paginate_by = 30
    queryset = Programs.objects.all().order_by('-date_created').filter(hidden=0).filter(versions__version=1)  # Default: Model.objects.all()
    template_name = "radio4all/home.html"

class DashboardView(LoginRequiredMixin,ListView):
    model = Programs
    context_object_name = 'latest_programs'  # Default: object_list
    paginate_by = 30
#    queryset =
    template_name = "radio4all/dashboard.html"

    def get_queryset(self):
        return Programs.objects.filter(uid=self.request.user.uid).order_by('-date_created')  # Default: Model.objects.all()

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

def length_page(request):
    return render(request, 'radio4all/length.html')

def type(request):
    return render(request, 'radio4all/type.html')

def license(request):
    return render(request, 'radio4all/license.html')

def series(request):
    return render(request, 'radio4all/series.html')

def contributor_browse(request):
    return render(request, 'radio4all/contributor_browse.html')

def handle_uploaded_file(email_dir, filename, f):
    with open('/tank/radio4all/files/' + email_dir + '/' + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def make_file_location(email_dir, filename):
    return "http://www.radio4all.net/files/" + email_dir + "/" + filename

def upload_content(request):
    if request.method == 'POST':
        nps = int(request.POST.get('program_segments'))
        now = datetime.datetime.now()
        p = Programs()
        p.program_title = request.POST.get('program_title')
        p.uid = Users.objects.get(uid = request.user.uid)
        p.type = request.POST.get('program_type')
        p.subtitle = request.POST.get('program_subtitle')
        series = request.POST.get('program_series')
        add_series = request.POST.get('program_add_series')
        if series == '':
            p.series = add_series
        else:
            p.series = series
        p.speaker = request.POST.get('program_speaker')
        p.summary = request.POST.get('program_summary')
        p.keywords = request.POST.get('program_keywords')
        p.credits = request.POST.get('program_credits')
        p.license = License.objects.get(cc_id=request.POST.get('program_license'))
        p.restriction = request.POST.get('program_restriction')
        p.notes = request.POST.get('program_notes')
        p.hidden = 0
        p.advisory = Advisories.objects.get(ad_id = request.POST.get('program_advisory'))
        p.keywords = request.POST.get('program_keywords')
        p.password = request.POST.get('program_password')
        p.permanent = 0
        p.date_created = now
        p.save()
        topics = request.POST.getlist('program_topics[]')
        for e in topics:
            t = TopicAssignment()
            t.topic_id = e
            t.program_id = p.program_id
            t.save()
        v = Versions()
        v.version_title = request.POST.get('version_title')
        v.version_description = request.POST.get('version_description')
        v.lang_id = request.POST.get('version_lang')
        v.date_recorded = request.POST.get('version_date_recorded')
        v.location = request.POST.get('version_location')
        v.script = request.POST.get('version_script')
        v.length = '00:00:00'
        v.version = 1
        v.date_created = now
        v.program_id = p.program_id
        v.save()
        f1 = Files()
        f1.program_id = p.program_id
        f1.version_id = v.version_id
        f1.segment = 1
        if request.POST.get('how') == 'upload':
            f1.filename = str(request.FILES['filename1'])
        else:
            f1.filename = request.POST.get('filenametext1')
        f1.title = request.POST.get('file_title1')
        f1.file_size = request.POST.get('size1') + request.POST.get('file_size_bytes1')
        f1.bitrate = request.POST.get('bitrate1')
        f1.stereo = request.POST.get('stereo1')
        if request.POST.get('how') == 'upload':
            f1.format_id = os.path.splitext(request.POST.get('file_type_text1'))[-1].replace('.','')
        else:
            f1.format_id = request.POST.get('file_type_text1')
        f1_hrs = request.POST.get('hour1')
        f1_minutes = request.POST.get('minute1')
        f1_seconds = request.POST.get('second1')
        f1.length = f1_hrs + ':' + f1_minutes + ':' + f1_seconds
        f1_timedelta = datetime.timedelta(0, (3600 * int(f1_hrs)) + (60 * int(f1_minutes)) + int(f1_seconds))
        f1.how = request.POST.get('how')
        f1.no_delete = 0
        handle_uploaded_file(request.user.email, str(request.FILES['filename1']), request.FILES['filename1'])
        f1.save()
        c1 = Locations()
        c1.file_id = f1.file_id
        c1.filename =  str(request.FILES['filename1'])
        c1.file_location = make_file_location(request.user.email, str(request.FILES['filename1']))
        c1.save()
        f2_timedelta = datetime.timedelta(0)
        if nps > 1:
            f2 = Files()
            f2.program_id = p.program_id
            f2.version_id = v.version_id
            f2.segment = 2
            if request.POST.get('how') == 'upload':
                f2.filename = str(request.FILES('filename2'))
            else:
                f2.filename = request.POST.get('filenametext2')
            f2.title = request.POST.get('file_title2')
            f2.file_size = request.POST.get('size2') + request.POST.get('file_size_bytes2')
            f2.bitrate = request.POST.get('bitrate2')
            f2.stereo = request.POST.get('stereo2')
            f2.format_id = request.POST.get('file_type_text2')
            f2_hrs = request.POST.get('hour2')
            f2_minutes = request.POST.get('minute2')
            f2_seconds = request.POST.get('second2')
            f2.length = f2_hrs + ':' + f2_minutes + ':' + f2_seconds
            f2_timedelta = datetime.timedelta(0, (3600 * int(f2_hrs)) + (60 * int(f2_minutes)) + int(f2_seconds))
            f2.how = request.POST.get('how')
            f2.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename2']), request.FILES['filename2'])
            f2.save()
            c2 = Locations()
            c2.file_id = f2.file_id
            c2.filename =  str(request.FILES['filename2'])
            c2.file_location = make_file_location(request.user.email, str(request.FILES['filename2']))
            c2.save()
        f3_timedelta = datetime.timedelta(0)
        if nps > 2:
            f3 = Files()
            f3.program_id = p.program_id
            f3.version_id = v.version_id
            f3.segment = 3
            if request.POST.get('how') == 'upload':
                f3.filename = str(request.FILES['filename3'])
            else:
                f3.filename = request.POST.get('filenametext3')
            f3.title = request.POST.get('file_title3')
            f3.file_size = request.POST.get('size3') + request.POST.get('file_size_bytes3')
            f3.bitrate = request.POST.get('bitrate3')
            f3.stereo = request.POST.get('stereo3')
            f3.format_id = request.POST.get('file_type_text3')
            f3_hrs = request.POST.get('hour3')
            f3_minutes = request.POST.get('minute3')
            f3_seconds = request.POST.get('second3')
            f3.length = f3_hrs + ':' + f3_minutes + ':' + f3_seconds
            f3_timedelta = datetime.timedelta(0, (3600 * int(f3_hrs)) + (60 * int(f3_minutes)) + int(f3_seconds))
            f3.how = request.POST.get('how')
            f3.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename3']), request.FILES['filename3'])
            f3.save()
            c3 = Locations()
            c3.file_id = f3.file_id
            c3.filename =  str(request.FILES['filename3'])
            c3.file_location = make_file_location(request.user.email, str(request.FILES['filename3']))
            c3.save()
        f4_timedelta = datetime.timedelta(0)
        if nps > 3:
            f4 = Files()
            f4.program_id = p.program_id
            f4.version_id = v.version_id
            f4.segment = 4
            if request.POST.get('how') == 'upload':
                f4.filename = str(request.FILES['filename4'])
            else:
                f4.filename = request.POST.get('filenametext4')
            f4.title = request.POST.get('file_title4')
            f4.file_size = request.POST.get('size4') + request.POST.get('file_size_bytes4')
            f4.bitrate = request.POST.get('bitrate4')
            f4.stereo = request.POST.get('stereo4')
            f4.format_id = request.POST.get('file_type_text4')
            f4_hrs = request.POST.get('hour4')
            f4_minutes = request.POST.get('minute4')
            f4_seconds = request.POST.get('second4')
            f4.length = f4_hrs + ':' + f4_minutes + ':' + f4_seconds
            f4_timedelta = datetime.timedelta(0, (3600 * int(f4_hrs)) + (60 * int(f4_minutes)) + int(f4_seconds))
            f4.how = request.POST.get('how')
            f4.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename4']), request.FILES['filename4'])
            f4.save()
            c4 = Locations()
            c4.file_id = f4.file_id
            c4.filename =  str(request.FILES['filename4'])
            c4.file_location = make_file_location(request.user.email, str(request.FILES['filename4']))
            c4.save()
        f5_timedelta = datetime.timedelta(0)
        if nps > 4:
            f5 = Files()
            f5.program_id = p.program_id
            f5.version_id = v.version_id
            f5.segment = 5
            if request.POST.get('how') == 'upload':
                f5.filename = str(request.FILES['filename5'])
            else:
                f5.filename = request.POST.get('filenametext5')
            f5.title = request.POST.get('file_title5')
            f5.file_size = request.POST.get('size5') + request.POST.get('file_size_bytes5')
            f5.bitrate = request.POST.get('bitrate5')
            f5.stereo = request.POST.get('stereo5')
            f5.format_id = request.POST.get('file_type_text5')
            f5_hrs = request.POST.get('hour5')
            f5_minutes = request.POST.get('minute5')
            f5_seconds = request.POST.get('second5')
            f5.length = f5_hrs + ':' + f5_minutes + ':' + f5_seconds
            f5_timedelta = datetime.timedelta(0, (3600 * int(f5_hrs)) + (60 * int(f5_minutes)) + int(f5_seconds))
            f5.how = request.POST.get('how')
            f6.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename5']), request.FILES['filename5'])
            f5.save()
            c5 = Locations()
            c5.file_id = f5.file_id
            c5.filename =  str(request.FILES['filename5'])
            c5.file_location = make_file_location(request.user.email, str(request.FILES['filename5']))
            c5.save()
        f6_timedelta = datetime.timedelta(0)
        if nps > 5:
            f6 = Files()
            f6.program_id = p.program_id
            f6.version_id = v.version_id
            f6.segment = 6
            if request.POST.get('how') == 'upload':
                f6.filename = str(request.FILES['filename6'])
            else:
                f6.filename = request.POST.get('filenametext6')
            f6.title = request.POST.get('file_title6')
            f6.file_size = request.POST.get('size6') + request.POST.get('file_size_bytes6')
            f6.bitrate = request.POST.get('bitrate6')
            f6.stereo = request.POST.get('stereo6')
            f6.format_id = request.POST.get('file_type_text6')
            f6_hrs = request.POST.get('hour6')
            f6_minutes = request.POST.get('minute6')
            f6_seconds = request.POST.get('second6')
            f6.length = f6_hrs + ':' + f6_minutes + ':' + f6_seconds
            f6_timedelta = datetime.timedelta(0, (3600 * int(f6_hrs)) + (60 * int(f6_minutes)) + int(f6_seconds))
            f6.how = request.POST.get('how')
            f6.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename6']), request.FILES['filename6'])
            f6.save()
            c6 = Locations()
            c6.file_id = f6.file_id
            c6.filename =  str(request.FILES['filename6'])
            c6.file_location = make_file_location(request.user.email, str(request.FILES['filename6']))
            c6.save()
        f7_timedelta = datetime.timedelta(0)
        if nps > 6:
            f7 = Files()
            f7.program_id = p.program_id
            f7.version_id = v.version_id
            f7.segment = 7
            if request.POST.get('how') == 'upload':
                f7.filename = str(request.FILES['filename7'])
            else:
                f7.filename = request.POST.get('filenametext7')
            f7.title = request.POST.get('file_title7')
            f7.file_size = request.POST.get('size7') + request.POST.get('file_size_bytes7')
            f7.bitrate = request.POST.get('bitrate7')
            f7.stereo = request.POST.get('stereo7')
            f7.format_id = request.POST.get('file_type_text7')
            f7_hrs = request.POST.get('hour7')
            f7_minutes = request.POST.get('minute7')
            f7_seconds = request.POST.get('second7')
            f7.length = f7_hrs + ':' + f7_minutes + ':' + f7_seconds
            f7_timedelta = datetime.timedelta(0, (3600 * int(f7_hrs)) + (60 * int(f7_minutes)) + int(f7_seconds))
            f7.how = request.POST.get('how')
            f7.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename7']), request.FILES['filename7'])
            f7.save()
            c7 = Locations()
            c7.file_id = f7.file_id
            c7.filename =  str(request.FILES['filename7'])
            c7.file_location = make_file_location(request.user.email, str(request.FILES['filename7']))
            c7.save()
        f8_timedelta = datetime.timedelta(0)
        if nps > 7:
            f8 = Files()
            f8.program_id = p.program_id
            f8.version_id = v.version_id
            f8.segment = 8
            if request.POST.get('how') == 'upload':
                f8.filename = str(request.FILES['filename8'])
            else:
                f8.filename = request.POST.get('filenametext8')
            f8.title = request.POST.get('file_title8')
            f8.file_size = request.POST.get('size8') + request.POST.get('file_size_bytes8')
            f8.bitrate = request.POST.get('bitrate8')
            f8.stereo = request.POST.get('stereo8')
            f8.format_id = request.POST.get('file_type_text8')
            f8_hrs = request.POST.get('hour8')
            f8_minutes = request.POST.get('minute8')
            f8_seconds = request.POST.get('second8')
            f8.length = f8_hrs + ':' + f8_minutes + ':' + f8_seconds
            f8_timedelta = datetime.timedelta(0, (3600 * int(f8_hrs)) + (60 * int(f8_minutes)) + int(f8_seconds))
            f8.how = request.POST.get('how')
            f8.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename8']), request.FILES['filename8'])
            f8.save()
            c8 = Locations()
            c8.file_id = f8.file_id
            c8.filename =  str(request.FILES['filename8'])
            c8.file_location = make_file_location(request.user.email, str(request.FILES['filename8']))
            c8.save()
        f9_timedelta = datetime.timedelta(0)
        if nps > 8:
            f9 = Files()
            f9.program_id = p.program_id
            f9.version_id = v.version_id
            f9.segment = 9
            if request.POST.get('how') == 'upload':
                f9.filename = str(request.FILES['filename9'])
            else:
                f9.filename = request.POST.get('filenametext9')
            f9.title = request.POST.get('file_title9')
            f9.file_size = request.POST.get('size9') + request.POST.get('file_size_bytes9')
            f9.bitrate = request.POST.get('bitrate9')
            f9.stereo = request.POST.get('stereo9')
            f9.format_id = request.POST.get('file_type_text9')
            f9_hrs = request.POST.get('hour9')
            f9_minutes = request.POST.get('minute9')
            f9_seconds = request.POST.get('second9')
            f9.length = f9_hrs + ':' + f9_minutes + ':' + f9_seconds
            f9_timedelta = datetime.timedelta(0, (3600 * int(f9_hrs)) + (60 * int(f9_minutes)) + int(f9_seconds))
            f9.how = request.POST.get('how')
            f9.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename9']), request.FILES['filename9'])
            f9.save()
            c9 = Locations()
            c9.file_id = f9.file_id
            c9.filename =  str(request.FILES['filename9'])
            c9.file_location = make_file_location(request.user.email, str(request.FILES['filename9']))
            c9.save()
        f10_timedelta = datetime.timedelta(0)
        if nps > 9:
            f10 = Files()
            f10.program_id = p.program_id
            f10.version_id = v.version_id
            f10.segment = 10
            if request.POST.get('how') == 'upload':
                f10.filename = str(request.FILES['filename1'])
            else:
                f10.filename = request.POST.get('filenametext10')
            f10.title = request.POST.get('file_title10')
            f10.file_size = request.POST.get('size10') + request.POST.get('file_size_bytes10')
            f10.bitrate = request.POST.get('bitrate10')
            f10.stereo = request.POST.get('stereo10')
            f10.format_id = request.POST.get('file_type_text10')
            f10_hrs = request.POST.get('hour10')
            f10_minutes = request.POST.get('minute10')
            f10_seconds = request.POST.get('second10')
            f10.length = f10_hrs + ':' + f10_minutes + ':' + f10_seconds
            f10_timedelta = datetime.timedelta(0, (3600 * int(f10_hrs)) + (60 * int(f10_minutes)) + int(f10_seconds))
            f10.how = request.POST.get('how')
            f10.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename10']), request.FILES['filename10'])
            f10.save()
            c10 = Locations()
            c10.file_id = f10.file_id
            c10.filename =  str(request.FILES['filename10'])
            c10.file_location = make_file_location(request.user.email, str(request.FILES['filename10']))
            c10.save()
        v.length = str(f1_timedelta + f2_timedelta + f3_timedelta + f4_timedelta + f5_timedelta + f6_timedelta + f7_timedelta + f8_timedelta + f9_timedelta + f10_timedelta)
        v.save()
        return HttpResponseRedirect('/')
    else:
        types_to_use = Types.objects.all()
        licenses_to_use = License.objects.all()
        restrictions_to_use = Restrictions.objects.all()
        advisories_to_use = Advisories.objects.all()
        languages_to_use = Lang.objects.all().order_by('lang')
        topics_to_use = Topics.objects.all().order_by('topic')
        uid = request.user.uid
        series_to_use = set([i.series for i in Programs.objects.filter(uid=uid)])
        formats_to_use = Formats.objects.all().order_by('format_name')
        return render(request, 'radio4all/upload_content.html', {
            'types_to_use': types_to_use,
            'license_list': licenses_to_use,
            'broadcast_restrictions_list': restrictions_to_use,
            'advisories_list': advisories_to_use,
            'language_list': languages_to_use,
            'series_list': series_to_use,
            'topics_list': topics_to_use,
            'help_list': formats_to_use
        },)

def edit_program(request, pk):
    if request.method == 'POST':
        now = datetime.datetime.now()
        p = Programs.objects.get(program_id = pk)
        p.program_title = request.POST.get('program_title')
        p.uid = Users.objects.get(uid = request.user.uid)
        p.type = request.POST.get('program_type')
        p.subtitle = request.POST.get('program_subtitle')
        series = request.POST.get('program_series')
        add_series = request.POST.get('program_add_series')
        if series == '':
            p.series = add_series
        else:
            p.series = series
        p.speaker = request.POST.get('program_speaker')
        p.summary = request.POST.get('program_summary')
        p.keywords = request.POST.get('program_keywords')
        p.credits = request.POST.get('program_credits')
        p.license = License.objects.get(cc_id=request.POST.get('program_license'))
        p.restriction = request.POST.get('program_restriction')
        p.notes = request.POST.get('program_notes')
        p.hidden = 0
        p.advisory = Advisories.objects.get(ad_id = request.POST.get('program_advisory'))
        p.keywords = request.POST.get('program_keywords')
        p.password = request.POST.get('program_password')
        p.permanent = 0
        p.save()
        topics = request.POST.getlist('program_topics[]')
        for e in topics:
            t = TopicAssignment()
            t.topic_id = e
            t.program_id = p.program_id
            t.save()
        return HttpResponseRedirect('/')
    else:
        types_to_use = Types.objects.all()
        licenses_to_use = License.objects.all()
        restrictions_to_use = Restrictions.objects.all()
        advisories_to_use = Advisories.objects.all()
        languages_to_use = Lang.objects.all().order_by('lang')
        topic_assignments_orig = TopicAssignment.objects.filter(program_id = pk).values_list('topic_id')
        topic_assignments = []
        for e in topic_assignments_orig:
            topic_assignments.append(e[0])
        topic_assignments_unused = Topics.objects.exclude(topic_id__in=topic_assignments).order_by('topic')
        topic_assignments_used = Topics.objects.filter(topic_id__in=topic_assignments).order_by('topic')
        uid = request.user.uid
        series_to_use = set([i.series for i in Programs.objects.filter(uid=uid)])
        formats_to_use = Formats.objects.all().order_by('format_name')
        program_data = Programs.objects.get(program_id = pk)
        return render(request, 'radio4all/edit_program.html', {
            'types_to_use': types_to_use,
            'license_list': licenses_to_use,
            'broadcast_restrictions_list': restrictions_to_use,
            'advisories_list': advisories_to_use,
            'language_list': languages_to_use,
            'series_list': series_to_use,
            'topic_assignments_used': topic_assignments_used,
            'topic_assignments_unused': topic_assignments_unused,
            'help_list': formats_to_use,
            'program_data': program_data
        },)

def edit_version(request, version_id):
    if request.method == 'POST':
        v = Versions.objects.get(version_id = version_id)
        v.version_title = request.POST.get('version_title')
        v.version_description = request.POST.get('version_description')
        v.lang_id = request.POST.get('version_lang')
        v.date_recorded = request.POST.get('version_date_recorded')
        v.location = request.POST.get('version_location')
        v.script = request.POST.get('version_script')
        v.save()
        return HttpResponseRedirect('/')
    else:
        languages_to_use = Lang.objects.all().order_by('lang')
        version_data = Versions.objects.get(version_id = version_id)
        formats_to_use = Formats.objects.all().order_by('format_name')
        return render(request, 'radio4all/edit_version.html', {
            'language_list': languages_to_use,
            'version_data': version_data,
            'help_list': formats_to_use,
            'date_recorded': str(version_data.date_recorded)
        },)

def add_version(request, program_id):
    if request.method == 'POST':
        nps = int(request.POST.get('program_segments'))
        now = datetime.datetime.now()
        format_map = {f.format_ext: f.format_id for f in Formats.objects.all().order_by('format_name')}
        v = Versions()
        v.version_title = request.POST.get('version_title')
        v.version_description = request.POST.get('version_description')
        v.lang_id = request.POST.get('version_lang')
        v.date_recorded = request.POST.get('version_date_recorded')
        v.location = request.POST.get('version_location')
        v.script = request.POST.get('version_script')
        v.length = '00:00:00'
        v.version = request.POST.get('version_number')
        v.date_created = now
        v.program_id = program_id
        v.save()
        f1 = Files()
        f1.program_id = program_id
        f1.version_id = v.version_id
        f1.segment = 1
        if request.POST.get('how') == 'upload':
            f1.filename = str(request.FILES['filename1'])
            f1.format_id = format_map[os.path.splitext(str(request.FILES['filename1']))[-1].replace('.','')]
        else:
            f1.filename = request.POST.get('filenametext1')
            f1.format_id = request.POST.get('file_type_text1')
        f1.title = request.POST.get('file_title1')
        f1.file_size = request.POST.get('size1') + request.POST.get('file_size_bytes1')
        f1.bitrate = request.POST.get('bitrate1')
        f1.stereo = request.POST.get('stereo1')
        f1_hrs = request.POST.get('hour1')
        f1_minutes = request.POST.get('minute1')
        f1_seconds = request.POST.get('second1')
        f1.length = f1_hrs + ':' + f1_minutes + ':' + f1_seconds
        f1_timedelta = datetime.timedelta(0, (3600 * int(f1_hrs)) + (60 * int(f1_minutes)) + int(f1_seconds))
        f1.how = request.POST.get('how')
        f1.no_delete = 0
        handle_uploaded_file(request.user.email, str(request.FILES['filename1']), request.FILES['filename1'])
        f1.save()
        f2_timedelta = datetime.timedelta(0)
        if nps > 1:
            f2 = Files()
            f2.program_id = p.program_id
            f2.version_id = v.version_id
            f2.segment = 2
            if request.POST.get('how') == 'upload':
                f2.filename = str(request.FILES('filename2'))
                f2.format_id = format_map[os.path.splitext(str(request.FILES['filename2']))[-1].replace('.','')]
            else:
                f2.filename = request.POST.get('filenametext2')
                f2.format_id = request.POST.get('file_type_text2')
            f2.title = request.POST.get('file_title2')
            f2.file_size = request.POST.get('size2') + request.POST.get('file_size_bytes2')
            f2.bitrate = request.POST.get('bitrate2')
            f2.stereo = request.POST.get('stereo2')
            f2_hrs = request.POST.get('hour2')
            f2_minutes = request.POST.get('minute2')
            f2_seconds = request.POST.get('second2')
            f2.length = f2_hrs + ':' + f2_minutes + ':' + f2_seconds
            f2_timedelta = datetime.timedelta(0, (3600 * int(f2_hrs)) + (60 * int(f2_minutes)) + int(f2_seconds))
            f2.how = request.POST.get('how')
            f2.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename2']), request.FILES['filename2'])
            f2.save()
        f3_timedelta = datetime.timedelta(0)
        if nps > 2:
            f3 = Files()
            f3.program_id = p.program_id
            f3.version_id = v.version_id
            f3.segment = 3
            if request.POST.get('how') == 'upload':
                f3.filename = str(request.FILES['filename3'])
                f3.format_id = format_map[os.path.splitext(str(request.FILES['filename3']))[-1].replace('.','')]
            else:
                f3.filename = request.POST.get('filenametext3')
                f3.format_id = request.POST.get('file_type_text3')
            f3.title = request.POST.get('file_title3')
            f3.file_size = request.POST.get('size3') + request.POST.get('file_size_bytes3')
            f3.bitrate = request.POST.get('bitrate3')
            f3.stereo = request.POST.get('stereo3')
            f3_hrs = request.POST.get('hour3')
            f3_minutes = request.POST.get('minute3')
            f3_seconds = request.POST.get('second3')
            f3.length = f3_hrs + ':' + f3_minutes + ':' + f3_seconds
            f3_timedelta = datetime.timedelta(0, (3600 * int(f3_hrs)) + (60 * int(f3_minutes)) + int(f3_seconds))
            f3.how = request.POST.get('how')
            f3.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename3']), request.FILES['filename3'])
            f3.save()
        f4_timedelta = datetime.timedelta(0)
        if nps > 3:
            f4 = Files()
            f4.program_id = p.program_id
            f4.version_id = v.version_id
            f4.segment = 4
            if request.POST.get('how') == 'upload':
                f4.filename = str(request.FILES['filename4'])
                f4.format_id = format_map[os.path.splitext(str(request.FILES['filename4']))[-1].replace('.','')]
            else:
                f4.filename = request.POST.get('filenametext4')
                f4.format_id = request.POST.get('file_type_text4')
            f4.title = request.POST.get('file_title4')
            f4.file_size = request.POST.get('size4') + request.POST.get('file_size_bytes4')
            f4.bitrate = request.POST.get('bitrate4')
            f4.stereo = request.POST.get('stereo4')
            f4_hrs = request.POST.get('hour4')
            f4_minutes = request.POST.get('minute4')
            f4_seconds = request.POST.get('second4')
            f4.length = f4_hrs + ':' + f4_minutes + ':' + f4_seconds
            f4_timedelta = datetime.timedelta(0, (3600 * int(f4_hrs)) + (60 * int(f4_minutes)) + int(f4_seconds))
            f4.how = request.POST.get('how')
            f4.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename4']), request.FILES['filename4'])
            f4.save()
        f5_timedelta = datetime.timedelta(0)
        if nps > 4:
            f5 = Files()
            f5.program_id = p.program_id
            f5.version_id = v.version_id
            f5.segment = 5
            if request.POST.get('how') == 'upload':
                f5.filename = str(request.FILES['filename5'])
                f5.format_id = format_map[os.path.splitext(str(request.FILES['filename5']))[-1].replace('.','')]
            else:
                f5.filename = request.POST.get('filenametext5')
                f5.format_id = request.POST.get('file_type_text5')
            f5.title = request.POST.get('file_title5')
            f5.file_size = request.POST.get('size5') + request.POST.get('file_size_bytes5')
            f5.bitrate = request.POST.get('bitrate5')
            f5.stereo = request.POST.get('stereo5')
            f5_hrs = request.POST.get('hour5')
            f5_minutes = request.POST.get('minute5')
            f5_seconds = request.POST.get('second5')
            f5.length = f5_hrs + ':' + f5_minutes + ':' + f5_seconds
            f5_timedelta = datetime.timedelta(0, (3600 * int(f5_hrs)) + (60 * int(f5_minutes)) + int(f5_seconds))
            f5.how = request.POST.get('how')
            f6.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename5']), request.FILES['filename5'])
            f5.save()
        f6_timedelta = datetime.timedelta(0)
        if nps > 5:
            f6 = Files()
            f6.program_id = p.program_id
            f6.version_id = v.version_id
            f6.segment = 6
            if request.POST.get('how') == 'upload':
                f6.filename = str(request.FILES['filename6'])
                f6.format_id = format_map[os.path.splitext(str(request.FILES['filename6']))[-1].replace('.','')]
            else:
                f6.filename = request.POST.get('filenametext6')
                f6.format_id = request.POST.get('file_type_text6')
            f6.title = request.POST.get('file_title6')
            f6.file_size = request.POST.get('size6') + request.POST.get('file_size_bytes6')
            f6.bitrate = request.POST.get('bitrate6')
            f6.stereo = request.POST.get('stereo6')
            f6_hrs = request.POST.get('hour6')
            f6_minutes = request.POST.get('minute6')
            f6_seconds = request.POST.get('second6')
            f6.length = f6_hrs + ':' + f6_minutes + ':' + f6_seconds
            f6_timedelta = datetime.timedelta(0, (3600 * int(f6_hrs)) + (60 * int(f6_minutes)) + int(f6_seconds))
            f6.how = request.POST.get('how')
            f6.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename6']), request.FILES['filename6'])
            f6.save()
        f7_timedelta = datetime.timedelta(0)
        if nps > 6:
            f7 = Files()
            f7.program_id = p.program_id
            f7.version_id = v.version_id
            f7.segment = 7
            if request.POST.get('how') == 'upload':
                f7.filename = str(request.FILES['filename7'])
                f7.format_id = format_map[os.path.splitext(str(request.FILES['filename7']))[-1].replace('.','')]
            else:
                f7.filename = request.POST.get('filenametext7')
                f7.format_id = request.POST.get('file_type_text7')
            f7.title = request.POST.get('file_title7')
            f7.file_size = request.POST.get('size7') + request.POST.get('file_size_bytes7')
            f7.bitrate = request.POST.get('bitrate7')
            f7.stereo = request.POST.get('stereo7')
            f7_hrs = request.POST.get('hour7')
            f7_minutes = request.POST.get('minute7')
            f7_seconds = request.POST.get('second7')
            f7.length = f7_hrs + ':' + f7_minutes + ':' + f7_seconds
            f7_timedelta = datetime.timedelta(0, (3600 * int(f7_hrs)) + (60 * int(f7_minutes)) + int(f7_seconds))
            f7.how = request.POST.get('how')
            f7.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename7']), request.FILES['filename7'])
            f7.save()
        f8_timedelta = datetime.timedelta(0)
        if nps > 7:
            f8 = Files()
            f8.program_id = p.program_id
            f8.version_id = v.version_id
            f8.segment = 8
            if request.POST.get('how') == 'upload':
                f8.filename = str(request.FILES['filename8'])
                f8.format_id = format_map[os.path.splitext(str(request.FILES['filename8']))[-1].replace('.','')]
            else:
                f8.filename = request.POST.get('filenametext8')
                f8.format_id = request.POST.get('file_type_text8')
            f8.title = request.POST.get('file_title8')
            f8.file_size = request.POST.get('size8') + request.POST.get('file_size_bytes8')
            f8.bitrate = request.POST.get('bitrate8')
            f8.stereo = request.POST.get('stereo8')
            f8_hrs = request.POST.get('hour8')
            f8_minutes = request.POST.get('minute8')
            f8_seconds = request.POST.get('second8')
            f8.length = f8_hrs + ':' + f8_minutes + ':' + f8_seconds
            f8_timedelta = datetime.timedelta(0, (3600 * int(f8_hrs)) + (60 * int(f8_minutes)) + int(f8_seconds))
            f8.how = request.POST.get('how')
            f8.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename8']), request.FILES['filename8'])
            f8.save()
        f9_timedelta = datetime.timedelta(0)
        if nps > 8:
            f9 = Files()
            f9.program_id = p.program_id
            f9.version_id = v.version_id
            f9.segment = 9
            if request.POST.get('how') == 'upload':
                f9.filename = str(request.FILES['filename9'])
                f9.format_id = format_map[os.path.splitext(str(request.FILES['filename9']))[-1].replace('.','')]
            else:
                f9.filename = request.POST.get('filenametext9')
                f9.format_id = request.POST.get('file_type_text9')
            f9.title = request.POST.get('file_title9')
            f9.file_size = request.POST.get('size9') + request.POST.get('file_size_bytes9')
            f9.bitrate = request.POST.get('bitrate9')
            f9.stereo = request.POST.get('stereo9')
            f9_hrs = request.POST.get('hour9')
            f9_minutes = request.POST.get('minute9')
            f9_seconds = request.POST.get('second9')
            f9.length = f9_hrs + ':' + f9_minutes + ':' + f9_seconds
            f9_timedelta = datetime.timedelta(0, (3600 * int(f9_hrs)) + (60 * int(f9_minutes)) + int(f9_seconds))
            f9.how = request.POST.get('how')
            f9.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename9']), request.FILES['filename9'])
            f9.save()
        f10_timedelta = datetime.timedelta(0)
        if nps > 9:
            f10 = Files()
            f10.program_id = p.program_id
            f10.version_id = v.version_id
            f10.segment = 10
            if request.POST.get('how') == 'upload':
                f10.filename = str(request.FILES['filename1'])
                f10.format_id = format_map[os.path.splitext(str(request.FILES['filename10']))[-1].replace('.','')]
            else:
                f10.filename = request.POST.get('filenametext10')
                f10.format_id = request.POST.get('file_type_text10')
            f10.title = request.POST.get('file_title10')
            f10.file_size = request.POST.get('size10') + request.POST.get('file_size_bytes10')
            f10.bitrate = request.POST.get('bitrate10')
            f10.stereo = request.POST.get('stereo10')
            f10_hrs = request.POST.get('hour10')
            f10_minutes = request.POST.get('minute10')
            f10_seconds = request.POST.get('second10')
            f10.length = f10_hrs + ':' + f10_minutes + ':' + f10_seconds
            f10_timedelta = datetime.timedelta(0, (3600 * int(f10_hrs)) + (60 * int(f10_minutes)) + int(f10_seconds))
            f10.how = request.POST.get('how')
            f10.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename10']), request.FILES['filename10'])
            f10.save()
        v.length = str(f1_timedelta + f2_timedelta + f3_timedelta + f4_timedelta + f5_timedelta + f6_timedelta + f7_timedelta + f8_timedelta + f9_timedelta + f10_timedelta)
        v.save()
        return HttpResponseRedirect('/')
    else:
        languages_to_use = Lang.objects.all().order_by('lang')
        formats_to_use = Formats.objects.all().order_by('format_name')
        version_tmp = Versions.objects.filter(program_id = program_id).order_by('-version')
        uid = request.user.uid
        return render(request, 'radio4all/add_version.html', {
            'language_list': languages_to_use,
            'help_list': formats_to_use,
            'program_id': program_id,
            'version_number_to_use': version_tmp[0].version + 1
        },)

def add_files(request, program_id, version_id):
    if request.method == 'POST':
        nps = int(request.POST.get('program_segments'))
        format_map = {f.format_ext: f.format_id for f in Formats.objects.all().order_by('format_name')}
        f1 = Files()
        f1.program_id = program_id
        f1.version_id = version_id
        f1.segment = int(request.POST.get('segment_number_to_use'))
        if request.POST.get('how') == 'upload':
            f1.filename = str(request.FILES['filename1'])
            f1.format_id = format_map[os.path.splitext(str(request.FILES['filename1']))[-1].replace('.','')]
        else:
            f1.filename = request.POST.get('filenametext1')
            f1.format_id = request.POST.get('file_type_text1')
        f1.title = request.POST.get('file_title1')
        f1.file_size = request.POST.get('size1') + request.POST.get('file_size_bytes1')
        f1.bitrate = request.POST.get('bitrate1')
        f1.stereo = request.POST.get('stereo1')
        f1_hrs = request.POST.get('hour1')
        f1_minutes = request.POST.get('minute1')
        f1_seconds = request.POST.get('second1')
        f1.length = f1_hrs + ':' + f1_minutes + ':' + f1_seconds
        f1_timedelta = datetime.timedelta(0, (3600 * int(f1_hrs)) + (60 * int(f1_minutes)) + int(f1_seconds))
        f1.how = request.POST.get('how')
        f1.no_delete = 0
        handle_uploaded_file(request.user.email, str(request.FILES['filename1']), request.FILES['filename1'])
        f1.save()
        f2_timedelta = datetime.timedelta(0)
        if nps > 1:
            f2 = Files()
            f2.program_id = program_id
            f2.version_id = version_id
            f2.segment = int(request.POST.get('segment_number_to_use')) + 1
            if request.POST.get('how') == 'upload':
                f2.filename = str(request.FILES('filename2'))
                f2.format_id = format_map[os.path.splitext(str(request.FILES['filename2']))[-1].replace('.','')]
            else:
                f2.filename = request.POST.get('filenametext2')
                f2.format_id = request.POST.get('file_type_text2')
            f2.title = request.POST.get('file_title2')
            f2.file_size = request.POST.get('size2') + request.POST.get('file_size_bytes2')
            f2.bitrate = request.POST.get('bitrate2')
            f2.stereo = request.POST.get('stereo2')
            f2_hrs = request.POST.get('hour2')
            f2_minutes = request.POST.get('minute2')
            f2_seconds = request.POST.get('second2')
            f2.length = f2_hrs + ':' + f2_minutes + ':' + f2_seconds
            f2_timedelta = datetime.timedelta(0, (3600 * int(f2_hrs)) + (60 * int(f2_minutes)) + int(f2_seconds))
            f2.how = request.POST.get('how')
            f2.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename2']), request.FILES['filename2'])
            f2.save()
        f3_timedelta = datetime.timedelta(0)
        if nps > 2:
            f3 = Files()
            f3.program_id = program_id
            f3.version_id = version_id
            f3.segment = int(request.POST.get('segment_number_to_use')) + 2
            if request.POST.get('how') == 'upload':
                f3.filename = str(request.FILES['filename3'])
                f3.format_id = format_map[os.path.splitext(str(request.FILES['filename3']))[-1].replace('.','')]
            else:
                f3.filename = request.POST.get('filenametext3')
                f3.format_id = request.POST.get('file_type_text3')
            f3.title = request.POST.get('file_title3')
            f3.file_size = request.POST.get('size3') + request.POST.get('file_size_bytes3')
            f3.bitrate = request.POST.get('bitrate3')
            f3.stereo = request.POST.get('stereo3')
            f3_hrs = request.POST.get('hour3')
            f3_minutes = request.POST.get('minute3')
            f3_seconds = request.POST.get('second3')
            f3.length = f3_hrs + ':' + f3_minutes + ':' + f3_seconds
            f3_timedelta = datetime.timedelta(0, (3600 * int(f3_hrs)) + (60 * int(f3_minutes)) + int(f3_seconds))
            f3.how = request.POST.get('how')
            f3.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename3']), request.FILES['filename3'])
            f3.save()
        f4_timedelta = datetime.timedelta(0)
        if nps > 3:
            f4 = Files()
            f4.program_id = program_id
            f4.version_id = version_id
            f4.segment = int(request.POST.get('segment_number_to_use')) + 3
            if request.POST.get('how') == 'upload':
                f4.filename = str(request.FILES['filename4'])
                f4.format_id = format_map[os.path.splitext(str(request.FILES['filename4']))[-1].replace('.','')]
            else:
                f4.filename = request.POST.get('filenametext4')
                f4.format_id = request.POST.get('file_type_text4')
            f4.title = request.POST.get('file_title4')
            f4.file_size = request.POST.get('size4') + request.POST.get('file_size_bytes4')
            f4.bitrate = request.POST.get('bitrate4')
            f4.stereo = request.POST.get('stereo4')
            f4_hrs = request.POST.get('hour4')
            f4_minutes = request.POST.get('minute4')
            f4_seconds = request.POST.get('second4')
            f4.length = f4_hrs + ':' + f4_minutes + ':' + f4_seconds
            f4_timedelta = datetime.timedelta(0, (3600 * int(f4_hrs)) + (60 * int(f4_minutes)) + int(f4_seconds))
            f4.how = request.POST.get('how')
            f4.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename4']), request.FILES['filename4'])
            f4.save()
        f5_timedelta = datetime.timedelta(0)
        if nps > 4:
            f5 = Files()
            f5.program_id = program_id
            f5.version_id = version_id
            f5.segment = int(request.POST.get('segment_number_to_use')) + 4
            if request.POST.get('how') == 'upload':
                f5.filename = str(request.FILES['filename5'])
                f5.format_id = format_map[os.path.splitext(str(request.FILES['filename5']))[-1].replace('.','')]
            else:
                f5.filename = request.POST.get('filenametext5')
                f5.format_id = request.POST.get('file_type_text5')
            f5.title = request.POST.get('file_title5')
            f5.file_size = request.POST.get('size5') + request.POST.get('file_size_bytes5')
            f5.bitrate = request.POST.get('bitrate5')
            f5.stereo = request.POST.get('stereo5')
            f5_hrs = request.POST.get('hour5')
            f5_minutes = request.POST.get('minute5')
            f5_seconds = request.POST.get('second5')
            f5.length = f5_hrs + ':' + f5_minutes + ':' + f5_seconds
            f5_timedelta = datetime.timedelta(0, (3600 * int(f5_hrs)) + (60 * int(f5_minutes)) + int(f5_seconds))
            f5.how = request.POST.get('how')
            f6.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename5']), request.FILES['filename5'])
            f5.save()
        f6_timedelta = datetime.timedelta(0)
        if nps > 5:
            f6 = Files()
            f6.program_id = program_id
            f6.version_id = version_id
            f6.segment = int(request.POST.get('segment_number_to_use')) + 5
            if request.POST.get('how') == 'upload':
                f6.filename = str(request.FILES['filename6'])
                f6.format_id = format_map[os.path.splitext(str(request.FILES['filename6']))[-1].replace('.','')]
            else:
                f6.filename = request.POST.get('filenametext6')
                f6.format_id = request.POST.get('file_type_text6')
            f6.title = request.POST.get('file_title6')
            f6.file_size = request.POST.get('size6') + request.POST.get('file_size_bytes6')
            f6.bitrate = request.POST.get('bitrate6')
            f6.stereo = request.POST.get('stereo6')
            f6_hrs = request.POST.get('hour6')
            f6_minutes = request.POST.get('minute6')
            f6_seconds = request.POST.get('second6')
            f6.length = f6_hrs + ':' + f6_minutes + ':' + f6_seconds
            f6_timedelta = datetime.timedelta(0, (3600 * int(f6_hrs)) + (60 * int(f6_minutes)) + int(f6_seconds))
            f6.how = request.POST.get('how')
            f6.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename6']), request.FILES['filename6'])
            f6.save()
        f7_timedelta = datetime.timedelta(0)
        if nps > 6:
            f7 = Files()
            f7.program_id = program_id
            f7.version_id = version_id
            f7.segment = int(request.POST.get('segment_number_to_use')) + 6
            if request.POST.get('how') == 'upload':
                f7.filename = str(request.FILES['filename7'])
                f7.format_id = format_map[os.path.splitext(str(request.FILES['filename7']))[-1].replace('.','')]
            else:
                f7.filename = request.POST.get('filenametext7')
                f7.format_id = request.POST.get('file_type_text7')
            f7.title = request.POST.get('file_title7')
            f7.file_size = request.POST.get('size7') + request.POST.get('file_size_bytes7')
            f7.bitrate = request.POST.get('bitrate7')
            f7.stereo = request.POST.get('stereo7')
            f7_hrs = request.POST.get('hour7')
            f7_minutes = request.POST.get('minute7')
            f7_seconds = request.POST.get('second7')
            f7.length = f7_hrs + ':' + f7_minutes + ':' + f7_seconds
            f7_timedelta = datetime.timedelta(0, (3600 * int(f7_hrs)) + (60 * int(f7_minutes)) + int(f7_seconds))
            f7.how = request.POST.get('how')
            f7.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename7']), request.FILES['filename7'])
            f7.save()
        f8_timedelta = datetime.timedelta(0)
        if nps > 7:
            f8 = Files()
            f8.program_id = p.program_id
            f8.version_id = v.version_id
            f8.segment = int(request.POST.get('segment_number_to_use')) + 7
            if request.POST.get('how') == 'upload':
                f8.filename = str(request.FILES['filename8'])
                f8.format_id = format_map[os.path.splitext(str(request.FILES['filename8']))[-1].replace('.','')]
            else:
                f8.filename = request.POST.get('filenametext8')
                f8.format_id = request.POST.get('file_type_text8')
            f8.title = request.POST.get('file_title8')
            f8.file_size = request.POST.get('size8') + request.POST.get('file_size_bytes8')
            f8.bitrate = request.POST.get('bitrate8')
            f8.stereo = request.POST.get('stereo8')
            f8_hrs = request.POST.get('hour8')
            f8_minutes = request.POST.get('minute8')
            f8_seconds = request.POST.get('second8')
            f8.length = f8_hrs + ':' + f8_minutes + ':' + f8_seconds
            f8_timedelta = datetime.timedelta(0, (3600 * int(f8_hrs)) + (60 * int(f8_minutes)) + int(f8_seconds))
            f8.how = request.POST.get('how')
            f8.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename8']), request.FILES['filename8'])
            f8.save()
        f9_timedelta = datetime.timedelta(0)
        if nps > 8:
            f9 = Files()
            f9.program_id = program_id
            f9.version_id = version_id
            f9.segment = int(request.POST.get('segment_number_to_use')) + 8
            if request.POST.get('how') == 'upload':
                f9.filename = str(request.FILES['filename9'])
                f9.format_id = format_map[os.path.splitext(str(request.FILES['filename9']))[-1].replace('.','')]
            else:
                f9.filename = request.POST.get('filenametext9')
                f9.format_id = request.POST.get('file_type_text9')
            f9.title = request.POST.get('file_title9')
            f9.file_size = request.POST.get('size9') + request.POST.get('file_size_bytes9')
            f9.bitrate = request.POST.get('bitrate9')
            f9.stereo = request.POST.get('stereo9')
            f9_hrs = request.POST.get('hour9')
            f9_minutes = request.POST.get('minute9')
            f9_seconds = request.POST.get('second9')
            f9.length = f9_hrs + ':' + f9_minutes + ':' + f9_seconds
            f9_timedelta = datetime.timedelta(0, (3600 * int(f9_hrs)) + (60 * int(f9_minutes)) + int(f9_seconds))
            f9.how = request.POST.get('how')
            f9.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename9']), request.FILES['filename9'])
            f9.save()
        f10_timedelta = datetime.timedelta(0)
        if nps > 9:
            f10 = Files()
            f10.program_id = program_id
            f10.version_id = version_id
            f10.segment = int(request.POST.get('segment_number_to_use')) + 9
            if request.POST.get('how') == 'upload':
                f10.filename = str(request.FILES['filename1'])
                f10.format_id = format_map[os.path.splitext(str(request.FILES['filename10']))[-1].replace('.','')]
            else:
                f10.filename = request.POST.get('filenametext10')
                f10.format_id = request.POST.get('file_type_text10')
            f10.title = request.POST.get('file_title10')
            f10.file_size = request.POST.get('size10') + request.POST.get('file_size_bytes10')
            f10.bitrate = request.POST.get('bitrate10')
            f10.stereo = request.POST.get('stereo10')
            f10_hrs = request.POST.get('hour10')
            f10_minutes = request.POST.get('minute10')
            f10_seconds = request.POST.get('second10')
            f10.length = f10_hrs + ':' + f10_minutes + ':' + f10_seconds
            f10_timedelta = datetime.timedelta(0, (3600 * int(f10_hrs)) + (60 * int(f10_minutes)) + int(f10_seconds))
            f10.how = request.POST.get('how')
            f10.no_delete = 0
            handle_uploaded_file(request.user.email, str(request.FILES['filename10']), request.FILES['filename10'])
            f10.save()
        return HttpResponseRedirect('/')
    else:
        segment_tmp = Files.objects.filter(program_id = program_id, version_id = version_id).order_by('-segment')
        uid = request.user.uid
        return render(request, 'radio4all/add_files.html', {
            'program_id': program_id,
            'version_id': version_id,
            'segment_number_to_use': segment_tmp[0].segment + 1
        },)

def delete_given_file(email_dir, file_name):
    file_to_delete = '/tank/radio4all/files/' + email_dir + '/' + file_name
    if os.path.isfile(file_to_delete):
        os.remove(file_to_delete)

def delete_version(request, program_id, version_id):
    if request.method == 'POST':
        # add in provisions to block for failed password in anonymous uploads
        program_data = Programs.objects.get(program_id = program_id)
        file_ids_to_use = [x.file_id for x in Files.objects.filter(version_id = version_id)]
        version_ids_to_use = [x.version_id for x in Versions.objects.filter(program_id = program_id).order_by('version')]
        keep_files = request.POST.get('keep_files')
        is_anonymous = request.POST.get('is_anonymous_hidden')
        curs = connection.cursor()
        curs.execute("SELECT t1.file_id, t1.how, t1.filename, t2.file_location FROM files AS t1, locations AS t2 WHERE t1.program_id = %s AND t1.version_id = %s AND t1.no_delete = 0 AND t1.file_id = t2.file_id", (program_id, version_id))
        files_to_keep = curs.fetchall()
        curs.execute('DELETE from versions where version_id = %s', (version_id,))
        for file_id in file_ids_to_use:
            curs.execute('DELETE from locations where file_id = %s', (file_id,))
        i = 1
        for version_id in version_ids_to_use:
            curs.execute('UPDATE versions set version = %s where version_id = %s', (i, file_id,))
            i = i + 1
        curs.close()
        if not keep_files:
            for e in files_to_keep:
                delete_given_file(request.user.email, e[2])
        return render(request, 'radio4all/delete_version_completed.html', {
            'program_id': program_id,
            'files_to_keep': files_to_keep,
            'keep_files': keep_files,
            'delete_title': program_data.program_title
        },)
    else:
        is_anonymous = (request.user.email == 'anonymous@radio4all.net')
        program_data = Programs.objects.get(program_id = program_id)
        version_data = Versions.objects.get(version_id = version_id)
        return render(request, 'radio4all/delete_version.html', {
            'program_id': program_id,
            'version_id': version_id,
            'program_title': program_data.program_title,
            'version': version_data.version,
            'is_anonymous': is_anonymous
        },)

def delete_program(request, program_id):
    if request.method == 'POST':
        # add in provisions to block for failed password
        file_ids_to_use = [x.file_id for x in Files.objects.filter(version_id = version_id)]
        version_ids_to_use = [x.version_id for x in Versions.objects.filter(program_id = program_id).order_by('version')]
        keep_files = request.POST.get('keep_files')
        program_data = Programs.objects.get(program_id = program_id)
        curs = connection.cursor()
        curs.execute("SELECT t1.file_id, t1.how, t1.filename, t2.file_location FROM files AS t1, locations AS t2 WHERE t1.program_id = %s AND t1.no_delete = 0 AND t1.file_id = t2.file_id", (program_id))
        files_to_keep = curs.fetchall()
        curs.execute('DELETE from programs where program_id = %s', (program_id,))
        for file_id in file_ids_to_use:
            curs.execute('DELETE from files where file_id = %s', (file_id,))
            curs.execute('DELETE from locations where file_id = %s', (file_id,))
        for version_id in version_ids_to_use:
            curs.execute('DELETE from versions where version_id = %s', (file_id,))
        curs.close()
        if not keep_files:
            for e in files_to_keep:
                delete_given_file(request.user.email, e[2])
        return render(request, 'radio4all/delete_program_completed.html', {
            'program_id': program_id,
            'files_to_keep': files_to_keep,
            'keep_files': keep_files,
            'program_title': program_data.program_title
        },)
    else:
        is_anonymous = (request.user.email == 'anonymous@radio4all.net')
        program_data = Programs.objects.get(program_id = program_id)
        return render(request, 'radio4all/delete_program.html', {
            'program_id': program_id,
            'program_title': program_data.program_title,
            'is_anonymous': is_anonymous
        },)

def show_script(request, program_id, version_id):
    curs = connection.cursor()
    curs.execute("SELECT t1.script, t2.program_title FROM versions AS t1, programs AS t2 WHERE t1.program_id = %s AND t2.hidden = '0' AND t1.version_id = %s AND t1.program_id = t2.program_id", (program_id, version_id))
    r = curs.fetchall()
    curs.close()
    return render(request, 'radio4all/script.html', {
        'program_title': r[0][1],
        'script': r[0][0]
    },)

def topic_browse(request):
    try:
        curs = connection.cursor()
        curs.execute("SELECT count(t1.assign_id) as quantity, t1.topic_id as tag_id, t2.topic as tag FROM topic_assignment AS t1, topics AS t2 WHERE t1.topic_id = t2.topic_id AND t1.program_id NOT IN (SELECT program_id FROM programs WHERE hidden != 0) GROUP BY t1.topic_id ORDER BY t2.topic ASC")
        raw_topic_data = curs.fetchall()
        curs.close()
        qtys = [x[0] for x in raw_topic_data]
        max_qty = max(qtys)
        min_qty = min(qtys)
        max_size = 270
        min_size = 110
        spread = max_qty - min_qty
        step = (max_size - min_size) / spread
        topic_data = []
        for r in raw_topic_data:
            size = ceil(min_size + ((r[0] - min_qty) * step))
            topic_data.append([size, r[0], r[1], r[2]])
        target = topic_data
    except Topics.DoesNotExist:
        return HttpResponse('<h1>No Topics Found</h1>')
    return render(request, 'radio4all/topic_cloud.html', {
        'topic_data': target,
    },)

def filter_topic(request, topic_id):
    try:
        topic = Topics.objects.get(topic_id=topic_id).topic
        curs = connection.cursor()
        curs.execute("SELECT t1.program_id, t1.program_title, t1.subtitle, t1.date_created, t2.length, t1.speaker FROM programs as t1 INNER JOIN (versions as t2, users AS t3, topic_assignment AS t4) ON (t1.program_id = t2.program_id AND t1.hidden = '0' AND t4.topic_id = %s AND t1.program_id = t4.program_id AND t2.version = '1' AND t3.uid = t1.uid) ORDER BY program_id DESC", (topic_id,))
        filter_topic_data = []
        for c in curs.fetchall():
            filter_topic_data.append({'program_id': c[0], 'program_title': c[1], 'subtitle': c[2], 'date_created': c[3], 'length': c[4], 'speaker': c[5]})
        curs.close()
        target = filter_topic_data
        paginator = Paginator(target, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/programs_in_topic.html', {
        'page_obj': page_obj,
        'topic': topic,
    },)

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
            programs_series = Programs.objects.filter(series__startswith='0') | Programs.objects.filter(series__startswith='1') | Programs.objects.filter(series__startswith='2') | Programs.objects.filter(series__startswith='3') | Programs.objects.filter(series__startswith='4') | Programs.objects.filter(series__startswith='5') | Programs.objects.filter(series__startswith='6') | Programs.objects.filter(series__startswith='7') | Programs.objects.filter(series__startswith='8') | Programs.objects.filter(series__startswith='9')
        else:
            programs_series = Programs.objects.filter(series__startswith=letter.capitalize()) | Programs.objects.filter(series__startswith=letter)
        target = programs_series.values('series').distinct()
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/programs_by_series.html', {
        'all_series': target,
        'letter': letter,
    },)

def filter_contributor(request, letter):
    try:
        if letter == "0-9":
            contributors = Users.objects.filter(full_name__startswith='0') | Users.objects.filter(full_name__startswith='1') | Users.objects.filter(full_name__startswith='2') | Users.objects.filter(full_name__startswith='3') | Users.objects.filter(full_name__startswith='4') | Users.objects.filter(full_name__startswith='5') | Users.objects.filter(full_name__startswith='6') | Users.objects.filter(full_name__startswith='7') | Users.objects.filter(full_name__startswith='8') | Users.objects.filter(full_name__startswith='9')
        else:
            contributors = Users.objects.filter(full_name__startswith=letter.capitalize()) | Users.objects.filter(full_name__startswith=letter)
        target = contributors.values('full_name', 'uid').distinct().order_by('full_name')
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/programs_by_contributor.html', {
        'all_contributors': target,
        'letter': letter,
    },)

def get_contributor(request, uid):
    try:
        target = Programs.objects.filter(uid=uid).order_by('-date_created')
        paginator = Paginator(target, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    user_to_use = Users.objects.get(uid=uid)
    return render(request, 'radio4all/programs_by_contributor_indiv.html', {
        'page_obj': page_obj,
        'user_to_use': user_to_use,
    },)

def get_contributor_contact(request, uid):
    target = Users.objects.get(uid=uid)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            to_email = target.email
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, 'info@radio4all.net', [to_email], fail_silently=False,)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('<h1>Message sent!  Thank you.  <a href="http://radio4all.net">Return to Radio4All</a></h1>')
    else:
        return render(request, 'radio4all/contributor_contact.html', {
            'uid': uid,
            'form': ContactForm(),
            'contributor': target,
        },)

def get_series(request, series_name):
    try:
        target = Programs.objects.filter(series=series_name).order_by('-date_created')
        paginator = Paginator(target, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/series_dashboard.html', {
        'page_obj': page_obj,
        'series_name': series_name,
    },)

def filter_license(request, abbrev):
    try:
        license = License.objects.get(cc_abbrev=abbrev)
    except License.DoesNotExist:
        return HttpResponse('<h1>No License Here</h1>')
    try:
        target = Programs.objects.filter(license=license)
        paginator = Paginator(target, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/dashboard.html', {
        'page_obj': page_obj,
    },)

def filter_legacy_license(request, legacy_license):
    restrictions = {'np': 1, 'ne': 2, 'cp': 3, 'sn': 4}
    restriction_to_use = restrictions[legacy_license]
    try:
        target = Programs.objects.filter(restriction=restriction_to_use).order_by('-date_created')
        paginator = Paginator(target, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/dashboard.html', {
        'page_obj': page_obj,
    },)

def filter_advisory(request, advisory_id):
    advisory_strings = {1: 'Unknown - program has not been checked for content', 2: 'No Advisories - content screened and verified', 3: 'Warning: Program may contain strong or potentially offensive language, including possible FCC violations.', 4: 'Warning: Program content only suitable for FCC-designated safe harbor (10PM to 6AM).'}
    advisory_to_use = advisory_strings[advisory_id]
    try:
        target = Programs.objects.filter(advisory=advisory_id).order_by('-date_created')
        paginator = Paginator(target, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/programs_by_advisory.html', {
        'page_obj': page_obj,
        'advisory_string': advisory_to_use
    },)

def filter_length(request, length_to_use):
    try:
        programs_by_length_verbiage = {'00:00:01': '0-1 minute', '00:01:00': '1-2 minutes', '00:02:00':'2-5 minutes', '00:05:00':'5-15 minutes', '00:15:00':'15-30 minutes', '00:30:00':'30-60 minutes', '01:00:00':'60-90 minutes', '01:30:00':'90-120 minutes', '02:00:00':'over 120 minutes'}
        start_time = length_to_use.split(',')[0]
        end_time = length_to_use.split(',')[1]
        curs = connection.cursor()
        curs.execute("SELECT t1.program_id, t1.program_title, t1.series, t1.date_created, t2.length, t3.full_name FROM programs as t1 INNER JOIN (versions as t2, users AS t3) ON (t1.program_id = t2.program_id AND t1.hidden = '0' AND t2.length BETWEEN %s AND %s AND t2.version = '1' AND t3.uid = t1.uid) ORDER BY program_id DESC", (start_time, end_time,))
        filter_length_data = []
        for c in curs.fetchall():
            filter_length_data.append({'program_id': c[0], 'program_title': c[1], 'series': c[2], 'date_created': c[3], 'length': c[4], 'contributor': c[5]})
        curs.close()
        target = filter_length_data
        paginator = Paginator(target, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/programs_by_length.html', {
        'page_obj': page_obj,
        'length_header': programs_by_length_verbiage[start_time],
    },)

def filter_type(request, pk):
    try:
        typer = Types.objects.get(pk=int(pk))
    except Types.DoesNotExist:
        return HttpResponse('<h1>No Type Here</h1>')
    try:
        target = Programs.objects.filter(type=typer.type)
        paginator = Paginator(target, 30)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Programs.DoesNotExist:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/dashboard.html', {
        'page_obj': page_obj,
    },)

def filter_search(request):
    try:
        search_terms = request.POST.get('searchtext')
        search_range = request.POST.get('range')
        if search_range == 'today':
            search_range_date = datetime.date.today()
        elif search_range == 'week':
            search_range_date = datetime.date.today() - datetime.timedelta(days=7)
        elif search_range == 'month':
            search_range_date = datetime.date.today() - datetime.timedelta(days=30)
        else:
            search_range_date = datetime.date(1996, 1, 1)
        search_typeselect = request.POST.get('type')
        search_contributor = request.POST.get('contributor')
        search_filename = request.POST.get('filename')
        search_results = Programs.objects.filter(program_title__icontains=search_terms) | Programs.objects.filter(subtitle__icontains=search_terms) | Programs.objects.filter(series__icontains=search_terms) | Programs.objects.filter(speaker__icontains=search_terms) | Programs.objects.filter(summary__icontains=search_terms) | Programs.objects.filter(keywords__icontains=search_terms) | Programs.objects.filter(credits__icontains=search_terms) | Programs.objects.filter(notes__icontains=search_terms)
        if search_typeselect != 'null' and search_typeselect != None:
            search_results = search_results.filter(type__iexact=search_typeselect)
        if search_contributor == True:
            contributors_to_use = Users.objects.filter(full_name__icontains=search_terms)
            search_results = Programs.objects.filter(uid__in=contributors_to_use.values('uid'))
        if search_filename == True:
            filenames_to_use = Files.objects.filter(filename__icontains=search_terms)
            search_results = Programs.objects.filter(program_id__in=filenames_to_use.values('program_id'))
        paginator = Paginator(search_results.filter(date_created__gte=search_range_date).order_by('-date_created'), 30)
        page_number = request.POST.get('browsecontrol')
        page_obj = paginator.get_page(page_number)
    except:
        return HttpResponse('<h1>No Programs Here</h1>')
    return render(request, 'radio4all/search.html', {
        'page_obj': page_obj,
        'search_terms': search_terms,
        'search_range': search_range,
        'search_typeselect': search_typeselect,
    },)

def podcast_view(request):
    uid = request.GET.get('uid')
    series_name = request.GET.get('series')
    if uid != None:
         queryset = Programs.objects.filter(uid=uid).order_by('-date_created')[:30]
         user_to_use = Users.objects.get(uid=uid)
         f = feedgenerator.Rss201rev2Feed(title="Contributor Podcast: " + user_to_use.full_name, link="http://www.radio4all.net/contributor/" + str(uid), description="Contributor Podcast: " + user_to_use.full_name, docs="http://blogs.law.harvard.edu/tech/rss", generator="A-Infos Radio Project http://www.radio4all.net/", managingEditor="rp@radio4all.net (Editor)",  webmaster="www@radio4all.net (Webmaster)", ttl="240")
    elif uid == None and series_name != None:
         queryset = Programs.objects.filter(series=series_name).order_by('-date_created')[:30]
         f = feedgenerator.Rss201rev2Feed(title="Series Podcast: " + series_name, link="http://www.radio4all.net/series/" + str(series_name), description="Radio Project Series: " + str(series_name), docs="http://blogs.law.harvard.edu/tech/rss", generator="A-Infos Radio Project http://www.radio4all.net/", managingEditor="rp@radio4all.net (Editor)",  webmaster="www@radio4all.net (Webmaster)", ttl="240")
    else:
         queryset = Programs.objects.all().order_by('-date_created')[:30]
         f = feedgenerator.Rss201rev2Feed(title="Radio Project Front Page Podcast", link="http://www.radio4all.net", description="Radio Project Front Page Podcast",pubdate="Sat, 17 Oct 2020 23:00:37 PDT", docs="http://blogs.law.harvard.edu/tech/rss", generator="A-Infos Radio Project http://www.radio4all.net/", managingEditor="rp@radio4all.net (Editor)",  webmaster="www@radio4all.net (Webmaster)", ttl="240")
    curs = connection.cursor()
    for i in queryset:
        fileset_tmp = Files.objects.filter(program_id = i.program_id)
        for s in fileset_tmp:
            title_to_use = i.series + ' - ' + i.program_title
            link_to_use = 'http://www.radio4all.net/program/' + str(i.program_id)
            desc_to_use = i.summary
            guid_to_use = 'http://www.radio4all.net/program/' + str(i.program_id) + '&' + str(s.file_id)
            date_to_use = i.date_created
            author_to_use = Users.objects.get(uid=str(i.uid_id)).full_name + "(" + str(i.uid) + ")"
            curs.execute('SELECT t1.file_size, t2.file_location, t3.mime_type FROM files AS t1, locations AS t2, formats AS t3 WHERE t1.file_id = t2.file_id AND t1.format_id = t3.format_id AND t1.program_id = %s', (i.program_id,))
            enclosures_to_use = []
            for c in curs.fetchall():
                enclosures_to_use = [feedgenerator.Enclosure(c[1], c[0], c[2])]
                f.add_item(title=title_to_use, link=link_to_use, description=desc_to_use, author_name=author_to_use, enclosures=enclosures_to_use)
    curs.close()
    return HttpResponse(f.writeString('UTF-8').encode('ascii', 'xmlcharrefreplace').decode('utf-8'), content_type='application/xml')

def podcast_program(request):
    program_id = request.GET.get('program_id')
    version_id = request.GET.get('version_id')
    version = request.GET.get('version')
    queryset = Programs.objects.get(program_id=program_id)
    f = feedgenerator.Rss201rev2Feed(title="Program Podcast: " + str(queryset.program_title), link="http://www.radio4all.net/program/" + str(program_id), description="Podcast for Program: " + str(queryset.program_title), docs="http://blogs.law.harvard.edu/tech/rss", generator="A-Infos Radio Project http://www.radio4all.net/", managingEditor="rp@radio4all.net (Editor)",  webmaster="www@radio4all.net (Webmaster)", ttl="240")
    curs = connection.cursor()
    fileset_tmp = Files.objects.filter(program_id = program_id, version_id = version_id)
    for s in fileset_tmp:
        title_to_use = queryset.series + ' - ' + queryset.program_title
        link_to_use = 'http://www.radio4all.net/program/' + str(queryset.program_id)
        desc_to_use = queryset.summary
        guid_to_use = 'http://www.radio4all.net/program/' + str(queryset.program_id) + '&' + str(s.file_id)
        date_to_use = queryset.date_created
        author_to_use = Users.objects.get(uid=str(queryset.uid_id)).full_name + "(" + str(queryset.uid) + ")"
        curs.execute('SELECT t1.file_size, t2.file_location, t3.mime_type FROM files AS t1, locations AS t2, formats AS t3 WHERE t1.file_id = t2.file_id AND t1.format_id = t3.format_id AND t1.program_id = %s AND t1.version_id = %s', (queryset.program_id, version_id,))
        enclosures_to_use = []
        for c in curs.fetchall():
            enclosures_to_use = [feedgenerator.Enclosure(c[1], c[0], c[2])]
            f.add_item(title=title_to_use, link=link_to_use, description=desc_to_use, author_name=author_to_use, enclosures=enclosures_to_use)
    curs.close()
    return HttpResponse(f.writeString('UTF-8').encode('ascii', 'xmlcharrefreplace').decode('utf-8'), content_type='application/xml')

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
