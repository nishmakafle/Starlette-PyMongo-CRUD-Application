from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from pydantic import ValidationError, Field
import os
from bson import ObjectId

from db_config import DBWrapper
from .models import Category, Blog
wrapper = DBWrapper("mongodb://db:27017/")



def make_serizable(obj):
     obj['_id'] = str(obj.get('_id'))
     return obj
     


def homepage(request):
    # print(request.url.port)
    return JSONResponse({"message":"Hello, Welcome first Starlette project"})


async def categories(request):
    results = wrapper.find("Blogdb", "Category")
    result = [make_serizable(data) for data in results]
    return JSONResponse(status_code=200, content=result)

async def create_category(request):    
    data = await request.json()
    try:
        result = Category(**data)
    except ValidationError as e:
        return JSONResponse({"error":e.json()})
    result = wrapper.insert_one("Blogdb", "Category", data)
    return JSONResponse({"message": "Category Created Successfully"}, status_code=201)



async def update_category(request):
    id = request.path_params['id']
    data = await request.json()
    try:
        results = Category(**data) 
    except ValidationError as e:
        return JSONResponse({"error": e.json()})
    changed_data = {k:v for k, v in data.items() if v is not None}
    update_report = wrapper.update_one(
            "Blogdb",
            "Category",
            {"_id": ObjectId(id)},
            {"$set": changed_data}
        )
    return JSONResponse({"message": "Data Update Successfully"}, status_code=200)

    

async def delete_category(request):
    id = request.path_params['id']
    obj = ObjectId(id)
    wrapper.delete_one("Blogdb", "Category", {"_id":obj})
    return JSONResponse({"message": "Caategory Deleted Successfully"}, status_code=200)


async def upload_image(image):
    directory = "media/blog"
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    file_path = os.path.join(directory, image.filename)
    if image:
        with open(file_path, "wb") as f:
            content = await image.read()
            f.write(content)
    return file_path



async def create_blog(request):
    data = await request.form()
    ### data validation
    try:
          result = Blog(**data)
    except ValidationError as e:
        return JSONResponse({"error": e.json()})
    
    ### image save in file
    if data.get("image"):
        image = data.get("image")
        file_path = await upload_image(image)        

    ## data preparation 
    
    data={
         "title": data.get("title"),
         "desciption":data.get("description"),
         "image": file_path or None,
         "author":data.get("author"),
         "created_date" : data.get("date")
    }

    wrapper.insert_one("Blogdb","Blog",  data)
    return JSONResponse({"message": "Blog Created Successfully"}, status_code=201)

async def blogs(request):
    result = wrapper.find("Blogdb", "Blog")
    results = [make_serizable(data) for data in result]
    return JSONResponse(status_code=200, content=results)


async def update_blog(request):
    id = request.path_params["id"]
    data = await request.form()
    changed_data = {k:v for k, v in data.items() if v is not None}

    if data.get("image"):
        image = data.get("image")
        file_path = await upload_image(image)
        changed_data["image"] = file_path
    update_blog = wrapper.update_one(
            "Blogdb",
            "Blog",
            {"_id": ObjectId(id)},
            {"$set": changed_data}
        )
    return JSONResponse({"message": "Blog Update Successfully"}, status_code=200)
    




async def delete_blog(request):
    id = request.path_params["id"]
    obj = ObjectId(id)
    wrapper.delete_one("Blogdb", "Blog", {"_id" : obj})
    return JSONResponse({"message": "Blog Deleted Successfully"}, status_code=200)
