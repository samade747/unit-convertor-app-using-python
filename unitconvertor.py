import streamlit as st
import json
import re
import pint
from currency_converter import CurrencyConverter

# -------------------------------
# Try to import OpenAI (LLM Parser)
# -------------------------------
try:
    import openai
    openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your API key
    LLM_OPENAI_AVAILABLE = True
except ModuleNotFoundError:
    LLM_OPENAI_AVAILABLE = False

# -------------------------------
# Try to import Google Gemini (PaLM API)
# -------------------------------
try:
    import google.generativeai as genai
    GEMINI_API_KEY = "YOUR_GOOGLE_GEMINI_API_KEY"  # Replace with your API key
    genai.configure(api_key=GEMINI_API_KEY)
    LLM_GEMINI_AVAILABLE = True
except ModuleNotFoundError:
    LLM_GEMINI_AVAILABLE = False

# -------------------------------
# Initialize Unit Registry & Currency Converter
# -------------------------------
ureg = pint.UnitRegistry()
ureg.define("celsius = kelvin; offset: 273.15")  # Handling temperature conversion
currency_converter = CurrencyConverter()

# -------------------------------
# Custom CSS for UI Styling
# -------------------------------
st.set_page_config(page_title="UniFlex Converter", layout="wide")

st.markdown(
    """
    <style>
    .header { font-size: 28px; font-weight: bold; text-align: center; padding: 10px; color: #4C7769; margin-bottom: 20px; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { border: 2px solid #ccc; border-radius: 8px; padding: 0.8rem; font-size: 1.1rem; }
    div.stButton > button { background-color: #4CAF50; color: white; border-radius: 8px; padding: 0.8rem 1.2rem; }
    div.stButton > button:hover { background-color: #45a049; }
    .stSelectbox>div>div { border: 2px solid #ccc; border-radius: 8px; padding: 0.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="header">🔄 UniFlex Converter</div>', unsafe_allow_html=True)

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("🌐 **UniFlex Converter**")
st.sidebar.markdown("### Select a category:")

categories = {
    "📏 Length": ["meter", "kilometer", "mile", "yard", "foot", "inch", "centimeter", "millimeter"],
    "⚖️ Weight": ["kilogram", "gram", "pound", "ounce", "ton", "stone"],
    "🌡️ Temperature": ["celsius", "fahrenheit", "kelvin"],
    "🚀 Speed": ["meter/second", "kilometer/hour", "mile/hour", "knot"],
    "⏳ Time": ["second", "minute", "hour", "day", "week", "month", "year"],
    "📐 Area": ["meter ** 2", "kilometer ** 2", "mile ** 2", "yard ** 2", "foot ** 2", "inch ** 2", "hectare", "acre"],
    "🛢️ Volume": ["liter", "milliliter", "gallon", "meter ** 3", "centimeter ** 3"],
    "⚡ Energy": ["joule", "kilojoule", "calorie", "kilocalorie", "watt_hour", "kilowatt_hour"],
    "💾 Digital Storage": ["bit", "byte", "kilobyte", "megabyte", "gigabyte", "terabyte"],
    "💰 Currency": None  # Currency handled separately
}

selected_category = st.sidebar.radio("", list(categories.keys()), index=0)

# -------------------------------
# Conversion Function
# -------------------------------
def convert_units(unit_list):
    input_value = st.number_input("Enter value:", value=1.0)
    from_unit = st.selectbox("From:", unit_list, key="from_unit")
    to_unit = st.selectbox("To:", unit_list, key="to_unit")

    try:
        if selected_category == "🌡️ Temperature":
            result = ureg.Quantity(input_value, ureg(from_unit)).to(ureg(to_unit))
        else:
            result = (input_value * ureg(from_unit)).to(to_unit)

        st.success(f"{input_value} {from_unit} = {result:.4f} {to_unit}")
    except Exception as e:
        st.error(f"Conversion error: {e}")

# -------------------------------
# Currency Converter Function
# -------------------------------
def convert_currency():
    currency_list = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "INR", "CNY"]
    input_value = st.number_input("Enter amount:", value=1.0)
    from_currency = st.selectbox("From:", currency_list, key="from_currency")
    to_currency = st.selectbox("To:", currency_list, key="to_currency")

    try:
        result = currency_converter.convert(input_value, from_currency, to_currency)
        st.success(f"{input_value} {from_currency} = {result:.2f} {to_currency}")
    except Exception as e:
        st.error(f"Currency conversion failed: {e}")

# -------------------------------
# LLM Parser: OpenAI GPT-3.5
# -------------------------------
def parse_conversion_query_openai(query):
    prompt = f"""
    Extract the numeric value, source unit, and target unit from this conversion query.
    Output JSON format: {{"value": 10, "source": "km", "target": "mile"}}
    Query: {query}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return json.loads(response['choices'][0]['message']['content'])
    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# LLM Parser: Google Gemini
# -------------------------------
def parse_conversion_query_gemini(query):
    prompt = f"""
    Extract the numeric value, source unit, and target unit from this conversion query.
    Output JSON format: {{"value": 10, "source": "km", "target": "mile"}}
    Query: {query}
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return json.loads(response.text.strip())
    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# Handle Categories
# -------------------------------
if selected_category in categories and selected_category != "💰 Currency":
    convert_units(categories[selected_category])
elif selected_category == "💰 Currency":
    convert_currency()

st.markdown("---")
st.markdown("Created by ❤️ samade747 using **Streamlit UV** and **Python**")




# import streamlit as st
# import json
# import re
# from pint import UnitRegistry

# # -------------------------------
# # Try to import OpenAI (LLM Parser)
# # -------------------------------
# try:
#     import openai
#     openai.api_key = "YOUR_OPENAI_API_KEY"  
#     LLM_OPENAI_AVAILABLE = True
# except ModuleNotFoundError:
#     LLM_OPENAI_AVAILABLE = False

# # -------------------------------
# # Try to import Google Gemini (PaLM API)
# # -------------------------------
# try:
#     import google.generativeai as genai
#     GEMINI_API_KEY = "AIzaSyBAYvcAK1-FbjHyWhRT36lWd5PmPgezV1Q"  
#     genai.configure(api_key=GEMINI_API_KEY)
#     LLM_GEMINI_AVAILABLE = True
# except ModuleNotFoundError:
#     LLM_GEMINI_AVAILABLE = False

# # -------------------------------
# # Custom CSS for UI Styling
# # -------------------------------
# st.markdown(
#     """
#     <style>
#     .main { background-color: #f0f2f6; padding: 2rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
#     h1, h2, h3, h4, h5, h6 { color: #333; font-weight: 600; }
#     p { color: #555; font-size: 1.1rem; }
#     .stTextInput>div>div>input { border: 2px solid #ccc; border-radius: 8px; padding: 0.8rem; font-size: 1.1rem; }
#     div.stButton > button { background-color: #4CAF50; color: white; border: none; border-radius: 8px; padding: 0.8rem 1.2rem; font-size: 1.1rem; cursor: pointer; }
#     div.stButton > button:hover { background-color: #45a049; }
#     .css-1d391kg { background-color: #ffffff; padding: 1rem; }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # -------------------------------
# # Unit Registry Initialization
# # -------------------------------
# ureg = UnitRegistry()

# # -------------------------------
# # LLM Parser: OpenAI GPT-3.5
# # -------------------------------
# def parse_conversion_query_openai(query):
#     prompt = f"""
#     Extract the numeric value, source unit, and target unit from this conversion query.
#     Output JSON format: {{"value": 10, "source": "km", "target": "mile"}}
#     Query: {query}
#     """
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "system", "content": "Extract conversion details from a query."},
#                       {"role": "user", "content": prompt}],
#             temperature=0
#         )
#         text = response['choices'][0]['message']['content']
#         return json.loads(text)
#     except Exception as e:
#         return {"error": str(e)}

