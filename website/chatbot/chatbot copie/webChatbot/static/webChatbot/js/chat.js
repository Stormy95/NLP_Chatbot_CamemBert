var sendBtn = document.getElementById("sendBtn");
var textQuestion = document.getElementById("text-question");
var QAFlow = document.getElementById("msg-container");

var classNameMap = {"0": "top", "1": "mid", "2": "bottom"};


sendBtn.addEventListener("click", (ev) => {
    ev.preventDefault();
    var sendURL = "/api/ask"
        text = textQuestion.value;
    
    if (text.length < 1) return;

    console.log(text);

    xhr = new XMLHttpRequest();

    var data = JSON.stringify({"text" : text});
    xhr.open("POST", sendURL);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(data);

    var questionDiv = document.createElement("div");
    questionDiv.className = "m-1 question"
    questionDiv.innerHTML = text;

    QAFlow.appendChild(questionDiv);

    xhr.onload = (ev) => {
        console.log(xhr.response);
        var resp = JSON.parse(xhr.response);

        if (resp) {
            var count = 0;
            var respTextContainer = document.createElement("div");
            respTextContainer.className = "response";

            for (r in resp) {
                if (r!="exec_time" && r!="bad_request"){
                    var txt = resp[r].answer,
                        ctx = resp[r].context,
                        score = resp[r].score;

                    console.log(txt, ctx, score);


                    var respAnswer = document.createElement("div"),
                        respCtx = document.createElement("div"),
                        respScr = document.createElement("div");

                    respAnswer.className = "answer";
                    respCtx.className = "context";
                    respScr.className = "score";


                    respAnswer.innerHTML = txt ;
                    respCtx.innerHTML = ctx;
                    if (count < 2) {
                        respScr.innerHTML = `<span class="badge badge-pill badge-warning">Score: ` +score + "</span><hr>";
                    } else {
                        respScr.innerHTML = `<span class="badge badge-pill badge-warning">Score: ` +score + "</span>";
                    }


                    respTextContainer.appendChild(respAnswer);
                    respTextContainer.appendChild(respCtx);
                    respTextContainer.appendChild(respScr);

                    QAFlow.appendChild(respTextContainer);
                    count += 1;
                }
                else if(r==="bad_request"){
                    var txt = resp[r];
                    var respAnswer = document.createElement("div");
                    respAnswer.innerHTML = txt ;
                    respAnswer.className = "answer" ;
                    respTextContainer.appendChild(respAnswer);
                    QAFlow.appendChild(respTextContainer);

                }
            }
            var exec_time = document.createElement("div");
            exec_time.className = "exec"
//            exec_time.element.style.fontSize = "small"
//            exec_time.element.style.paddingLeft = "5px"
            exec_time.innerHTML = "Temps execution : " + resp.exec_time;

            QAFlow.appendChild(exec_time);
            textQuestion.value = "";
        }
    }

});


textQuestion.addEventListener("keypress", (ev) => {   
    if (ev.key === 'Enter') {
        ev.preventDefault();
        sendBtn.click();
    }
});