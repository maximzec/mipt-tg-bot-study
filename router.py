from chatgpt_wrapper import ChatGPTWrapper
class Router:
    
    
    def __init__(self):
        self.chatgpt = ChatGPTWrapper()
        intent_handlers = {
            "analyze": self.analyze,
            "record": self.record,
            "stats": self.stats,
            "unknown": self.unknown
        }

    def route(self, user_text):
        intent = self.chatgpt.analyze_intent(user_text)
        return self.routes[intent](user_text)

    def analyze(self, user_text):
        pass

    def record(self, user_text):

        pass

    def stats(self, user_text):
        pass

    def unknown(self, user_text):
        pass