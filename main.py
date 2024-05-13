from fastapi import FastAPI, HTTPException
from typing import List
import os
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()

# MongoDB connection
url = os.getenv("ATLAS_URL")
database = os.getenv("DB_NAME")
collection = os.getenv("COLLECTION_NAME")
client = MongoClient(url)
db = client[database]
posts_collection = db[collection]
print("url-->",url)
print("database-->",database)
print("collection-->",collection)

# Post model
class Post(BaseModel):
    title: str
    content: str
    author: str

# Comment model
class Comment(BaseModel):
    text: str
    author: str

# Post class
class BlogPost:
    def __init__(self, title: str, content: str, author: str, comments: List[Comment] = None, likes: int = 0, dislikes: int = 0, id: str = None):
        self.id = id
        self.title = title
        self.content = content
        self.author = author
        self.comments = comments or []
        self.likes = likes
        self.dislikes = dislikes

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "comments": [comment.dict() for comment in self.comments],
            "likes": self.likes,
            "dislikes": self.dislikes
        }

# FastAPI instance
app = FastAPI()

# Create operation
@app.post("/posts/")
async def create_post(post: Post):
    post_obj = BlogPost(**post.dict())
    inserted_post = posts_collection.insert_one(post_obj.to_dict())
    return {"message": "Post created successfully", "post_id": str(inserted_post.inserted_id)}

# Read operation
@app.get("/posts/")
async def read_posts():
    posts = list(posts_collection.find())
    formatted_posts = []
    for post in posts:
        post["_id"] = str(post["_id"])  # Convert ObjectId to string
        formatted_posts.append(post)
    return formatted_posts


# Update operation
@app.put("/posts/{post_id}")
async def update_post(post_id: str, post: Post):
    updated_post = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": post.dict()})
    if updated_post.modified_count == 1:
        return {"message": "Post updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Delete operation
@app.delete("/posts/{post_id}")
async def delete_post(post_id: str):
    deleted_post = posts_collection.delete_one({"_id": ObjectId(post_id)})
    if deleted_post.deleted_count == 1:
        return {"message": "Post deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Comment operation
@app.put("/posts/{post_id}/comments/")
async def create_comment(post_id: str, comment: Comment):
    new_comment = comment.dict()
    updated_post = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$push": {"comments": new_comment}})
    if updated_post.modified_count == 1:
        return {"message": "Comment added successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Like operation
@app.put("/posts/{post_id}/like/")
async def like_post(post_id: str):
    updated_post = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$inc": {"likes": 1}})
    if updated_post.modified_count == 1:
        return {"message": "Post liked successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Dislike operation
@app.put("/posts/{post_id}/dislike/")
async def dislike_post(post_id: str):
    updated_post = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$inc": {"dislikes": 1}})
    if updated_post.modified_count == 1:
        return {"message": "Post disliked successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")