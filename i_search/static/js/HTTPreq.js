// v1.1

class HTTPreq{
    constructor(url, dataType, headers){
        this.url = typeof url != "string" ? "" : url;
        this.dataType = dataType == "fd" ? "fd" : "txt";
        this.headers = headers == undefined ? {} : headers;
        this.readyState = 0;
        this.status = 0;
        this.resultLength = 0;
        this.result = null;
    }

    async posta(data){
        this.sendReq("POST", data);
        await this.returnValue();
        return this;
    }
    async geta(data){
        this.sendReq("GET", data);
        await this.returnValue();
        return this;
    }

    post(data){
        var T = this;
        return new Promise((resolve) => {
            T.posta(data).then(rcv => resolve(rcv));
        });
    }
    get(data){
        var T = this;
        return new Promise((resolve) => {
            T.geta(data).then(rcv => resolve(rcv));
        });
    }

    setUrl(url){
        this.url = typeof url != "string" ? "" : url;
        return this;
    }

    setDataType(dataType){
        this.dataType = dataType == "fd" ? "fd" : "txt";
        return this;
    }

    setHeaders(headers){
        this.headers = headers == undefined ? {} : headers;
        return this;
    }

    sendReq(method, data){
        var Xreq = new XMLHttpRequest(), sd, T = this;
        this.readyState = 0;
        this.result = null;

        Xreq.open(method, this.url);
        for (var i in this.headers) {
            Xreq.setRequestHeader(i, this.headers[i]);
        }

        Xreq.onreadystatechange = function () {
            if(Xreq.readyState == 4){
                T.status = Xreq.status;
                T.result = Xreq.responseText;
                T.resultLength = Xreq.responseText.length;
                
                setTimeout(()=>{
                    T.readyState = 4;
                }, Math.log10(T.resultLength) * 10);
            }
        }

        if(this.dataType == "txt"){
            if(!data){}
            else if(typeof data == "string") sd = data;
            else if(data.constructor.name == "FormData"){
                var s = {};
                data.forEach(function(value, key){
                    s[key] = value;
                });
                sd = JSON.stringify(s);
            }
            else sd = JSON.stringify(data);
        }
        else if(this.dataType == "fd"){
            if(!data){}
            else if(data.constructor.name == "FormData") sd = data;
            else{
                sd = new FormData();
                for(var i in data){
                    // sd.append(i, data[i]);
                    if(Array.isArray(data[i]) || data[i]?.constructor == Object) sd.append(i, JSON.stringify(data[i]));
                    else sd.append(i, data[i]);
                    // [Object, Array].includes(data[i] && data[i].constructor) ? sd.append(i, JSON.stringify(data[i])) : sd.append(i, data[i]);
                }
            }
        }
        Xreq.send(sd);
        this.Xreq = Xreq;
    }

    returnValue(){
        var T = this;
        return new Promise((resolve) => {
            var s = setInterval(()=>{
                if(T.result !== null && T.readyState == 4 && T.result.length == T.resultLength){
                    clearInterval(s);
                    resolve(T.result);
                }
            }, 10);
        });
    }
}

class HTTPreq2{
    constructor(argw){
        if(argw == undefined) argw = {};
        this.ref = new HTTPreq(argw.url, argw.dt, argw.hd);
    }

    post(data){
        this.ref.sendReq("POST", data);
    }
    get(data){
        this.ref.sendReq("GET", data);
    }
}

class cycleHTTPreq{
    constructor(req, data, delay, totalCount){
        if(req.constructor.name != "HTTPreq"){
            console.error("invalid HTTPreq");
            return;
        }
        this.interval = 0;
        this.counter = 0;
        this.req = req;
        this.data = data;
        this.delay = typeof parseInt(delay) == "number" ? delay : 100;
        this.totalCount = typeof parseInt(totalCount) == "number" ? totalCount : 5;
        this.reqStatus = 0; // 0=waiting 1=working 2=pause 3=done

        this.rcvSolve = (rcv) => {
            console.log(rcv.result);
        };
        this.method = "geta";
        this.onDone_callBack
    }

    posta(rcvSolve){
        if(typeof rcvSolve == "function") this.rcvSolve = rcvSolve;
        this.method = "posta";
        this.reqStatus = 1;
        this.start(this.rcvSolve, this.method);
        return this;
    }
    geta(rcvSolve){
        if(typeof rcvSolve == "function") this.rcvSolve = rcvSolve;
        this.method = "geta";
        this.reqStatus = 1;
        this.start(this.rcvSolve, this.method);
        return this;
    }
    
    start(rcvSolve, method){
        var T = this, isNext = this.counter++ < this.totalCount || this.totalCount == -1;
        if(this.rcvSolve != rcvSolve) this.rcvSolve = rcvSolve;

        if(isNext){
            this.req[method](this.data).then((rcv) =>{
                rcvSolve(rcv);
                
                if(this.reqStatus == 1) T.interval = setTimeout(()=>{
                    T.start(rcvSolve, method);
                }, this.counter == this.totalCount ? 0 : T.delay);
            });
        }
        else{
            T.reqStatus = 3;
            if(typeof this.onDone_callBack == "function") this.onDone_callBack();
        }
    }

    onDone(callBack){
        if(this.totalCount == -1) {
            console.warn("eternal HTTPreq");
        }
        else if(typeof callBack != "function"){
            this.onDone_callBack = () => {
                console.log("Done.");
            };
        }
        else {
            this.onDone_callBack = callBack;
        }
        return this;
    }

    pause(){
        clearInterval(this.interval);
        this.reqStatus = 2;
        return this;
    }

    reset(){
        this.reqStatus = 0;
        this.counter = 0;
        return this;
    }

    resume(){
        this.reqStatus = 1;
        this.start(this.rcvSolve, this.method);
        return this;
    }

    setDelay(delay){
        this.delay = typeof parseInt(delay) == "number" ? delay : (this.delay, console.warn("set delay failed."));
        return this;
    }

    setTotalCount(totalCount){
        this.totalCount = typeof parseInt(totalCount) == "number" ? totalCount : (this.totalCount, console.warn("set totalCount failed."));
        return this;
    }
}