from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from openai import OpenAI
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')



# TODO: Correctly register your component with its type
@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
)
class IssueSummariser(GraphComponent):

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        # TODO: Replace this with config file
        cls.llm_instruction = """

                                                        You are a helpful emotional assistance bot. You read the user's chat and figure out the following.
                                                       1. The emotional state of the user through out the day
                                                       2. The cause of the emotional state. Should be one of self, family or colleagues
                                                       3. How did the person behave when he went through the emotion.


                                                        The response should be in this format
                                                        emotion: {emotion state}
                                                        behaviour: {behavior} 
                                                        cause: {Self, family, colleagues}

                                                        All of the three values should be single word. Not sentences
                                                        If any of the fields are missing, then give "None".
                                                         Do not assume anything if its not explicitly mentioned.

                                                        Additionally, instead of the above text, the user might also affirm or deny a statement. In that case response should be
                                                        is_understanding_correct: True or False. default is False.
                        """
        cls.summariser_client = OpenAI(api_key=api_key, timeout=httpx.Timeout(15.0, read=5.0, write=10.0, connect=3.0))
        cls.model = 'gpt-3.5-turbo-1106'
        cls.temperature = 0.0
        return cls()

    def process(self, messages: List[Message]) -> List[Message]:
        # TODO: This is the method which Rasa Open Source will call during inference.
        for idx, message in enumerate(messages):
            # We can avoid LLM calls for greet and any direct intent which starts with '/' like '/restart'
            if message.get('intent')['name'] != "greet" and '/' not in message.get('text'):
                text = message.get("text")
                response = self.summariser_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.llm_instruction},
                        {"role": "user", "content": text},
                    ],
                    temperature=self.temperature
                )
                metadata = response.choices[0].message.content
                message.set("metadata", metadata, add_to_output=True)
        return messages
