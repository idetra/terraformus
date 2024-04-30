from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

from terraformus.core.forms import SolutionForm
from terraformus.core.models import Solution, Strategy


def home(request):
    q = request.session.get('q', '')

    if request.method == "POST":
        form = SolutionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)

    form = SolutionForm()

    # if 'dismiss_alert' in request.GET and request.GET.get('dismiss_alert') == 'true':
    #     request.session['dismiss_alert'] = True
    #     return redirect('/')
    #
    # dismiss_alert = request.session.get('dismiss_alert', False)
    # home_page = HomePageControl.objects.get(active=True)
    # endorsement = Endorsement.objects.all()
    # scientific_sources = ScientificSource.objects.all()
    context = {'q': q,
               'form': form
               #'home_page': home_page, 'endorsement': endorsement, 'scientific_sources': scientific_sources,
               # 'dismiss_alert': dismiss_alert
               }

    return render(request, 'index.html', context)


# SOLUTIONS ------------------------------------------------------------------------------------------------------------

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


def solution(request, uuid, slug):
    """ for slug to show on url, it is necessary to receive here even if it's not used in the view """
    q = request.session.get('q', '')
    # data_point = get_object_or_404(DataPoint, uuid=uuid)
    # rating = Rating.objects.select_related('rating_reply').filter(content=data_point)
    #
    # if data_point.banned:
    #     return render(request, 'datapoint/banned.html', {'q': q})

    context = {'q': q,
        # "data_point": data_point,  'rating': rating
               }

    return render(request, 'solution/solution.html', context)


@login_required
def create_solution(request):
    q = request.session.get('q', '')
    # ReferenceFormSet = formset_factory(ReferenceForm, extra=1)  # noqa
    # ConnectsToFormSet = formset_factory(ConnectsToForm, extra=1)  # noqa
    #
    # if request.method == 'POST':
    #     form = DataPointForm(request.POST, prefix='data_point')
    #     reference_formset = ReferenceFormSet(request.POST, prefix='reference')
    #     connects_to_formset = ConnectsToFormSet(request.POST, prefix='connects_to')
    #     if form.is_valid() and connects_to_formset.is_valid() and reference_formset.is_valid():
    #         data_point = form.save(commit=False)
    #         data_point.author = request.user
    #         data_point.save()
    #         for connects_to_form in connects_to_formset:
    #             connects_to_datapoint = connects_to_form.cleaned_data.get('title')
    #             if connects_to_datapoint:
    #                 Connection.objects.create(from_datapoint=data_point, to_datapoint=connects_to_datapoint)
    #         for reference_form in reference_formset:
    #             if reference_form.cleaned_data:
    #                 reference = reference_form.save(commit=False)
    #                 reference.content = data_point
    #                 reference.save()
    #         return redirect('datapoint', slug=data_point.slug)
    # else:
    #     form = DataPointForm(prefix='data_point')
    #     reference_formset = ReferenceFormSet(prefix='reference')
    #     connects_to_formset = ConnectsToFormSet(prefix='connects_to')

    context = {
        # 'form': form, 'reference_formset': reference_formset, 'connects_to_formset': connects_to_formset,
        'q': q
    }

    return render(request, 'solution/create_solution.html', context)


