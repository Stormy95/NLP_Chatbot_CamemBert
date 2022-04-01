import time

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pathlib import Path
import json

from .ml.chatbot_qa import pipe 

#############################################
## Defining views                          ##
#############################################

def index(request):
    context = {}
    return render(request, 'webChatbot/home.html', context)

@csrf_exempt
def get_question(request):
    if request.method == "POST":
        text = json.loads(request.body)
        print(text['text'])
        start = time.time()
        chat_response = pipe.run(
            query=text['text'],
            params={'Reader': {"top_k": 3}}
        )
        exec_time = time.time() - start
        chat_response = chat_response["answers"]
        if chat_response:
            if chat_response[0].score>0.1:
                print(chat_response)
                print(chat_response[0].answer)
                # chat_response = chat_response[0].answer
                return JsonResponse({"response_1": {"answer":chat_response[0].answer,
                                                    "context": "..." + chat_response[0].context + "...",
                                                    "score": str(chat_response[0].score)},
                                     "response_2": {"answer": chat_response[1].answer,
                                                    "context": "..."+chat_response[1].context+"...",
                                                    "score": str(chat_response[1].score)},
                                     "response_3": {"answer": chat_response[2].answer,
                                                    "context": "..."+chat_response[2].context+"...",
                                                    "score": str(chat_response[2].score)},
                                     "exec_time": str(round(exec_time, 2)) + " s"
                                     })
            else:
                return JsonResponse({
                    "bad_request": "Veuillez préciser votre demande car la réponse n'est pas trouvée dans le texte",
                    "exec_time": str(round(exec_time, 2)) + " s"
                })
        else:
            return JsonResponse({
                "bad_request" : "Veuillez préciser votre demande car la réponse n'est pas trouvée dans le texte",
                "exec_time": str(round(exec_time, 2)) + " s"
            })

