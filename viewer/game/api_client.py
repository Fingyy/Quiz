from requests import get

DIFFICULTY = ('easy', 'medium', 'hard')
MAX_QUESTIONS = 50


class ApiClient:
    CATEGORIES_URL = "https://opentdb.com/api_category.php"
    QUESTIONS_URL = "https://opentdb.com/api.php?amount={}&category={}&difficulty={}"

    @classmethod
    def get_quiz_options(cls) -> dict:
        result = {'categories': get(ApiClient.CATEGORIES_URL).json()['trivia_categories'],
                  'max_questions': MAX_QUESTIONS, 'difficulty': DIFFICULTY}
        return result

    @classmethod
    def get_questions(cls, difficulty: str, number_of_questions: int, category: int, request: None) -> list:
        number_of_decreasing = 0
        number_of_questions = int(number_of_questions)
        while number_of_questions > 0:
            url = cls.QUESTIONS_URL.format(number_of_questions, category, difficulty)
            response = get(url)
            response_data = response.json()

            # Kontrola úspěchu požadavku a případné vrácení seznamu otázek
            if response_data['response_code'] == 0:
                if request is not None and number_of_decreasing > 0:
                    request.session['number_of_decreasing'] = number_of_decreasing
                return response_data['results']

            del response_data
            number_of_questions -= 1
            number_of_decreasing += 1

        return []
