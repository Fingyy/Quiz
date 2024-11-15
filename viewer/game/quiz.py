from dataclasses import dataclass
from .api_client import ApiClient
from .question import Question
from typing import List


@dataclass
class Quiz:
    number_of_questions: int
    difficulty: str
    questions: List[Question]  # stary zapis pro list[Question]
    current_question: int
    number_of_correct_answers: int

    @classmethod
    def create_game(cls, number_of_questions, difficulty, category):
        raw_questions = ApiClient.get_questions(difficulty, number_of_questions, category)
        questions = list([Question(**raw_question) for raw_question in raw_questions])
        return Quiz(number_of_questions, difficulty, questions, 0, 0)

    def save(self, request):
        request.session['saved_quiz'] = self

    @staticmethod
    def stop(request):
        del request.session['saved_quiz']

    @classmethod
    def restore(cls, request):
        return request.session.get('saved_quiz')

    def check_answer(self, answer):
        if self.questions[self.current_question - 1].correct_answer == answer:
            self.number_of_correct_answers += 1

    def get_result(self):
        return {
            'correct_answers': self.number_of_correct_answers,
            'all_questions': self.number_of_questions
        }

    def get_question(self):
        if self.current_question >= len(self.questions):
            raise IndexError("No more questions.")
        question = self.questions[self.current_question]
        self.current_question += 1
        return question

