from requests import get

DIFFICULTY = ('easy', 'medium', 'hard')
MAX_QUESTIONS = 50


class ApiClient:
    CATEGORIES_URL = "https://opentdb.com/api_category.php"
    QUESTIONS_URL = "https://opentdb.com/api.php?amount={}&category={}&difficulty={}"
    question_count_max = {}


    @classmethod
    def get_quiz_options(cls) -> dict:
        result = {'categories': get(ApiClient.CATEGORIES_URL).json()['trivia_categories'],
                  'max_questions': MAX_QUESTIONS, 'difficulty': DIFFICULTY}
        return result

    @classmethod
    def get_questions(cls, difficulty: str, number_of_questions: int, category: int, request = None) -> list:
        request.session['number_of_decreasing'] = 0
        number_of_decreasing = 0
        number_of_questions = int(number_of_questions)
        print(cls.question_count_max)
        tolik_je_maximum = cls.question_count_max.get(category, {}).get(difficulty, 999999999)
        if tolik_je_maximum < number_of_questions:
            number_of_decreasing = number_of_questions - tolik_je_maximum
            number_of_questions = tolik_je_maximum

        print(f"self.question_count_max {cls.question_count_max}")
        while number_of_questions > 0:
            #Zde ve while cyklu ošetřit, pokud nastane  response_data['response_code'] == 5
            url = cls.QUESTIONS_URL.format(number_of_questions, category, difficulty)
            response = get(url)
            response_data = response.json()

            # Kontrola úspěchu požadavku a případné vrácení seznamu otázek

            if response_data['response_code'] == 0:
                print(f"number_of_questions {number_of_questions} je OK")
                request.session['number_of_decreasing'] = number_of_decreasing
                return response_data['results']
            elif response_data['response_code'] == 1:
                print(f"number_of_questions {number_of_questions} je příliš")
                if category not in cls.question_count_max:
                    cls.question_count_max[category] = {}
                if difficulty not in cls.question_count_max[category]:
                    cls.question_count_max[category][difficulty] = 9999999
                cls.question_count_max[category][difficulty] = number_of_questions -1
                #známá chyba - není dostatečný počet otázek
            else:
                print("CHYBA response_data")
                pass
            #del response_data
            number_of_questions -= 1
            number_of_decreasing += 1
            import time
            time.sleep(3)

        return []
