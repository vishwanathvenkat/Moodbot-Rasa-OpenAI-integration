# Moodbot: Emotional Analysis and Upliftment Bot
<sub><sup>*This readme was auto-generated using LLM prompts*</sup></sub>
## Introduction
**Moodbot** is an integration utilizing the capabilities of RASA framework alongside the advanced AI processing of LLMs. This bot aims to understand a user's emotional state through their input statement and responds with an uplifting quote fetched online. The demonstration will showcase a newly initiated Rasa project augmented with OPENAI commands replacing the traditional NLU (Natural Language Understanding) and NLG (Natural Language Generation) components. 

The key contribution of this project is the addition of a custom component to RASA's NLU pipeline, allowing users to input large paragraphs. The LLMs then extract relevant details without the need for extensive training data. Additionally, LLM calls are used for response generation, making OpenAI calls directly from the action server.

Note: This functionality can be entirely developed using openai - assistants. However, this is just a demo of the integration capabilities.

## Key contribution

## Pre-requisites

### Setting Up RASA Project

To interact with Moodbot, you need a default RASA setup. Follow these steps to get started:

1. Install Rasa: `pip install rasa`
2. Initiate a new Rasa project: `rasa init`

### Acquiring OPENAI Key

Ensure you have an OPENAI API key. Visit [OPENAI](https://openai.com/api/) to obtain your key if you don’t have one.

## Logic

- **NLU**: Any input other than a standard greeting (like Hi, Hello, etc.) will trigger the fallback path, rerouting the dialogue to OPENAI for understanding.
- **Core**: The sequence of interaction will be determined by RASA's decision-making logic.
- **NLG**: Output generation will
  invoke OPENAI to provide responses, integrated as custom actions in RASA.

## Flow Chart
![](https://github.com/vishwanathvenkat/moodbot/blob/master/moodbot-flow.png)

## LLM Variables

Customize your bot's behavior and interaction patterning through these:

- **Model (LLM Id)**: Defines the AI model you're using.
- **Temperature (0-2)**: Dictates response variability.
- **Instruction**: Contextual commands given to OPENAI.

## Architecture

Moodbot leverages the `RASA server backend` paired with a `Streamlit` frontend for data input interaction. Real-time user entries trigger emotional analysis and subsequent response generation.

## Demo - Click on the image
### Happy path
[![](https://github.com/vishwanathvenkat/moodbot/blob/master/Thumbnail.png)](https://www.youtube.com/watch?v=tSHLao7PYhE&ab_channel=VishwanathVenkat)

### Rogue Path
[![](https://github.com/vishwanathvenkat/moodbot/blob/master/Thumbnail.png)](https://www.youtube.com/watch?v=8gt8v19O9xY&ab_channel=VishwanathVenkat)

### Data missing Path
[![](https://github.com/vishwanathvenkat/moodbot/blob/master/Thumbnail.png)](https://www.youtube.com/watch?v=9KFdWlyAk4U&ab_channel=VishwanathVenkat)


## Future Enhancements

Key aspects pinpointed for improvement:

1. **Integration of Vector Databases**: Aims at relieving the load on LLM requests concerning token counts.
2. **Enhanced Information Extraction**: Prioritizes refining prompt constructions for deeper content understanding.
3. **LM Fine-Tuning**: Emphasizes data probingly based on therapy dialogues to generate more resonant responses.
4. **Exploration of OpenAI Language Models**: Skews towards harnessing evolving features and lactations set forth by OpenAI advancements.

Moodbot showcases the extraordinary interface of RASA with OPENAI, indicating major milestones ahead in emotionally intelligent chatbots.
