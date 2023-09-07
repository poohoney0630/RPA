import streamlit as st

def main():
    st.title("Embedding Geogebra App in Streamlit")

    # Replace this with the actual Geogebra app URL
    geogebra_url = "https://www.geogebra.org/m/b85v7zww"

    st.write("Here's the embedded Geogebra app:")
    st.components.v1.iframe(geogebra_url, height=600, scrolling=True)

if __name__ == "__main__":
    main()
