import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # Your FastAPI base URL

st.title("Text Similarity Checker 🚀")
method = st.radio("Choose similarity method:", ("tfidf", "semantic"))

tab1, tab2 = st.tabs(["Paste Texts", "Upload Files"])

with tab1:
    st.subheader("Paste two texts to compare")
    text1 = st.text_area("Text 1", height=150)
    text2 = st.text_area("Text 2", height=150)
    if st.button("Compare Texts"):
        if text1.strip() and text2.strip():
            payload = {
                'text1': text1,
                'text2': text2,
                'method': method
            }
            with st.spinner("Calculating similarity..."):
                response = requests.post(f"{API_URL}/compare-texts/", data=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Similarity: {result['percentage_similarity']} (Score: {result['similarity_score']})")
                st.info(f"Method used: {result['method_used']}")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.warning("Please enter both texts.")

with tab2:
    st.subheader("Upload two text files to compare")
    file1 = st.file_uploader("Upload File 1", type=["txt"])
    file2 = st.file_uploader("Upload File 2", type=["txt"])
    if st.button("Compare Files"):
        if file1 is not None and file2 is not None:
            files = {
                'file1': (file1.name, file1, 'text/plain'),
                'file2': (file2.name, file2, 'text/plain')
            }
            data = {'method': method}
            with st.spinner("Calculating similarity..."):
                response = requests.post(f"{API_URL}/compare-files/", files=files, data=data)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Similarity: {result['percentage_similarity']} (Score: {result['similarity_score']})")
                st.info(f"Method used: {result['method_used']}")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.warning("Please upload both files.")