@login_required
def edit_solution(request, slug):
    q = request.session.get('q', '')
    user = request.user
    # valid_datapoint = get_object_or_404(Solution, slug=slug, author=user)
    # ReferenceFormSet = inlineformset_factory(DataPoint, Reference, ReferenceForm, can_delete=True, extra=1)  # noqa
    # ConnectsToFormSet = inlineformset_factory(DataPoint, Connection, InlineConnectsToForm, fk_name='from_datapoint', can_delete=True, extra=1)  # noqa
    # if request.method == 'POST':
    #     form = DataPointForm(request.POST, prefix='data_point', instance=valid_datapoint)
    #     reference_formset = ReferenceFormSet(request.POST, prefix='reference', instance=valid_datapoint)
    #     connects_to_formset = ConnectsToFormSet(request.POST, prefix='connects_to', instance=valid_datapoint)
    #     if form.is_valid() and connects_to_formset.is_valid() and reference_formset.is_valid():
    #         data_point = form.save()
    #         reference_formset.instance = data_point
    #         reference_formset.save()
    #
    #         connects_to_formset.instance = data_point
    #         connects_to_formset.save()
    #
    #         return redirect('datapoint', slug=data_point.slug)
    # else:
    #     form = DataPointForm(prefix='data_point', instance=valid_datapoint)
    #     reference_formset = ReferenceFormSet(prefix='reference', instance=valid_datapoint)
    #     connects_to_formset = ConnectsToFormSet(prefix='connects_to', instance=valid_datapoint)

    context = {
        # 'form': form, 'reference_formset': reference_formset, 'connects_to_formset': connects_to_formset,
        'q': q}

    return render(request, 'solution/edit_solution.html', context)


@login_required
def delete_solution(request, slug):
    user = request.user
    data_point = Solution.objects.get(slug=slug, author=user)
    data_point.delete()
    return redirect('home')


# STRATEGIES -----------------------------------------------------------------------------------------------------------


def strategies(request):
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

    return render(request, 'strategies.html', context)


def strategy(request, uuid, slug):
    """ for slug to show on url, it is necessary to receive here even if it's not used in the view """
    q = request.session.get('q', '')
    # data_point = get_object_or_404(DataPoint, uuid=uuid)
    # rating = Rating.objects.select_related('rating_reply').filter(content=data_point)
    #
    # if data_point.banned:
    #     return render(request, 'datapoint/banned.html', {'q': q})

    context = {'q': q,
        # "data_point": data_point,  'rating': rating
               }

    return render(request, 'strategy/strategy.html', context)


@login_required
def create_strategy(request):
    q = request.session.get('q', '')
    # ReferenceFormSet = formset_factory(ReferenceForm, extra=1)  # noqa
    # ConnectsToFormSet = formset_factory(ConnectsToForm, extra=1)  # noqa
    #
    # if request.method == 'POST':
    #     form = DataPointForm(request.POST, prefix='data_point')
    #     reference_formset = ReferenceFormSet(request.POST, prefix='reference')
    #     connects_to_formset = ConnectsToFormSet(request.POST, prefix='connects_to')
    #     if form.is_valid() and connects_to_formset.is_valid() and reference_formset.is_valid():
    #         data_point = form.save(commit=False)
    #         data_point.author = request.user
    #         data_point.save()
    #         for connects_to_form in connects_to_formset:
    #             connects_to_datapoint = connects_to_form.cleaned_data.get('title')
    #             if connects_to_datapoint:
    #                 Connection.objects.create(from_datapoint=data_point, to_datapoint=connects_to_datapoint)
    #         for reference_form in reference_formset:
    #             if reference_form.cleaned_data:
    #                 reference = reference_form.save(commit=False)
    #                 reference.content = data_point
    #                 reference.save()
    #         return redirect('datapoint', slug=data_point.slug)
    # else:
    #     form = DataPointForm(prefix='data_point')
    #     reference_formset = ReferenceFormSet(prefix='reference')
    #     connects_to_formset = ConnectsToFormSet(prefix='connects_to')

    context = {
        # 'form': form, 'reference_formset': reference_formset, 'connects_to_formset': connects_to_formset,
        'q': q
    }

    return render(request, 'strategy/create_strategy.html', context)