# # -------------------------------
# # LLM Parser: Google Gemini (PaLM API)
# # -------------------------------
# def parse_conversion_query_gemini(query):
#     prompt = f"""
#     Extract the numeric value, source unit, and target unit from this conversion query.
#     Output JSON format: {{"value": 10, "source": "km", "target": "mile"}}
#     Query: {query}
#     """
#     try:
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(prompt)
#         return json.loads(response.text.strip())
#     except Exception as e:
#         return {"error": str(e)}

# # -------------------------------
# # Regex-Based Parser (No LLM)
# # -------------------------------
# def parse_conversion_query_regex(query):
#     pattern = r'(?i)(?:convert\s+)?([-+]?[0-9]*\.?[0-9]+)\s*([a-zA-Z°²³]+)\s+(?:to|in)\s+([a-zA-Z°²³]+)'
#     match = re.search(pattern, query)
#     if match:
#         return {"value": match.group(1), "source": match.group(2), "target": match.group(3)}
#     else:
#         return {"error": "Invalid format. Use 'Convert 10 km to miles'."}

# # -------------------------------
# # Unit Conversion Function
# # -------------------------------
# def convert_units(value, source_unit, target_unit):
#     try:
#         quantity = value * ureg(source_unit)
#         converted = quantity.to(target_unit)
#         return converted.magnitude
#     except Exception as e:
#         return None

