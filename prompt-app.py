import os
import streamlit as st
import json
import pandas as pd
from streamlit_navigation_bar import st_navbar
from data_manager import DataManager
import streamlit as st

# Set page configuration
st.set_page_config(page_title="My Streamlit App", initial_sidebar_state="collapsed")

# Define the absolute path to the JSON file
data_manager = DataManager('data.json')
base_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory where the script is located
data_file = os.path.join(base_dir, 'data.json')

# Function to load data from JSON file
def load_data():
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("File not found, returning empty list.")
        return []  # Return an empty list if the file does not exist
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file: {e}")
        return []  # Return an empty list if the JSON is corrupt

# Function to save data to JSON file
def save_data(data):
    try:
        with open(data_file, 'w') as file:
            json.dump(data, file)
        # Immediately read back and print to verify
        with open(data_file, 'r') as file:
            print("Data immediately after saving:", json.load(file))
    except Exception as e:
        print(f"Error writing or reading file: {e}")

# Add entry and save to file
def add_entry(prompt, effect):
    data = load_data()  # Make sure this function gets the current data
    data.append({'Prompt': prompt, 'Effect': effect})
    save_data(data)  # Save
    st.rerun()

# Custom CSS for DataFrame styling
def custom_css():
    st.markdown(
        """
        <style>
        .dataframe th, .dataframe td {
            font-size: 18px !important;  /* Adjust font size */
            padding: 15px 10px !important; /* Adjust padding */
            text-align: center;
        }
        .dataframe thead th {
            background-color: #4267B2;
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True
        )

def display_data():
    st.title("Home Page")
    data = load_data()
    if data:
        df = pd.DataFrame(data)
        # Convert \n to <br> in HTML for proper display
        df['Prompt'] = df['Prompt'].apply(lambda x: x.replace('\n', '<br>'))
        df['Effect'] = df['Effect'].apply(lambda x: x.replace('\n', '<br>'))
        # Replace double backticks with HTML <code> tags for inline code
        df['Prompt'] = df['Prompt'].apply(lambda x: x.replace('`', '<code>'))
        df['Effect'] = df['Effect'].apply(lambda x: x.replace('`', '<code>'))
        
        html = df.to_html(escape=False, index=False)
        st.markdown(f"""
        <div style="overflow-x: auto; border: 1px solid #ccc;">
            <style>
                table {{
                    width: 100%;
                    table-layout: fixed; /* Ensures that all columns are of equal width */
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                    vertical-align: top;
                    white-space: normal;
                    word-wrap: break-word;
                }}
                thead th {{
                    background-color: #4267B2;
                    color: #ffffff;
                }}
                th, td {{
                    width: 50%; /* Assign equal width to each column */
                }}
                code {{  /* Style for inline code elements */
                    font-family: monospace;
                    background-color: #f4f4f4;
                    padding: 2px 4px;
                    border-radius: 4px;
                }}
            </style>
            {html}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write("No data available.")


# Define the home page
def home():
    custom_css()  # Apply custom CSS for DataFrame styling
    data = load_data()
    #search_query = st.text_input("Search for prompts:")
    display_data()
    # if data:
    #     df = pd.DataFrame(data, columns=['Prompt', 'Effect'])
    #     if search_query:
    #         df = df[df['Prompt'].str.lower().str.contains(search_query.lower())]
    #     if not df.empty:
    #         st.dataframe(df, width=None, height=600, use_container_width=True)  # Customized DataFrame display
    #     else:
    #         st.write("No matching results found.")
    # else:
    #     st.write("No data yet. Add some from the Input page!")


# Define the input page
def input_page():
    st.title("Input Page")
    with st.form("input_form"):
        prompt = st.text_area("Enter the prompt/token:", height=100)
        effect = st.text_area("Enter the expected effect:", height=100)
        submitted = st.form_submit_button("Add")
        if submitted and prompt and effect:
            add_entry(prompt, effect)
            st.success("Entry added successfully!")  # Optional success message

# Navigation bar styling, defined before usage
styles = {
    "nav": {"background-color": "rgb(123, 209, 146)"},
    "div": {"max-width": "10%"},
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(49, 51, 63)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {"background-color": "rgba(255, 255, 255, 0.25)"},
    "hover": {"background-color": "rgba(255, 255, 255, 0.35)"},
}


# Setup navigation
pages = ["Home", "Input"]
page_functions = {
    "Home": home,
    "Input": input_page
}
selected_page = st_navbar(pages, styles=styles)

# Sidebar optional content
with st.sidebar:
    st.write("Sidebar content here")

page_functions[selected_page]()