@login_required
def edit_strategy(request, slug):
    q = request.session.get('q', '')
    user = request.user
    # valid_datapoint = get_object_or_404(Solution, slug=slug, author=user)
    # ReferenceFormSet = inlineformset_factory(DataPoint, Reference, ReferenceForm, can_delete=True, extra=1)  # noqa
    # ConnectsToFormSet = inlineformset_factory(DataPoint, Connection, InlineConnectsToForm, fk_name='from_datapoint', can_delete=True, extra=1)  # noqa
    # if request.method == 'POST':
    #     form = DataPointForm(request.POST, prefix='data_point', instance=valid_datapoint)
    #     reference_formset = ReferenceFormSet(request.POST, prefix='reference', instance=valid_datapoint)
    #     connects_to_formset = ConnectsToFormSet(request.POST, prefix='connects_to', instance=valid_datapoint)
    #     if form.is_valid() and connects_to_formset.is_valid() and reference_formset.is_valid():
    #         data_point = form.save()
    #         reference_formset.instance = data_point
    #         reference_formset.save()
    #
    #         connects_to_formset.instance = data_point
    #         connects_to_formset.save()
    #
    #         return redirect('datapoint', slug=data_point.slug)
    # else:
    #     form = DataPointForm(prefix='data_point', instance=valid_datapoint)
    #     reference_formset = ReferenceFormSet(prefix='reference', instance=valid_datapoint)
    #     connects_to_formset = ConnectsToFormSet(prefix='connects_to', instance=valid_datapoint)

    context = {
        # 'form': form, 'reference_formset': reference_formset, 'connects_to_formset': connects_to_formset,
        'q': q}

    return render(request, 'strategy/edit_strategy.html', context)


@login_required
def delete_strategy(request, slug):
    user = request.user
    data_point = Strategy.objects.get(slug=slug, author=user)
    data_point.delete()
    return redirect('home')


# RATING/REPORT --------------------------------------------------------------------------------------------------------


@login_required
def rate(request, slug):
    q = request.session.get('q', '')
    # data_point = get_object_or_404(DataPoint, slug=slug)
    #
    # if data_point.author == request.user:
    #     message = "You can't rate your own DataPoint."
    #     rating = Rating.objects.select_related('rating_reply').filter(content=data_point)
    #     context = {"data_point": data_point, 'q': q, 'rating': rating, 'message': message}
    #     return render(request, 'datapoint/datapoint.html', context)
    #
    # rating, created = Rating.objects.get_or_create(content=data_point, author=request.user)
    #
    # if request.method == 'POST':
    #     form = RatingForm(request.POST, instance=rating)
    #     if form.is_valid():
    #         rating = form.save()
    #         rating.save()
    #
    #     return redirect('datapoint', slug=slug)
    #
    # else:
    #     form = RatingForm(instance=rating)

    context = {
        # 'form': form, 'data_point': data_point,
               'q': q}

    return render(request, 'rate_report/rate.html', context)


@login_required
def rating_reply(request, pk):
    q = request.session.get('q', '')
    # rating = get_object_or_404(Rating, pk=pk)
    # reply, created = RatingReply.objects.get_or_create(rating=rating, author=request.user)
    # data_point = rating.content
    # if request.method == 'POST':
    #     form = RatingReplyForm(request.POST, instance=reply)
    #     if form.is_valid():
    #         reply = form.save()
    #         reply.save()
    #
    #     return redirect('datapoint', slug=data_point.slug)
    #
    # else:
    #     form = RatingReplyForm(instance=reply)

    context = {
        # 'form': form, 'rating': rating,
               'q': q}

    return render(request, 'rate_report/rating_reply.html', context)


@login_required
def report(request, slug):
    q = request.session.get('q', '')
    # data_point = get_object_or_404(DataPoint, slug=slug)
    # user_report, created = Report.objects.get_or_create(content=data_point, author=request.user)
    # if request.method == 'POST':
    #     form = ReportForm(request.POST, instance=user_report)
    #     if form.is_valid():
    #         user_report = form.save()
    #         user_report.save()
    #
    #     return redirect('datapoint', slug=slug)
    #
    # else:
    #     form = ReportForm(instance=user_report)

    context = {
        # 'form': form, 'data_point': data_point,
               'q': q}

    return render(request, 'rate_report/report.html', context)


# USER -----------------------------------------------------------------------------------------------------------------


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