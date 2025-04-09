import os
from mistralai import Mistral

api_key = "6rJnvjrYHYNMR9yrWHT3u5o7AJjIRUPd"

client = Mistral(api_key=api_key)

chat_response = client.agents.complete(
    agent_id="ag:d6a2a39e:20250408:thriverflow-agent:70d068e5",
    messages=[
        {
            "role": "user",
            "content": "J'ai une idée sur la mise en place d'un système de motivation pour les étudiants?",
        },
    ],
)
print(chat_response.choices[0].message.content)
