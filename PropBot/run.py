import glob
import os
import streamlit as st
from main import *
import openai
from streamlit_chat import message
from streamlit_image_select import image_select

def setOpenAIKey(key):
    os.environ['OPENAI_API_KEY'] = key

def get_text(n):
    input_text = st.text_input('How can I help?', '', key="input{}".format(n))
    return input_text 

def show_data(tabs, df_arr):
    for i, df_ in enumerate(df_arr):
        with tabs[i]:
            st.dataframe(df_)

def main():
    st.title("Pandas AI Agent - Demo")
    openai_key = st.sidebar.text_input('Open AI API KEY', key="openai_key", type="password")
    if st.sidebar.button('Update Key'):
        setOpenAIKey(openai_key)

    st.sidebar.title('Pandas AI Agent Demo')

    uploaded_file = st.file_uploader("Choose files to upload (csv, xls, xlsx)", type=["csv", "xls", "xlsx"], accept_multiple_files=True)
    agent = ''
    if uploaded_file:
        for file in uploaded_file:
            agent, selected_df, selected_df_names = save_uploaded_file(file)
        st.session_state["tabs"].clear()
        for df_name in selected_df_names:
            st.session_state.tabs.append(df_name)
        tabs = st.tabs([s.center(9, "\u2001") for s in st.session_state["tabs"]])
        show_data(tabs, selected_df)

    st.header("Agent Output Directory")
    if st.button('Open Directory'):
        os.startfile(os.getcwd())
    imgs_png = glob.glob('*.png')
    imgs_jpg = glob.glob('*.jpg')
    imgs_jpeeg = glob.glob('*.jpeg')
    imgs_ = imgs_png + imgs_jpg + imgs_jpeeg
    if len(imgs_) > 0:
        img = image_select("Generated Charts/Graphs", imgs_, captions =imgs_, return_value = 'index')
        st.write(img)

    st.header("Query The Dataframes")
    x = 0
    user_input = get_text(x)
    if st.button('Query'):
        if agent:
            response, thought, action, action_input, observation = run_query(agent, user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            
            # Display generated images in chat
            img_files = glob.glob('*.png') + glob.glob('*.jpg') + glob.glob('*.jpeg')
            if img_files:
                latest_img_path = max(img_files, key=os.path.getctime)
                st.image(latest_img_path, caption=os.path.basename(latest_img_path), width=400)


if __name__ == "__main__":
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    if 'tabs' not in st.session_state:
        st.session_state['tabs'] = []

    main()