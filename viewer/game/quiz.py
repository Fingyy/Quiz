from dataclasses import dataclass
from .api_client import ApiClient
from .question import Question
from typing import List
from django.shortcuts import render


@dataclass
class Quiz:
    number_of_questions: int
    difficulty: str
    questions: List[Question]  # stary zapis pro list[Question]
    current_question: int
    number_of_correct_answers: int
    just_started: bool

    @classmethod
    def create_game(cls, number_of_questions, difficulty, category):
        raw_questions = ApiClient.get_questions(difficulty, number_of_questions, category)
        questions = list([Question(**raw_question) for raw_question in raw_questions])
        # if len(questions) == 0:
        #     raise ValueError("Žádné otázky nejsou k dispozici.")
        # if int(number_of_questions) > len(questions):
        #     # number_of_questions = str(len(questions))
        #     return Quiz(len(questions), difficulty, questions, 0, 0, True)
        return Quiz(number_of_questions, difficulty, questions, 0, 0, True)

    def save(self, request):
        request.session['saved_quiz'] = self

    @staticmethod
    def stop(request):
        del request.session['saved_quiz']  # jen smaže klíč 'saved_quiz'] ze sessionu

    @classmethod
    def restore(cls, request):
        return request.session.get('saved_quiz')

    def get_question(self):
        if self.current_question >= len(self.questions):
            raise IndexError("No more questions.")

        # Pokud je kvíz právě inicializován, vrať aktuální otázku
        if self.just_started or self.current_question == 0:
            self.just_started = False
            return self.questions[self.current_question]
        return self.questions[self.current_question]

    def check_answer(self, answer):
        if self.questions[self.current_question].correct_answer == answer:
            self.number_of_correct_answers += 1

        if (answer == self.questions[self.current_question].correct_answer or
                answer in self.questions[self.current_question].incorrect_answers):
            self.current_question += 1
            self.just_started = True

    def get_result(self):
        return {
            'correct_answers': self.number_of_correct_answers,
            'all_questions': self.number_of_questions
        }
