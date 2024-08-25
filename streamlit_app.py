import streamlit as st
import requests
import json

def process_data(data):
    # Send a POST request to the backend API
    url = "http://your-api-url.com/endpoint"  # Replace with your backend API URL
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the response data
        response_data = response.json()
        return response_data
    else:
        return {"error": "Failed to process the data"}

def render_response(response_data, selected_option):
    if "error" in response_data:
        st.error(response_data["error"])
    else:
        st.success("Data processed successfully!")

        # Render the response based on the selected option
        if selected_option == "Alphabets & Numbers":
            if "alphabets_numbers" in response_data:
                result = response_data["alphabets_numbers"]
                st.write("Alphabets and Numbers:")
                for item in result:
                    st.write(f"- {item}")
            else:
                st.write("No data found for Alphabets and Numbers.")
        elif selected_option == "Symbols":
            if "symbols" in response_data:
                result = response_data["symbols"]
                st.write("Symbols:")
                for item in result:
                    st.write(f"- {item}")
            else:
                st.write("No data found for Symbols.")
        # Add more options as needed

def main():
    st.set_page_config(page_title="21BCE5542")

    # Set background color
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

    # Header
    st.header("Bajaj Finserv Health Challenge: By Aastha Tiwari")

    # Big Title
    st.markdown("<h1 style='text-align: center; color: red;'>21BCE5542</h1>", unsafe_allow_html=True)

    # Get user input
    input_data = st.text_area("Enter JSON data", placeholder='{"data": ["A", "C", "z"]}')

    # Create a dropdown for selecting the option
    options = ["Alphabets & Numbers", "Symbols"]
    selected_option = st.selectbox("Select an option", options)

    if st.button("Process Data"):
        # Parse the input JSON
        try:
            data = json.loads(input_data)
        except json.JSONDecodeError:
            st.error("Invalid JSON format")
            return

        # Process the data
        response = process_data(data)

        # Render the response based on the selected option
        render_response(response, selected_option)

if __name__ == "__main__":
    main()
