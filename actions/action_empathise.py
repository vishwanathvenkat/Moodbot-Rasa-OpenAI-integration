# action_llm_empathise.py
from typing import Any, Text, Dict, List
from dotenv import load_dotenv


from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from openai import OpenAI
from rasa_sdk.events import SlotSet
import httpx
import os


load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

class ActionEmpathise(Action):

    def __init__(self):
        super().__init__()
        self.nlg_client = OpenAI(timeout=httpx.Timeout(15.0, read=5.0, write=10.0, connect=3.0))
        self.false_llm_instruction = """
        You are a mental wellness bot.
        You take a string of dictionary with key values.
        You can summarize the details but don't assume anything.
        You should check if the string of dictionary has all the values not equal to "None".
        If not, you should prompt the user to fill in the rest of the details by specifically.

        If all the values are not equal to "None", you just ask the user if your understanding is correct asking them to answer the question.

        If the user strays off topic and enters random answers, gently remind them you are just a mental wellness bot and ask them to stick to the topic
        """

        self.true_llm_instruction = """You are a mental wellness bot.
                                    You take a string of dictionary with key values.
                                    You say something cheerful or consolation based on the
                                    values that are filled.
                                    You give a quote from the internet relevant to the emotion, behavior, and cause of the user
                                    You also recommend some psychology practice for the user appropriate to the current situation
        """

        self.temperature = 0.2
        self.top_p = 0.2
        self.model = 'gpt-3.5-turbo-1106'

    def name(self) -> Text:
        return "action_llm_empathise"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message
        text = message['metadata']

        if "is_understanding_correct" in text:
            to_bool = {'True': True, 'False': False}
            is_understanding_correct = to_bool[text.split(": ")[-1]]
            llm_input_text = self.get_text_from_slots(tracker)
        else:
            llm_input_text = text
            is_understanding_correct = False

        if not is_understanding_correct:
            response = self.nlg_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.false_llm_instruction},
                    {"role": "user", "content": llm_input_text},
                ],
                temperature=self.temperature,
                top_p=self.top_p
            )
            message = response.choices[0].message.content
            dispatcher.utter_message(text=message)
        else:
            response = self.nlg_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.true_llm_instruction},
                    {"role": "user", "content": llm_input_text},
                ],
                temperature=self.temperature,
                top_p=self.top_p
            )
            message = response.choices[0].message.content
            dispatcher.utter_message(text=message)

        dictionary = self.get_values(text)
        return [SlotSet(key, value) for key, value in dictionary.items() if value != "None"]

    def get_text_from_slots(self, tracker: Tracker):
        dictionary = {}
        for slot in ["emotion", "behaviour", "cause"]:
            dictionary[slot] = tracker.get_slot(slot)

        return str(dictionary)

    # Extract a dict from a string of dict
    def get_values(self, input):
        lines = input.split('\n')

        # Initialize an empty dictionary
        result_dict = {}

        # Iterate through each line
        for line in lines:
            # Split each line into key and value using ':'
            parts = line.split(':')

            # Extract key and value
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()

                # Add key-value pair to the dictionary
                result_dict[key] = value

        return result_dict
