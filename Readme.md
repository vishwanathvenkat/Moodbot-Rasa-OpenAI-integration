# RASA-LLM Integration - Moodbot

## Introduction



This project is a simple example demonstrating how to **enhance RASA's capabilities** by integrating **OpenAI's language models (LLMs)**. We extract relevant details from user-provided paragraphs, a task traditionally achieved using RASA slots and forms, which typically demands extensive training data.

The **key contribution** of this project is the addition of a custom component to RASA's NLU pipeline, allowing users to input **large paragraphs**. The LLMs then extract relevant details without the need for extensive training data. Additionally, **LLM calls are used for response generation**, making OpenAI calls directly from the action server.

**Why a Moodbot?**

The decision to use a `moodbot` for this example is driven by the fact that when users are asked about their feelings, they often prefer to respond with paragraphs rather than short sentences. This scenario serves as an excellent use case for leveraging **Language Models (LLMs)**.



# Flow
![](/home/wizav/Downloads/moodbot-flow.png)


# How to Setup
To set up and use this integration, follow these steps:

# Prerequisites:
Ensure you have a working RASA installation.
Obtain OpenAI API credentials and replace the placeholder in the configuration file.
Installation:
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/rasa-openai-integration.git
cd rasa-openai-integration
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure OpenAI API credentials:

Replace the placeholder in config.yml with your OpenAI API key.

Run RASA:

bash
Copy code
rasa train
rasa shell
Now, your RASA instance is set up with the OpenAI integration, ready to process user inputs.

#  Output
Once the integration is set up, users can input paragraphs, and the system will leverage OpenAI's language models to extract relevant details. The extracted details can be used for further interaction within the RASA framework.

Example:

User Input: "I recently visited Paris, and the Eiffel Tower was amazing!"
Extracted Details: {"Location": "Paris", "Attraction": "Eiffel Tower"}
5. Future Enhancements
The current focus of this integration is on the seamless interaction between RASA and OpenAI. Future enhancements may include:

Utilizing vector databases to reduce the number of tokens required for LLM requests.
Improving the efficiency of information extraction.
Exploring additional features and capabilities offered by OpenAI's evolving language models.
Contributions and feedback are welcome to make this integration even more robust and versatile. Feel free to open issues or submit pull requests to contribute to the project's evolution.