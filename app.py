import os, config
from flask import Flask, request
from flask_cors import CORS, cross_origin
from llama_index import GPTVectorStoreIndex, StorageContext, load_index_from_storage, download_loader
os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY

import streamlit as st
from llama_index import ServiceContext, LLMPredictor
from langchain.llms import OpenAI
import jsonpickle, json


llm = OpenAI(model_name='gpt-4', max_tokens=6000)

llm_predictor = LLMPredictor(llm=llm)

service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

storage_context = StorageContext.from_defaults(persist_dir="./mysite/storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/get_news_report')
@cross_origin()
def getReport():
    reportType = request.args.get('report_type')
    if reportType == "1":
        response = query_engine.query(f"Write a report on the outlook for {request.args.get('symbol_1')} stock from the years 2023-2027. Be sure to include potential risks and headwinds.")
    else:
        response = query_engine.query(f"Write a report on the competition between {request.args.get('symbol_1')} stock and {request.args.get('symbol_2')} stock.")

    return {'Result' :json.loads(jsonpickle.encode(response))['response']}

@app.route('/get_rss_news')
def getRssNews():
    feedlyRssReader = download_loader("FeedlyRssReader")
    loader = feedlyRssReader(bearer_token = "A76sHAjtUq98Lh6TWMlW5ctaYP45S83NFelo0LZ73PhSQrL8Jlyzc_4Qqc8sBx0uP2JSppVHLcyp8ajVrQ8dUHRT05hOvZzASbPZXVseeTIB6ahw8Iou2Z0HwxLQqJMzvF-FLGrDGvKEtvpbG1Wc5rSEqVH9wxlQ0qhyM8aG3KA3Aw81G2o1RhueP01NB91E4b9BpNl4_UD9cVsyeLLJ5UNOwmUUickryME7OmUcC1j5SQm445ihpjX6dyZyyw:feedlydev")
    documents = loader.load_data(category_name = "Test", max_count = 5)
    return json.loads(jsonpickle.encode(documents))

if __name__ == '__main__':
    app.run(debug=True)

# st.title('Financial Analyst')

# st.header("Financial Reports")

# report_type = st.selectbox(
#     'What type of report do you want?',
#     ('Single Stock Outlook', 'Competitor Analysis'))


# if report_type == 'Single Stock Outlook':
#     symbol = st.text_input("Stock Symbol")

#     if symbol:
#         with st.spinner(f'Generating report for {symbol}...'):
#             response = query_engine.query(f"Write a report on the outlook for {symbol} stock from the years 2023-2027. Be sure to include potential risks and headwinds.")

#             st.write(response)

# if report_type == 'Competitor Analysis':
#     symbol1 = st.text_input("Stock Symbol 1")
#     symbol2 = st.text_input("Stock Symbol 2")

#     if symbol1 and symbol2:
#         with st.spinner(f'Generating report for {symbol1} vs. {symbol2}...'):
#             response = query_engine.query(f"Write a report on the competition between {symbol1} stock and {symbol2} stock.")

#             st.write(response)



