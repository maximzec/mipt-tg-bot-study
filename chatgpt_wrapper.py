from openai import OpenAI
from pydantic import BaseModel
from enum import Enum
from models import  IntentResponse, IntentRequest
import json

client = OpenAI()


class ChatGPTWrapper:
    def __init__(self):
        self.client = OpenAI()

    def analyze_intent(self, user_text)->IntentResponse:
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": ("Ты выступаешь в качестве ИИ для бота в телеграмм."
                        "В твои задачи входит анализ сообщений пользователя и определение направления, в котором будет развиваться диалог. "
                    "Если пользователь задает тебе открытые вопросы, то его намерение ANALYZE. Примеры: как мне улучшить свой бюджет, как я могу сэкономить на еде и т.д."
                    "Если пользователь хочет записать трату или доход, то его намерение RECORD. Примеры: потратил 1000 рублей на еду, заработал 5000 рублей на фрилансе."
                    "Если пользователь хочет получить статистику, то его намерение STATS. Примеры: сколько я потратил за последнюю неделю, сколько я заработал за последний месяц и т.д."
                    "Если пользователь задает общие вопросы, не относящиеся к вышеперечисленным, то его намерение UNKNOWN.")
                    },
                {
                    "role": "user",
                    "content": f"{user_text}"
                }
            ],
            response_format=IntentResponse
        )
        intent = json.loads(completion.choices[0].message.content)["intent"]
        return IntentResponse(intent=intent)

    def record(self, user_text):
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": ("Ты выступаешь в качестве ИИ для бота в телеграмм."
                    "Ты должен записать трату или доход пользователя. "
                    "Твоя задача - выписать из сообщения пользователя сумму и категорию.")
                    },
                {
                    "role": "user",
                    "content": f"{user_text}"
                }
            ],
            response_format=RecordResponse
        )
        return completion.choices[0].message.content