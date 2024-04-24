from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, redirect


def home(request):
    q = request.session.get('q', '')
    # if 'dismiss_alert' in request.GET and request.GET.get('dismiss_alert') == 'true':
    #     request.session['dismiss_alert'] = True
    #     return redirect('/')
    #
    # dismiss_alert = request.session.get('dismiss_alert', False)
    # home_page = HomePageControl.objects.get(active=True)
    # endorsement = Endorsement.objects.all()
    # scientific_sources = ScientificSource.objects.all()
    context = {'q': q, #'home_page': home_page, 'endorsement': endorsement, 'scientific_sources': scientific_sources,
               # 'dismiss_alert': dismiss_alert
               }

    return render(request, 'index.html', context)


def solutions(request):
    # page_number = request.GET.get('page', '1')
    # number_of_rows_per_page = request.GET.get('rows_per_page', '10')
    #
    # if not (number_of_rows_per_page.isdigit() and int(number_of_rows_per_page) > 0):
    #     number_of_rows_per_page = '10'
    #
    q = request.GET.get('q', '')
    # request.session['q'] = q
    # search_fields = ['title', 'description', 'slug', 'content', 'author__first_name', 'author__last_name']
    #
    # query = Q()
    # for field in search_fields:
    #     query |= Q(**{f'{field}__icontains': q})
    #
    # data_points_query = DataPoint.objects.filter(query, banned=False).annotate(
    #     avg_rating=Avg('rating__rate')).order_by('-avg_rating')
    #
    # paginator = Paginator(data_points_query, number_of_rows_per_page)
    # data_points = paginator.get_page(page_number)

    context = {
        # 'possible_rows_per_page': [10, 50, 100],
        # 'data_points': data_points,
        'q': q
    }

    return render(request, 'solutions.html', context)


@login_required
def profile(request):
    q = request.session.get('q', '')
    user = request.user
    # user_profile = user.profile
    # data_points = DataPoint.objects.filter(author__username=user.username)

    # if request.method == 'POST':
    #     profile_form = ProfileForm(request.POST, instance=user_profile)
    #     user_form = UserUpdateForm(request.POST, instance=user)
    #     if profile_form.is_valid() and user_form.is_valid():
    #         profile_form.save()
    #         user_form.save()
    #         return redirect('home')
    # else:
    #     profile_form = ProfileForm(instance=user_profile)
    #     user_form = UserUpdateForm(instance=user)

    context = {
        # 'profile_form': profile_form, 'user_form': user_form, 'data_points': data_points,
        'q': q}
    return render(request, 'user/profile.html', context)


def author(request, name):
    q = request.session.get('q', '')
    # data_points = DataPoint.objects.filter(author__username=name)
    # author_profile = Profile.objects.get(user__username=name)

    context = {
        # 'author_profile': author_profile, 'data_points': data_points,
        'q': q}
    return render(request, 'user/author.html', context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return redirect('home')
    else:
        return render(request, 'account/delete_account.html')


def about(request):
    q = request.session.get('q', '')
    context = {'q': q}
    return render(request, 'about.html', context)


def privacy_policy(request):
    q = request.session.get('q', '')
    context = {'q': q}
    return render(request, 'privacy_policy.html', context)


def terms_of_service(request):
    q = request.session.get('q', '')
    context = {'q': q}
    return render(request, 'terms_of_service.html', context)