import streamlit as st
from pymongo import MongoClient
from PIL import Image
import io
from bson.binary import Binary

client = MongoClient(st.secrets["mongo"]["url"])
db = client["user_database"]
collection = db["users_bson"]

st.set_page_config(page_title="PIT-CRUD", layout="wide")
st.title("Streamlit CRUD operation")

menu = ["Create", "Read", "Update", "Delete"]
choice = st.sidebar.selectbox("Select Action", menu)

def image_binary(image):
    return Binary(image.read())

def binary_image(binary_data):
    return Image.open(io.BytesIO(binary_data))

if choice=="Create":
    st.subheader("--CREATE USERS--")
    name=st.text_input("Name")
    email=st.text_input("Email")
    image=st.file_uploader("Upload images",accept_multiple_files=True,type=['jpg','png','jpeg','pdf'])

    if st.button("Save user"):
        if name and email and image:
            binary=[image_binary(img) for img in image]
            collection.insert_one({"name":name,"email":email,"image":binary})
            st.success("User created successfully")
        else:
            st.error("Please select thsese fields")
        
elif choice=="Read":
    st.subheader("--READ USERS--")
    if st.button("Get data"):
        data_read=list(collection.find())
        if not data_read:
            st.warning("NO users data found!")
        else:
            for user in data_read:
                st.markdown(f"Name : {user['name']} | Emaail : {user['email']}")
                colm = st.columns(4)
                for i,img_get in enumerate(user.get("image",[])):
                    with colm(i%4):
                        st.image(binary_image(img_get), width=150)
            
elif choice=="Update":
    st.subheader("--Update users--")
    data_fetch=list(collection.find())
    names=[u["name"] for u in data_fetch]
    if not data_fetch:
        st.info("firstly insert data using create data button")
    else:
        if names:
            select=st.selectbox("Select user",names)
            new_name=st.text_input("ENTER NAME ")
            new_email=st.text_input("ENTER EMAIL")
            new_image=st.file_uploader("Update images ",accept_multiple_files=True,type=['jpg','jpeg','png','pdf'])
            if st.button("Update"):
                update_data={}
                if new_name and new_email and new_image:
                    update_data['name']=new_name
                    update_data['email']=new_email
                    update_data['image']=[image_binary(img) for img in new_image]
                    if update_data:
                        collection.update_one({"$set": update_data})
                        st.success("User data successfully updated")
                
elif choice=="Delete":
    st.subheader("--DELETE YOUR USER DATA--")
    user_data=list(collection.find())
    dta_name=[u["name"] for u in user_data]
    if dta_name:
        select=st.selectbox("Select user for delete", dta_name)
        if st.button("delete data"):
            collection.delete_one({"name": select})
            st.warning("User data deleted..")



        




                           

