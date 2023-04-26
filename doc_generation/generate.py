import os
import openai
import tiktoken
 
openai.api_key = os.getenv("OPENAPI_KEY")

"""
This is a script that demonstrates how to use the Chat API.
You can use this script to chat with the GPT-3 engine.
And generate a conversation with the engine, and save it to a file.
"""
class ChatBot:
    def __init__(self, message):
        self.messages = [
            { "role": "system", "content": message }
        ]
    def chat(self):
        prompt = input("You: ")
         
        self.messages.append(
            { "role": "user", "content": prompt}
        )
         
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = self.messages,
            temperature = 0.2
        )
         
        answer = response.choices[0]['message']['content']
         
        print(answer)
         
        self.messages.append(
           { "role": "assistant", "content": answer} 
        )
 
        tokens = self.num_tokens_from_messages(self.messages)
        print(f"Total tokens: {tokens}")
 
        if tokens > 8000:
            print("WARNING: Number of tokens exceeds 8000. Truncating messages.")
            self.messages = self.messages[2:]

    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo"):
            try:
                encoding = tiktoken.encoding_for_model(model)
            except KeyError:
                encoding = tiktoken.get_encoding("cl100k_base")
            if model == "gpt-3.5-turbo":  # note: future models may deviate from this
                num_tokens = 0
                for message in messages:
                    num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                    for key, value in message.items():
                        num_tokens += len(encoding.encode(value))
                        if key == "name":  # if there's a name, the role is omitted
                            num_tokens += -1  # role is always required and always 1 token
                num_tokens += 2  # every reply is primed with <im_start>assistant
                return num_tokens
            else:
                raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.""")

if __name__ == "__main__":
    bot = ChatBot("You are an assistant that always answers correctly. If not sure, say 'I don't know'.")
    count = 0
    while count < 5:
        bot.chat()
        count += 1
    with open('messages{}.txt'.format(count), 'w') as f:
        for message in bot.messages:
            f.write(message['role'] + ": " + message['content'])