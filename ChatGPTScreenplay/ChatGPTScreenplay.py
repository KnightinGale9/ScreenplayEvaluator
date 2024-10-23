from openai import OpenAI


class ChatGPT:
    def __init__(self):
        # Setting the API key to use the OpenAI API
        self.messages=[
        {
            "role": "system",
            "content": "You are a screenwriter's assistant. Your task is to generate screenplay scenes in the following format: \
            1. Scene heading: INT./EXT. LOCATION - TIME OF DAY \
            2. Action: Describes what is happening in the scene. \
            3. Character: The name of the person speaking, in all caps. \
            4. Dialogue: What the character says. \
            5. Parentheticals: If necessary, to describe how the dialogue is delivered. \
            6. Transition: If needed, include transitions like 'CUT TO:' or 'FADE OUT:' at the end of the scene."
        }    ]
    def chat(self, input):
        self.messages.append({"role": "user", "content": input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.2
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response["choices"][0]["message"]