from functools import cmp_to_key
from itertools import chain
from django.apps import apps
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Q, Prefetch
from django.forms import formset_factory, inlineformset_factory

from django.shortcuts import render, redirect, get_object_or_404

from terraformus.core.forms import SolutionForm, DependsOnForm, ProfileForm, UserUpdateForm, ExternalAssetForm, \
    InLineLifeCycleInputForm, LifeCycleForm, InLineLifeCycleWasteForm, StrategyForm, StrategySolutionForm, RatingForm, \
    RatingReplyForm, ReportForm
from terraformus.core.models import Solution, Strategy, ExternalAsset, LifeCycle, LifeCycleInput, LifeCycleWaste, \
    Rating, StrategySolution, HomePageControl, Profile, RatingReply, Report
from terraformus.core import services


def home(request):
    q = request.session.get('q', '')
    home_page = get_object_or_404(HomePageControl, active=True)
    all_strategies = Strategy.objects.prefetch_related(
        Prefetch('solutions', queryset=StrategySolution.objects.select_related('solution'))
    )

    for strategy in all_strategies:  # noqa
        strategy.solutions_uuids = ",".join(str(solution.solution.uuid) for solution in strategy.solutions.all())  # noqa

    cost_types = [key for key, value in services.choices.cost_types.items()]
    dimensions = services.aux_lists.dimension_target
    un_targets = services.aux_lists.un_target
    sectors = services.aux_lists.sector

    dimensions_table = services.generators.TableGenerator("Solution", "cost_type", dimensions, cost_types).table()
    un_targets_table = services.generators.TableGenerator("Solution", "cost_type", un_targets, cost_types).table()
    sectors_table = services.generators.TableGenerator("Solution", "cost_type", sectors, cost_types).table()

    context = {'q': q, 'home_page': home_page,'all_strategies': all_strategies,
               'dimensions_table': dimensions_table, 'un_targets_table': un_targets_table, 'sectors_table': sectors_table}

    return render(request, 'index.html', context)


# SOLUTIONS ------------------------------------------------------------------------------------------------------------

def solutions(request):
    page_number = request.GET.get('page', '1')
    number_of_rows_per_page = request.GET.get('rows_per_page', '10')

    if not (number_of_rows_per_page.isdigit() and int(number_of_rows_per_page) > 0):
        number_of_rows_per_page = '10'

    q = request.GET.get('q', '')
    request.session['q'] = q

    solution_search_fields = ['title', 'subtitle', 'slug', 'goal', 'user__first_name', 'user__last_name', 'uuid']
    strategy_search_fields = ['title', 'slug', 'goal', 'user__first_name', 'user__last_name', 'uuid']

    solution_query = services.generators.build_query(q, solution_search_fields)
    strategy_query = services.generators.build_query(q, strategy_search_fields)

    uuid_string = request.GET.get('uuids', '')
    if uuid_string:
        uuids = uuid_string.split(',')
        for uuid in uuids:
            solution_query |= Q(uuid__icontains=uuid.strip())
            # strategy_query |= Q(uuid__icontains=uuid.strip())  # not needed, just future ref.
        strategies_query_result = Strategy.objects.none()  # When 'uuids' is provided, ignore the strategies

    else:
        strategies_query_result = Strategy.objects.filter(strategy_query, banned=False).annotate(
            avg_rating=Avg('rating__rate'))

    solutions_query_result = Solution.objects.filter(solution_query, banned=False).annotate(avg_rating=Avg('rating__rate'))
    # strategies_query_result = Strategy.objects.filter(strategy_query, banned=False).annotate(avg_rating=Avg('rating__rate'))

    results = sorted(
        chain(solutions_query_result, strategies_query_result),
        key=cmp_to_key(services.generators.rate_compare)
    )

    paginator = Paginator(results, number_of_rows_per_page)
    solutions_result = paginator.get_page(page_number)

    context = {
        'possible_rows_per_page': [10, 50, 100],
        'solutions_result': solutions_result,
        'q': q,
        'uuids': uuid_string
    }

    return render(request, 'solutions.html', context)


