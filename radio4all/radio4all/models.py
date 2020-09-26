# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import UserManager

from django.utils import timezone


class Advisories(models.Model):
    ad_id = models.AutoField(primary_key=True)
    ad_desc = models.CharField(max_length=255)
    ad_abbrev = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'advisories'


class ApplicationKey(models.Model):
    appkey = models.CharField(unique=True, max_length=50)
    uid = models.IntegerField()
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'application_key'


class Captcha(models.Model):
    word = models.CharField(max_length=25, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'captcha'


class Faq(models.Model):
    q = models.CharField(max_length=255, blank=True, null=True)
    a = models.TextField(blank=True, null=True)
    sort_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faq'

class Files(models.Model):
    file_id = models.AutoField(primary_key=True)
    program = models.ForeignKey('Programs', on_delete=models.PROTECT, related_name='files',default=1)
    version = models.ForeignKey('Versions', models.DO_NOTHING)
    segment = models.IntegerField()
    filename = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
#    length = models.TimeField()
    format = models.ForeignKey('Formats', on_delete=models.PROTECT, related_name='+',default=1)
    bitrate = models.IntegerField(blank=True, null=True)
    file_size = models.CharField(max_length=50)
    stereo = models.CharField(max_length=7, blank=True, null=True)
    how = models.CharField(max_length=20, blank=True, null=True)
    downloads = models.IntegerField(blank=True, null=True)
    no_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'files'

class Types(models.Model):
    type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'types'


class Formats(models.Model):
    format_id = models.AutoField(primary_key=True)
    format_name = models.CharField(max_length=255)
    format_ext = models.CharField(max_length=7)
    mime_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'formats'


class Lang(models.Model):
    lang_id = models.AutoField(primary_key=True)
    lang = models.CharField(max_length=255)
    lang_abbreviation = models.CharField(max_length=7)
    native_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lang'


class License(models.Model):
    cc_id = models.AutoField(primary_key=True)
    cc_name = models.CharField(max_length=255, blank=True, null=True)
    cc_abbrev = models.CharField(max_length=50, blank=True, null=True)
    cc_icon = models.CharField(max_length=255, blank=True, null=True)
    cc_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'license'


class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    file = models.ForeignKey(Files, models.DO_NOTHING,related_name='locations', blank=True, null=True)
    file_location = models.CharField(max_length=500, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    mirror = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'locations'


class News(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    pub_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class Programs(models.Model):
    program_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey('Users', db_column='uid', on_delete=models.PROTECT, related_name='+',default=1)
    type = models.CharField(max_length=255)
    program_title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    series = models.CharField(max_length=255, blank=True, null=True)
    speaker = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    credits = models.TextField(blank=True, null=True)
    license = models.ForeignKey('License',db_column='license',to_field='cc_id', on_delete=models.PROTECT, related_name='+',default=1)
    restriction = models.IntegerField()
#    restriction = models.ForeignKey('Restrictions', on_delete=models.PROTECT, related_name='+',default=1)
#    advisory = models.ForeignKey('Advisories' ,on_delete=models.PROTECT, related_name='+',default=1)
    notes = models.TextField(blank=True, null=True)
    hidden = models.IntegerField()
    permanent = models.IntegerField()
    date_created = models.DateTimeField()
    password = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'programs'


class Restrictions(models.Model):
    lic_id = models.AutoField(primary_key=True)
    lic_description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'restrictions'


class Sessions(models.Model):
    session_id = models.AutoField(primary_key=True)
    session = models.CharField(max_length=255)
    uid = models.IntegerField()
    ip_addr = models.CharField(max_length=25, blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions'


class TopicAssignment(models.Model):
    assign_id = models.AutoField(primary_key=True)
    topic_id = models.ForeignKey('Topics', on_delete=models.PROTECT, related_name='+',default=1)
    program_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'topic_assignment'


class Topics(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=255)
    topic_parent = models.IntegerField()
    topic_root = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'topics'



class Users(AbstractBaseUser, PermissionsMixin):
    uid = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_level = models.IntegerField()
    full_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    display_email = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    suspended = models.IntegerField()
    special = models.IntegerField()
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    class Meta:
        managed = False
        db_table = 'users'


class Versions(models.Model):
    version_id = models.AutoField(primary_key=True)
    program = models.ForeignKey(Programs, models.DO_NOTHING)
    version = models.IntegerField()
    version_title = models.CharField(max_length=255, blank=True, null=True)
    version_description = models.CharField(max_length=255, blank=True, null=True)
    length = models.TimeField()
    lang = models.ForeignKey('Lang', on_delete=models.PROTECT, related_name='+',default=1)
    date_recorded = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    script = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'versions'
