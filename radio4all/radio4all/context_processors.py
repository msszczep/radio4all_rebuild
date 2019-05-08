from .models import Types, License, Advisories

def categories(request):
    return {'categories': Types.objects.all()}

def licenses(request):
    return {'licenses': License.objects.all()}

def advisories(request):
    return {'advisories': Advisories.objects.all()}
