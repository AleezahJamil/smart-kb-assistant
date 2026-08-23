import os
from groq import Groq
from dotenv import load_dotenv
from vector_db import search

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_question(question):
    context_chunks = search(question, top_k=3)
    context = "\n\n".join(context_chunks)

    prompt = f"""You are a friendly AI assistant.

Rules:
- If the user greets you (Hi, Hello, Hey, etc.), greet them naturally.
- If the answer exists in the provided context, answer using the context.
- If the context does not contain the answer, answer using your own general knowledge.
- If the user is chatting normally,behave like ChatGpt

- Be clear, concise,friendly and helpful.

Context:
{context}

Question: {question}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    answer = ask_question("What does the len() function do?")
    print(answer)