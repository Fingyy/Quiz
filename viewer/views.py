from django.shortcuts import render, redirect
from django.views.generic import ListView
from viewer.game.api_client import ApiClient
from viewer.game.quiz import Quiz
from django.views.decorators.cache import cache_page
from time import time
from viewer.models  import Game


@cache_page(60 * 15)  # ulozi do cache na 15min (at se nemusi prikaz pokazde vykonat)
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
    nick = request.POST['nick']

    if 'quiz_result' in request.session:
        del request.session['quiz_result']
    try:
        quiz = Quiz.create_game(number_of_questions, difficulty, category)
        quiz.save(request)  # musim ulozit jinak po konci start_game se data ztrati
        game_stat = Game(nick_name=nick, difficulty=difficulty, category=category, total_questions=number_of_questions)
        game_stat.save()
        request.session['game_stat'] = game_stat
        request.session['start_time'] = time()
        return redirect('/on_game')
    except ValueError as e:
        return render(request, 'error.html',{"message": str(e)})


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
        context = vars(question)
        context['quiz'] = quiz
        return render(request, 'game.html', context)
    except IndexError as x:
        start_quiz = request.session['start_time']
        end_quiz = time()
        duration = end_quiz - start_quiz
        request.session['duration'] = duration

        return redirect('/finish')


def finish(request):
    # v případě F5 se díky uloženému sessionu zobrazi výsledek
    if 'quiz_result' in request.session:
        result = request.session['quiz_result']
        return render(request, 'finish.html', result)

    # Obnovení uloženého stavu kvízu
    quiz = Quiz.restore(request)
    if not quiz:
        return render(request, 'error.html', {"message": "Quiz data not found in session."})

    # Získání výsledků kvízu
    result = quiz.get_result()
    request.session['quiz_result'] = result
    number_of_correct_answers = quiz.number_of_correct_answers
    # Ukončení kvízu a odstranění ze session
    quiz.stop(request)
    if request.session['duration']:
        result['duration'] = str(request.session['duration'])
        game_stat = request.session['game_stat']
        game_stat.duration = request.session['duration']
        game_stat.correct_answers = number_of_correct_answers
        game_stat.save()
        result['rate'] = game_stat.success_rate
        result['duration_format'] = game_stat.duration_format()

    # Zobrazení výsledků v šabloně
    return render(request, 'finish.html', result)


class ResultList(ListView):
    model = Game
    template_name = 'result_list.html'
    context_object_name = 'results'
    ordering = ['total_questions']  # Seřadíme výsledky od nejlepších

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset[:11]  # Vrátíme jen prvních 10
