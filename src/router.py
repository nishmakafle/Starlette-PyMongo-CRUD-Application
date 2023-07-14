from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from .main import homepage, categories, create_category, blogs, create_blog, update_category, delete_category, update_blog, delete_blog


routers = [
    Route('/', homepage),
    Route("/categories", categories, methods=["GET"]),
    Route("/create-category", create_category, methods=["POST"]),
    Route("/update-category/{id}", update_category, methods=["PUT"]),
    Route("/delete-category/{id}", delete_category, methods=["DELETE"]),
    Route("/blogs", blogs, methods=["GET"]),
    Route("/create-blog", create_blog, methods=["POST"]),
    Route("/update-blog/{id}", update_blog, methods=["PUT"]),
    Route("/delete-blog/{id}", delete_blog, methods=["DELETE"])



]

app = Starlette(debug=True, routes=routers)
