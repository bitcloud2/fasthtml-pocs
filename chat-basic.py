from fasthtml.common import *
from huggingface_hub import InferenceClient
import os


HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")  # Set this in your environment
if not HUGGINGFACE_API_TOKEN:
    raise ValueError("Please set the HUGGINGFACE_API_TOKEN environment variable. "
                     "Get your token from https://huggingface.co/settings/tokens")

client = InferenceClient(api_key=HUGGINGFACE_API_TOKEN)

sp = "You are a helpful and concise assistant."
messages = [
    { "role": "system", "content": f"{sp}" },
]


def get_inference_response(messages: list[str], system_prompt: str = None) -> str:
    return client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct", 
        messages=messages, 
        max_tokens=2048,
        temperature=0.5,
        top_p=0.7
    ).choices[0].message.content


# Set up the app, including daisyui and tailwind for the chat component
hdrs = (picolink, Script(src="https://cdn.tailwindcss.com"),
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css"))
app = FastHTML(hdrs=hdrs, cls="p-4 max-w-lg mx-auto")

# Chat message component (renders a chat bubble)
def ChatMessage(msg, user):
    bubble_class = "chat-bubble-primary" if user else 'chat-bubble-secondary'
    chat_class = "chat-end" if user else 'chat-start'
    return Div(cls=f"chat {chat_class}")(
               Div('user' if user else 'assistant', cls="chat-header"),
               Div(msg, cls=f"chat-bubble {bubble_class}"),
               Hidden(msg, name="messages")
           )

# The input field for the user message. Also used to clear the
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(name='msg', id='msg-input', placeholder="Type a message",
                 cls="input input-bordered w-full", hx_swap_oob='true')

# The main screen
@app.get
def index():
    page = Form(hx_post=send, hx_target="#chatlist", hx_swap="beforeend")(
           Div(id="chatlist", cls="chat-box h-[73vh] overflow-y-auto"),
               Div(cls="flex space-x-2 mt-2")(
                   Group(ChatInput(), Button("Send", cls="btn btn-primary"))
               )
           )
    return Titled('Chatbot Demo', page)

# Handle the form submission
@app.post
def send(msg:str):
    messages.append({ "role": "user", "content": f"{msg.rstrip()}" })
    r = get_inference_response(messages)
    messages.append({ "role": "assistant", "content": f"{r.rstrip()}" })
    return (ChatMessage(msg, True),
            ChatMessage(r, False),
            ChatInput())

serve(port=8000)
