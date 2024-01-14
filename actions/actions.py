# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from openai import OpenAI
from rasa_sdk.events import SlotSet
import httpx

#
class ActionEnquire(Action):

    def __init__(self):
        super().__init__()
        self.llm_instruction = "You are a mental wellness bot. "\
                               "You greet the user and enquire how their day has been. "\
                               "You ask the user to share their day's update in the form of a paragraph. "\
                               "you ask the user to include information on their emotional state."\
                               "You ask the user to also explain what is the cause of that emotion"\
                               "YOu ask the user to explain how they behave when such emotions occur "\
                               "Give an example like this to explain the situation"\
                               " e.g. Encountered a setback when a major software release had unexpected issues post-deployment. "\
                                "I felt a mix of stress and urgency. My reaction was to coordinate with the team to identify "\
                               "and resolve the issues promptly. The reason for my emotional state was the unexpected post-deployment issues, making it a professional cause."

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


class ActionEmpathise(Action):

    def __init__(self):
        super().__init__()
        self.nlg_client = OpenAI(timeout=httpx.Timeout(15.0, read=5.0, write=10.0, connect=3.0))
        self.false_llm_instruction = "You are a mental wellness bot. "\
                                     "You take a string of dictionary with key values. "\
                                     "You can summarize the details but dont assume assume anything "\
                                     "You should check if the string of dictionary has all the values not equal to None."\
                                     " If not, You should prompt the user to fill in the rest of the details by specifically"\
                                     "If all the values are not equal to none. You just ask the user if your understanding is correct"\
                                     "asking them to answer the question. If the user strays off topic and enters random answers, "\
                                     "gently remind them you are just a mental wellness bot and ask them to stick to the topic"

        self.true_llm_instruction = "You are a mental wellness bot. "\
                                    "You take a string of dictionary with key values. "\
                                    "YOu say something cheerful or consolation based on the "\
                                    "values that are filled."\
                                    "You give a quote from internet to relevant to the emotion, behaviour and cause of the user"\
                                    " You also recommend some psychology practice for the user appropriate to the current situation"

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
            toBool = {'True': True, 'False': False}
            is_understanding_correct = toBool[text.split(": ")[-1]]
            llm_input_text = self.get_text_from_slots(tracker)
        else:
            llm_input_text = text
            is_understanding_correct = False

        if is_understanding_correct is False:

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

        dict = self.get_values(text)
        return [SlotSet(key, value) for key, value in dict.items() if value != "None"]

    def get_text_from_slots(self, tracker: Tracker):
        dict = {}
        for slot in ["emotion", "behaviour", "cause"]:
            dict[slot] = tracker.get_slot(slot)

        return str(dict)

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