# # -------------------------------
# # Unit Converter UI
# # -------------------------------
# def converter_app(conversion_mode, llm_choice):
#     st.markdown('<div class="main">', unsafe_allow_html=True)
#     st.header("🔄 Smart Unit Converter")

#     query = st.text_input("🔍 Enter Conversion Query", "")

#     if st.button("Convert") and query:
#         with st.spinner("Processing..."):
#             if conversion_mode == "LLM Parser":
#                 if llm_choice == "OpenAI GPT-3.5":
#                     if LLM_OPENAI_AVAILABLE:
#                         conversion_details = parse_conversion_query_openai(query)
#                     else:
#                         st.error("OpenAI API is not configured.")
#                         return
#                 elif llm_choice == "Google Gemini":
#                     if LLM_GEMINI_AVAILABLE:
#                         conversion_details = parse_conversion_query_gemini(query)
#                     else:
#                         st.error("Google Gemini API is not configured.")
#                         return
#             else:
#                 conversion_details = parse_conversion_query_regex(query)

#             if "error" in conversion_details:
#                 st.error(conversion_details["error"])
#             else:
#                 value = float(conversion_details["value"])
#                 source_unit = conversion_details["source"]
#                 target_unit = conversion_details["target"]
#                 result = convert_units(value, source_unit, target_unit)

#                 if result is not None:
#                     st.success(f"✅ {value} {source_unit} = {result} {target_unit}")
#                 else:
#                     st.error("❌ Conversion failed. Check the units.")

#     st.markdown('</div>', unsafe_allow_html=True)

# # -------------------------------
# # About Page
# # -------------------------------
# def about_page():
#     st.markdown('<div class="main">', unsafe_allow_html=True)
#     st.header("📌 About This App")
#     st.write(
#         "This **Smart Unit Converter** app is built using **Python, Streamlit, and LLMs (OpenAI/Gemini)**. "
#         "It supports **Length, Temperature, Weight, Time, Area, and more!**"
#     )
#     st.markdown('</div>', unsafe_allow_html=True)

# # -------------------------------
# # Main App Navigation
# # -------------------------------
# def main():
#     st.sidebar.title("🔍 Navigation")
#     page = st.sidebar.radio("📌 Go to", ["Converter", "About"])

#     if page == "Converter":
#         mode = st.sidebar.radio("⚙️ Select Parser", ["LLM Parser", "Regex Parser"])
#         llm_choice = None
#         if mode == "LLM Parser":
#             llm_choice = st.sidebar.radio("🤖 Choose LLM", ["OpenAI GPT-3.5", "Google Gemini"])
#         converter_app(mode, llm_choice)
#     elif page == "About":
#         about_page()

# if __name__ == "__main__":
#     main()






# # import streamlit as st
# # import json
# # import re
# # from pint import UnitRegistry

