import json
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import ElasticsearchRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from pathlib import Path
import pickle
from time import sleep


# #############################################
# ## Launching and setting up pipe obj       ##
# #############################################
from haystack.utils import launch_es

#launch_es()
#sleep(180)

document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
# report_path = Path(__file__).resolve().parent / "static/webChatbot/json/rapport_rte_v1.json"
report_path = "/Users/louisladuve/Desktop/COURS Centrale/COURS_4A/Chatbot/chatbot/webChatbot/static/webChatbot/json" \
              "/rapport_rte_v2.json"


with open(report_path) as json_file:
    dict_rapport = json.load(json_file)["data"]

document_store.write_documents(dict_rapport)

retriever = ElasticsearchRetriever(document_store=document_store)
reader = FARMReader(model_name_or_path="/Users/louisladuve/Desktop/COURS Centrale/COURS_4A/Chatbot/chatbot/webChatbot/ml/camembertV2", use_gpu=False)

pipe = ExtractiveQAPipeline(reader, retriever)
