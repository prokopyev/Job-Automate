from django.shortcuts import render
import jobautomate


def index(request):
    context = {}
    if request.POST.get('run'):
        what = request.POST['job_title']
        where = request.POST['job_location']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        resume = request.FILES['resume'].read()
        jobautomate.django_view(what, where, first_name,
                                last_name, email, resume)
    return render(request, 'web_search/index.html', context)