# # # -------------------------------
# # # Try to import OpenAI (LLM Parser)
# # # -------------------------------
# # try:
# #     import openai
# #     openai.api_key = "AIzaSyBAYvcAK1-FbjHyWhRT36lWd5PmPgezV1Q"  # Replace with your API key for LLM parsing
# #     LLM_AVAILABLE = True
# # except ModuleNotFoundError:
# #     LLM_AVAILABLE = False

# # # -------------------------------
# # # Custom CSS for Enhanced UI
# # # -------------------------------
# # st.markdown(
# #     """
# #     <style>
# #     .main {
# #         background-color: #f0f2f6;
# #         padding: 2rem;
# #         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# #     }
# #     h1, h2, h3, h4, h5, h6 { 
# #         color: #333; 
# #         font-weight: 600; 
# #     }
# #     p { 
# #         color: #555; 
# #         font-size: 1.1rem; 
# #     }
# #     .stTextInput>div>div>input {
# #         border: 2px solid #ccc;
# #         border-radius: 8px;
# #         padding: 0.8rem;
# #         font-size: 1.1rem;
# #     }
# #     div.stButton > button {
# #         background-color: #4CAF50;
# #         color: white;
# #         border: none;
# #         border-radius: 8px;
# #         padding: 0.8rem 1.2rem;
# #         font-size: 1.1rem;
# #         cursor: pointer;
# #     }
# #     div.stButton > button:hover { 
# #         background-color: #45a049; 
# #     }
# #     .css-1d391kg { 
# #         background-color: #ffffff; 
# #         padding: 1rem; 
# #     }
# #     </style>
# #     """,
# #     unsafe_allow_html=True,
# # )

# # # -------------------------------
# # # Configuration & Initialization
# # # -------------------------------
# # ureg = UnitRegistry()  # Supports various unit types like length, temperature, weight, time, area, etc.

# # # -------------------------------
# # # Parser Functions
# # # -------------------------------
# # def parse_conversion_query_llm(query):
# #     """
# #     Uses OpenAI's GPT-3.5-turbo to extract conversion details from a natural language query.
# #     Expected JSON output:
# #       {
# #         "value": 10,
# #         "source": "km",
# #         "target": "mile"
# #       }
# #     """
# #     prompt = (
# #         "Extract the numeric value, the source unit, and the target unit from the following conversion query.\n"
# #         "The query may involve units such as length, temperature, weight, time, area, and others.\n"
# #         "Return the result as a JSON object with keys 'value', 'source', and 'target'.\n"
# #         "For example, if the input is 'Convert 10 km to miles', then return:\n"
# #         '{"value": 10, "source": "km", "target": "mile"}\n'
# #         f"Query: {query}"
# #     )
# #     try:
# #         response = openai.ChatCompletion.create(
# #             model="gpt-3.5-turbo",
# #             messages=[
# #                 {"role": "system", "content": "You are an assistant that extracts conversion details from queries."},
# #                 {"role": "user", "content": prompt}
# #             ],
# #             temperature=0
# #         )
# #         text = response['choices'][0]['message']['content']
# #         data = json.loads(text)
# #         return data
# #     except Exception as e:
# #         return {"error": str(e)}

# # def parse_conversion_query_regex(query):
# #     """
# #     Parses a natural language conversion query using a regular expression.
# #     Supported formats:
# #       - "Convert 10 km to miles"
# #       - "10 km to miles"
# #     Returns a dictionary with keys 'value', 'source', and 'target',
# #     or an 'error' key if parsing fails.
# #     """
# #     pattern = r'(?i)(?:convert\s+)?([-+]?[0-9]*\.?[0-9]+)\s*([a-zA-Z°²³]+)\s+(?:to|in)\s+([a-zA-Z°²³]+)'
# #     match = re.search(pattern, query)
# #     if match:
# #         return {"value": match.group(1), "source": match.group(2), "target": match.group(3)}
# #     else:
# #         return {"error": "Unable to parse the query. Please use a format like 'Convert 10 km to miles'."}

