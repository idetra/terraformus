from django.apps import apps
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Avg
from django.forms import formset_factory, inlineformset_factory

from django.shortcuts import render, redirect, get_object_or_404

from terraformus.core.forms import SolutionForm, DependsOnForm, ProfileForm, UserUpdateForm, ExternalAssetForm, \
    InLineLifeCycleInputForm, LifeCycleForm
from terraformus.core.models import Solution, Strategy, ExternalAsset, LifeCycle, LifeCycleInput, LifeCycleWaste


def home(request):
    q = request.session.get('q', '')

    context = {'q': q}

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
    DependsOnFormSet = formset_factory(DependsOnForm, extra=1)  # noqa

    if request.method == 'POST':
        form = SolutionForm(request.POST)
        depends_on_formset = DependsOnFormSet(request.POST, prefix='connects_to')
        if form.is_valid() and depends_on_formset.is_valid():
            solution_form = form.save(commit=False)
            solution_form.user = request.user
            solution_form.save()
            for depends_on_form in depends_on_formset:
                depends_on_solution = depends_on_form.cleaned_data.get('title')
                if depends_on_solution:
                    depends_on_solution_setup, created = Solution.objects.get_or_create(title=depends_on_solution, user=request.user)
                    solution_form.depends_on.add(depends_on_solution_setup)
                    solution_form.save()
            return redirect('my_proposals')

    else:
        form = SolutionForm(prefix='connects_to')
        depends_on_formset = DependsOnFormSet(prefix='connects_to')

    context = {'q': q, 'form': form, 'depends_on_formset': depends_on_formset}

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


# EXTERNAL ASSETS & LIFE CYCLES -----------------------------------------------------------------------------------------


@login_required
def create_external_asset(request, model_name, pk):
    user = request.user
    if model_name.lower() == 'solution':
        proposal_instance = get_object_or_404(Solution, pk=pk, user=user)
    elif model_name.lower() == 'strategy':
        proposal_instance = get_object_or_404(Strategy, pk=pk, user=user)
    else:
        raise Exception("Invalid model_name")

    if request.method == 'POST':
        form = ExternalAssetForm(request.POST)
        if form.is_valid():
            ext_form = form.save(commit=False)
            setattr(ext_form, model_name.lower(), proposal_instance)
            ext_form.save()
            return redirect('my_proposals')
    else:
        form = ExternalAssetForm()

    context = {'form':form}
    return render(request, 'solution/create_external_asset.html', context)


@login_required
def edit_external_asset(request, model_name, pk):
    user = request.user
    if model_name.lower() == 'solution':
        external_asset = get_object_or_404(ExternalAsset, pk=pk, solution__user=user)
    elif model_name.lower() == 'strategy':
        external_asset = get_object_or_404(ExternalAsset, pk=pk, strategy__user=user)
    else:
        raise Exception("Invalid model_name")
    if request.method == "POST":
        form = ExternalAssetForm(request.POST, instance=external_asset)
        if form.is_valid():
            form.save()
            return redirect('my_proposals')
    else:
        form = ExternalAssetForm(instance=external_asset)

    context = {'form': form, 'model_name': model_name}
    return render(request, 'solution/edit_external_asset.html', context)



@login_required
def delete_external_asset(request, model_name, pk):
    user = request.user
    if model_name.lower() == 'solution':
        external_asset = get_object_or_404(ExternalAsset, pk=pk, solution__user=user)
    elif model_name.lower() == 'strategy':
        external_asset = get_object_or_404(ExternalAsset, pk=pk, strategy__user=user)
    else:
        raise Exception("Invalid model_name")
    external_asset.delete()
    return redirect('my_proposals')


@login_required
def create_life_cycle(request, pk):
    user = request.user
    valid_life_cycle = get_object_or_404(Solution, pk=pk, author=user)
    InputFormSet = inlineformset_factory(LifeCycle, LifeCycleInput, InLineLifeCycleInputForm, can_delete=True, extra=1)
    WasteFormSet = inlineformset_factory(Solution, LifeCycleWaste, InLineLifeCycleInputForm, can_delete=True, extra=1)

    if request.method == 'POST':
        form = LifeCycleForm(request.POST, prefix='life_cycle', instance=valid_life_cycle)
        input_formset = InputFormSet(request.POST, prefix='life_cycle_input', instance=valid_life_cycle)
        waste_formset = WasteFormSet(request.POST, prefix='life_cycle_waste', instance=valid_life_cycle)
        if form.is_valid() and waste_formset.is_valid() and input_formset.is_valid():
            life_cycle = form.save()
            input_formset.instance = life_cycle
            input_formset.save()

            waste_formset.instance = life_cycle
            waste_formset.save()

            return redirect('my_proposals')
    else:
        form = LifeCycleForm(prefix='life_cycle', instance=valid_life_cycle)
        input_formset = InputFormSet(prefix='life_cycle_input', instance=valid_life_cycle)
        waste_formset = WasteFormSet(prefix='life_cycle_waste', instance=valid_life_cycle)

    context = {'form': form, 'input_formset': input_formset, 'waste_formset': waste_formset}
    return render(request, 'solution/create_life_cycle.html', context)


@login_required
def edit_life_cycle(request):

    context = {}
    return render(request, 'solution/edit_life_cycle.html', context)


@login_required
def delete_life_cycle(request, pk):
    user = request.user
    life_cycle = LifeCycle.objects.get(pk=pk, solution__user=user)
    life_cycle.delete()
    return redirect('my_proposals')

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
    user_profile = user.profile

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user_profile)
        user_form = UserUpdateForm(request.POST, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('home')
    else:
        profile_form = ProfileForm(instance=user_profile)
        user_form = UserUpdateForm(instance=user)

    context = {'profile_form': profile_form, 'user_form': user_form,'q': q}

    return render(request, 'user/profile.html', context)


@login_required
def my_proposals(request):
    q = request.session.get('q', '')
    user = request.user

    all_solutions = Solution.objects.filter(user=user)
    all_strategies = Strategy.objects.filter(user=user)

    for item in all_solutions:
        item.has_ex_assets = item.externalasset_set.filter(type='ex.').exists()
        item.has_ref_assets = item.externalasset_set.filter(type='ref').exists()
        item.has_doc_assets = item.externalasset_set.filter(type='doc').exists()
        item.has_build_lifecycle = item.lifecycle_set.filter(type='b').exists()
        item.has_operation_lifecycle = item.lifecycle_set.filter(type='o').exists()
        item.has_end_of_life_lifecycle = item.lifecycle_set.filter(type='e').exists()

    context = { 'q': q, 'all_solutions': all_solutions, 'all_strategies': all_strategies}
    return render(request, 'user/my_proposals.html', context)


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