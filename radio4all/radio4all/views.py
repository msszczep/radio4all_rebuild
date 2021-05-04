from .models import Files, Locations, Programs, News, Faq, Types, License, Users, Topics, TopicAssignment, Restrictions, Advisories, Lang, Formats
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
from django.http import HttpResponse, Http404, BadHeaderError
from django.shortcuts import redirect, render
from django.db import connection
from django.utils import feedgenerator
from math import ceil

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

def upload_content(request):
    if request.method == 'POST':
        now = datetime.datetime.now()
        p = Programs()
        p.program_title = request.POST.get('program_title')
        # add p.uid
        p.program_type = request.POST.get('program_type')
        p.subtitle = request.POST.get('program_subtitle')
        series = request.POST.get('program_series')
        add_series = request.POST.get('program_add_series')
        if series == '':
            p.series = add_series
        else:
            p.series = series
        p.speaker = request.POST.get('program_speaker')
        p.summary = request.POST.get('program_summary')
        # add p.keywords
        p.credits = request.POST.get('program_credits')
        p.license = request.POST.get('program_license')
        p.restriction = request.POST.get('program_restriction')
        p.notes = request.POST.get('program_notes')
        p.hidden = 0
        p.advisory = request.POST.get('program_advisory')
        p.keywords = request.POST.get('program_keywords')
        p.password = ''
        # account for anonymous password
        # p.permanent = ?
        p.date_created = now
        p.save()
        v = Versions()
        v.program = p.program_id
        v.version_title = request.POST.get('version_title')
        v.version_description = request.POST.get('version_description')
        v.lang = request.POST.get('version_lang')
        v.date_recorded = request.POST.get('version_date_recorded')
        v.location = request.POST.get('version_location')
        v.script = request.POST.get('version_script')
        # v.length = ?
        # v.version_id = ?
        v.date_created = now
        v.program_id = p.id # is this right?
        v.save()
        # check for number of files, follow this pattern
        f1 = Files()
        f1.program_id = p.id # is this right?
        f1.version_id = v.id # is this right?
        f1.segment = 1
        f1.filename = request.POST.get('filename1') # check for filename, file content
        f1.title = request.POST.get('file_title1')
        f1.file_size = request.POST.get('size1') + ' ' + request.POST.get('file_size_bytes1') # double check db
        f1.bitrate = request.POST.get('bitrate1')
        f1.stereo = request.POST.get('stereo1')
        f1.format_id = request.POST.get('file_type_text1')
        # length?
        # how?
        # work out file upload to server
        # f.no_delete = ?
        f.save()
        return HttpResponseRedirect('radio4all/home.html')
    else:
        types_to_use = Types.objects.all()
        licenses_to_use = License.objects.all()
        restrictions_to_use = Restrictions.objects.all()
        advisories_to_use = Advisories.objects.all()
        languages_to_use = Lang.objects.all().order_by('lang')
        topics_to_use = Topics.objects.all().order_by('topic')
        if request.user.is_authenticated:
            uid = request.user.uid
        else:
            uid = 16
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

def topic_browse(request):
    try:
        curs = connection.cursor()
        curs.execute("SELECT count(t1.assign_id) as quantity, t1.topic_id as tag_id, t2.topic as tag FROM topic_assignment AS t1, topics AS t2 WHERE t1.topic_id = t2.topic_id AND t1.program_id NOT IN (SELECT program_id FROM programs WHERE hidden != 0) GROUP BY t1.topic_id ORDER BY t2.topic ASC")
        raw_topic_data = curs.fetchall()
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
