import io
import threading
import time
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

st.set_page_config(page_title="AI Code Debugger", layout="wide")

st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stAlert {
        margin-top: 50px;
    }
    div[data-testid="stCodeBlock"] {
        width: 100% !important;
    }
    div[data-testid="stCodeBlock"] pre {
        white-space: pre-wrap;
        word-break: break-word;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# State Management Setup
if "is_analyzing" not in st.session_state:
    st.session_state.is_analyzing = False
if "analysis_text" not in st.session_state:
    st.session_state.analysis_text = ""
if "stop_requested" not in st.session_state:
    st.session_state.stop_requested = False

with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Enter your Google API Key", type="password")
    model_name = st.selectbox("Select Model", ["gemma-4-26b-a4b-it", "gemini-2.0-flash"])
    
    st.info(
        "This app uses Google GenAI to analyze code (via screenshots or pasted text) and fix errors."
    )
    st.divider()
    st.caption("Built with Streamlit & Google GenAI")

st.title("AI Code Debugger")
st.subheader("Upload a screenshot or paste your code, and let AI find the bugs.")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Input Code")
    
    # Create tabs for the two input methods
    tab1, tab2 = st.tabs(["Upload Screenshot", "Paste Code"])
    
    with tab1:
        uploaded_file = st.file_uploader(
            "Choose an image file (png, jpg, jpeg)", type=["png", "jpg", "jpeg"]
        )

        image = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(
                image, caption="Uploaded Screenshot", use_container_width=True
            )
            
    with tab2:
        pasted_code = st.text_area(
            "Paste your code here",
            height=300,
            placeholder="def hello_world():\n    print('Hello world!')"
        )

    user_prompt = st.text_area(
        "Additional instructions?",
        placeholder="e.g., Rewrite this in Python 3.12, optimize for performance...",
        height=120,
    )

# The updated System Prompt handles both image and text inputs
PROMPT = """
You are an expert programming debugger.
Analyse the provided code (either from the attached image or pasted text).

1. Identify the programming language.
2. If an image is provided, transcribe the code as accurately as possible.
3. Identify all errors and explain why they occur.
4. Provide corrected code.
5. Preserve the original functionality.

If any part of a screenshot is unreadable, tell me instead of guessing.
Clearly separate your explanation from the corrected code.
"""

if user_prompt.strip():
    PROMPT += f"\n\nAdditional User Request:\n{user_prompt}"


def run_stream_analysis(client, model, contents, stop_event, state_dict):
    try:
        response = client.models.generate_content_stream(
            model=model, contents=contents
        )
        for chunk in response:
            if stop_event.is_set():
                break
            if chunk.text:
                state_dict["text"] += chunk.text
    except Exception as e:
        state_dict["error"] = str(e)


with col2:
    st.markdown("### AI Analysis")

    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        start_click = st.button(
            "🔍 Analyze Code",
            type="primary",
            disabled=st.session_state.is_analyzing,
        )

    with btn_col2:
        stop_click = st.button(
            "🛑 Stop Analysis", disabled=not st.session_state.is_analyzing
        )

    if stop_click:
        st.session_state.stop_requested = True
        st.session_state.is_analyzing = False
        st.rerun()

    if start_click:
        if not api_key:
            st.error("Please enter your API Key in the sidebar!")
        elif uploaded_file is None and not pasted_code.strip():
            st.error("Please upload an image or paste some code first!")
        else:
            st.session_state.is_analyzing = True
            st.session_state.analysis_text = ""
            st.session_state.stop_requested = False
            st.rerun()

    if st.session_state.is_analyzing:
        output_container = st.empty()
        status_container = st.empty()

        status_container.info("Analyzing code stream...")

        try:
            client = genai.Client(api_key=api_key)
            
            # Construct the contents list dynamically based on user input
            contents = [PROMPT]
            
            # Prioritize pasted code if both are provided, or you can allow both.
            # Here we append whichever is available.
            if pasted_code.strip():
                contents.append(f"\n\nHere is the pasted code:\n```\n{pasted_code}\n```")
                
            if uploaded_file is not None:
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format="PNG")
                image_bytes = img_byte_arr.getvalue()
                image_part = types.Part.from_bytes(
                    data=image_bytes, mime_type="image/png"
                )
                contents.append(image_part)

            stop_event = threading.Event()
            shared_state = {"text": "", "error": None}

            thread = threading.Thread(
                target=run_stream_analysis,
                args=(
                    client,
                    model_name,
                    contents,
                    stop_event,
                    shared_state,
                ),
            )
            thread.start()

            while thread.is_alive():
                if st.session_state.stop_requested:
                    stop_event.set()
                    break

                st.session_state.analysis_text = shared_state["text"]
                if st.session_state.analysis_text:
                    output_container.markdown(st.session_state.analysis_text)

                time.sleep(0.1)

            thread.join(timeout=1.0)

            if shared_state["error"]:
                st.error(f"An error occurred: {shared_state['error']}")
                st.session_state.is_analyzing = False
            elif st.session_state.stop_requested:
                status_container.warning("⚠️ Analysis stopped by user.")
                st.session_state.is_analyzing = False
            else:
                st.session_state.analysis_text = shared_state["text"]
                output_container.markdown(st.session_state.analysis_text)
                status_container.success("Analysis Complete!")
                st.session_state.is_analyzing = False

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.is_analyzing = False

    elif st.session_state.analysis_text:
        st.markdown(st.session_state.analysis_text)
        if st.session_state.stop_requested:
            st.warning("⚠️ Analysis was stopped.")

st.divider()
st.caption(
    "Note: For best results when uploading, ensure the screenshot is clear and high resolution."
)