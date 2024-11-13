import openai

class ChatGPT:
    def __init__(self):
        # Setting the API key to use the OpenAI API
        openai.api_key = skey
        self.messages=[
        {
            "role": "system",
            "content": "You are a screenwriter's assistant. \
            Format the screenplay so it would be in the left justified of the page. \
            Your task is to generate screenplay scenes that include the following: \
            1. Scene heading: INT./EXT. LOCATION - TIME OF DAY.\
            2. Action: Use descriptive paragraphs to set up the scene, location, and environment. Use short and visual description to set up the scene and enviorment. \
            3. Character: The name of the person speaking, in all caps. \
            4. Dialogue: What the character says. \
            5. Parentheticals: If necessary, to describe how the dialogue is delivered."
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

total=100
content=ChatGPT()
story=[]
firstprompt  = "Write the beginning long and creative scene of screenplay in the adventure genre. "


out= content.chat(firstprompt)
story.append(out["content"])
for i in range(2,total):
    current=i
    continuepromt = f"Use the information from the previous scene and write the next scene of a screenplay. " \
                    f"Make the scene kong and creative. This is scene {current} of {total} "
    print(continuepromt)
    out= content.chat(continuepromt)
    story.append(out["content"])

lastprompt = "Use the information from the previous scene and write the last scene of a long and creative screenplay. "
out= content.chat(lastprompt)
story.append(out["content"])

with open('example43full.txt', 'w') as file:
    for info in story:
        file.write(info)
        file.write("\n\n")