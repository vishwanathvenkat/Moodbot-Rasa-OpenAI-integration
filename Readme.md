# RASA-LLM Integration - Moodbot

## Introduction



This project is a simple example demonstrating how to **enhance RASA's capabilities** by integrating **OpenAI's language models (LLMs)**. We extract relevant details from user-provided paragraphs, a task traditionally achieved using RASA slots and forms, which typically demands extensive training data.

The **key contribution** of this project is the addition of a custom component to RASA's NLU pipeline, allowing users to input **large paragraphs**. The LLMs then extract relevant details without the need for extensive training data. Additionally, **LLM calls are used for response generation**, making OpenAI calls directly from the action server.

**Why a Moodbot?**

The decision to use a `moodbot` for this example is driven by the fact that when users are asked about their feelings, they often prefer to respond with paragraphs rather than short sentences. This scenario serves as an excellent use case for leveraging **Language Models (LLMs)**.



# Flow
![](/media/wizav/DATA/personal-upskill/rasa-openai/moodbot/moodbot-flow.png)


# How to setup
1. Create a virtual environment and install requirements
2. Obtain OpenAI API credentials and add to ~/.bashrc as `OPENAI_API_KEY`=''
3. Repository Installation
```git clone https://github.com/your-username/rasa-openai-integration.git```

#  Output
Once the integration is set up, users can input paragraphs, and the system will leverage OpenAI's language models to extract relevant details. The extracted details can be used for further interaction within the RASA framework.

## Demo


5. Future Enhancements
The current focus of this integration is on the seamless interaction between RASA and OpenAI. Future enhancements may include:

Utilizing vector databases to reduce the number of tokens required for LLM requests.
Improving the efficiency of information extraction.
Exploring additional features and capabilities offered by OpenAI's evolving language models.
Contributions and feedback are welcome to make this integration even more robust and versatile. Feel free to open issues or submit pull requests to contribute to the project's evolution.