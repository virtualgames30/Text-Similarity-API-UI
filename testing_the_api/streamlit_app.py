# streamlit_app.py

import streamlit as st
import requests

st.set_page_config(page_title="Text Similarity Checker", page_icon="🔍", layout="centered")
st.title("📝 Text Similarity API Frontend")
st.markdown("Upload files or paste text to check similarity between two texts.")

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Tabs for input type
tab1, tab2 = st.tabs(["Paste Text", "Upload Files"])

with tab1:
    text1 = st.text_area("Text 1", height=150)
    text2 = st.text_area("Text 2", height=150)

with tab2:
    file1 = st.file_uploader("Upload first text file", type=["txt"])
    file2 = st.file_uploader("Upload second text file", type=["txt"])

method = st.radio("Choose similarity method:", options=("tfidf", "semantic"))

if st.button("Compare Similarity"):
    # Validate input presence
    if not ((text1.strip() or file1) and (text2.strip() or file2)):
        st.error("Please provide two texts either by pasting or uploading files.")
        st.stop()

    # Read content from files or textareas
    try:
        content1 = file1.read().decode("utf-8") if file1 else text1
        content2 = file2.read().decode("utf-8") if file2 else text2
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
