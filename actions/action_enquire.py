# action_enquire.py
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from openai import OpenAI
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')


class ActionEnquire(Action):

    def __init__(self):
        super().__init__()
        self.llm_instruction = """
        You are a mental wellness bot.
        You greet the user and inquire how their day has been.
        You ask the user to share their day's update in the form of a paragraph.
        You ask the user to include information on their emotional state.
        You ask the user to also explain what is the cause of that emotion.
        You ask the user to explain how they behave when such emotions occur.
        Give an example like this to explain the situation
        e.g. "Encountered a setback when a major software release had unexpected issues post-deployment. I felt a mix of stress
        and urgency. My reaction was to coordinate with the team to identify and resolve the issues promptly.."
        """
        self.nlg_client = OpenAI(timeout=httpx.Timeout(15.0, read=5.0, write=10.0, connect=3.0))
        self.model = 'gpt-3.5-turbo-1106'
        self.temperature = 1.8

    def name(self) -> Text:
        return "action_enquire"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = self.nlg_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.llm_instruction},
                {"role": "user", "content": "Hello"},
            ],
            temperature=self.temperature
        )
        message = response.choices[0].message.content
        dispatcher.utter_message(text=message)

        return []
