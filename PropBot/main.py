from langchain_experimental.agents import create_pandas_dataframe_agent # type: ignore
from langchain_community.llms import OpenAI # type: ignore
import pandas as pd
import glob
import json
from datetime import datetime
import os

def save_chart(query):
    q_s = ' If any charts or graphs or plots were created save them locally and include the save file names in your response.'
    query += ' . ' + q_s
    return query

def save_uploaded_file(uploaded_file):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    df_arr, df_arr_names = load_dataframe()

    agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df_arr, return_intermediate_steps=True, save_charts=True, verbose=True, allow_dangerous_code=True)
    return agent, df_arr, df_arr_names

def load_dataframe():
    selected_df = []

    all_files_csv = glob.glob("*.csv")
    all_files_xlsx = glob.glob("*.xlsx")
    all_files_xls = glob.glob("*.xls")
    for filename in all_files_csv:
        df = pd.read_csv(filename)
        selected_df.append(df)
    for filename in all_files_xlsx:
        df = pd.read_excel(filename)
        selected_df.append(df)
    for filename in all_files_xls:
        df = pd.read_excel(filename)
        selected_df.append(df)
    selected_df_names = all_files_csv + all_files_xlsx + all_files_xls
    return selected_df, selected_df_names

def run_query(agent, query_):
    if 'chart' or 'charts' or 'graph' or 'graphs' or 'plot' or 'plt' in query_:
        query_ = save_chart(query_)
    output = agent(query_)
    response, intermediate_steps = output['output'], output['intermediate_steps']
    thought, action, action_input, observation, steps = decode_intermediate_steps(intermediate_steps)
    store_convo(query_, steps, response)
    return response, thought, action, action_input, observation

def decode_intermediate_steps(steps):
    log, thought_, action_, action_input_, observation_ = [], [], [], [], []
    text = ''
    for step in steps:
        thought_.append(':green[{}]'.format(step[0].log.split('Action:')[0]))
        action_.append(':green[Action:] {}'.format(step[0].tool.split('Action Input:')[0]))
        action_input_.append(':green[Action Input:] {}'.format(step[0].tool_input))
        observation_.append(':green[Observation:] {}'.format(step[1]))
        log.append(step[0].log)
        text = step[0].log + ' Observation: {}'.format(step[1])
    return thought_, action_, action_input_, observation_, text

def get_convo():
    convo_file = 'convo_history.json'
    if not os.path.exists(convo_file):
        with open(convo_file, 'w', encoding='utf-8') as f:
            json.dump({}, f)
    with open(convo_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data, convo_file

def store_convo(query, response_, response):
    data, convo_file = get_convo()
    current_dateTime = datetime.now()
    data['{}'.format(current_dateTime)] = []
    data['{}'.format(current_dateTime)].append({'Question': query, 'Answer':response, 'Steps':response_})
    
    with open(convo_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)