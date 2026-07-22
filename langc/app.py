import streamlit as st
import json
import pandas as pd
import os
import requests
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import (
    CommaSeparatedListOutputParser,
    PydanticOutputParser,
    JsonOutputParser
)
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
from pydantic import BaseModel, Field

# Load API Key from .env
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

# ---------------------------------------------------------------------------
# Custom Chat Model for OpenRouter API
# ---------------------------------------------------------------------------
class OpenRouterChat(BaseChatModel):
    model_name: str = "openrouter/free"
    openai_api_key: str = ""
    openai_api_base: str = "https://openrouter.ai/api/v1"
    temperature: float = 0.0

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        formatted_messages = []
        for m in messages:
            role = "user"
            if m.type == "system":
                role = "system"
            elif m.type == "ai":
                role = "assistant"
            formatted_messages.append({"role": role, "content": m.content})
            
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model_name,
            "messages": formatted_messages,
            "temperature": self.temperature
        }
        
        response = requests.post(
            f"{self.openai_api_base}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        res_data = response.json()
        
        text = res_data["choices"][0]["message"]["content"]
        ai_message = AIMessage(content=text)
        return ChatResult(generations=[ChatGeneration(message=ai_message)])

    @property
    def _llm_type(self) -> str:
        return "openrouter-chat"


# App Config
st.set_page_config(
    page_title="LangChain Output Parsers Playground",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .reportview-container {
        background: #0f1116;
    }
    .main-title {
        font-family: 'Outfit', sans-serif;
        color: #1E88E5;
        font-weight: 700;
    }
    .parser-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# App Title & Description
st.markdown("<h1 class='main-title'>🧩 LangChain Output Parsers Playground</h1>", unsafe_allow_html=True)
st.write("Large Language Models (LLMs) output plain strings. Output Parsers convert those strings into structured Python objects like lists, dictionaries, or Pydantic models.")

# Sidebar Settings
st.sidebar.header("⚙️ Model Configuration")
model_name = st.sidebar.selectbox(
    "OpenRouter Model",
    ["openrouter/free", "meta-llama/llama-3-8b-instruct:free", "google/gemini-2.5-flash:free"],
    help="Select the model from OpenRouter to generate outputs."
)
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.1,
    help="0.0 makes response deterministic (recommended for parsing). Higher values add creativity."
)

if api_key:
    st.sidebar.success("🔑 OpenRouter API Key Loaded!")
else:
    st.sidebar.error("❌ OpenRouter API Key Not Found in .env!")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### How Output Parsers Work:
1. **Define Schema**: You specify what shape the output should have.
2. **Get Format Instructions**: The parser generates instructions for the LLM.
3. **Prompt Injection**: Instructions are added to your prompt template.
4. **Parsing**: The LLM output is fed through the parser to build a structured Python object.
""")

# Parser selection
parser_type = st.radio(
    "Select Output Parser Type:",
    ["List Parser (Comma Separated)", "Structured Schema Parser (ResponseSchema)", "Pydantic Model Parser"],
    horizontal=True
)

# Initialize LLM with OpenRouter
llm = OpenRouterChat(model_name=model_name, openai_api_key=api_key, temperature=temperature)

st.markdown("---")

if parser_type == "List Parser (Comma Separated)":
    st.subheader("📋 Comma Separated List Output Parser")
    st.write("Generates instructions for the LLM to output list items separated by commas, then parses it into a Python `list`.")
    
    # Setup parser
    parser = CommaSeparatedListOutputParser()
    format_instructions = parser.get_format_instructions()
    
    col1, col2 = st.columns(2)
    with col1:
        prompt_input = st.text_area(
            "Enter list generation prompt:",
            value="List 5 popular coding tools or IDEs.",
            height=100
        )
    with col2:
        st.markdown("**Parser Format Instructions** (Injected into LLM prompt):")
        st.code(format_instructions, language="text")
        
    if st.button("Generate & Parse List", type="primary"):
        if not api_key:
            st.error("Please provide an OPEN_API_KEY in your .env file.")
        else:
            with st.spinner("Invoking LLM on OpenRouter..."):
                try:
                    prompt_template = PromptTemplate(
                        template="{user_prompt}\n{format_instructions}",
                        input_variables=["user_prompt"],
                        partial_variables={"format_instructions": format_instructions}
                    )
                    
                    chain = prompt_template | llm | parser
                    raw_chain = prompt_template | llm  # To capture raw output for side-by-side demo
                    
                    raw_response = raw_chain.invoke({"user_prompt": prompt_input})
                    parsed_response = parser.parse(raw_response.content)
                    
                    # Show results side-by-side
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.success("📝 Raw LLM Output (String)")
                        st.text_area("Raw Text:", value=raw_response.content, height=180, disabled=True)
                    with res_col2:
                        st.success("🐍 Parsed Output (Python List)")
                        st.write(parsed_response)
                        st.code(f"Type: {type(parsed_response)}\nLength: {len(parsed_response)} items", language="python")
                        
                except Exception as e:
                    st.error(f"Failed to generate/parse: {e}")

elif parser_type == "Structured Schema Parser (ResponseSchema)":
    st.subheader("📂 Structured Output Parser (Schemas)")
    st.write("Useful when you need multiple distinct key-value pairs (fields) returned as a dictionary, but don't want to use Pydantic.")
    
    # Presets
    preset = st.selectbox(
        "Load Schema Preset:",
        ["Travel Destination Details", "Product Specification Details"]
    )
    
    if preset == "Travel Destination Details":
        default_prompt = "Tokyo"
        response_schemas = [
            ResponseSchema(name="destination", description="Name of the city/destination."),
            ResponseSchema(name="country", description="Country where it's located."),
            ResponseSchema(name="currency", description="The official local currency code."),
            ResponseSchema(name="famous_food", description="A well-known local food or delicacy.")
        ]
    else:
        default_prompt = "Apple iPhone 15"
        response_schemas = [
            ResponseSchema(name="product_name", description="Official name of the product."),
            ResponseSchema(name="brand", description="The manufacturing brand."),
            ResponseSchema(name="screen_size", description="Screen size in inches or text description."),
            ResponseSchema(name="main_feature", description="Highlight main feature or selling point.")
        ]
        
    parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = parser.get_format_instructions()
    
    col1, col2 = st.columns(2)
    with col1:
        prompt_input = st.text_input(
            "Enter entity/topic name:",
            value=default_prompt
        )
        st.markdown("**Defined Response Schemas:**")
        schema_df = pd.DataFrame([{ "Field Name": s.name, "Description": s.description } for s in response_schemas])
        st.dataframe(schema_df, use_container_width=True, hide_index=True)
        
    with col2:
        st.markdown("**Parser Format Instructions** (Injected into LLM prompt):")
        st.code(format_instructions, language="text")
        
    if st.button("Generate & Parse Fields", type="primary"):
        if not api_key:
            st.error("Please provide an OPEN_API_KEY in your .env file.")
        else:
            with st.spinner("Invoking LLM on OpenRouter..."):
                try:
                    # We inject a strict instruction to prevent system text headers/footers
                    prompt_template = PromptTemplate(
                        template="You must respond ONLY with valid JSON. Do not include any introduction, explanations, or system headers.\n\nQuery: Provide details for: {user_prompt}.\n{format_instructions}",
                        input_variables=["user_prompt"],
                        partial_variables={"format_instructions": format_instructions}
                    )
                    
                    raw_chain = prompt_template | llm
                    raw_response = raw_chain.invoke({"user_prompt": prompt_input})
                    
                    # Parse
                    parsed_response = parser.parse(raw_response.content)
                    
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.success("📝 Raw LLM Output (String)")
                        st.text_area("Raw Text:", value=raw_response.content, height=220, disabled=True)
                    with res_col2:
                        st.success("🐍 Parsed Output (Python Dict)")
                        st.json(parsed_response)
                        st.code(f"Type: {type(parsed_response)}", language="python")
                        
                except Exception as e:
                    st.error(f"Parsing failed: {e}")
                    st.info("💡 Tip: Some models output system safety warnings or introductions which can break strict parsers. Try running again or use a different model in the sidebar.")

else:  # Pydantic Model Parser
    st.subheader("🛡️ Pydantic Model Output Parser")
    st.write("The most robust parser. Validates that the LLM output conforms to a strict Pydantic BaseModel class structure. Returns a real Python Pydantic object.")
    
    # Define class inside
    class MovieReview(BaseModel):
        title: str = Field(description="The exact title of the movie.")
        rating_out_of_10: int = Field(description="Rating from 1 to 10.")
        sentiment: str = Field(description="Whether the review sentiment is Positive, Negative, or Neutral.")
        critic_name: str = Field(description="Name of the critic.")
        pros: list[str] = Field(description="A list of 2 or 3 positive aspects of the movie.")
        cons: list[str] = Field(description="A list of 2 or 3 negative aspects of the movie.")
        
    parser = PydanticOutputParser(pydantic_object=MovieReview)
    format_instructions = parser.get_format_instructions()
    
    col1, col2 = st.columns(2)
    with col1:
        prompt_input = st.text_area(
            "Enter movie review prompt:",
            value="Review the movie 'The Matrix' (1999). Critic name: Keanu Fan.",
            height=100
        )
        st.markdown("**Pydantic Model Schema (`MovieReview`):**")
        st.code("""
class MovieReview(BaseModel):
    title: str = Field(description="The title of the movie.")
    rating_out_of_10: int = Field(...)
    sentiment: str = Field(...)
    critic_name: str = Field(...)
    pros: list[str] = Field(...)
    cons: list[str] = Field(...)
        """, language="python")
        
    with col2:
        st.markdown("**Parser Format Instructions** (Injected into LLM prompt):")
        st.code(format_instructions, language="text")
        
    if st.button("Generate & Validate Model", type="primary"):
        if not api_key:
            st.error("Please provide an OPEN_API_KEY in your .env file.")
        else:
            with st.spinner("Invoking LLM on OpenRouter..."):
                try:
                    # We inject a strict instruction to prevent system text headers/footers
                    prompt_template = PromptTemplate(
                        template="You must respond ONLY with valid JSON. Do not include any introduction, explanations, or system headers.\n\nQuery: {user_prompt}\n{format_instructions}",
                        input_variables=["user_prompt"],
                        partial_variables={"format_instructions": format_instructions}
                    )
                    
                    raw_chain = prompt_template | llm
                    raw_response = raw_chain.invoke({"user_prompt": prompt_input})
                    
                    # Parse
                    parsed_response = parser.parse(raw_response.content)
                    
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.success("📝 Raw LLM Output (String)")
                        st.text_area("Raw Text:", value=raw_response.content, height=220, disabled=True)
                    with res_col2:
                        st.success("🐍 Parsed Pydantic Object Details")
                        
                        st.markdown(f"**Movie Title:** {parsed_response.title}")
                        st.markdown(f"**Critic:** {parsed_response.critic_name}")
                        st.markdown(f"**Rating:** ⭐ {parsed_response.rating_out_of_10} / 10")
                        st.markdown(f"**Sentiment:** `{parsed_response.sentiment}`")
                        
                        p_col, c_col = st.columns(2)
                        with p_col:
                            st.markdown("**Pros:**")
                            for p in parsed_response.pros:
                                st.write(f"- {p}")
                        with c_col:
                            st.markdown("**Cons:**")
                            for c in parsed_response.cons:
                                st.write(f"- {c}")
                                
                        st.markdown("---")
                        st.code(f"Type: {type(parsed_response)}\nRaw Dump: {parsed_response.model_dump()}", language="python")
                        
                except Exception as e:
                    st.error(f"Parsing failed: {e}")
                    st.info("💡 Tip: Some models output system safety warnings or introductions which can break strict parsers. Try running again or use a different model in the sidebar.")
