from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def create_prompt(title):
    prompt = """
    Biography:
    My name is Jinny and I am a Python student for coding.

    Blog
    Title: {}
    tags: tech, python, coding, AI, machine learning
    Summary: I talk about what the future of AI could hold for python
    Full Text: 
    """.format(title)
    return prompt


def create_content(title):
    prompt = create_prompt(title)
    response = client.completions.create(model='davinci-002',
                                         prompt=prompt,
                                         max_tokens=256,
                                         temperature=0.7)
    blog_content = response.choices[0].text
    return blog_content
