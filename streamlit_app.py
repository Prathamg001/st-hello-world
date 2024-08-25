import streamlit as st
import requests
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from threading import Thread

# FastAPI application
app = FastAPI()

# Allow CORS for all origins (so that Streamlit can interact with FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/bfhl")
async def get_operation_code():
    response = {
        "operation_code": 1
    }
    return response

@app.post("/process-data")
async def process_request(request: Request):
    body = await request.json()

    # Extract the required data from the request body
    user_id = body.get("user_id", "")
    college_email = body.get("college_email", "")
    college_roll_number = body.get("college_roll_number", "")
    numbers = body.get("numbers", [])
    alphabets = body.get("alphabets", [])

    # Find the highest lowercase alphabet
    lowercase_alphabets = [char for char in alphabets if char.islower()]
    highest_lowercase_alphabet = max(lowercase_alphabets) if lowercase_alphabets else ""

    # Prepare the response
    response = {
        "status": "success",
        "user_id": user_id,
        "college_email": college_email,
        "college_roll_number": college_roll_number,
        "numbers": numbers,
        "alphabets": alphabets,
        "highest_lowercase_alphabet": highest_lowercase_alphabet
    }

    return response

# Function to run FastAPI in a separate thread
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Streamlit application
def process_data(data):
    url = "http://localhost:8000/process-data"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        return {"error": "Failed to process the data"}

def render_response(response_data, selected_option):
    if "error" in response_data:
        st.error(response_data["error"])
    else:
        st.success("Data processed successfully!")

        if selected_option == "Alphabets & Numbers":
            if "alphabets" in response_data and "numbers" in response_data:
                alphabets = response_data["alphabets"]
                numbers = response_data["numbers"]
                st.write("Alphabets and Numbers:")
                st.write(f"Alphabets: {', '.join(alphabets)}")
                st.write(f"Numbers: {', '.join(map(str, numbers))}")
            else:
                st.write("No data found for Alphabets and Numbers.")
        elif selected_option == "Symbols":
            st.write("No Symbols option implemented.")
        # Add more options as needed

def main():
    st.set_page_config(page_title="21BCE1966")

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #D3D3D3;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.header("Bajaj Finserv Health Challenge: By Pratham Gupta")
    st.markdown("<h1 style='text-align: center; color: red;'>21BCE1966</h1>", unsafe_allow_html=True)

    input_data = st.text_area("Enter JSON data", placeholder='{"user_id": "21BCE1966", "college_email": "abc@example.com", "college_roll_number": "21BCE1966", "numbers": [1, 2, 3], "alphabets": ["A", "C", "z"]}')

    options = ["Alphabets & Numbers", "Symbols"]
    selected_option = st.selectbox("Select an option", options)

    if st.button("Process Data"):
        try:
            data = json.loads(input_data)
        except json.JSONDecodeError:
            st.error("Invalid JSON format")
            return

        response = process_data(data)
        render_response(response, selected_option)

if __name__ == "__main__":
    # Run FastAPI in a separate thread
    fastapi_thread = Thread(target=run_fastapi)
    fastapi_thread.daemon = True
    fastapi_thread.start()

    # Run Streamlit application
    main()
