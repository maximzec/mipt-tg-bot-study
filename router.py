from datetime import datetime
from chatgpt_wrapper import ChatGPTWrapper
from database import insert_record, get_unique_categories, get_aggregated_expenses, get_all_records


class Router:

    def __init__(self):
        self.chatgpt = ChatGPTWrapper()
        self.routes = {
            "analyze": self.analyze,
            "record": self.record,
            "stats": self.stats,
            "unknown": self.unknown
        }

    def route(self, user_text, user_id):
        intent = self.chatgpt.analyze_intent(user_text)
        return self.routes[intent](user_text, user_id)

    def analyze(self, user_text, user_id):
        records = get_all_records(user_id)
        return self.chatgpt.analyze(user_text, records)

    def record(self, user_text, user_id):
        record = self.chatgpt.record(user_text)
        insert_record(user_id, record['type'], record['amount'],
                      record['category'], datetime.now())
        return f"Запись на сумму {record['amount']} в категорию {record['category']} добавлена"

    def stats(self, user_text, user_id):
        categories = get_unique_categories(user_id)
        stats = self.chatgpt.stats(user_text, categories)

        return get_aggregated_expenses(user_id, stats['start_date'], stats['end_date'], stats['categories'])

    def unknown(self, user_text, user_id):
        return "Пожалуйста, перефразируйте ваш запрос"
