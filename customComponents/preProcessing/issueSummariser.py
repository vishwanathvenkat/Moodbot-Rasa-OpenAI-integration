from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from openai import OpenAI


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
        # TODO: Implement this
        ...

    def train(self, training_data: TrainingData) -> Resource:
        # TODO: Implement this if your component requires training
        ...

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        # TODO: Implement this if your component augments the training data with
        #       tokens or message features which are used by other components
        #       during training.
        ...

        return training_data

    def process(self, messages: List[Message]) -> List[Message]:
        # TODO: This is the method which Rasa Open Source will call during inference.
        llm_instruction = """

                                        You are a helpful emotional assistance bot. You read the user's chat and figure out the following.
                                       1. The emotional state of the user through out the day
                                       2. The cause of the emotional state. Should be one of self, family or colleagues
                                       3. How did the person behave when he went through the emotion.


                                        The response should be in this format
                                        1. Emotion: {emotion state}
                                        2. Behaviour: {behavior}
                                        3. Cause: {Self, family, friends}

                                        If any of the fields are missing, then give none. Dont hallucinate
        """
        summariser_client = OpenAI()
        for idx, message in enumerate(messages):
            if message.get('intent')['name'] != "greet"  and '/' not in message.get('text'):
                text = messages[-1].data["text"]
                response = summariser_client.chat.completions.create(
                    model='gpt-3.5-turbo-1106',
                    messages=[
                        {"role": "system", "content": llm_instruction},
                        {"role": "user", "content": text},
                    ],
                    temperature=0.0
                )
                metadata = response.choices[0].message.content
                # assert len(metadata) == 3, "The IssueSummarizer did not return 3 keys"
                message.set("metadata", metadata, add_to_output=True)
        return messages
