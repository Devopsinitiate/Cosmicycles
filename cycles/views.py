from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from datetime import datetime
from django.views.decorators.http import require_POST

from io import BytesIO

from django.template.loader import render_to_string

from .models import UserProfile, Business, CycleTemplate, CyclePeriodDetail, JournalEntry, GlossaryTerm, QuizQuestion, UserLessonProgress
from .forms import UserProfileForm, BusinessForm, JournalEntryForm, SignUpForm
from .email_service import send_verification_email
from .utils import (
    get_current_daily_cycle_period, get_current_yearly_cycle_period,
    get_current_soul_cycle_period, get_current_business_cycle_period,
    get_current_health_cycle_period, get_current_reincarnation_cycle_period,
    get_current_human_cycle_period, get_upcoming_transitions,
)
from .serializers import CycleTemplateSerializer

def home(request):
    """Public landing page — shows daily cycle only, no auth required."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    current_time = datetime.now().time()
    daily_cycle_data = get_current_daily_cycle_period(current_time)
    day_name = datetime.now().strftime('%A')
    template_name = f'Daily Cycle - {day_name}'
    try:
        daily_template = CycleTemplate.objects.get(name=template_name)
        daily_periods = daily_template.period_details.all().order_by('start_value')
    except CycleTemplate.DoesNotExist:
        daily_periods = []
    context = {
        'daily_cycle_period': daily_cycle_data,
        'daily_periods': daily_periods,
    }
    return render(request, 'cycles/home.html', context)


@login_required
def dashboard(request):
    from .services import get_all_current_periods, get_experience_based_recommendations

    UserProfile.objects.get_or_create(user=request.user)
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    cycles = get_all_current_periods(request.user)
    transitions = get_upcoming_transitions(
        request.user.userprofile.birth_date, current_date, current_time)

    # Extract soul period duration/remaining (MMDD format → date math)
    soul_cycle_data = cycles['soul']
    soul_days_into_period = None
    soul_period_duration = None
    if soul_cycle_data:
        try:
            sm = soul_cycle_data.start_value // 100
            sd = soul_cycle_data.start_value % 100
            em = soul_cycle_data.end_value // 100
            ed = soul_cycle_data.end_value % 100
            start = current_date.replace(month=sm, day=sd)
            end = current_date.replace(month=em, day=ed)
            if end < start:
                end = end.replace(year=end.year + 1)
            soul_period_duration = (end - start).days
            soul_days_into_period = (current_date - start).days
            if soul_days_into_period < 0:
                start = start.replace(year=start.year - 1)
                soul_days_into_period = (current_date - start).days
        except (ValueError, AttributeError):
            pass

    # Build set of current period IDs for recommendations
    current_period_ids = set()
    for key in ['daily', 'soul']:
        obj = cycles[key]
        if obj and hasattr(obj, 'id'):
            current_period_ids.add(obj.id)
    for key in ['yearly', 'business', 'health', 'reincarnation', 'human']:
        obj = cycles[key]
        if obj and obj.get('period'):
            current_period_ids.add(obj['period'].id)

    experience_based_recommendations = get_experience_based_recommendations(
        request.user, current_period_ids)

    context = {
        'transitions': transitions,
        'experience_based_recommendations': experience_based_recommendations,
        'daily_cycle_period': cycles['daily'],
        'human_cycle_period': cycles['human']['period'] if cycles['human'] else None,
        'human_age': cycles['human']['age'] if cycles['human'] else None,
        'human_days_into_period': cycles['human']['days_into_period'] if cycles['human'] else None,
        'human_period_duration': cycles['human']['period_duration'] if cycles['human'] else None,
        'yearly_cycle_period': cycles['yearly']['period'] if cycles['yearly'] else None,
        'yearly_days_into_period': cycles['yearly']['days_into_period'] if cycles['yearly'] else None,
        'yearly_period_duration': cycles['yearly']['period_duration'] if cycles['yearly'] else None,
        'business_cycle_period': cycles['business']['period'] if cycles['business'] else None,
        'business_days_into_period': cycles['business']['days_into_period'] if cycles['business'] else None,
        'business_period_duration': cycles['business']['period_duration'] if cycles['business'] else None,
        'soul_cycle_period': cycles['soul'],
        'soul_days_into_period': soul_days_into_period,
        'soul_period_duration': soul_period_duration,
        'health_cycle_period': cycles['health']['period'] if cycles['health'] else None,
        'health_days_into_period': cycles['health']['days_into_period'] if cycles['health'] else None,
        'health_period_duration': cycles['health']['period_duration'] if cycles['health'] else None,
        'reincarnation_cycle_period': cycles['reincarnation']['period'] if cycles['reincarnation'] else None,
        'reincarnation_days_into_period': cycles['reincarnation']['days_into_period'] if cycles['reincarnation'] else None,
        'reincarnation_period_duration': cycles['reincarnation']['period_duration'] if cycles['reincarnation'] else None,
    }
    return render(request, 'cycles/dashboard.html', context)


def about(request):
    if request.user.is_authenticated:
        return render(request, 'cycles/about.html', {'user': request.user})
    return render(request, 'cycles/about.html')

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard') # Redirect to dashboard after saving
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'cycles/profile_edit.html', {'form': form})

@login_required
@require_POST
def profile_update_api(request):
    profile = request.user.userprofile
    form = UserProfileForm(request.POST, instance=profile)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    errors = form.errors.get_json_data()
    return JsonResponse({'success': False, 'errors': errors}, status=400)

@login_required
def business_list(request):
    businesses = Business.objects.filter(user=request.user)
    return render(request, 'cycles/business_list.html', {'businesses': businesses})

@login_required
def business_create(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.save()
            return redirect('business_list')
    else:
        form = BusinessForm()
    return render(request, 'cycles/business_form.html', {'form': form})

@login_required
def business_edit(request, pk):
    business = get_object_or_404(Business, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BusinessForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business_list')
    else:
        form = BusinessForm(instance=business)
    return render(request, 'cycles/business_form.html', {'form': form})

@login_required
@require_POST
def business_delete(request, pk):
    business = get_object_or_404(Business, pk=pk, user=request.user)
    business.delete()
    return redirect('business_list')

@login_required
@require_POST
def business_delete_api(request, pk):
    business = get_object_or_404(Business, pk=pk, user=request.user)
    business.delete()
    return JsonResponse({'status': 'success'})

@login_required
def education(request):
    user_profile = request.user.userprofile
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    day_name = datetime.now().strftime('%A')

    cycles_data = []
    templates = CycleTemplate.objects.all().order_by('cycle_type')
    for t in templates:
        periods = t.period_details.all().order_by('start_value')
        current_period = None
        if t.cycle_type == 'daily':
            cp = get_current_daily_cycle_period(current_time)
            current_period = cp.period_name if cp else None
        elif t.cycle_type == 'yearly':
            cp = get_current_yearly_cycle_period(user_profile.birth_date, current_date)
            current_period = cp['period'].period_name if cp else None
        elif t.cycle_type == 'soul':
            cp = get_current_soul_cycle_period(current_date)
            current_period = cp.period_name if cp else None
        elif t.cycle_type == 'business':
            biz = Business.objects.filter(user=request.user).first()
            if biz:
                cp = get_current_business_cycle_period(biz.start_date, current_date)
                current_period = cp['period'].period_name if cp else None
        elif t.cycle_type == 'health':
            cp = get_current_health_cycle_period(current_date)
            current_period = cp['period'].period_name if cp else None
        elif t.cycle_type == 'reincarnation':
            cp = get_current_reincarnation_cycle_period(user_profile.birth_date, current_date)
            current_period = cp['period'].period_name if cp else None
        elif t.cycle_type == 'human':
            cp = get_current_human_cycle_period(user_profile.birth_date, current_date)
            current_period = cp['period'].period_name if cp else None

        cycles_data.append({
            'template': t,
            'periods': periods,
            'current_period': current_period,
        })

    glossary_terms = GlossaryTerm.objects.all().order_by('sort_order')
    return render(request, 'cycles/education.html', {'cycles_data': cycles_data, 'glossary_terms': glossary_terms})


@login_required
def education_detail(request, cycle_type):
    user_profile = request.user.userprofile
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    valid_types = dict(CycleTemplate.CYCLE_TYPES)
    if cycle_type not in valid_types:
        return render(request, 'errors/404.html', status=404)

    templates = CycleTemplate.objects.filter(cycle_type=cycle_type)
    if not templates.exists():
        raise Http404
    template = templates.first()
    periods = CyclePeriodDetail.objects.filter(cycle_template__cycle_type=cycle_type).order_by('start_value')

    current_period = None
    if cycle_type == 'daily':
        cp = get_current_daily_cycle_period(current_time)
        current_period = cp.period_name if cp else None
    elif cycle_type == 'yearly':
        cp = get_current_yearly_cycle_period(user_profile.birth_date, current_date)
        current_period = cp['period'].period_name if cp else None
    elif cycle_type == 'soul':
        cp = get_current_soul_cycle_period(current_date)
        current_period = cp.period_name if cp else None
    elif cycle_type == 'business':
        biz = Business.objects.filter(user=request.user).first()
        if biz:
            cp = get_current_business_cycle_period(biz.start_date, current_date)
            current_period = cp['period'].period_name if cp else None
    elif cycle_type == 'health':
        cp = get_current_health_cycle_period(current_date)
        current_period = cp['period'].period_name if cp else None
    elif cycle_type == 'reincarnation':
        cp = get_current_reincarnation_cycle_period(user_profile.birth_date, current_date)
        current_period = cp['period'].period_name if cp else None
    elif cycle_type == 'human':
        cp = get_current_human_cycle_period(user_profile.birth_date, current_date)
        current_period = cp['period'].period_name if cp else None

    glossary_terms = GlossaryTerm.objects.filter(
        Q(related_cycle_type=cycle_type) | Q(related_cycle_type__isnull=True)
    ).order_by('sort_order')

    context = {
        'template': template,
        'periods': periods,
        'current_period': current_period,
        'glossary_terms': glossary_terms,
    }
    return render(request, 'cycles/education_detail.html', context)


@login_required
def education_period_detail(request, cycle_type, period_id):
    valid_types = dict(CycleTemplate.CYCLE_TYPES)
    if cycle_type not in valid_types:
        return render(request, 'errors/404.html', status=404)

    period = get_object_or_404(CyclePeriodDetail, id=period_id, cycle_template__cycle_type=cycle_type)
    glossary_terms = GlossaryTerm.objects.filter(
        Q(related_cycle_type=cycle_type) | Q(related_cycle_type__isnull=True)
    ).order_by('sort_order')

    context = {
        'period': period,
        'glossary_terms': glossary_terms,
    }
    return render(request, 'cycles/education_period_detail.html', context)


@login_required
def education_quiz(request, period_id):
    period = get_object_or_404(CyclePeriodDetail, id=period_id)
    question = QuizQuestion.objects.filter(cycle_period=period).order_by('sort_order').first()
    progress, _ = UserLessonProgress.objects.get_or_create(user=request.user, cycle_period=period)

    if request.method == 'POST' and question:
        answer = request.POST.get('answer', '')
        correct = answer == question.correct_answer
        if correct and not progress.completed:
            progress.completed = True
            progress.quiz_score = 100
            progress.save()
        return JsonResponse({
            'correct': correct,
            'correct_answer': question.correct_answer,
            'explanation': question.explanation,
        })

    context = {
        'period': period,
        'question': question,
        'progress': progress,
    }
    return render(request, 'cycles/education_quiz.html', context)


@login_required
def visualizations(request):
    from .services import get_all_current_periods
    cycles = get_all_current_periods(request.user)

    context = {
        'daily_cycle_period': cycles['daily'],
        'yearly_cycle_period': cycles['yearly']['period'] if cycles['yearly'] else None,
        'yearly_days_into_period': cycles['yearly']['days_into_period'] if cycles['yearly'] else None,
        'yearly_period_duration': cycles['yearly']['period_duration'] if cycles['yearly'] else None,
        'soul_cycle_period': cycles['soul'],
        'health_cycle_period': cycles['health']['period'] if cycles['health'] else None,
        'health_days_into_period': cycles['health']['days_into_period'] if cycles['health'] else None,
        'health_period_duration': cycles['health']['period_duration'] if cycles['health'] else None,
        'reincarnation_cycle_period': cycles['reincarnation']['period'] if cycles['reincarnation'] else None,
        'human_cycle_period': cycles['human']['period'] if cycles['human'] else None,
        'human_age': cycles['human']['age'] if cycles['human'] else None,
    }
    return render(request, 'cycles/visualizations.html', context)

@login_required
def generate_report_pdf(request):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cycle_report.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    Story = []

    # Title
    Story.append(Paragraph("Cycles of Life Mastery Report", styles['h1']))
    Story.append(Spacer(1, 0.2 * inch))

    # User Information
    user_profile = UserProfile.objects.get(user=request.user)
    Story.append(Paragraph(f"Report for: {request.user.username}", styles['h2']))
    Story.append(Paragraph(f"Birth Date: {user_profile.birth_date or 'N/A'}", styles['Normal'])) # Handle None for birth_date
    Story.append(Paragraph(f"Gender: {user_profile.gender or 'N/A'}", styles['Normal'])) # Handle None for gender
    Story.append(Spacer(1, 0.2 * inch))

    # Cycle Information
    cycle_types = CycleTemplate.objects.all().order_by('name')
    for cycle_template in cycle_types:
        Story.append(Paragraph(f"<br/><b>{cycle_template.name}</b>", styles['h2']))
        Story.append(Paragraph(cycle_template.description or '', styles['Normal'])) # Handle None for description
        Story.append(Spacer(1, 0.1 * inch))

        for period_detail in cycle_template.period_details.all():
            Story.append(Paragraph(f"<b>{period_detail.period_name}</b> ({period_detail.start_value} - {period_detail.end_value})", styles['h3']))
            Story.append(Paragraph(period_detail.description or '', styles['Normal'])) # Handle None for description
            Story.append(Paragraph(f"Recommendations: {period_detail.recommendations or 'N/A'}", styles['Normal'])) # Handle None for recommendations
            Story.append(Spacer(1, 0.1 * inch))

    doc.build(Story)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def user_cycle_api(request, cycle_type):
    if cycle_type != 'daily' and not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    try:
        if cycle_type == 'daily':
            day_name = datetime.now().strftime('%A')
            template_name = f'Daily Cycle - {day_name}'
            cycle_template = CycleTemplate.objects.get(name=template_name)
        else:
            cycle_template = CycleTemplate.objects.get(cycle_type=cycle_type)

        serializer = CycleTemplateSerializer(cycle_template)
        return JsonResponse(serializer.data)
    except CycleTemplate.DoesNotExist:
        return JsonResponse({'error': 'Cycle type not found'}, status=404)
    except CycleTemplate.MultipleObjectsReturned:
        return JsonResponse({'error': 'Multiple cycle templates found for this type. Please contact an administrator.'}, status=500)


def htmx_cycle_tab(request, cycle_type):
    """Returns rendered HTML partial for a cycle tab via htmx."""
    if cycle_type != 'daily' and not request.user.is_authenticated:
        login_url = reverse('login')
        return HttpResponse(f'<p class="text-gray-500">Please <a href="{login_url}" class="text-purple-400 hover:underline">log in</a> to view this cycle.</p>')
    try:
        if cycle_type == 'daily':
            day_name = datetime.now().strftime('%A')
            template_name = f'Daily Cycle - {day_name}'
            cycle_template = CycleTemplate.objects.get(name=template_name)
        else:
            cycle_template = CycleTemplate.objects.get(cycle_type=cycle_type)

        periods = cycle_template.period_details.all().order_by('start_value')
        html = render_to_string('cycles/partials/cycle_tab_content.html', {
            'periods': periods,
            'cycle_type': cycle_type,
        })
        return HttpResponse(html)
    except (CycleTemplate.DoesNotExist, CycleTemplate.MultipleObjectsReturned):
        return HttpResponse('<p class="text-gray-500">Cycle data not available.</p>')

@login_required
def journal_list(request):
    entries_list = JournalEntry.objects.filter(user=request.user)
    paginator = Paginator(entries_list, 20)
    page = request.GET.get('page', 1)
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    form = JournalEntryForm()
    current_time = datetime.now().time()
    current_period = get_current_daily_cycle_period(current_time)
    period_prompt = None
    if current_period and hasattr(current_period, 'period_name'):
        prompts = {
            "Morning": "What intentions are you setting for the day ahead?",
            "Midday": "How has your energy and focus been so far today?",
            "Afternoon": "What progress have you made on today's priorities?",
            "Evening": "What went well today? What would you do differently?",
            "Night": "What are you grateful for today? What did you learn?",
        }
        period_prompt = prompts.get(current_period.period_name,
            f"Reflect on your current period: {current_period.description}")
    return render(request, 'cycles/journal_list.html', {
        'entries': entries,
        'form': form,
        'current_period': current_period,
        'period_prompt': period_prompt,
    })

@login_required
@require_POST
def journal_create(request):
    form = JournalEntryForm(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        daily_period = get_current_daily_cycle_period(datetime.now().time())
        if daily_period:
            entry.cycle_period = daily_period
        entry.save()
    return redirect('journal_list')

@login_required
@require_POST
def journal_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    entry.delete()
    return redirect('journal_list')

@login_required
def alerts(request):
    user_profile = UserProfile.objects.get(user=request.user)
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    transitions = get_upcoming_transitions(user_profile.birth_date, current_date, current_time)
    return render(request, 'cycles/alerts.html', {'transitions': transitions})

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            send_verification_email(self.request, self.object)
        except Exception:
            pass
        messages.success(self.request, 'Account created! Check your email for a verification link.')
        return response


def verify_email(request, token):
    profile = get_object_or_404(UserProfile, verification_token=token)
    if not profile.email_verified:
        profile.email_verified = True
        profile.verification_token = ''
        profile.save(update_fields=['email_verified', 'verification_token'])
        messages.success(request, 'Email verified successfully! You can now log in.')
    else:
        messages.info(request, 'Email was already verified.')
    return redirect('login')

def bad_request(request, exception=None):
    return render(request, 'errors/400.html', status=400)

def permission_denied(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def page_not_found(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def server_error(request):
    return render(request, 'errors/500.html', status=500)