# # # -------------------------------
# # # Conversion Function
# # # -------------------------------
# # def convert_units(value, source_unit, target_unit):
# #     """
# #     Performs the unit conversion using pint.
# #     Returns the converted magnitude or None if the conversion fails.
# #     """
# #     try:
# #         quantity = value * ureg(source_unit)
# #         converted = quantity.to(target_unit)
# #         return converted.magnitude
# #     except Exception as e:
# #         st.error(f"Conversion error: {e}")
# #         return None

# # # -------------------------------
# # # App Pages
# # # -------------------------------
# # def converter_app(conversion_mode):
# #     st.markdown('<div class="main">', unsafe_allow_html=True)
# #     st.header("Smart Unit Converter")
# #     st.write(
# #         """
# #         Enter your conversion query below. Examples:
        
# #         - **Length:** Convert 10 km to miles  
# #         - **Temperature:** Convert 100°F to °C  
# #         - **Weight:** Convert 5 kg to lb  
# #         - **Time:** Convert 2 hours to minutes  
# #         - **Area:** Convert 50 m² to ft²  
        
# #         The converter supports various unit types including length, temperature, weight, time, area, and more.
# #         """
# #     )
    
# #     query = st.text_input("Conversion Query", "")
    
# #     if st.button("Convert") and query:
# #         with st.spinner("Processing your query..."):
# #             # Choose parser based on selected mode
# #             if conversion_mode == "LLM Parser":
# #                 if LLM_AVAILABLE:
# #                     conversion_details = parse_conversion_query_llm(query)
# #                 else:
# #                     st.error("LLM Parser is not available because the openai module is not installed.")
# #                     return
# #             else:
# #                 conversion_details = parse_conversion_query_regex(query)
            
# #             if "error" in conversion_details:
# #                 st.error(conversion_details["error"])
# #             else:
# #                 value = conversion_details.get("value")
# #                 source_unit = conversion_details.get("source")
# #                 target_unit = conversion_details.get("target")
# #                 if value is None or source_unit is None or target_unit is None:
# #                     st.error("Could not extract conversion details. Please try a different query.")
# #                 else:
# #                     try:
# #                         value = float(value)
# #                         result = convert_units(value, source_unit, target_unit)
# #                         if result is not None:
# #                             st.success(f"{value} {source_unit} = {result} {target_unit}")
# #                         else:
# #                             st.error("Conversion failed. Please check the provided units.")
# #                     except ValueError:
# #                         st.error("Invalid numeric value provided in the query.")
# #     st.markdown('</div>', unsafe_allow_html=True)

# # def about_page():
# #     st.markdown('<div class="main">', unsafe_allow_html=True)
# #     st.header("About This App")
# #     st.write(
# #         """
# #         This Smart Unit Converter app is built using Python and Streamlit. It supports conversions for various unit types 
# #         including length, temperature, weight, time, area, and more using the 'pint' library.
        
# #         The app provides two options for parsing the conversion query:
        
# #         1. **LLM Parser:** Uses OpenAI's GPT-3.5-turbo to extract conversion details from a natural language query.
# #         2. **Regex Parser:** Uses a regular expression to parse the query without external API calls.
        
# #         Use the sidebar navigation to select your desired parser and switch between the Converter and this About page.
# #         """
# #     )
# #     st.markdown('</div>', unsafe_allow_html=True)

# # # -------------------------------
# # # Main App
# # # -------------------------------
# # def main():
# #     st.sidebar.title("Navigation")
# #     page = st.sidebar.radio("Go to", ["Converter", "About"])
    
# #     if page == "Converter":
# #         mode = st.sidebar.radio("Select Parser", ["LLM Parser", "Regex Parser"])
# #         converter_app(mode)
# #     elif page == "About":
# #         about_page()

# # if __name__ == "__main__":
# #     main()



# # # import streamlit as st
# # # import openai
# # # import json
# # # import re
# # # from pint import UnitRegistry

