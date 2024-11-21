from django.shortcuts import render, redirect
from viewer.game.api_client import ApiClient
from viewer.game.quiz import Quiz


def index(request):
    try:
        quiz = ApiClient.get_quiz_options()
        return render(request, 'index.html', quiz)
    except ValueError:
        return render(request, 'error.html',{"message": "Chyba nacitani databaze"})


def start_game(request):
    number_of_questions = request.POST['quantity']  # rovnou [] kdyz je to povinny parametr
    difficulty = request.POST['difficulty']
    category = request.POST['category']
    quiz = Quiz.create_game(number_of_questions, difficulty, category)
    quiz.save(request)  # musim ulozit jinak po konci start_game se data ztrati
    return redirect('/on_game')


def on_game(request):
    quiz = Quiz.restore(request)
    if not quiz:
        return render(request, 'error.html')

    answer = request.POST.get('answer')  # get() u POST použiji, když je to nepovinny parametr
    if answer:
        quiz.check_answer(answer)

    try:
        question = quiz.get_question()
        quiz.save(request)
        return render(request, 'game.html', vars(question))
    except IndexError as x:
        return redirect('/finish')


def finish(request):
    # Obnovení uloženého stavu kvízu
    quiz = Quiz.restore(request)
    if not quiz:
        return render(request, 'error.html', {"message": "Quiz data not found in session."})

    # Získání výsledků kvízu
    result = quiz.get_result()
    # Ukončení kvízu a odstranění ze session
    quiz.stop(request)
    # Zobrazení výsledků v šabloně
    return render(request, 'finish.html', result)
