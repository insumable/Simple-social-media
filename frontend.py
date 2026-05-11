import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Simple Social Media", layout="centered")

st.title("Simple Social Media App")

# ----------------------------
# Upload Section
# ----------------------------

st.header("Upload a Post")

caption = st.text_input("Caption")
uploaded_file = st.file_uploader(
    "Choose an image or video",
    type=["png", "jpg", "jpeg", "mp4", "mov"]
)

if st.button("Upload"):
    if uploaded_file is not None:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type
            )
        }

        data = {
            "caption": caption
        }

        response = requests.post(
            f"{BASE_URL}/upload",
            files=files,
            data=data
        )

        if response.status_code == 200:
            st.success("Post uploaded successfully!")
        else:
            st.error(f"Upload failed: {response.text}")

    else:
        st.warning("Please upload a file")


# ----------------------------
# Feed Section
# ----------------------------

st.header("Feed")

refresh = st.button("Refresh Feed")

response = requests.get(f"{BASE_URL}/feed")

if response.status_code == 200:

    posts = response.json().get("posts", [])

    if not posts:
        st.info("No posts yet")

    for post in posts:

        st.divider()

        st.subheader(post.get("caption", ""))

        file_type = post.get("file_type")
        url = post.get("url")

        if file_type == "image":
            st.image(url, use_container_width=True)

        elif file_type == "video":
            st.video(url)

        st.caption(f"Created at: {post.get('created_at')}")

        # Delete button
        if st.button("Delete", key=post["id"]):

            delete_response = requests.delete(
                f"{BASE_URL}/posts/{post['id']}"
            )

            if delete_response.status_code == 200:
                st.success("Post deleted")
                st.rerun()
            else:
                st.error(delete_response.text)

else:
    st.error("Could not fetch feed")