def solution(request, uuid, slug=None):
    """
    for slug to show on url, it is necessary to receive here even if it's not used in the view
    """
    q = request.session.get('q', '')
    solution_view = get_object_or_404(
        Solution.objects.select_related('derives_from').prefetch_related('depends_on'), uuid=uuid)
    rating = Rating.objects.select_related('rating_reply').filter(solution=solution_view)
    external_assets = ExternalAsset.objects.filter(solution=solution_view)
    lifecycles = LifeCycle.objects.filter(solution=solution_view)

    build_lifecycles = [lc for lc in lifecycles if lc.type == "b"]
    operation_lifecycles = [lc for lc in lifecycles if lc.type == "o"]
    end_lifecycles = [lc for lc in lifecycles if lc.type == "e"]

    boolean_fieldnames = services.generators.collect_boolean_fieldnames('Solution', solution_view)

    solution_type_bools = [sol for sol in boolean_fieldnames if sol in services.help_text.sol_type_ht]
    dimension_target_bools = [sol for sol in boolean_fieldnames if sol in services.help_text.sol_dimension_target_ht]
    un_target_bools = [sol for sol in boolean_fieldnames if sol in services.help_text.sol_un_target_ht]
    sector_bools = [sol for sol in boolean_fieldnames if sol in services.help_text.sol_sector_ht]

    if solution_view.banned:
        return render(request, 'banned.html', {'q': q})

    context = {'q': q, "solution_view": solution_view,  'rating': rating, 'build_lifecycles': build_lifecycles,
        'operation_lifecycles': operation_lifecycles, 'end_lifecycles': end_lifecycles, 'external_assets': external_assets,
        'boolean_fieldnames': boolean_fieldnames, 'solution_type_bools': solution_type_bools, 'dimension_target_bools': dimension_target_bools,
        'un_target_bools': un_target_bools, 'sector_bools': sector_bools}

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
            return redirect('my_solutions')

    else:
        form = SolutionForm()
        depends_on_formset = DependsOnFormSet(prefix='connects_to')

    context = {'q': q, 'form': form, 'depends_on_formset': depends_on_formset,
               'solutions_booleans': services.aux_lists.solutions_booleans}

    return render(request, 'solution/create_solution.html', context)


