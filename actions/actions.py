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


#
class ActionEnquire(Action):

    def __init__(self):
        super().__init__()
        self.llm_instruction = "You are a mental wellness bot. "\
                               "You greet the user and enquire how their day has been. "\
                               "You ask the user to share their day's update in the form of a paragraph. "\
                                "you ask them to include information on their emotional state, the cause of that emotion, and how they reacted during that situation."

        self.nlg_client = OpenAI()

    def name(self) -> Text:
        return "action_enquire"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = self.nlg_client.chat.completions.create(
            model='gpt-3.5-turbo-1106',
            messages=[
                {"role": "system", "content": self.llm_instruction },
                {"role": "user", "content": "Hello"},
            ],
            temperature=1.8
        )
        message = response.choices[0].message.content
        dispatcher.utter_message(text=message)

        return []


class ActionEmpathise(Action):

    def __init__(self):
        super().__init__()
        self.nlg_client = OpenAI(
        )

    def name(self) -> Text:
        return "action_llm_empathise"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message
        text = message['metadata']


        response = self.nlg_client.chat.completions.create(
            model='gpt-3.5-turbo-1106',
            messages=[
                {"role": "system", "content": "You are a mental wellness bot. "
                                              "You take a string of dictionary with three key values. "
                                              "YOu say something cheerful or consolation based on the "
                                              "values that are filled. You can summarize the details but dont assume assume anything "
                                              "You should prompt the user to fill in the rest of the details "},
                {"role": "user", "content": text},
            ],
            temperature=0.5,
            top_p=0.5
        )
        message = response.choices[0].message.content
        dispatcher.utter_message(text=message)
        dict = self.get_slots(text)
        return [SlotSet(key, value) for key, value in dict.items() if value != "None"]

    def get_slots(self, input):
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