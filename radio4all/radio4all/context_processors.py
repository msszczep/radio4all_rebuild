from .models import Types, License

def categories(request):
    return {'categories': Types.objects.all()}

def licenses(request):
    return {'licenses': License.objects.all()}
