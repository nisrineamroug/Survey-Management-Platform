from django.shortcuts import render, redirect
from .forms import SondageForm, QuestionForm, FilterForm
from django.contrib.auth.decorators import login_required
from .models import Sondage, Question, Choice, Reponse, Answer
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import timezone
from collections import Counter
import json

@login_required
def dashboard(request):
    my_sondages = Sondage.objects(user_id=request.user.id)
    total_surveys = Sondage.objects(user_id=request.user.id).count()
    # Count responses for surveys created by this user
    user_survey_ids = [s.id for s in Sondage.objects(user_id=request.user.id)]
    total_responses = Reponse.objects(sondage__in=user_survey_ids).count()

    return render(request, 'sondages/dashboard.html', {
        'my_sondages': my_sondages,
        'total_surveys': total_surveys,
        'total_responses': total_responses,
    })

@login_required
def add_question(request, sondage_id):
    try:
        sondage = Sondage.objects.get(id=sondage_id, user_id=request.user.id)
    except Sondage.DoesNotExist:
        from django.http import Http404
        raise Http404("Sondage not found")

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # Formset not needed with mongoengine - handled manually

        if form.is_valid():
            question = Question(
                sondage=sondage,
                text=form.cleaned_data['text'],
                question_type=form.cleaned_data['question_type'],
                required=form.cleaned_data.get('required', True)
            )
            question.save()

            # Handle choices manually since we can't use formset with mongoengine
            choice_texts = request.POST.getlist('choices')
            for choice_text in choice_texts:
                if choice_text and choice_text.strip():
                    choice = Choice(question=question, text=choice_text.strip())
                    choice.save()
            # Redirect back to survey details to see the updated survey
            return redirect('survey_details', sondage_id=str(sondage.id))
    else:
        form = QuestionForm()
        formset = None  # We'll handle choices differently

    return render(request, 'sondages/add_question.html', {'form': form, 'formset': formset, 'sondage': sondage})

