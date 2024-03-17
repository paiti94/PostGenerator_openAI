
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import post_util
import openai_util

load_dotenv()
client = OpenAI()

PATH_TO_BLOG_REPO = Path("/Users/jinnykim/IdeaProjects/github_website/.git")
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
PATH_TO_CONTENT = PATH_TO_BLOG/"content"

PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)



if __name__ == '__main__':
    title = "The future of Python and AI"

    blog_content = openai_util.create_content(title)

    path_to_new_content = post_util.create_new_blog(title, blog_content, 'logo.png',PATH_TO_CONTENT)

    post_util.write_to_index(path_to_new_content, PATH_TO_BLOG)

    post_util.update_blog(PATH_TO_BLOG_REPO)


