from dataclasses import dataclass, field
from typing import List
from random import shuffle
from html import unescape


@dataclass
class Question:
    category: str
    type: str
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]
    answers: List[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.question = unescape(self.question)  # unescape prevede znaky jako &quot -> ", z JSON souboru
        self.correct_answer = unescape(self.correct_answer)
        self.incorrect_answers = [unescape(answer) for answer in self.incorrect_answers]
        self.answers.extend(self.incorrect_answers)
        self.answers.append(self.correct_answer)
        shuffle(self.answers)  # shuffle náhodně zamíchá prvky v seznamu
    
    def check_answer(self, answer: str):
        return answer == self.correct_answer
