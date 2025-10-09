import streamlit as st
import requests
from PIL import Image
import pdfplumber
from docx import Document
import io

# Helper function to extract text from a .pdf file
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

# Helper function to extract text from a .docx file
def extract_text_from_docx(file):
    doc = Document(io.BytesIO(file.read()))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Helper function to read and extract text from different file formats
def extract_text_from_file(file):
    if file.type == "application/pdf":
        return extract_text_from_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file)
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file format")

st.set_page_config(page_title="Text Similarity Checker", page_icon="🔍", layout="centered")
st.title("📝 Document Similarity Checker API Frontend")
st.markdown("##### Upload files or paste text to check similarity between two texts.")

# Open the image file
img = Image.open(r"C:\Users\futan\Desktop\masters project\similarity checker image.jpg")

# Define the target height and maintain the aspect ratio
target_height = 400  # Set the desired height here
width, height = img.size
aspect_ratio = width / height
new_width = int(target_height * aspect_ratio)

# Resize the image
img_resized = img.resize((new_width, target_height))

# Display the resized image
st.image(img_resized, caption="Document Similarity Checker", width=700)

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Tabs for input type
tab1, tab2 = st.tabs(["Paste Text", "Upload Files"])

with tab1:
    text1 = st.text_area("Text 1", height=150)
    text2 = st.text_area("Text 2", height=150)

with tab2:
    file1 = st.file_uploader("Upload first text file", type=["txt", "pdf", "docx"])
    file2 = st.file_uploader("Upload second text file", type=["txt", "pdf", "docx"])

method = st.radio("Choose similarity method:", options=("tfidf", "semantic"))

if st.button("Compare Similarity"):
    # Validate input presence
    if not ((text1.strip() or file1) and (text2.strip() or file2)):
        st.error("Please provide two texts either by pasting or uploading files.")
        st.stop()

    # Read content from files or textareas
    try:
        if file1:
            content1 = extract_text_from_file(file1)
        else:
            content1 = text1

        if file2:
            content2 = extract_text_from_file(file2)
        else:
            content2 = text2
    except Exception as e:
        st.error(f"Error reading files: {e}")
        st.stop()

    api_url = "http://127.0.0.1:8000/compare-texts/"  # Update if needed

    payload = {
        "text1": content1,
        "text2": content2,
        "method": method
    }

    with st.spinner("Calculating similarity..."):
        try:
            # Send form-encoded data, not JSON
            response = requests.post(api_url, data=payload)
            response.raise_for_status()
            result = response.json()

            # Extract similarity score safely
            similarity_score = result.get("percentage_similarity") or result.get("similarity_score")
            method_used = result.get("method_used") or result.get("method", method)

            # Convert score to float if possible
            try:
                similarity_score_float = float(similarity_score)
            except (ValueError, TypeError):
                similarity_score_float = similarity_score  # fallback

            if similarity_score is not None:
                st.success(
                    f"The Similarity Score is {similarity_score} : Method used in calculating score --> {method_used.upper()} "
                )
                # Add to history with float score if possible
                st.session_state.history.append({
                    "text1": content1[:100] + ("..." if len(content1) > 100 else ""),
                    "text2": content2[:100] + ("..." if len(content2) > 100 else ""),
                    "method": method_used,
                    "score": similarity_score_float
                })
            else:
                st.warning("API returned no similarity score.")
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")

# Display history
if st.session_state.history:
    st.markdown("---")
    st.header("🕘 Previous Similarity Checks")
    for idx, entry in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.markdown(f"**Check #{idx}**")
        st.markdown(f"- **Method:** {entry['method'].upper()}")
        # Format score if it's a float, else print as is
        try:
            st.markdown(f"- **Score:** {float(entry['score']):.4f}")
        except (ValueError, TypeError):
            st.markdown(f"- **Score:** {entry['score']}")
        st.markdown(f"- **Text 1 Preview:** {entry['text1']}")
        st.markdown(f"- **Text 2 Preview:** {entry['text2']}")
        st.markdown("")
