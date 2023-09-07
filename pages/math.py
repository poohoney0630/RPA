
import streamlit as st
import requests

# Replace with your Wolfram Alpha API key
API_KEY = "XUET5P-R5286VWWP8"

def wolfram_alpha_query(query):
    base_url = "http://api.wolframalpha.com/v2/query"
    params = {
        "input": query,
        "format": "plaintext",
        "output": "JSON",
        "appid": API_KEY,
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def main():
    st.title("Wolfram Alpha Query with Streamlit")

    query = st.text_input("Enter your Wolfram Alpha query:")
    if query:
        result = wolfram_alpha_query(query)

        if result:
            pods = result.get("queryresult", {}).get("pods", [])
            for pod in pods:
                title = pod.get("title", "")
                plaintext = pod.get("subpods", [])[0].get("plaintext", "")
                st.write(f"**{title}:** {plaintext}")
        else:
            st.error("An error occurred while querying Wolfram Alpha.")

if __name__ == "__main__":
    main()