import os
from git import Repo
from pathlib import Path
import shutil
# Web Scraping
from bs4 import BeautifulSoup as Soup
def update_blog(path_to_blog_repo, commit_message='Updates blog', ):
    #GitPython -- Repo Location
    repo = Repo(Path(path_to_blog_repo))

    #git add .
    repo.git.add(all=True)

    #git commit -m "updates blog"
    repo.index.commit(commit_message)

    #git push origin
    origin = repo.remote(name="origin")
    origin.push()

def create_new_blog(title, content, cover_image, path_to_content):
    cover_image = Path(cover_image)
    files = len(list(path_to_content.glob("*.html")))
    new_title = f"{files+1}.html"
    path_to_new_content = path_to_content/new_title

    shutil.copy(cover_image, path_to_content)

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

def write_to_index(path_to_new_content, path_to_blog):
    with open(path_to_blog/'index.html') as index:
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

    with open(path_to_blog/'index.html','w') as f:
        f.write(str(soup.prettify(formatter='html')))
