import os
from dotenv import load_dotenv
from openai import OpenAI
from git import Repo
from pathlib import Path
import shutil
# Web scraping for
from bs4 import BeautifulSoup as Soup

load_dotenv()
client = OpenAI()

PATH_TO_BLOG_REPO = Path("/Users/jinnykim/IdeaProjects/github_website/.git")
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
PATH_TO_CONTENT = PATH_TO_BLOG/"content"

PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

def update_blog(commit_message='Updates blog'):
    #GitPython -- Repo Location
    repo = Repo(PATH_TO_BLOG_REPO)

    #git add .
    repo.git.add(all=True)

    #git commit -m "updates blog"
    repo.index.commit(commit_message)

    #git push origin
    origin = repo.remote(name="origin")
    origin.push()

def create_new_blog(title, content, cover_image):
    cover_image = Path(cover_image)
    files = len(list(PATH_TO_CONTENT.glob("*.html")))
    new_title = f"{files+1}.html"
    path_to_new_content = PATH_TO_CONTENT/new_title

    shutil.copy(cover_image, PATH_TO_CONTENT)

    if not os.path.exists(path_to_new_content):
        # WRITE A NEW HTML FILE
        with open(path_to_new_content, 'w') as f:
            f.write("<!DOCTYPE HTML>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write(f"<title> {title} </title>\n")
            f.write("</head>\n")

            f.write("<body>\n")
            f.write(f"<img src='{cover_image.name}' alt='Cover Image'> <br />\n")
            f.write(f"<h1> {title} </h1>")
            # OpenAI ---> Completion GPT --> "hello\nblog post]\n"
            f.write(content.replace("\n", "<br />\n"))
            f.write("</body>\n")
            f.write("</html>\n")
            print("Blog created")
            return path_to_new_content
    else:
        raise FileExistsError("File already exists, Please check again your name! Aborting!")

def check_for_duplicate_links(path_to_new_content, links):
     urls = [str(link.get("href")) for link in links]   #1.html, 2.html, 3.html...
     content_path = str(Path(*path_to_new_content.parts[-2:]))
     return content_path in urls

def write_to_index(path_to_new_content):
    with open(PATH_TO_BLOG/'index.html') as index:
        soup = Soup(index.read(),features="html.parser")
    # finding a tag
    links = soup.find_all('a')
    # getting the last a tag as soup
    last_link = links[-1]

    if check_for_duplicate_links(path_to_new_content, links):
        raise ValueError("Link already exists!")

    link_to_new_blog = soup.new_tag("a", href=Path(*path_to_new_content.parts[-2:]))
    link_to_new_blog.string = path_to_new_content.name.split('.')[0]
    last_link.insert_after(link_to_new_blog)

    with open(PATH_TO_BLOG/'index.html','w') as f:
        f.write(str(soup.prettify(formatter='html')))


def create_prompt(title):
    prompt="""
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

if __name__ == '__main__':
    title = "The future of Python and AI"

    blog_content = create_content(title)

    path_to_new_content = create_new_blog(title, blog_content, 'logo.png')

    write_to_index(path_to_new_content)

    update_blog()


