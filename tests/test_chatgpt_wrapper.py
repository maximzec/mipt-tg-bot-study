import unittest
from unittest.mock import patch, MagicMock

from chatgpt_wrapper import ChatGPTWrapper
from models import IntentResponse, RecordResponse, StatsResponse
import json
import sys
import os

# sys.path.insert(0, os.path.abspath(os.path.join(
#     os.path.dirname(__file__), '..')))


class TestChatGPTWrapper(unittest.TestCase):

    @patch('chatgpt_wrapper.OpenAI')
    def setUp(self, MockOpenAI):
        self.mock_client = MockOpenAI.return_value
        self.wrapper = ChatGPTWrapper()

    def test_analyze_intent(self):
        self.mock_client.beta.chat.completions.parse.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(
                content=json.dumps({'intent': 'ANALYZE'})))]
        )
        result = self.wrapper.analyze_intent("Как мне улучшить свой бюджет?")
        self.assertEqual(result, 'ANALYZE')

    def test_record(self):
        self.mock_client.beta.chat.completions.parse.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(
                content=json.dumps({'amount': 1000, 'category': 'еда'})))]
        )
        result = self.wrapper.record("Потратил 1000 рублей на еду")
        self.assertEqual(result['amount'], 1000)
        self.assertEqual(result['category'], 'еда')

    def test_stats(self):
        self.mock_client.beta.chat.completions.parse.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=json.dumps(
                {'period': 'неделя', 'categories': ['еда']})))]
        )
        result = self.wrapper.stats(
            "Сколько я потратил за последнюю неделю?", ['еда', 'транспорт'])
        self.assertEqual(result['period'], 'неделя')
        self.assertIn('еда', result['categories'])

    def test_analyze(self):
        self.mock_client.beta.chat.completions.parse.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(
                content="Совет по улучшению бюджета"))]
        )
        result = self.wrapper.analyze("Как мне улучшить свой бюджет?", [
                                      {'amount': 1000, 'category': 'еда'}])
        self.assertEqual(result, "Совет по улучшению бюджета")


if __name__ == '__main__':
    unittest.main()
