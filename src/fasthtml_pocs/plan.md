# FastHTML Chat Application Plan - Simplified

## Project Setup
- Install FastHTML (`pip install python-fasthtml`)
- Create a single file application (chat.py)

## Simplest Initial Implementation
- Import required FastHTML components
- Set up basic app structure with fast_app(live=True)
- All implementation will be done using fasthtml and htmx attributes
- Do not use async calls in the code.
- Ensure any fasthtml functions for routes have type annotation.
- Note that in FastHTML, form parameters are automatically mapped to function parameters with the same name.
- Note that in FastHTML, HTTP methods are determined by the function name rather than a method parameter in the route decorator.
- Add DaisyUI/Tailwind CSS via CDN to fasthtml app through the hdrs argument during app initializtion.
    - Headers/Script can be structured like this:
    ```python
    headers = (Script(src="https://cdn.tailwindcss.com"),
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css"))
    ```
- Show a single message. Example in html below that will need to be converted to fasthtml:

```html
<div class="chat chat-start">
  <div class="chat-bubble chat-bubble-primary">What kind of nonsense is this</div>
</div>
<div class="chat chat-end">
  <div class="chat-bubble chat-bubble-secondary">Put me on the Council and not make me a Master!??</div>
</div>
```

## Core Chat Functionality
- Create a basic chat interface layout
- Create a simple in-memory list to store chat messages
- Create a form for submitting new messages
    - Note: In FastHTML, form parameters are automatically extracted and passed directly to your route handler functions as named parameters
- Implement a simple message display component
- Implement chat bubbles with two consistent colors:
  - One color for "chat-start" messages (left-aligned)
  - One color for "chat-end" messages (right-aligned)
- Use HTMX attributes for form submissions without page reload
- Display new messages immediately upon submission
- Handle message overflow in the chat with a scroll bar

## Chat with LLM
- Write a inference function to chat with a hosted LLM.
    - Use the httpx library to handle the request/response.
    - IP Address: 0.0.0.0
    - Port number: 8000
    - Example curl command:
```bash
curl -N http://0.0.0.0:8000/v1/chat/completions       -H "Content-Type: application/json"       -d '{
          "model": "Qwen/Qwen2.5-Coder-7B-Instruct",
          "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a quick sort algorithm"}
          ]
      }'
```
- The user message sent should be passed to the inference function.
- The message response from the inference function should added to the messages and displayed in the chat.