@login_required
def create_sondage(request):
    if request.method == 'POST':
        form = SondageForm(request.POST)
        if form.is_valid():
            sondage = Sondage(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                user_id=request.user.id
            )
            sondage.save()
            return redirect('add_question', sondage_id=str(sondage.id))
    else:
        form = SondageForm()
    return render(request, 'sondages/create_sondage.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .forms import SondageForm, QuestionForm  # Added ChoiceForm
from django.contrib.auth.decorators import login_required
from .models import Sondage, Question, Choice, Reponse, Answer
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone

def participer_sondage(request, sondage_id):
    try:
        import uuid
        # Convert string to UUID if needed
        link_uuid = uuid.UUID(sondage_id) if isinstance(sondage_id, str) else sondage_id
        sondage = Sondage.objects.get(shareable_link=link_uuid)
    except (Sondage.DoesNotExist, ValueError):
        from django.http import Http404
        raise Http404("Sondage not found")
    questions = Question.objects(sondage=sondage)
    ip_address = request.META.get('REMOTE_ADDR')

    if sondage.limit_ip and Reponse.objects(sondage=sondage, ip_address=ip_address).count() > 0:
        return HttpResponse("You have already submitted this survey from this IP address.")

    if request.method == 'POST':
        reponse = Reponse(
            sondage=sondage,
            user_id=request.user.id if request.user.is_authenticated else None,
            ip_address=ip_address
        )
        reponse.save()

        for question in questions:
            texte = request.POST.get(f"text_{question.id}", "")
            choix_ids = request.POST.getlist(f"choice_{question.id}")

            answer = Answer(
                reponse=reponse,
                question=question,
                texte=texte if question.question_type in ["tx", "scal"] else None
            )
            if question.question_type in ["sc", "mc"]:
                # Convert choice IDs to Choice objects
                choices = []
                for cid in choix_ids:
                    if cid:
                        try:
                            # Mongoengine can handle string ObjectIds
                            choice_obj = Choice.objects.get(id=cid)
                            choices.append(choice_obj)
                        except (Choice.DoesNotExist, Exception) as e:
                            print(f"Error finding choice {cid}: {e}")
                            # Try to continue with other choices
                            continue
                answer.choix = choices
            # Always save the answer
            try:
                answer.save()
            except Exception as e:
                print(f"Error saving answer: {e}")
                import traceback
                traceback.print_exc()
                # Continue with next question even if this one fails
        return redirect('merci')
    print(f"sondage.shareable_link: {sondage.shareable_link}")  # Add this line
    return render(request, 'sondages/participer.html', {
        'sondage': sondage,
        'questions': questions,
    })



@login_required
def my_surveys(request):
    surveys = Sondage.objects(user_id=request.user.id)
    return render(request, 'sondages/my_surveys.html', {'surveys': surveys})

@login_required
def survey_analytics(request):
    return render(request, 'sondages/survey_analytics.html', {'surveys': []})

@login_required
def survey_responses(request, survey_id=None):
    if survey_id:
        # Your survey responses logic here
        return render(request, 'sondages/survey_responses.html', {'survey_id': survey_id})
    else:
        return render(request, 'sondages/survey_responses.html', {'survey_id': None})


def QCM(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('dashboard')
    else:
        form = QuestionForm()
    return render(request, 'sondages/QCM.html', {'form': form})

def QCU(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('dashboard')
    else:
        form = QuestionForm()
    return render(request, 'sondages/QCU.html', {'form': form})

def TEXT(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('dashboard')
    else:
        form = QuestionForm()
    return render(request, 'sondages/TEXT.html', {'form': form})

def SCALE(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('dashboard')
    else:
        form = QuestionForm()
    return render(request, 'sondages/SCALE.html', {'form': form})

def mixed(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('dashboard')
    else:
        form = QuestionForm()
    return render(request, 'sondages/mixed.html', {'form': form})



@csrf_exempt  # Be careful with this in production
def save_scale_sondage(request):
    if request.method == 'POST':
        
        try:
            data = json.loads(request.body.decode('utf-8'))
            survey_title = data.get('surveyTitle')
            survey_description = data.get('surveyDescription')
            questions = data.get('questions')

            # Create Sondage object
            sondage = Sondage(
                title=survey_title,
                description=survey_description,
                user_id=request.user.id  # Assuming the user is logged in
            )
            sondage.save()

            # Create Question objects
            for question_data in questions:
                question = Question(
                   sondage=sondage,
                   text=question_data.get('questionText'),
                   question_type='scal',
                   min_value=question_data.get('minValue'),
                   max_value=question_data.get('maxValue')
                )
                question.save()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            print("Error:", e)  # Print the error message
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    
  

@csrf_exempt  # Be careful with this in production
def save_qcu_sondage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            survey_title = data.get('surveyTitle')
            survey_description = data.get('surveyDescription')
            questions = data.get('questions')

            # Create Sondage object
            sondage = Sondage(
                title=survey_title,
                description=survey_description,
                user_id=request.user.id  # Assuming the user is logged in
            )
            sondage.save()

            # Create Question objects
            for question_data in questions:
                question = Question(
                    sondage=sondage,
                    text=question_data.get('questionText'),
                    question_type='sc'  # Single Choice
                )
                question.save()

                # Create Choice objects
                options = question_data.get('options')
                for option_text in options:
                    choice = Choice(
                        question=question,
                        text=option_text
                    )
                    choice.save()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            print("Error:", e)  # Print the error message
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
    
    
    
    
    
    
@csrf_exempt  # Be careful with this in production
def save_qcm_sondage(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body.decode('utf-8'))
                survey_title = data.get('surveyTitle')
                survey_description = data.get('surveyDescription')
                questions = data.get('questions')
    
                # Create Sondage object
                sondage = Sondage(
                    title=survey_title,
                    description=survey_description,
                    user_id=request.user.id  # Assuming the user is logged in
                )
                sondage.save()

                # Create Question objects
                for question_data in questions:
                    question = Question(
                        sondage=sondage,
                        text=question_data.get('questionText'),
                        question_type='mc'  # Multiple Choice
                    )
                    question.save()

                    # Create Choice objects
                    options = question_data.get('options')
                    for option_text in options:
                        choice = Choice(
                            question=question,
                            text=option_text
                        )
                        choice.save()
    
                return JsonResponse({'status': 'success'})
    
            except Exception as e:
                print("Error:", e)  # Print the error message
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        

@csrf_exempt  # Be careful with this in production
def save_text_sondage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            survey_title = data.get('surveyTitle')
            survey_description = data.get('surveyDescription')
            questions = data.get('questions')

            # Create Sondage object
            sondage = Sondage(
                title=survey_title,
                description=survey_description,
                user_id=request.user.id  # Assuming the user is logged in
            )
            sondage.save()

            # Create Question objects
            for question_data in questions:
                question = Question(
                    sondage=sondage,
                    text=question_data.get('questionText'),
                    question_type='tx',  # Text
                    required=question_data.get('required', True),
                    min_value=question_data.get('minLength'),
                    max_value=question_data.get('maxLength')
                )
                question.save()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            print("Error:", e)  # Print the error message
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    



@csrf_exempt  # Be careful with this in production
def save_mixed_sondage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            survey_title = data.get('surveyTitle')
            survey_description = data.get('surveyDescription')
            questions = data.get('questions')

            # Create Sondage object
            sondage = Sondage(
                title=survey_title,
                description=survey_description,
                user_id=request.user.id  # Assuming the user is logged in
            )
            sondage.save()

            # Create Question objects
            for question_data in questions:
                question_text = question_data.get('questionText')
                question_type = question_data.get('questionType')
                question = Question(
                    sondage=sondage,
                    text=question_text,
                    question_type=question_type
                )
                question.save()

                # Create Choice objects if the question type is Single Choice or Multiple Choice
                if question_type in ['sc', 'mc']:
                    options = question_data.get('options')
                    for option_text in options:
                        choice = Choice(
                            question=question,
                            text=option_text
                        )
                        choice.save()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            print("Error:", e)  # Print the error message
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    

@login_required
def update_sondage(request, sondage_id):
    try:
        sondage = Sondage.objects.get(id=sondage_id, user_id=request.user.id)
    except Sondage.DoesNotExist:
        from django.http import Http404
        raise Http404("Sondage not found")
    
    # Get all questions for this survey
    questions = Question.objects(sondage=sondage)
    
    if request.method == 'POST':
        sondage.title = request.POST['title']
        sondage.description = request.POST['description']
        sondage.password = request.POST.get('password', '')  # Handle optional password
        sondage.limit_responses = request.POST.get('limit_responses', False) == 'on'
        sondage.limit_ip = request.POST.get('limit_ip', False) == 'on'
        sondage.save()
        return redirect('survey_details', sondage_id=str(sondage.id))
    
    return render(request, 'sondages/update_sondage.html', {
        'sondage': sondage,
        'questions': questions
    })

@login_required
def delete_sondage(request, sondage_id):
    try:
        sondage = Sondage.objects.get(id=sondage_id, user_id=request.user.id)
    except Sondage.DoesNotExist:
        from django.http import Http404
        raise Http404("Sondage not found")
    if request.method == 'POST':
        sondage.delete()
        return redirect('dashboard')
    return render(request, 'sondages/delete_sondage.html', {'sondage': sondage})



def survey_details(request, sondage_id):
    try:
        sondage = Sondage.objects.get(id=sondage_id, user_id=request.user.id)
    except Sondage.DoesNotExist:
        from django.http import Http404
        raise Http404("Sondage not found")
    
    # Get all questions for this survey
    questions = Question.objects(sondage=sondage)
    
    # Get choices for each question
    questions_with_choices = []
    for question in questions:
        question_data = {
            'question': question,
            'choices': Choice.objects(question=question) if question.question_type in ['sc', 'mc'] else []
        }
        questions_with_choices.append(question_data)
    
    shareable_link = request.build_absolute_uri(reverse('participer_sondage', args=[sondage.shareable_link]))
    embed_code = format_html('<iframe src="{}" width="600" height="400"></iframe>', shareable_link)

    return render(request, 'sondages/survey_details.html', {
        'sondage': sondage,
        'questions': questions_with_choices,
        'shareable_link': shareable_link,
        'embed_code': embed_code,
    })


from collections import Counter

def apply_filters(responses, user, date):
    if user:
        responses = responses.filter(user__username__icontains=user)
    if date:
        responses = responses.filter(date__date=date)
    return responses

def survey_results(request, sondage_id):
    try:
        sondage = Sondage.objects.get(id=sondage_id)
    except Sondage.DoesNotExist:
        from django.http import Http404
        raise Http404("Sondage not found")
    questions = Question.objects(sondage=sondage)
    responses = Reponse.objects(sondage=sondage)
    num_responses = len(responses)

    # Apply filters
    form = FilterForm(request.GET)
    if form.is_valid():
        user = form.cleaned_data.get('user')
        date = form.cleaned_data.get('date')
        if user:
            # Filter by username - need to get user IDs first
            user_ids = [u.id for u in User.objects.filter(username__icontains=user)]
            responses = [r for r in responses if r.user_id in user_ids]
        if date:
            responses = [r for r in responses if r.date.date() == date]

    chart_data = []

    for question in questions:
        data_entry = {
            'question_text': question.text,
            'chart_type': '',
            'labels': [],
            'values': [],
            'responses': [],
        }

        if question.question_type in ['sc', 'mc']:
            choices = Choice.objects(question=question)
            labels = [choice.text for choice in choices]
            values = []
            response_ids = [r.id for r in responses]

            # Get all answers for this question and these responses
            answers = Answer.objects(question=question, reponse__in=response_ids)
            
            for choice in choices:
                count = 0
                current_choice_id = str(choice.id)
                
                for answer in answers:
                    if answer.choix and len(answer.choix) > 0:
                        # answer.choix is a list of Choice objects (ReferenceFields)
                        # Convert each to string ID and compare
                        for choix_item in answer.choix:
                            choix_item_id = str(choix_item.id if hasattr(choix_item, 'id') else choix_item)
                            if choix_item_id == current_choice_id:
                                count += 1
                                break  # Found match for this answer, count once
                values.append(count)

            data_entry['chart_type'] = 'pie' if question.question_type == 'sc' else 'bar'
            data_entry['labels'] = labels
            data_entry['values'] = values

        elif question.question_type == 'scal':
            labels = [str(i) for i in range(question.min_value, question.max_value + 1)]
            values = []
            response_ids = [r.id for r in responses]

            for i in range(question.min_value, question.max_value + 1):
                count = len([a for a in Answer.objects(question=question, reponse__in=response_ids) 
                            if a.texte == str(i)])
                values.append(count)

            data_entry['chart_type'] = 'bar'
            data_entry['labels'] = labels
            data_entry['values'] = values

        elif question.question_type == 'tx':
            response_ids = [r.id for r in responses]
            text_responses = [answer.texte for answer in Answer.objects(question=question, reponse__in=response_ids) if answer.texte]
            data_entry['chart_type'] = 'text'
            data_entry['responses'] = text_responses

        chart_data.append(data_entry)

    return render(request, 'sondages/survey_results.html', {
        'sondage': sondage,
        'num_responses': num_responses,
        'chart_data': chart_data,
        'filter_form': form,  # Pass the form to the template
    })


import csv
from django.http import HttpResponse
from .models import Sondage, Reponse, Answer


def export_responses(request, sondage_id):
    try:
        sondage = Sondage.objects.get(id=sondage_id)
    except Sondage.DoesNotExist:
        from django.http import Http404
        raise Http404("Sondage not found")
    responses = Reponse.objects(sondage=sondage)
    questions = Question.objects(sondage=sondage)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{sondage.title}_responses.csv"'

    writer = csv.writer(response)

    # Write header row
    header = ['Date', 'User', 'IP Address'] + [q.text for q in questions]
    writer.writerow(header)

    # Write data rows
    for r in responses:
        row = [r.date, r.user.username if r.user else '', r.ip_address or '']
        for q in questions:
            answers = Answer.objects(reponse=r, question=q)
            if answers:
                answer = answers[0]
                if q.question_type in ['sc', 'mc']:
                    choices = ", ".join([c.text for c in answer.choix])
                    row.append(choices)
                else:
                    row.append(answer.texte or '')
            else:
                row.append('')
        writer.writerow(row)

    return response


import xlsxwriter
from django.http import HttpResponse
from .models import Sondage, Reponse, Answer

def export_responses_excel(request, sondage_id):
    try:
        sondage = Sondage.objects.get(id=sondage_id)
    except Sondage.DoesNotExist:
        from django.http import Http404
        raise Http404("Sondage not found")
    responses = Reponse.objects(sondage=sondage)
    questions = Question.objects(sondage=sondage)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{sondage.title}_responses.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'remove_timezone': True})
    worksheet = workbook.add_worksheet()

    # Write header row
    header = ['Date', 'User', 'IP Address'] + [q.text for q in questions]
    for col_num, column_title in enumerate(header):
        worksheet.write(0, col_num, column_title)

    # Write data rows
    for row_num, r in enumerate(responses, 1):
        row = [str(r.date), r.user.username if r.user else '', r.ip_address or '']
        for q in questions:
            answers = Answer.objects(reponse=r, question=q)
            if answers:
                answer = answers[0]
                if q.question_type in ['sc', 'mc']:
                    choices = ", ".join([c.text for c in answer.choix])
                    row.append(choices)
                else:
                    row.append(answer.texte or '')
            else:
                row.append('')
        for col_num, cell_value in enumerate(row):
            worksheet.write(row_num + 1, col_num, cell_value)

    workbook.close()
    return response

