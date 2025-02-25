import streamlit as st
import openai
import json
import re
from pint import UnitRegistry

# -------------------------------
# Custom CSS for Enhanced UI
# -------------------------------
st.markdown(
    """
    <style>
    /* Main container styling */
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #333;
        font-weight: 600;
    }
    /* Paragraph styling */
    p {
        color: #555;
        font-size: 1.1rem;
    }
    /* Text input styling */
    .stTextInput>div>div>input {
        border: 2px solid #ccc;
        border-radius: 8px;
        padding: 0.8rem;
        font-size: 1.1rem;
    }
    /* Button styling */
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        font-size: 1.1rem;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: #45a049;
    }
    /* Sidebar styling */
    .css-1d391kg { 
        background-color: #ffffff;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# Configuration & Initialization
# -------------------------------

# Set your OpenAI API key (only needed for the LLM parser)
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual API key if using LLM parsing

# Initialize the pint unit registry (supports length, temperature, weight, time, area, etc.)
ureg = UnitRegistry()

# -------------------------------
# Parser Functions
# -------------------------------

def parse_conversion_query_llm(query):
    """
    Uses OpenAI's GPT-3.5-turbo to extract conversion details from a natural language query.
    Expected JSON output:
      {
        "value": 10,
        "source": "km",
        "target": "mile"
      }
    """
    prompt = (
        "Extract the numeric value, the source unit, and the target unit from the following conversion query.\n"
        "The query may involve units such as length, temperature, weight, time, area, and others.\n"
        "Return the result as a JSON object with keys 'value', 'source', and 'target'.\n"
        "For example, if the input is 'Convert 10 km to miles', then return:\n"
        '{"value": 10, "source": "km", "target": "mile"}\n'
        f"Query: {query}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts conversion details from queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        text = response['choices'][0]['message']['content']
        data = json.loads(text)
        return data
    except Exception as e:
        return {"error": str(e)}

def parse_conversion_query_regex(query):
    """
    Parses a natural language conversion query using a regular expression.
    Supported formats:
      - "Convert 10 km to miles"
      - "10 km to miles"
      
    Returns a dictionary with keys 'value', 'source', and 'target',
    or an 'error' key if parsing fails.
    """
    pattern = r'(?i)(?:convert\s+)?([-+]?[0-9]*\.?[0-9]+)\s*([a-zA-Z°²³]+)\s+(?:to|in)\s+([a-zA-Z°²³]+)'
    match = re.search(pattern, query)
    if match:
        return {"value": match.group(1), "source": match.group(2), "target": match.group(3)}
    else:
        return {"error": "Unable to parse the query. Please use a format like 'Convert 10 km to miles'."}

# -------------------------------
# Conversion Function
# -------------------------------

def convert_units(value, source_unit, target_unit):
    """
    Performs the unit conversion using the pint library.
    Returns the converted magnitude or None if the conversion fails.
    """
    try:
        quantity = value * ureg(source_unit)
        converted = quantity.to(target_unit)
        return converted.magnitude
    except Exception as e:
        st.error(f"Conversion error: {e}")
        return None

# -------------------------------
# App Pages
# -------------------------------

def converter_app(conversion_mode):
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.header("Smart Unit Converter")
    st.write(
        """
        Enter your conversion query below. Examples:
        
        - **Length:** Convert 10 km to miles  
        - **Temperature:** Convert 100°F to °C  
        - **Weight:** Convert 5 kg to lb  
        - **Time:** Convert 2 hours to minutes  
        - **Area:** Convert 50 m² to ft²  

        The converter supports various unit types including length, temperature, weight, time, area, and more.
        """
    )
    
    query = st.text_input("Conversion Query", "")
    
    if st.button("Convert") and query:
        with st.spinner("Processing your query..."):
            # Choose parser based on selected mode
            if conversion_mode == "LLM Parser":
                conversion_details = parse_conversion_query_llm(query)
            else:
                conversion_details = parse_conversion_query_regex(query)
            
            # Check if parsing was successful
            if "error" in conversion_details:
                st.error(conversion_details["error"])
            else:
                value = conversion_details.get("value")
                source_unit = conversion_details.get("source")
                target_unit = conversion_details.get("target")
                if value is None or source_unit is None or target_unit is None:
                    st.error("Could not extract conversion details. Please try a different query.")
                else:
                    try:
                        value = float(value)
                        result = convert_units(value, source_unit, target_unit)
                        if result is not None:
                            st.success(f"{value} {source_unit} = {result} {target_unit}")
                        else:
                            st.error("Conversion failed. Please check the provided units.")
                    except ValueError:
                        st.error("Invalid numeric value provided in the query.")
    st.markdown('</div>', unsafe_allow_html=True)

def about_page():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.header("About This App")
    st.write(
        """
        This Smart Unit Converter app is built using Python and Streamlit. It supports conversions for various unit types 
        including length, temperature, weight, time, area, and more using the 'pint' library.
        
        The app provides two options for parsing the conversion query:
        
        1. **LLM Parser:** Uses OpenAI's GPT-3.5-turbo to extract conversion details from a natural language query.
        2. **Regex Parser:** Uses a regular expression to parse the query without external API calls.
        
        Use the sidebar navigation to select your desired parser and switch between the Converter and this About page.
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Main App
# -------------------------------

def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Converter", "About"])
    
    if page == "Converter":
        # Choose conversion parser mode
        mode = st.sidebar.radio("Select Parser", ["LLM Parser", "Regex Parser"])
        converter_app(mode)
    elif page == "About":
        about_page()

if __name__ == "__main__":
    main()
