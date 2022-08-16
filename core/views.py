from django.shortcuts import render
from django.views import View
from courses.models import Course
from django.core.paginator import Paginator

class HomeView(View):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.filter(is_active = True)

        paginator = Paginator(courses, 9)
        page_number = request.GET.get('page')
        courses_data = paginator.get_page(page_number)

        context = {
            'courses':courses_data
        }
        return render(request,'pages/index.html', context)

class AboutView(View):
    def get(self, request, *args, **kwargs):

        context = {

        }

        return render(request,'pages/about.html', context)