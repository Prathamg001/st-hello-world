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
    data = body.get("data", [])

    # Categorize data into alphabets, numbers, and symbols
    numbers = [item for item in data if item.isdigit()]
    alphabets = [item for item in data if item.isalpha()]
    symbols = [item for item in data if not item.isalnum()]

    # Find the highest lowercase alphabet
    lowercase_alphabets = [char for char in alphabets if char.islower()]
    highest_lowercase_alphabet = max(lowercase_alphabets) if lowercase_alphabets else ""

    # Prepare the response
    response = {
        "status": "success",
        "numbers": numbers,
        "alphabets": alphabets,
        "symbols": symbols,
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
            alphabets = response_data.get("alphabets", [])
            numbers = response_data.get("numbers", [])
            st.write("Alphabets and Numbers:")
            st.write(f"Alphabets: {', '.join(alphabets)}")
            st.write(f"Numbers: {', '.join(map(str, numbers))}")
        elif selected_option == "Symbols":
            symbols = response_data.get("symbols", [])
            st.write("Symbols:")
            st.write(f"Symbols: {', '.join(symbols)}")

        # Display the highest lowercase alphabet
        highest_lowercase = response_data.get("highest_lowercase_alphabet", "")
        if highest_lowercase:
            st.write(f"Highest Lowercase Alphabet: {highest_lowercase}")

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

    input_data = st.text_area("Enter JSON data", placeholder='{"data": ["A", "C", "Z", "c", "i"]}')

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