# # # # -------------------------------
# # # # Custom CSS for Enhanced UI
# # # # -------------------------------
# # # st.markdown(
# # #     """
# # #     <style>
# # #     /* Main container styling */
# # #     .main {
# # #         background-color: #f0f2f6;
# # #         padding: 2rem;
# # #         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
# # #     }
# # #     /* Header styling */
# # #     h1, h2, h3, h4, h5, h6 {
# # #         color: #333;
# # #         font-weight: 600;
# # #     }
# # #     /* Paragraph styling */
# # #     p {
# # #         color: #555;
# # #         font-size: 1.1rem;
# # #     }
# # #     /* Text input styling */
# # #     .stTextInput>div>div>input {
# # #         border: 2px solid #ccc;
# # #         border-radius: 8px;
# # #         padding: 0.8rem;
# # #         font-size: 1.1rem;
# # #     }
# # #     /* Button styling */
# # #     div.stButton > button {
# # #         background-color: #4CAF50;
# # #         color: white;
# # #         border: none;
# # #         border-radius: 8px;
# # #         padding: 0.8rem 1.2rem;
# # #         font-size: 1.1rem;
# # #         cursor: pointer;
# # #     }
# # #     div.stButton > button:hover {
# # #         background-color: #45a049;
# # #     }
# # #     /* Sidebar styling */
# # #     .css-1d391kg { 
# # #         background-color: #ffffff;
# # #         padding: 1rem;
# # #     }
# # #     </style>
# # #     """,
# # #     unsafe_allow_html=True,
# # # )

# # # # -------------------------------
# # # # Configuration & Initialization
# # # # -------------------------------

# # # # Set your OpenAI API key (only needed for the LLM parser)
# # # openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual API key if using LLM parsing

# # # # Initialize the pint unit registry (supports length, temperature, weight, time, area, etc.)
# # # ureg = UnitRegistry()

# # # # -------------------------------
# # # # Parser Functions
# # # # -------------------------------

# # # def parse_conversion_query_llm(query):
# # #     """
# # #     Uses OpenAI's GPT-3.5-turbo to extract conversion details from a natural language query.
# # #     Expected JSON output:
# # #       {
# # #         "value": 10,
# # #         "source": "km",
# # #         "target": "mile"
# # #       }
# # #     """
# # #     prompt = (
# # #         "Extract the numeric value, the source unit, and the target unit from the following conversion query.\n"
# # #         "The query may involve units such as length, temperature, weight, time, area, and others.\n"
# # #         "Return the result as a JSON object with keys 'value', 'source', and 'target'.\n"
# # #         "For example, if the input is 'Convert 10 km to miles', then return:\n"
# # #         '{"value": 10, "source": "km", "target": "mile"}\n'
# # #         f"Query: {query}"
# # #     )
# # #     try:
# # #         response = openai.ChatCompletion.create(
# # #             model="gpt-3.5-turbo",
# # #             messages=[
# # #                 {"role": "system", "content": "You are an assistant that extracts conversion details from queries."},
# # #                 {"role": "user", "content": prompt}
# # #             ],
# # #             temperature=0
# # #         )
# # #         text = response['choices'][0]['message']['content']
# # #         data = json.loads(text)
# # #         return data
# # #     except Exception as e:
# # #         return {"error": str(e)}

# # # def parse_conversion_query_regex(query):
# # #     """
# # #     Parses a natural language conversion query using a regular expression.
# # #     Supported formats:
# # #       - "Convert 10 km to miles"
# # #       - "10 km to miles"
      
# # #     Returns a dictionary with keys 'value', 'source', and 'target',
# # #     or an 'error' key if parsing fails.
# # #     """
# # #     pattern = r'(?i)(?:convert\s+)?([-+]?[0-9]*\.?[0-9]+)\s*([a-zA-Z°²³]+)\s+(?:to|in)\s+([a-zA-Z°²³]+)'
# # #     match = re.search(pattern, query)
# # #     if match:
# # #         return {"value": match.group(1), "source": match.group(2), "target": match.group(3)}
# # #     else:
# # #         return {"error": "Unable to parse the query. Please use a format like 'Convert 10 km to miles'."}

