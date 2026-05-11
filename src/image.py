from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv()

imagekit = ImageKit(
    public_key=os.getenv("IMAGEKIT-PUBLIC-KEY"),
    private_key=os.getenv("IMAGEKIT-PRIVATE-KEY"),
    url_endpoint=os.getenv("IMAGEKIT-URL-ENDPOINT")
)

