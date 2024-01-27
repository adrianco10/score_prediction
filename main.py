import streamlit as st
import prediction_tool
import walkthrough

if __name__ == '__main__':

    st.sidebar.markdown("You can switch between the actual tool and my walkthrough here:")
    sidebar_button = st.sidebar.selectbox('Walkthrough', ("Walkthrough", "Score Prediction"))
    signature = st.sidebar.subheader('Author:\n\n Adrian Cortes\n\n Email: cortes_10@live.com\n\nLinkedIn:\n'
                                     'https://www.linkedin.com/in/cortesadrian/')
    st.sidebar.subheader("Coming Soon")
    st.sidebar.markdown("Other European leagues...maybe?")

    if sidebar_button == 'Walkthrough':
        walkthrough.walkthrough()

    if sidebar_button == 'Score Prediction':
        prediction_tool.prediction()
