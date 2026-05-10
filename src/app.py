from fastapi import FastAPI
app = FastAPI() 


text_posts = {1:{"title": "First Post", "content": "This is the content of the first post."}}


@app.get("/posts")
def read_posts():
    return text_posts