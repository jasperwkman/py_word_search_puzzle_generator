
import openai,sys,time,os

openai.api_key = os.getenv('CHATGPT_API_KEY');
if openai.api_key == None:
    exit()

start_after="caution"
start = False
#messages = [
#    {"role": "system", "content": "You are a helpful assistant."},
#    {"role": "user", "content": "Tell me a joke."}
#]

# Open and read the file
with open('word_lists/11 plus 500 words superset ordered.txt', 'r') as file:
    words = file.read().split()
    with open('11 plus 500 words superset sentence.txt', 'a') as sentence:
        for w in words:
            if start or w == start_after:
                start = True
            if start:
                print(w)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"give me a easy sentence include the word '{w}' in 15 words, for kids to learn the word '{w}', "}
                    ]
                )
                assistant_reply = response['choices'][0]['message']['content']
                print("Assistant:", assistant_reply)
                sentence.write(f"{w}|{assistant_reply}\n")
                time.sleep(20)