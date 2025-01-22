import json

from requests import get
import time

DIFFICULTY = ('easy', 'medium', 'hard')
MAX_QUESTIONS = 50


class ApiClient:
    CATEGORIES_URL = "https://opentdb.com/api_category.php"
    QUESTIONS_URL = "https://opentdb.com/api.php?amount={}&category={}&difficulty={}"
    STORAGE_FILE = "max_questions.json"
    question_count_max = {}

    @classmethod
    def load_json_data(cls):
        """Načtení dat z JSON souboru při spuštění programu."""
        try:
            with open(cls.STORAGE_FILE, "r") as file:
                cls.question_count_max = json.load(file)
        except FileNotFoundError:
            cls.question_count_max = {}

    @classmethod
    def save_json_data(cls):
        """Uložení dat do JSON souboru."""
        with open(cls.STORAGE_FILE, "w") as file:
            json.dump(cls.question_count_max, file)

    @classmethod
    def get_quiz_options(cls) -> dict:
        result = {'categories': get(ApiClient.CATEGORIES_URL).json()['trivia_categories'],
                  'max_questions': MAX_QUESTIONS, 'difficulty': DIFFICULTY}
        return result

    @classmethod
    def get_questions(cls, difficulty: str, number_of_questions: int, category: int, request=None) -> list:
        number_of_decreasing = 0
        request.session['number_of_decreasing'] = number_of_decreasing
        number_of_questions = int(number_of_questions)
        cls.load_json_data()

        max_possible_question = cls.question_count_max.get(category, {}).get(difficulty, 50)
        if number_of_questions > max_possible_question:
            number_of_decreasing = number_of_questions - max_possible_question
            number_of_questions = max_possible_question

        while number_of_questions > 0:
            url = cls.QUESTIONS_URL.format(number_of_questions, category, difficulty)
            response = get(url)
            response_data = response.json()

            # Kontrola úspěchu požadavku a případné vrácení seznamu otázek
            if response_data['response_code'] == 0:
                request.session['number_of_decreasing'] = number_of_decreasing
                if category not in cls.question_count_max:
                    cls.question_count_max[category] = {}
                if (difficulty not in cls.question_count_max[category] or
                        cls.question_count_max[category][difficulty] < number_of_questions):
                    cls.question_count_max[category][difficulty] = number_of_questions
                cls.save_json_data()
                return response_data['results']
            elif response_data['response_code'] == 1:
                print(f'není v databazi')
            elif response_data['response_code'] == 5:
                print(f'pozdavek se posila moc rychle za sebou')

            else:
                print(f"neznama chyba")

            number_of_questions -= 1
            number_of_decreasing += 1
            time.sleep(4)

        return []