@login_required
def edit_solution(request, uuid):
    q = request.session.get('q', '')
    user = request.user
    solution_view = get_object_or_404(Solution, user=user, uuid=uuid)
    depends_on_form_factory = formset_factory(DependsOnForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = SolutionForm(request.POST, instance=solution_view, prefix='form')
        depends_on_form = depends_on_form_factory(request.POST, prefix='connects_to')

        if form.is_valid() and depends_on_form.is_valid():
            solution_form = form.save()

            # Process forms marked for deletion
            for single_depends_on_form in depends_on_form:
                depends_on_solution = single_depends_on_form.cleaned_data.get('title') # title is unique, so the rest works
                if depends_on_solution:  # only proceed if a Solution was found
                    if single_depends_on_form.cleaned_data.get('DELETE'):  # Check if marked for deletion
                        solution_form.depends_on.remove(depends_on_solution)
                    else:  # if not marked for deletion, process normally
                        solution_form.depends_on.add(depends_on_solution)
            return redirect('my_solutions')

    else:
        form = SolutionForm(instance=solution_view, prefix='form')
        depends_on_form = depends_on_form_factory(
            prefix='connects_to', initial=[{'title': dep.title} for dep in solution_view.depends_on.all()])

    context = {'q': q, 'form': form, 'depends_on_form': depends_on_form,
               'solutions_booleans': services.aux_lists.solutions_booleans}

    return render(request, 'solution/edit_solution.html', context)


@login_required
def delete_solution(request, uuid):
    user = request.user
    deletable_solution = Solution.objects.get(uuid=uuid, user=user)
    deletable_solution.delete()
    return redirect('my_solutions')


# STRATEGIES -----------------------------------------------------------------------------------------------------------


def strategy(request, uuid, slug=None):
    """
    for slug to show on url, it is necessary to receive here even if it's not used in the view
    """
    q = request.session.get('q', '')
    strategy_view = get_object_or_404(Strategy.objects.prefetch_related('solutions'), uuid=uuid)
    external_assets = ExternalAsset.objects.filter(strategy=strategy_view)
    rating = Rating.objects.select_related('rating_reply').filter(strategy=strategy_view)

    if strategy_view.banned:
        return render(request, 'strategy/banned.html', {'q': q})

    context = {'q': q,
        "strategy_view": strategy_view,  'rating': rating, 'external_assets': external_assets,
               }

    return render(request, 'strategy/strategy.html', context)


@login_required
def create_strategy(request):
    q = request.session.get('q', '')
    StrategySolutionFormSet = formset_factory(StrategySolutionForm, extra=1)  # noqa

    if request.method == 'POST':
        form = StrategyForm(request.POST)
        strategy_solution_formset = StrategySolutionFormSet(request.POST, prefix='strategy_solution')
        if form.is_valid() and strategy_solution_formset.is_valid():
            strategy_form = form.save(commit=False)
            strategy_form.user = request.user
            strategy_form.save()

            for solution_form in strategy_solution_formset:
                solution_instance = solution_form.cleaned_data.get('solution_title')
                notes = solution_form.cleaned_data.get('notes')

                if solution_instance:
                    strategy_solution_instance, created = StrategySolution.objects.get_or_create(
                        solution=solution_instance, defaults={'notes': notes})

                    strategy_form.solutions.add(strategy_solution_instance)

                    if not created:
                        strategy_solution_instance.notes = notes
                        strategy_solution_instance.save()

                    strategy_form.solutions.add(strategy_solution_instance)

            return redirect('my_strategies')

    else:
        form = StrategyForm()
        strategy_solution_formset = StrategySolutionFormSet(prefix='strategy_solution')

    context = {'q': q, 'form': form, 'strategy_solution_formset': strategy_solution_formset}

    return render(request, 'strategy/create_strategy.html', context)


@login_required
def edit_strategy(request, uuid):
    q = request.session.get('q', '')
    user = request.user
    strategy_view = get_object_or_404(Strategy, user=user, uuid=uuid)
    StrategySolutionFormSet = formset_factory(StrategySolutionForm, extra=1, can_delete=True)  # noqa

    if request.method == 'POST':
        form = StrategyForm(request.POST, instance=strategy_view, prefix='form')
        strategy_solution_formset = StrategySolutionFormSet(request.POST, prefix='strategy_solution')

        if form.is_valid() and strategy_solution_formset.is_valid():
            strategy_form = form.save()

            for strategy_solution_form in strategy_solution_formset:
                strategy_solution = strategy_solution_form.cleaned_data.get('solution_title')
                if strategy_solution:
                    notes = strategy_solution_form.cleaned_data.get('notes')
                    if strategy_solution_form.cleaned_data.get('DELETE'):
                        strategy_solution_obj = StrategySolution.objects.get(solution=strategy_solution)
                        strategy_form.solutions.remove(strategy_solution_obj)
                        strategy_solution_obj.delete()
                    else:
                        strategy_solution_obj, created = StrategySolution.objects.get_or_create(
                            solution=strategy_solution, defaults={'notes': notes})

                        if not created:
                            strategy_solution_obj.notes = notes
                            strategy_solution_obj.save()

                        strategy_form.solutions.add(strategy_solution_obj)
            return redirect('my_strategies')

    else:
        form = StrategyForm(instance=strategy_view, prefix='form')
        strategy_solution_formset = StrategySolutionFormSet(
            prefix='strategy_solution',
            initial=[{'solution_title': sol.solution.title, 'notes': sol.notes} for sol in strategy_view.solutions.all()])

    context = {'q': q, 'form': form, 'strategy_solution_formset': strategy_solution_formset}

    return render(request, 'strategy/edit_strategy.html', context)



@login_required
def delete_strategy(request, uuid):
    user = request.user
    deletable_strategy = Strategy.objects.get(uuid=uuid, user=user)
    deletable_strategy.delete()
    return redirect('my_strategies')


# EXTERNAL ASSETS & LIFE CYCLES -----------------------------------------------------------------------------------------


@login_required
def create_external_asset(request, model_name, uuid):
    q = request.session.get('q', '')  # noqa
    user = request.user
    if model_name.lower() == 'solution':
        proposal_instance = get_object_or_404(Solution, uuid=uuid, user=user)
        redirect_url = 'my_solutions'
    elif model_name.lower() == 'strategy':
        proposal_instance = get_object_or_404(Strategy, uuid=uuid, user=user)
        redirect_url = 'my_strategies'
    else:
        raise Exception("Invalid model_name")

    if request.method == 'POST':
        form = ExternalAssetForm(request.POST)
        if form.is_valid():
            ext_form = form.save(commit=False)
            setattr(ext_form, model_name.lower(), proposal_instance)
            ext_form.save()
            return redirect(redirect_url)
    else:
        form = ExternalAssetForm()

    context = {'q': q, 'form':form}
    return render(request, 'solution/create_external_asset.html', context)


@login_required
def edit_external_asset(request, model_name, uuid):
    q = request.session.get('q', '')  # noqa
    user = request.user
    if model_name.lower() == 'solution':
        external_asset = get_object_or_404(ExternalAsset, uuid=uuid, solution__user=user)
        redirect_url = 'my_solutions'
    elif model_name.lower() == 'strategy':
        external_asset = get_object_or_404(ExternalAsset, uuid=uuid, strategy__user=user)
        redirect_url = 'my_strategies'
    else:
        raise Exception("Invalid model_name")
    if request.method == "POST":
        form = ExternalAssetForm(request.POST, instance=external_asset)
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    else:
        form = ExternalAssetForm(instance=external_asset)

    context = {'q': q, 'form': form, 'model_name': model_name}
    return render(request, 'solution/edit_external_asset.html', context)



@login_required
def delete_external_asset(request, model_name, uuid):
    user = request.user  # noqa
    if model_name.lower() == 'solution':
        external_asset = get_object_or_404(ExternalAsset, uuid=uuid, solution__user=user)
        redirect_url = 'my_solutions'
    elif model_name.lower() == 'strategy':
        external_asset = get_object_or_404(ExternalAsset, uuid=uuid, strategy__user=user)
        redirect_url = 'my_strategies'
    else:
        raise Exception("Invalid model_name")
    external_asset.delete()
    return redirect(redirect_url)


@login_required
def create_life_cycle(request, uuid):
    q = request.session.get('q', '')
    user = request.user
    valid_solution = Solution.objects.get(uuid=uuid, user=user)
    lc_input_form_factory = inlineformset_factory(LifeCycle, LifeCycleInput, form=InLineLifeCycleInputForm, extra=1)
    lc_waste_form_factory = inlineformset_factory(LifeCycle, LifeCycleWaste, form=InLineLifeCycleWasteForm, extra=1)

    if request.method == 'POST':
        form = LifeCycleForm(request.POST, prefix='life_cycle')
        input_form = lc_input_form_factory(request.POST, prefix='life_cycle_input')
        waste_form = lc_waste_form_factory(request.POST, prefix='life_cycle_waste')
        if form.is_valid() and waste_form.is_valid() and input_form.is_valid():
            lc_form = form.save(commit=False)
            lc_form.solution = valid_solution
            lc_form.save()

            for form in input_form:
                if form.has_changed():
                    input_instance = form.save(commit=False)
                    input_instance.lifecycle = lc_form
                    input_instance.save()

            for form in waste_form:
                if form.has_changed():
                    waste_instance = form.save(commit=False)
                    waste_instance.lifecycle = lc_form
                    waste_instance.save()
            return redirect('my_solutions')
    else:
        form = LifeCycleForm(prefix='life_cycle')
        input_form = lc_input_form_factory(prefix='life_cycle_input')
        waste_form = lc_waste_form_factory(prefix='life_cycle_waste')

    context = {'q': q, 'form': form, 'input_form': input_form, 'waste_form': waste_form}
    return render(request, 'solution/create_life_cycle.html', context)


@login_required
def edit_life_cycle(request, uuid):
    q = request.session.get('q', '')
    user = request.user
    life_cycle = LifeCycle.objects.get(uuid=uuid, solution__user=user)
    lc_input_form_factory = inlineformset_factory(LifeCycle, LifeCycleInput, form=InLineLifeCycleInputForm, extra=1, can_delete=True)
    lc_waste_form_factory = inlineformset_factory(LifeCycle, LifeCycleWaste, form=InLineLifeCycleWasteForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = LifeCycleForm(request.POST, instance=life_cycle, prefix='life_cycle')
        input_form = lc_input_form_factory(request.POST, instance=life_cycle, prefix='life_cycle_input')
        waste_form = lc_waste_form_factory(request.POST, instance=life_cycle, prefix='life_cycle_waste')

        if form.is_valid() and waste_form.is_valid() and input_form.is_valid():
            lc = form.save()
            input_form.instance = lc
            input_form.save()
            waste_form.instance = lc
            waste_form.save()
            return redirect('my_solutions')

    else:
        form = LifeCycleForm(instance=life_cycle, prefix='life_cycle')
        input_form = lc_input_form_factory(instance=life_cycle, prefix='life_cycle_input')
        waste_form = lc_waste_form_factory(instance=life_cycle, prefix='life_cycle_waste')

    context = {'q': q, 'form': form, 'input_form': input_form, 'waste_form': waste_form}
    return render(request, 'solution/edit_life_cycle.html', context)


@login_required
def delete_life_cycle(request, uuid):
    user = request.user
    deletable_life_cycle = LifeCycle.objects.get(uuid=uuid, solution__user=user)
    deletable_life_cycle.delete()
    return redirect('my_solutions')

# RATING/REPORT --------------------------------------------------------------------------------------------------------


@login_required
def rate(request, model_name, uuid):
    q = request.session.get('q', '')
    used_model = apps.get_model('core', model_name)
    data_point = get_object_or_404(used_model, uuid=uuid)
    kwargs = {f"{model_name.lower()}": data_point}
    # template_path = f'{model_name.lower()}/{model_name.lower()}.html'

    if data_point.user == request.user:
        return redirect('home')
        # message = "You can't rate your own solution/strategy."
        # rating = Rating.objects.select_related('rating_reply').filter(**kwargs, )
        # context = {f"{model_name.lower()}_view": data_point, 'q': q, 'rating': rating, 'message': message}
        # return render(request, template_path, context)

    rating, created = Rating.objects.get_or_create(**kwargs, user=request.user)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save()
            rating.save()

        return redirect(f'{model_name.lower()}', uuid=uuid, slug=data_point.slug)

    else:
        form = RatingForm(instance=rating)

    context = {
        'form': form, 'data_point': data_point,
               'q': q}

    return render(request, 'rate_report/rate.html', context)


@login_required
def rating_reply(request, pk):
    q = request.session.get('q', '')
    rating = get_object_or_404(Rating, pk=pk)
    reply, created = RatingReply.objects.get_or_create(rating=rating, user=request.user)

    if rating.solution:
        model_name = "solution"
        data_point = rating.solution
    elif rating.strategy:
        model_name = "strategy"
        data_point = rating.strategy
    else:
        return redirect('home')

    if request.method == 'POST':
        form = RatingReplyForm(request.POST, instance=reply)
        if form.is_valid():
            reply = form.save()
            reply.save()

        return redirect(f'{model_name}', uuid=data_point.uuid, slug=data_point.slug)

    else:
        form = RatingReplyForm(instance=reply)

    context = {
        'form': form, 'rating': rating,
               'q': q}

    return render(request, 'rate_report/rating_reply.html', context)


@login_required
def report(request, model_name, uuid):
    q = request.session.get('q', '')
    used_model = apps.get_model('core', model_name)
    data_point = get_object_or_404(used_model, uuid=uuid)
    kwargs = {f"{model_name.lower()}": data_point}

    user_report, created = Report.objects.get_or_create(**kwargs, user=request.user)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=user_report)
        if form.is_valid():
            user_report = form.save()
            user_report.save()

        return redirect(f'{model_name.lower()}', uuid=uuid, slug=data_point.slug)

    else:
        form = ReportForm(instance=user_report)

    context = {
        'form': form, 'data_point': data_point,
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
def my_solutions(request):
    q = request.session.get('q', '')
    user = request.user

    all_solutions = Solution.objects.filter(user=user)

    for item in all_solutions:
        item.has_ex_assets = item.externalasset_set.filter(type='ex.').exists()
        item.has_ref_assets = item.externalasset_set.filter(type='ref').exists()
        item.has_doc_assets = item.externalasset_set.filter(type='doc').exists()
        item.has_build_lifecycle = item.lifecycle_set.filter(type='b').exists()
        item.has_operation_lifecycle = item.lifecycle_set.filter(type='o').exists()
        item.has_end_of_life_lifecycle = item.lifecycle_set.filter(type='e').exists()

    context = { 'q': q, 'all_solutions': all_solutions}
    return render(request, 'user/my_solutions.html', context)


@login_required
def my_strategies(request):
    q = request.session.get('q', '')
    user = request.user

    all_strategies = Strategy.objects.filter(user=user)

    context = { 'q': q, 'all_strategies': all_strategies}
    return render(request, 'user/my_strategies.html', context)


def author(request, name):
    q = request.session.get('q', '')
    author_solutions = Solution.objects.filter(user__username=name)
    author_strategies = Strategy.objects.filter(user__username=name)
    author_profile = Profile.objects.get(user__username=name)

    context = {
        'author_profile': author_profile, 'author_solutions': author_solutions, 'author_strategies': author_strategies,
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