from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from news.models import Profile

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        if user.is_authenticated:
            context['is_not_authors'] = not user.groups.filter(name='authors').exists()
            if Profile.objects.filter(user=user):
                profile = Profile.objects.get(user=user)
                context['is_not_activate'] = not profile.sendedcode == profile.recivedcode
            else:
                context['is_not_activate'] = False
        else:
            context['is_not_activate'] = False
        return context