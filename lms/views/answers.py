from django.shortcuts import render, redirect, get_object_or_404

from lms.models import UserAnswer, Test, Question


def show_answers(request, test_id):
    answers = get_object_or_404(Test, pk=test_id)
    return render(request, 'answers/show_answers.html', {'answers': answers})


def submit_answer(request, test_id):
    test = Test.objects.get(pk=test_id)
    questions = Question.objects.filter(test=test)
    if request.method == 'POST':
        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                answer = UserAnswer.objects.get(pk=answer_id)
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
