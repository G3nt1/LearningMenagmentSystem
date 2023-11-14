from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from lms.models import UserAnswer, Test, Question, Options


def submit_answers(request, test_id):
    test = Test.objects.get(pk=test_id)
    if UserAnswer.objects.filter(user=request.user, test=test).exists():
        return redirect('answers', test_id=test.id)
    questions = Question.objects.filter(test=test)

    if request.method == 'POST':
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                answer = Options.objects.get(pk=answer_id)
                is_correct = answer.is_correct
            else:
                answer = None
                is_correct = False

            # Check if the user already has an answer for this question and test
            user_answer, created = UserAnswer.objects.get_or_create(
                user=request.user,
                test=test,
                question=question,
                defaults={
                    'answer': answer,
                    'is_correct': is_correct,
                    'points_earned': question.points if is_correct else 0
                }
            )

            # If the user has already answered this question before, update the answer
            if not created:
                user_answer.answer = answer
                user_answer.is_correct = is_correct
                user_answer.points_earned = question.points if is_correct else 0
                user_answer.save()

        return redirect('answers', test_id=test.id)

    return render(request, 'answers/submit_answers.html',
                  {'test': test, 'questions': questions})


def show_answers(request, test_id):
    test = get_object_or_404(Test, pk=test_id)

    # Check if the current user is the test creator
    if request.user == test.creator:
        user_answers = UserAnswer.objects.filter(test=test_id)
    else:
        user_answers = UserAnswer.objects.filter(test=test, user=request.user)

    # Group user answers by user
    user_answers_by_user = {}
    for user_answer in user_answers:
        user = user_answer.user
        if user in user_answers_by_user:
            user_answers_by_user[user].append(user_answer)
        else:
            user_answers_by_user[user] = [user_answer]

    # Calculate total points, max points, and percentage for each user
    user_results = []
    for user, answers in user_answers_by_user.items():
        total_points = sum(answer.points_earned for answer in answers)

        max_points = test.question_set.aggregate(Sum('points'))['points__sum']
        max_points = max_points if max_points is not None else 0

        percentage = total_points / max_points * 100 if max_points > 0 else 0
        user_results.append({
            'user': user,
            'user_answers': answers,
            'total_points': total_points,
            'max_points': max_points,
            'percentage': percentage
        })

    # Save the user answers to the database
    for user_answer in user_answers:
        user_answer.save()

    return render(request, 'answers/show_answers.html', {
        'test': test,
        'user_results': user_results,
    })