# # # # -------------------------------
# # # # Conversion Function
# # # # -------------------------------

# # # def convert_units(value, source_unit, target_unit):
# # #     """
# # #     Performs the unit conversion using the pint library.
# # #     Returns the converted magnitude or None if the conversion fails.
# # #     """
# # #     try:
# # #         quantity = value * ureg(source_unit)
# # #         converted = quantity.to(target_unit)
# # #         return converted.magnitude
# # #     except Exception as e:
# # #         st.error(f"Conversion error: {e}")
# # #         return None

# # # # -------------------------------
# # # # App Pages
# # # # -------------------------------

# # # def converter_app(conversion_mode):
# # #     st.markdown('<div class="main">', unsafe_allow_html=True)
# # #     st.header("Smart Unit Converter")
# # #     st.write(
# # #         """
# # #         Enter your conversion query below. Examples:
        
# # #         - **Length:** Convert 10 km to miles  
# # #         - **Temperature:** Convert 100°F to °C  
# # #         - **Weight:** Convert 5 kg to lb  
# # #         - **Time:** Convert 2 hours to minutes  
# # #         - **Area:** Convert 50 m² to ft²  

# # #         The converter supports various unit types including length, temperature, weight, time, area, and more.
# # #         """
# # #     )
    
# # #     query = st.text_input("Conversion Query", "")
    
# # #     if st.button("Convert") and query:
# # #         with st.spinner("Processing your query..."):
# # #             # Choose parser based on selected mode
# # #             if conversion_mode == "LLM Parser":
# # #                 conversion_details = parse_conversion_query_llm(query)
# # #             else:
# # #                 conversion_details = parse_conversion_query_regex(query)
            
# # #             # Check if parsing was successful
# # #             if "error" in conversion_details:
# # #                 st.error(conversion_details["error"])
# # #             else:
# # #                 value = conversion_details.get("value")
# # #                 source_unit = conversion_details.get("source")
# # #                 target_unit = conversion_details.get("target")
# # #                 if value is None or source_unit is None or target_unit is None:
# # #                     st.error("Could not extract conversion details. Please try a different query.")
# # #                 else:
# # #                     try:
# # #                         value = float(value)
# # #                         result = convert_units(value, source_unit, target_unit)
# # #                         if result is not None:
# # #                             st.success(f"{value} {source_unit} = {result} {target_unit}")
# # #                         else:
# # #                             st.error("Conversion failed. Please check the provided units.")
# # #                     except ValueError:
# # #                         st.error("Invalid numeric value provided in the query.")
# # #     st.markdown('</div>', unsafe_allow_html=True)

# # # def about_page():
# # #     st.markdown('<div class="main">', unsafe_allow_html=True)
# # #     st.header("About This App")
# # #     st.write(
# # #         """
# # #         This Smart Unit Converter app is built using Python and Streamlit. It supports conversions for various unit types 
# # #         including length, temperature, weight, time, area, and more using the 'pint' library.
        
# # #         The app provides two options for parsing the conversion query:
        
# # #         1. **LLM Parser:** Uses OpenAI's GPT-3.5-turbo to extract conversion details from a natural language query.
# # #         2. **Regex Parser:** Uses a regular expression to parse the query without external API calls.
        
# # #         Use the sidebar navigation to select your desired parser and switch between the Converter and this About page.
# # #         """
# # #     )
# # #     st.markdown('</div>', unsafe_allow_html=True)

# # # # -------------------------------
# # # # Main App
# # # # -------------------------------

# # # def main():
# # #     # Sidebar navigation
# # #     st.sidebar.title("Navigation")
# # #     page = st.sidebar.radio("Go to", ["Converter", "About"])
    
# # #     if page == "Converter":
# # #         # Choose conversion parser mode
# # #         mode = st.sidebar.radio("Select Parser", ["LLM Parser", "Regex Parser"])
# # #         converter_app(mode)
# # #     elif page == "About":
# # #         about_page()

# # # if __name__ == "__main__":
# # #     main()
