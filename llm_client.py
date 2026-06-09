from typing import Dict, List
from openai import OpenAI

def generate_response(openai_key: str, user_message: str, context: str, 
                     conversation_history: List[Dict], model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI with context"""

    # TODO: Define system prompt
    # TODO: Set context in messages
    # TODO: Add chat history
    # TODO: Creaet OpenAI Client
    # TODO: Send request to OpenAI
    # TODO: Return response

    system_prompt='You are aassistant who can answer all the project details about  NASA space projects'
    client=OpenAI(api_key='voc-1265197693126677482020869dee0adca8000.90916735',base_url='https://openai.vocareum.com/v1')

    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "system", "content": f"Context: {context}"},
        ]

    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})


    response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.7,
)

    return response.choices[0].message.content