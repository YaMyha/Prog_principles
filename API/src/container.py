import logging

from db.services.post_service import PostService
from db.services.user_services import UserService

# Services
user_service = UserService()
post_service = PostService()

# Logging
logging.basicConfig(filename="myapp.log", level=logging.INFO)

