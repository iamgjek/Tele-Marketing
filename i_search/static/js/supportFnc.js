class supfnc{
    static getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
    static getHrefArg = () => {
        var hrefArg = (window.location.href.split("?")[1] || "").split("#")[0];
        if(hrefArg){
            hrefArg = hrefArg.split("&").reduce((a, e) => {
                e = e.split("=");
                a[e[0]] = e[1];
                return a;
            }, {});
        }
        return hrefArg;
    }

    static toJSON = (arg, option) => {
        try{
            arg = arg.replace(new RegExp(option, 'g'),""); 
            return JSON.parse(arg.replace(new RegExp("\\&amp;", 'g'), "&").replace(new RegExp("\\&\\#39;", 'g'), "\""));
        }
        catch(e){
            try{
                var ch = {}, tmp; // /(?<=[^\\])\"(\\\"|[^\"])*\'+(\\\"|[^\"])*\"(?=[^\\])/g
                arg = arg.replace(new RegExp("(?<=[^\\])\"(\\\"|[^\"])*\'+(\\\"|[^\"])*\"(?=[^\\])", 'g'), (x) => {
                    tmp = "@"+this.randAlphabet(10);
                    ch[tmp] = x;
                    return tmp;
                }); // /(?<=(([:,{]|[^\\])\s*))\'|(?<=[^\\])\'(?=(\s*([:,}])))/g
                arg = arg.replace(new RegExp("(?<=(([:,{]|[^\\])\\s*))\'|(?<=[^\\])\'(?=(\\s*([:,}])))", 'g'), "\"");
                for(var i in ch){
                    arg = arg.replace(i, ch[i]);
                }
                return JSON.parse(arg.replace(new RegExp("\\&amp;", 'g'), "&").replace(new RegExp("\\&\\#39;", 'g'), "\""));
            }
            catch(e){
                console.log(arg, e);
                return {};
            }
        }
    }

    static remove_illiegalChar = (str) => {
        if (typeof str != "string") return "";
        return str.replace(new RegExp("[\\\\/:*?\"\'<>|\\n\\b\\0\\t]", "g"), "");
    }

    static taiwanTime = (time) => {
        if(!time) time = new Date(Date.now() + 8*3600*1000).toISOString();
        var t = time.split("-");
        return "民國" + (t[0]>1000? t[0]-1911:t[0]) + "年" + t[1] + "月" + t[2].slice(0,2) + "日";
    }

    static getRelativeTime = (dateStr) => {
        if(isNaN(Date.parse(dateStr))) return "時間格式錯誤 yyyy-mm-dd (hh:mm:ss)";
        var D_dateValue = (Date.now()-Date.parse(dateStr))/1000, timeGap = [1, 60, 3600, 86400, 604800, 18144000, 220752000], unit=["秒", "分", "小時", "天", "周", "個月", "年"];
        for(var i=0;i<6;i++){
            if(D_dateValue / timeGap[i+1] < 1){
                return parseInt(D_dateValue / timeGap[i]) + unit[i] + "前";
            }
        }
    }

    static getMonthDays(m = new Date()){
        return new Date(m.getFullYear(), m.getMonth() + 1, 0).getDate();
    }

    static clickCopy = (el) => {
        try{
            navigator.clipboard?.writeText && navigator.clipboard.writeText(el.innerText);
        }
        catch{
            var range = document.createRange();
            range.selectNode(el);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            document.execCommand("copy");
            window.getSelection().removeAllRanges();
        }
    }

    static getZindex = (el) => {
        if (window.getComputedStyle) {
            return document.defaultView.getComputedStyle(el, null).getPropertyValue("z-index");
        }
        else if (el.currentStyle) {
            return el.currentStyle["z-index"];
        }
    }

    static randAlphabet = (n) => {
        var t = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789", r="";
        for(var i=0;i<n;i++){
            r+=t[parseInt(Math.random() * (52 + i ? 10 : 0))];
        }
        return r;
    }

    static getObjType(obj){
        if(typeof obj != "object") return typeof obj;
        if(Array.isArray(obj)) return "array";
        if(obj == null) return "null";
        return typeof obj;
    }

    static isParentElement(target, parent){
        while(target){
            if(target == parent) return 1;
            target = target.parentElement;
        }
        return 0;
    }

    static createElement(tagName, options){
        var el = document.createElement(tagName), tmp;
        for(var i in options){
            if(!options[i]) continue;
            if(i == "class"){
                tmp = [];
                if(typeof options.class == "string") tmp = options.class.split(" ");
                else if(Array.isArray(options.class)) tmp = options.class;
                for(var j in tmp) el.classList.add(tmp[j]);
            }
            else if(i == "style"){
                for(var j in options.style){
                    el.style[j] = options.style[j];
                }
            }
            else if(i == "attr"){
                for(var j in options.attr){
                    el.setAttribute(j, options.attr[j]);
                }
            }
            else if(i == "id"){
                el.id = options.id;
            }
        }
        return el;
    }

    static bindEvent(element, eventsFnc, ...argw){
        var chr = Array.prototype.slice.call(element.getElementsByTagName('*') || []), events, fncName;
        chr.push(element);
        for(let c in chr){ // loop
            events = chr[c].getAttributeNames().reduce((a,e)=>{if(e[0]=='@')a.push(e); return a;}, []);
            for(let fncIdx in events){
                fncName = chr[c].getAttribute(events[fncIdx]);
                if(typeof eventsFnc[fncName] != "function") continue;
                chr[c].addEventListener(events[fncIdx].slice(1), (e)=>{
                    eventsFnc[fncName](e, ...argw);
                });
                chr[c].removeAttribute(events[fncIdx]);
            }
        }
    }

    static dateFormat = (dateStr, option) => {
        dateStr = dateStr ? dateStr.splice(4,0,'-').splice(7,0,'-').splice(10,0,':').splice(13,0,':').splice(16,0,':') : "";
        switch(option){
            case "distance":
                var dateValue = Date.parse(dateStr);
                return Date.now()-dateValue;
            case "flex":
                var D_dateValue = (Date.now()-Date.parse(dateStr))/1000, timeGap = [1, 60, 3600, 86400, 604800, 18144000, 220752000], unit=["秒", "分", "小時", "天", "周", "月", "年"];
                for(var i=0;i<6;i++){
                    if(D_dateValue / timeGap[i+1] < 1){
                        return parseInt(D_dateValue / timeGap[i]) + unit[i] + "前";
                    }
                }
                return;
            case "year":
                return dateStr.slice(0,4);
                
            case "month":
                return dateStr.slice(0,7);
                
            case "day":
                return dateStr.slice(0,10);
                
            case "hour":
                return dateStr.slice(0,13);
                
            case "minute":
                return dateStr.slice(0,16);
                
            case "second":
                return dateStr
                
            case "getMonth":
                return dateStr.slice(5,7);
                
            case "getDay":
                return dateStr.slice(8,10);
                
            case "getHour":
                return dateStr.slice(11,13);
                
            case "getMinute":
                return dateStr.slice(14,16);
                
            case "getSecond":
                return dateStr.slice(17);
        }
    }

    static loadScript = (testStatement, scriptUrl, callback, ...args) => {
        try{
            eval(testStatement);
            return 0;
        }
        catch(e){
            var sc = document.createElement("script");
            sc.src = scriptUrl;
            document.body.appendChild(sc);
            var t = 0, s = setInterval(()=>{
                try{
                    eval(testStatement);
                    clearInterval(s);
                    if(typeof callback == "function") callback(...args);
                }
                catch(e){
                    t++;
                    if(t>100){
                        clearInterval(s);
                        console.error("fail to load script");
                    }
                }
            }, 50);
            return 1;
        }
    }

    static downloadPDF = (target, fileName, callback, ...args) => {
        // requirements
        // https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js
        // https://html2canvas.hertzen.com/dist/html2canvas.min.js
        // font file download https://github.com/zxniuniu/SourceHanSansCN/tree/main/dist
        if(this.loadScript("jspdf.jsPDF", "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js", this.downloadPDF, target, fileName)) return;
        if(this.loadScript("html2canvas", "https://html2canvas.hertzen.com/dist/html2canvas.min.js", this.downloadPDF, target, fileName)) return;
        target
        var ele = Array.prototype.slice.call(target.getElementsByTagName("*")), scale = (595.28-36)/target.offsetWidth, pageNum = Math.ceil(target.offsetHeight * scale / (841.89 - 60));
        for(var i in ele){
            ele[i].style.fontFamily = "SourceHanSansCN-Normal"
        }
        var doc = new jspdf.jsPDF('p','pt','a4');
        doc.addFont("/static/font/SourceHanSansCN-Normal.ttf", "SourceHanSansCN-Normal", "normal");
        doc.setFont("SourceHanSansCN-Normal", "normal");
        doc.html(target, {
            callback: function (pdf) {
                var mx = pdf.internal.getNumberOfPages() - pageNum;
                for(var i=0; i<mx; i++) pdf.deletePage(pdf.internal.getNumberOfPages());
                pdf.save(fileName);
                if(typeof callback == "function") callback(...args);
                // window.open(pdf.output("bloburl"), "_blank");
            },
            html2canvas:{
                scale: scale
            },
            x: 18,
            margin: [30, 0, 30, 0],
            autoPaging: 'text',
        });
    }

    static getClickedElement = (x, y) => {
        return document.elementFromPoint(x, y);
    }
    
    static isEqual = (a,b) => {
        if(typeof a != typeof b) return 0;
        if(typeof a == "object"){
            if(Object.keys(a).length != Object.keys(b).length) return 0;
            for(var i in a){
                if(!this.isEqual(a[i], b[i])) return 0;
            }
            return 1;
        }
        else return a == b;
    }

    // console.log(supfnc.arrayFromTo([0,1,2,3], [0,1,3,4])); // add [4] del [2]
    // console.log(supfnc.arrayFromTo([0,1,2,3], [0,1,4,5,3])); // add [4,5] del [2]
    // console.log(supfnc.arrayFromTo([0,1,2,3], [0,1,3])); // add [] del [2]
    // console.log(supfnc.arrayFromTo([0,1,2,3], [0,1,4,5,2,3])); // add [4,5] del []
    // console.log(supfnc.arrayFromTo([0,1,2,3,4,5,6,7,8,9,10], [0,1,6,5,4,8,10])); // add [6,5] del [2,3,5,6,7,9]
    // console.log(supfnc.arrayFromTo([0,1,2,3,4,5,6,7,8,9,10], [0,1,4,11,6,8,12,10])); // add [11,12] del [2,3,5,7,9]
    
    static arrayFromTo = (origArr, distArr) =>{
        var r = {add:[], del:[], addIdx:[], delIdx:[]}, origEx = [], tmpArr = [], tmpL, tmpIdx = 0, ref, refArrMax, refArrMaxIdx = 0, refArrMaxL = 0;
        ref = this.LCS(origArr, distArr);
        // console.log("arrayFromToB", origArr, origArr, ref);
        
        if(ref.length > 0){
            for(var i in origArr){
                if(this.isEqual(origArr[i], distArr[i])) tmpArr.push(origArr[i]);
            }
            for(var i in ref) {
                refArrMax = this.LCS(ref[i], tmpArr);
                if(refArrMax.length){
                    tmpL = refArrMax[0].length;
                    if(tmpL > refArrMaxL){
                        refArrMaxL = tmpL;
                        refArrMaxIdx = i;
                    }
                }
            }
            ref = ref[refArrMaxIdx];
            for(let i in origArr){
                if(!this.isEqual(origArr[i], ref[tmpIdx])){
                    r.del.push(origArr[i]);
                    r.delIdx.push(parseInt(i));
                    // origEx.push(origArr[i]);
                }
                else{
                    origEx.push(ref[tmpIdx]);
                    tmpIdx++;
                }
            }
            tmpIdx = 0;
            for(var i in distArr){
                if(!this.isEqual(distArr[i], origEx[tmpIdx])){
                    r.add.push(distArr[i]);
                    r.addIdx.push(parseInt(i));
                }
                else{
                    tmpIdx++;
                }
            }

            r.del.reverse();
            r.delIdx.reverse();
            return r;
        }
        else{
            for(var i in origArr){
                r.del.push(origArr[i]);
                r.delIdx.push(parseInt(i));
            }
            for(var i in distArr){
                r.add.push(distArr[i]);
                r.addIdx.push(parseInt(i));
            }
            r.del.reverse();
            r.delIdx.reverse();
            return r;
        }
    }
    
    static arrayFromToB = (origArr, distArr) =>{
        var r = {add:[], del:[], addIdx:[], delIdx:[], movIdx: []}, origDict = {}, distDict = {};
        
        for(var i in origArr){
            for(var j in distArr){
                if(this.isEqual(origArr[i], distArr[j]) && !(i in origDict) && !(j in distDict)){
                    origDict[i] = 1;
                    distDict[j] = 1;
                    r.movIdx.push([parseInt(i), parseInt(j)]);
                    break;
                }
            }
        }
        for(var i in origArr){
            if(!(i in origDict)){
                r.del.push(origArr[i]);
                r.delIdx.push(parseInt(i));
            }
        }
        for(var i in distArr){
            if(!(i in distDict)){
                r.add.push(origArr[i]);
                r.addIdx.push(parseInt(i));
            }
        }

        r.del.reverse();
        r.delIdx.reverse();

        for(var i in r.movIdx){
            for(var j in r.delIdx){
                if(r.delIdx[j] < r.movIdx[i][0]) r.movIdx[i][0]--;
            }
        }
        for(var i=0; i<r.movIdx.length; i++){
            for(var j=0; j<i; j++){
                if(r.movIdx[i][0] == r.movIdx[j][1]){
                    r.movIdx[i][0] = r.movIdx[j][0];
                }
            }
        }
        for(var i=0; i<r.movIdx.length; i++){
            if(r.movIdx[i][1] == r.movIdx[i][0]){
                r.movIdx.splice(i, 1);
                i--;
                continue;
            }
            if(r.movIdx[i][1] < r.movIdx[i][0]) {
                var tmp = r.movIdx[i][1];
                r.movIdx[i][1] = r.movIdx[i][0];
                r.movIdx[i][0] = tmp;
            }
        }
        return r;
    }

    // 最長共同子序列 (Longest Common Subsequence; LCS)
    static LCS = (arr1, arr2) => {
        if(!Array.isArray(arr1) || !Array.isArray(arr2)) return [];

        var mapping = (p, q) => {
            var m = [];
            for (var i = 0; i <= p.length; i++){
                m[i] = [];
                m[i][0] = 0;
            }
            for (var i = 0; i <= q.length; i++) m[0][i] = 0;
            for (var i = 0; i < p.length; ++i){
                for (var j = 0; j < q.length; ++j){
                    m[i+1][j+1] = this.isEqual(p[i], q[j]) ? m[i][j] + 1 : Math.max(m[i+1][j], m[i][j+1]);
                }
            }
            return m;
        };
        var map = mapping(arr1, arr2), maxL = map[arr1.length][arr2.length], route = {}, rtn = [];
        for(var i=arr1.length; i>=0; i--){
            for(var j=arr2.length; j>=0; j--){
                if(map[i][j-1] == map[i][j]-1 && map[i-1][j] == map[i][j]-1){
                    if(!route[map[i][j]]) route[map[i][j]] = [[i, j]];
                    else route[map[i][j]].push([i, j]);
                }
            }
        }

        var findAll = (point = maxL, lst = []) => {
            var tmp, l, idx;
            if(!lst.length){
                for(var i in route[point]){
                    lst.push({v: [arr1[route[point][i][0]-1]], x: route[point][i][0], y: route[point][i][1]})
                }
            }
            else{
                l = idx = lst.length;
                for(var i=0; i<l; i++){
                    tmp = [];
                    for(var j in route[point]){
                        if(lst[i].x > route[point][j][0] && lst[i].y > route[point][j][1]){
                            tmp.push(j);
                        }
                    }
                    for(var j=0; j<tmp.length-1; j++){
                        lst.push({v:lst[i].v.slice(), x:lst[i].x, y:lst[i].y});
                    }
                    for(var j=0; j<tmp.length; j++){
                        if(!j){
                            lst[i].v.push(arr1[route[point][tmp[j]][0]-1]);
                            // lst[i].v += arr1[route[point][tmp[j]][0]-1];
                            lst[i].x = route[point][tmp[j]][0];
                            lst[i].y = route[point][tmp[j]][1];
                        }
                        else{
                            lst[idx].v.push(arr1[route[point][tmp[j]][0]-1]);
                            // lst[idx].v += arr1[route[point][tmp[j]][0]-1];
                            lst[idx].x = route[point][tmp[j]][0];
                            lst[idx].y = route[point][tmp[j]][1];
                            idx++;
                        }
                    }
                }
            }
            if(point > 0) findAll(point - 1, lst);
            return lst;
        }
        var res = findAll();
        for(var i in res){
            res[i] = res[i].v.reverse();
        }
        
        return res;
    }

    // console.log(supfnc.LCS([0,1,2,3], [0,1,3,4])); // ['0,1,3']
    // console.log(supfnc.LCS([0,1,2,3], [0,1,4,5,3])); // ['0,1,3']
    // console.log(supfnc.LCS([0,1,2,3], [3,2,1,0])); // ['0','1','2','3']
    // console.log(supfnc.LCS([0,1,2,3,4,5,6,7,8,9,10], [0,1,6,5,4,8,10])); // ['0,1,4,8,10', '0,1,5,8,10', '0,1,6,8,10']
    // console.log(supfnc.LCS([0,1,2,3,4,5,6,7,8,9,10], [0,1,4,11,6,8,12,10,9])); // ['0,1,4,6,8,9', '0,1,4,6,8,10']
    // console.log(supfnc.LCS([0,1,2,3,4,5,6], [0,8,3,7,6,5,2])); // ['0,3,5', '0,3,6']

    static oneNumBinary = (n) => {
        if(typeof n == "number"){
            var r = 0, x = 1;
            while(x <= n){
                if(x & n) r++;
                x *= 2;
            }
            return r;
        }
        return -1;
    }

    static lowbit = (x) => {
        return x&-x;
    }

    static factor = (n) => { // factorization
        if(typeof n == "number"){
            var w = [], g = Math.sqrt(n);
            while(n > 1){
                if(!(n%2)) {
                    w.push(2);
                    n /= 2;
                    g = Math.sqrt(n);
                    continue;
                }
                for(var i=3; i<=g; i+=2){
                    if(!(n%i)){
                        w.push(i);
                        n /= i;
                        g = Math.sqrt(n);
                        break;
                    }
                }
                if(i>g){
                    w.push(n);
                    n = g = 1;
                }
            }
            return w;
        }
        return [];
    }

    // Prim's algorithm
    static MST_P = (links, directional = 0) => {
        // directional 無向 = 0, 有向 = 1
        // links = [[from, to, cost], ...]
        var nowVertex;
        let vertexStatus = {}, vertexTo = {}, vertexToSorted = {}, tree = [];
        var vertexNumAdded = 0, vertexNum = 0;

        var st, ed, cost;
        for(var i in links){
            st = links[i][0];
            ed = links[i][1];
            cost = links[i][2];
            for(var j=0; j<(directional?1:2); j++){
                if(!(st in vertexStatus)){
                    vertexTo[st] = {};
                    vertexStatus[st] = [null, Infinity, 0];
                    vertexNum++;
                }
                if(vertexTo[st][ed]) vertexTo[st][ed] = Math.min(vertexTo[st][ed], cost);
                else vertexTo[st][ed] = cost;

                [st, ed] = [ed, st];
            }
        }

        var routeTmp;
        for(var i in vertexTo){
            routeTmp = [];
            for(j in vertexTo[i]){
                routeTmp.push([j, vertexTo[i][j]]);
            }
            vertexToSorted[i] = routeTmp.sort((a,b) => {return a[1]<b[1]?1:-1});
        }

        nowVertex = Object.keys(vertexStatus)[0];
        vertexStatus[nowVertex][2] = 1;
        tree.push(nowVertex);
        vertexNumAdded++;

        var minV, minOrig, minDest, tmp;
        while(vertexNumAdded < vertexNum){
            minV = Infinity;
            for(var i=0; i<vertexNumAdded; i++){
                tmp = vertexToSorted[tree[i]].slice(-1)[0];
                
                if(!tmp) continue;
                if(vertexStatus[tmp[0]][2]) {
                    vertexToSorted[tree[i]].pop();
                    i--;
                    continue;
                }
                if(tmp[1] < minV){
                    minV = tmp[1];
                    minOrig = tree[i];
                    minDest = tmp[0];
                }
            }
            vertexStatus[minDest][0] = minOrig;
            vertexStatus[minDest][1] = minV;
            vertexStatus[minDest][2] = 1;
            vertexToSorted[minOrig].pop();
            tree.push(minDest);
            vertexNumAdded++;
        }
        return vertexStatus;
    }

    // Prim's algorithm another
    static MST_P2 = (links, directional = 0) => {
        // directional 無向 = 0, 有向 = 1
        // links = [[from, to, cost], ...]
        var nowVertex;
        var vertexStatus = {}, vertexTo = {}, tree = [], edges = [];
        var vertexNumAdded = 0, vertexNum = 0, edgeIdx = 0;

        var st, ed, cost;
        for(var i in links){
            st = links[i][0];
            ed = links[i][1];
            cost = links[i][2];
            for(var j=0; j<(directional?1:2); j++){
                if(!(st in vertexStatus)){
                    vertexTo[st] = {};
                    vertexStatus[st] = [null, Infinity, 0];
                    vertexNum++;
                }
                if(vertexTo[st][ed]) vertexTo[st][ed] = Math.min(vertexTo[st][ed], cost);
                else vertexTo[st][ed] = cost;

                [st, ed] = [ed, st];
            }
        }

        var setMinEdge = (vertex) => {
            var costTmp, nowMin;
            for(var i in vertexTo[vertex]){
                if(vertexStatus[i][2]) continue;
                costTmp = vertexTo[vertex][i];

                if(costTmp < vertexStatus[i][1]){
                    if(vertexStatus[i][1] == Infinity) edges.push(i);
                    
                    vertexStatus[i][0] = vertex;
                    vertexStatus[i][1] = costTmp;
                }
            }
            
            var eL = edges.length;
            
            nowMin = vertexStatus[edges.slice(-1)[0]][1];
            for(var i=edgeIdx; i<eL; i++){
                if(edges[i] === null || vertexStatus[edges[i]][2]){
                    edges[i] = null;
                    [edges[i], edges[edgeIdx]] = [edges[edgeIdx], edges[i]];
                    edgeIdx++;
                    continue;
                }
                if(vertexStatus[edges[i]][1] < nowMin){
                    nowMin = vertexStatus[edges[i]][1];
                    [edges[i], edges[eL-1]] = [edges[eL-1], edges[i]];
                }
            }
        }

        nowVertex = Object.keys(vertexStatus)[0];
        vertexStatus[nowVertex][1] = -Infinity;
        vertexStatus[nowVertex][2] = 1;
        
        var minV, minDest, minOrig, tmpEdge;
        while(vertexNumAdded < vertexNum - 1){
            setMinEdge(nowVertex);
            do{
                tmpEdge = edges.pop();
                minDest = tmpEdge;
                minOrig = vertexStatus[tmpEdge][0];
                minV = vertexStatus[tmpEdge][1];
            }
            while(!tmpEdge || vertexStatus[tmpEdge][2]);
            vertexStatus[minDest][2] = 1;
            tree.push([minOrig, minDest, minV]);
            vertexNumAdded++;
            nowVertex = minDest;
        }

        return tree;
    }

    // Prim's algorithm another
    static MST_P3 = (links, directional = 0) => {
        // directional 無向 = 0, 有向 = 1
        // links = [[from, to, cost], ...]
        var nowVertex;
        var vertexStatus = {}, vertexTo = {}, tree = [];
        var vertexNumAdded = 0, vertexNum = 0;
        // var minHeap = new heap("min");
        var minHeap = new SMMH();

        var st, ed, cost;
        for(var i in links){
            st = links[i][0];
            ed = links[i][1];
            cost = links[i][2];
            for(var j=0; j<(directional?1:2); j++){
                if(!(st in vertexStatus)){
                    vertexTo[st] = {};
                    vertexStatus[st] = [null, Infinity, 0];
                    vertexNum++;
                }
                if(vertexTo[st][ed]) vertexTo[st][ed] = Math.min(vertexTo[st][ed], cost);
                else vertexTo[st][ed] = cost;

                [st, ed] = [ed, st];
            }
        }

        var setMinEdge = (vertex) => {
            var costTmp;
            for(var i in vertexTo[vertex]){
                if(vertexStatus[i][2]) continue;
                costTmp = vertexTo[vertex][i];

                if(costTmp < vertexStatus[i][1]){
                    minHeap.insert(i, costTmp);
                    vertexStatus[i][0] = vertex;
                    vertexStatus[i][1] = costTmp;
                }
            }
        }

        nowVertex = Object.keys(vertexStatus)[0];
        vertexStatus[nowVertex][1] = -Infinity;
        vertexStatus[nowVertex][2] = 1;
        
        var minV, minDest, minOrig, tmpEdge;
        while(vertexNumAdded < vertexNum - 1){
            setMinEdge(nowVertex);
            do{
                // tmpEdge = minHeap.pop()[0];
                tmpEdge = minHeap.popMin()[0];
            }
            while(vertexStatus[tmpEdge][2])
            
            minDest = tmpEdge;
            minOrig = vertexStatus[tmpEdge][0];
            minV = vertexStatus[tmpEdge][1];
            
            vertexStatus[minDest][2] = 1;
            tree.push([minOrig, minDest, minV]);
            vertexNumAdded++;
            nowVertex = minDest;
        }

        return tree;
    }

    // Kruskal's algorithm
    static MST_K = (links) => {
        var vertexStatus = {}, vertexGroup = {}, tree = []//, links = linksRaw.slice();
        var vertexNum = 0, vertexAddedNum = 0;
        var checkingEdge;

        var vertexTmp;
        for(var i in links){
            for(var j=0; j<2; j++){
                vertexTmp = links[i][j];
                if(!(vertexTmp in vertexStatus)){
                    vertexStatus[vertexTmp] = -1; // what group it belongs
                    vertexNum++;
                }
            }
        }

        links.sort((a,b) => {return a[2]<b[2]?1:-1});

        var getGroupKey = () => {
            for(var i=0; i<vertexNum; i++){
                if(!(i in vertexGroup)){
                    return i;
                }
            }
        }

        var groupKeyTmp;
        while(links.length && (vertexNum-vertexAddedNum)){
            checkingEdge = links.pop();
            if(checkingEdge[0] == checkingEdge[1]) continue;
            
            if(vertexStatus[checkingEdge[0]] == -1 && vertexStatus[checkingEdge[1]] == -1){
                groupKeyTmp = getGroupKey();
                vertexStatus[checkingEdge[0]] = vertexStatus[checkingEdge[1]] = groupKeyTmp;
                vertexGroup[groupKeyTmp] = [checkingEdge[0], checkingEdge[1]];
                tree.push(checkingEdge);
            }
            else if(vertexStatus[checkingEdge[0]] == -1 && vertexStatus[checkingEdge[1]] != -1){
                vertexStatus[checkingEdge[0]] = vertexStatus[checkingEdge[1]];
                vertexGroup[vertexStatus[checkingEdge[1]]].push(checkingEdge[0]);
                tree.push(checkingEdge);
            }
            else if(vertexStatus[checkingEdge[0]] != -1 && vertexStatus[checkingEdge[1]] == -1){
                vertexStatus[checkingEdge[1]] = vertexStatus[checkingEdge[0]];
                vertexGroup[vertexStatus[checkingEdge[0]]].push(checkingEdge[1]);
                tree.push(checkingEdge);
            }
            else if(vertexStatus[checkingEdge[0]] != vertexStatus[checkingEdge[1]]){
                groupKeyTmp = vertexStatus[checkingEdge[0]];
                for(var i in vertexGroup[groupKeyTmp]){
                    vertexStatus[vertexGroup[groupKeyTmp][i]] = vertexStatus[checkingEdge[1]];
                    vertexGroup[vertexStatus[checkingEdge[1]]].push(vertexGroup[groupKeyTmp][i]);
                }
                delete vertexGroup[groupKeyTmp];
                tree.push(checkingEdge);
            }
        }

        return tree;
    }
    
    static inPolygon = (point, polygon) => { // is point in polygon
        if(!Array.isArray(polygon)) return 0;
        var x = point[0] || point.x || 0, y = point[1] || point.y || 0;
        var a = 0, x1, x2, y1, y2, cx;
        for(var i=0; i<polygon.length; i++){
            x1 = polygon[i][0] || polygon[i].x || 0;
            y1 = polygon[i][1] || polygon[i].y || 0;

            x2 = polygon[(i+1)%polygon.length][0] || polygon[(i+1)%polygon.length].x || 0;
            y2 = polygon[(i+1)%polygon.length][1] || polygon[(i+1)%polygon.length].y || 0;
            
            if((y1-y)*(y2-y) > 0 || (x1 < x && x2 < x)) continue;
            cx = (y-y1)*(x2-x1)/(y2-y1) + x1;
            if((x1-cx)*(cx-x2) >= 0 && x <= cx){
                if(cx == x) return 0.5;
                a++;
            }
        }

        return a%2;
    }
    
    static gcPolygon = (polygon) => { // get gravity of center of polygon
        if(!Array.isArray(polygon)) return 0;
        var gx = 0, gy = 0, a = this.areaPolygon(polygon), x1, x2, y1, y2;

        for(var i=0; i<polygon.length; i++){
            x1 = polygon[i][0] || polygon[i].x || 0;
            y1 = polygon[i][1] || polygon[i].y || 0;

            x2 = polygon[(i+1)%polygon.length][0] || polygon[(i+1)%polygon.length].x || 0;
            y2 = polygon[(i+1)%polygon.length][1] || polygon[(i+1)%polygon.length].y || 0;
            
            if(x1-x2) gx += (y1-y2)/(x1-x2)/3 * (x2**3 - x1**3) + (y1-(y1-y2)/(x1-x2)*x1)/2 * (x2**2 - x1**2);
            if(y1-y2) gy += (x1-x2)/(y1-y2)/3 * (y2**3 - y1**3) + (x1-(x1-x2)/(y1-y2)*y1)/2 * (y2**2 - y1**2);
        }
        return [gx/a, -gy/a];
    }
    
    static areaPolygon = (polygon) => { // get area of polygon
        if(!Array.isArray(polygon)) return 0;
        var a = 0, x1, x2, y1, y2;
        for(var i=0; i<polygon.length; i++){
            x1 = polygon[i][0] || polygon[i].x || 0;
            y1 = polygon[i][1] || polygon[i].y || 0;

            x2 = polygon[(i+1)%polygon.length][0] || polygon[(i+1)%polygon.length].x || 0;
            y2 = polygon[(i+1)%polygon.length][1] || polygon[(i+1)%polygon.length].y || 0;
            
            a += (x1 * y2) - (x2 * y1);
        }
        a = Math.abs(a)/2;
        return a;
    }
    
    static untitledFnc = () => {
        return ;
    }
}


/* ----------------------------------- Init Fnc----------------------------------- */


/* ----------------------------------- Math Extend----------------------------------- */
Math.gcd = (a, b) => {
    if(!a || !b) return null;
    var flt = Math.max((a.toString().split(".")[1] || "").length, (b.toString().split(".")[1] || "").length), tmp;
    if(a<b){
        tmp = a;
        a = b;
        b = tmp;
    }
    tmp = Math.round(Math.pow(10, flt) * (a%b)) / Math.pow(10, flt);
    if(tmp != 0){
        return Math.gcd(b, tmp);
    }
    return b;
}
Math.lcm = (a, b) => {
    if(!a || !b) return null;
    return a*b / Math.gcd(a,b);
}
Math.fraction = (a,b) => {
    if(!a || !b) return [null, null];
    var d = Math.gcd(a,b);
    return [a/d, b/d];
}
Math.randomI = (x, m) => {
    x = x ? x : 0;
    m = m ? m : 0;
    return Math.floor(Math.random() * x + m);
}

Math.factor = (n) => { // factorization
    if(typeof n == "number"){
        var w = [], g = Math.sqrt(n);
        while(n > 1){
            if(!(n%2)) {
                w.push(2);
                n /= 2;
                g = Math.sqrt(n);
                continue;
            }
            for(var i=3; i<=g; i+=2){
                if(!(n%i)){
                    w.push(i);
                    n /= i;
                    g = Math.sqrt(n);
                    break;
                }
            }
            if(i>g){
                w.push(n);
                n = g = 1;
            }
        }
        return w;
    }
    return [];
}

/* ----------------------------------- Math Extend----------------------------------- */
/* ---------------------------------- Class Watcher --------------------------------- */
class ClassWatcher {
    constructor(targetNode, classToWatch, classAddedCallback, classRemovedCallback) {
        this.targetNode = targetNode
        this.classToWatch = classToWatch
        this.classAddedCallback = classAddedCallback
        this.classRemovedCallback = classRemovedCallback
        this.observer = null
        this.lastClassState = targetNode.classList.contains(this.classToWatch)

        this.init()
    }

    init() {
        this.observer = new MutationObserver(this.mutationCallback)
        this.observe()
    }

    observe() {
        this.observer.observe(this.targetNode, { attributes: true })
    }

    disconnect() {
        this.observer.disconnect()
    }

    mutationCallback = mutationsList => {
        for(let mutation of mutationsList) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                let currentClassState = mutation.target.classList.contains(this.classToWatch)
                if(this.lastClassState !== currentClassState) {
                    this.lastClassState = currentClassState
                    if(currentClassState) {
                        this.classAddedCallback()
                    }
                    else {
                        this.classRemovedCallback()
                    }
                }
            }
        }
    }
}
/* ---------------------------------- Class Watcher --------------------------------- */
/* ---------------------------------- Table Object ---------------------------------- */
class tableObject{
    constructor({onePageNum: onePageNum = 20, pageBtnShowNum: pageBtnShowNum = 5, getDataConfig: getDataConfig={}, getDataTpye: getDataTpye = 0} = {}){
        var _data = [];
        var _dataNum = 0;

        var _onePageNum = typeof onePageNum == "number" ? onePageNum : 20;
        var _nowPage = 1;
        var _maxPage = 1;
        var _getDataTpye = getDataTpye ? 1 : 0; // 1=get one page one time, 0=get all page one time

        var _pageBtnShowNum = typeof pageBtnShowNum == "number" ? pageBtnShowNum : 5;
        var _pageBtnBox = [];
        var _inpageData = [];
        var _getDataConfig = {
            url: "",
            dataType: "txt",
            method: "GET",
            dataRoute: {
                data: "data",
                dataNum: "dataNum"
            },
            parameter: (_nowPage) => {return {page: _nowPage};},
            callback: [],
        };

        // self data
        this.data = [];
        this.nowPage = 1;
        this.maxPage = 1;
        this.pageBtnBox = [];
        this.inpageData = [];
        this.updateFnc = {};
        this.status = [1];

        // init
        for(var i in _getDataConfig) if(getDataConfig[i] && _getDataConfig[i].constructor == getDataConfig[i].constructor) _getDataConfig[i] = getDataConfig[i].duplicate();
        for(var i in _getDataConfig.dataRoute) _getDataConfig.dataRoute[i] = _getDataConfig.dataRoute[i].split(".");

        // functions
        var _assignData = (target, newData) => {
            while(target.length) target.pop();
            for(var i in newData) target[i] = newData[i];
            target.length = newData.length;
        }

        // ***
        this.updateData = (data, page, force=0) => {
            if(!Array.isArray(data)) {
                console.warn(data, "is not Array");
                return this;
            }
            if(page){
                var tmpPageIdx;
                for(var i=0; i<_onePageNum; i++){
                    tmpPageIdx = (page - 1) * _onePageNum + i;
                    if(i >= data.length) break;
                    _data[tmpPageIdx] = data[i];
                }
            }
            else {
                _data = data;
                _dataNum = data.length;
            }
            _assignData(this.data, _data);
    
            this.selectPage(_nowPage, force);
            // console.log(this, this.data, _data);
            return this;
        }

        this.selectPage = (page, force=0) => {
            _maxPage = Math.floor((_dataNum - 1) / _onePageNum + 1);
            _nowPage = Math.max(Math.min(page, _maxPage), 1);
    
            while(_pageBtnBox.length) _pageBtnBox.pop();
            var s = Math.max(Math.min(_maxPage - _pageBtnShowNum + 1, Math.floor(_nowPage - _pageBtnShowNum / 2) + 1), 1);
            for(var i=0; i<_pageBtnShowNum; i++) _pageBtnBox.push(i + s);
            _assignData(this.pageBtnBox, _pageBtnBox);

            this.nowPage = _nowPage;
            this.maxPage = _maxPage;
            for(var i in this.updateFnc) if(typeof this.updateFnc[i] == "function") this.updateFnc[i](this);
            if((_nowPage == 1 || _getDataTpye) && _data[(_nowPage - 1) * _onePageNum] == undefined || force) {
                var T = this, sendData, tmp;
                this.status[0] = 1; // getting data
                _assignData(T.inpageData, []);
                sendData = _getDataConfig.parameter(_nowPage);

                new HTTPreq(_getDataConfig.url, _getDataConfig.dataType)[_getDataConfig.method.toLowerCase() + "a"](sendData).then((rcv) => {
                    try{
                        var res = supfnc.toJSON(rcv.result), tmpData;
                        tmpData = res;
                        for(var i in _getDataConfig.dataRoute.data) if(tmpData[_getDataConfig.dataRoute.data[i]]) tmpData = tmpData[_getDataConfig.dataRoute.data[i]];

                        if(_getDataTpye){
                            tmp = res;
                            for(var i in _getDataConfig.dataRoute.dataNum) if(tmp[_getDataConfig.dataRoute.dataNum[i]]) tmp = tmp[_getDataConfig.dataRoute.dataNum[i]];
                            
                            if(typeof tmp == "number") T.setDataNum(tmp);
                        }
                        else{
                            T.setDataNum(tmpData.length);
                        }
                        
                        if(tmpData.length) {
                            T.status[0] = 0;
                            T.updateData(tmpData, page, 0);
                        }
                        else if(page == T.nowPage) T.status[0] = 2; // empty data

                        for(var i in _getDataConfig.callback){
                            if(typeof _getDataConfig.callback[i] == "function") _getDataConfig.callback[i](res);
                        }
                    }
                    catch(e){
                        console.error(rcv.result, e)
                        T.status[0] = 3; // get data error
                    }
                });
            }
            else{
                while(_inpageData.length) _inpageData.pop();
                var tmpPageIdx;
                for(var i=0; i<_onePageNum; i++){
                    tmpPageIdx = (_nowPage - 1) * _onePageNum + i;
                    if(tmpPageIdx >= _dataNum) break;
                    _inpageData.push(_data[tmpPageIdx]);
                }
                _assignData(this.inpageData, _inpageData);

                if(_inpageData.length) this.status[0] = 0; // normal status
                else this.status[0] = 2; // empty data
            }
            return this;
        }

        this.setDataNum = (dataNum) => {
            _dataNum = dataNum || _dataNum;
            _maxPage = Math.floor((_dataNum - 1) / _onePageNum + 1);
            _data.length = _dataNum;
            this.maxPage = _maxPage;
            return this;
        }
    
        this.setOnePageNum = (onePageNum) => {
            _onePageNum = onePageNum || _onePageNum;
            this.selectPage(this.nowPage);
            return this;
        }
    
        this.getOnePageNum = () => {
            return _onePageNum;
        }
    
        this.setPageBtnShowNum = (pageBtnShowNum) => {
            _pageBtnShowNum = pageBtnShowNum || _pageBtnShowNum;
            return this;
        }

        this.setParameter = (fnc) => {
            if(typeof fnc == "function") _getDataConfig.parameter = fnc;
        }

        this.bindProxy = (instance) => {
            for(var i in instance) this[i] = instance[i];
            // this.data = instance.data;
            // this.inpageData = instance.inpageData;
            // this.nowPage = instance.nowPage;
            // this.maxPage = instance.maxPage;
            return this;
        }

        // usage (this.tabletest = new tableObject()).bindProxy(this.tabletest);
    }

    static Init = function(){
        var _onePageNum = 20;
        var _getDataTpye = 0;
        var _pageBtnShowNum = 5;
        var _getDataConfig = {
            url: "",
            dataType: "txt",
            method: "GET",
            dataRoute: {
                data: "data",
                dataNum: "dataNum"
            },
            parameter: () => {return [{page: "page"}];},
            callback: []
        };

        return {
            onePageNum:_onePageNum,
            getDataTpye:_getDataTpye,
            pageBtnShowNum:_pageBtnShowNum,
            getDataConfig:_getDataConfig,
        }
    }
}

/* ---------------------------------- Table Object ---------------------------------- */


/* ----------------------------------- Heap Object ---------------------------------- */
class heap{
    constructor(theType = 0){
        this.minmaxMultiply = (theType == "min" || theType === 0) ? 1 : -1;
        this.rootHeap = null;
    }

    insert(pointNowKey, pointNowWeight = 0){
        var nowVertexHeap = {
            key: pointNowKey,
            weight: pointNowWeight,
            children: [],
            childrenNum: [0, 0],
            parent: null,
        }
        
        if(!this.rootHeap){
            this.rootHeap = nowVertexHeap;
        }
        else{
            var tmpHeap = this.rootHeap;
            var chn, insertIdx;
            while(tmpHeap.children.length == 2){
                chn = tmpHeap.childrenNum;
                insertIdx = chn[0] <= chn[1] ? 0 : 1;

                chn[insertIdx]++;
                tmpHeap = tmpHeap.children[insertIdx];
            }

            for(var i=0; i<2; i++){
                if(!tmpHeap.children[i]){
                    tmpHeap.children[i] = nowVertexHeap;
                    tmpHeap.childrenNum[i]++;
                    nowVertexHeap.parent = tmpHeap;
                    break;
                }
            }
            var heapkeylist = ["key", "weight"];
            // if max heap minmaxMultiply = -1
            while(nowVertexHeap.parent && nowVertexHeap.weight * this.minmaxMultiply < nowVertexHeap.parent.weight * this.minmaxMultiply){
                for(var i in heapkeylist){
                    [nowVertexHeap[heapkeylist[i]], nowVertexHeap.parent[heapkeylist[i]]] = [nowVertexHeap.parent[heapkeylist[i]], nowVertexHeap[heapkeylist[i]]];
                }
                nowVertexHeap = nowVertexHeap.parent;
            }
        }
    }

    pop(){
        if(!this.rootHeap) return null;
        var tmpHeap = this.rootHeap;
        var rtn = [tmpHeap.key, tmpHeap.weight], minV, minIdx;

        while(tmpHeap.children.length){
            minV = Infinity;
            for(var i in tmpHeap.children){
                // if max heap minmaxMultiply = -1
                if(tmpHeap.children[i].weight * this.minmaxMultiply < minV * this.minmaxMultiply){
                    minV = tmpHeap.children[i].weight;
                    minIdx = i;
                }
            }
            tmpHeap.key = tmpHeap.children[minIdx].key;
            tmpHeap.weight = tmpHeap.children[minIdx].weight;
            tmpHeap.childrenNum[minIdx]--;

            tmpHeap = tmpHeap.children[minIdx];
        }
        if(tmpHeap.parent) tmpHeap.parent.children.splice(minIdx,1);

        return rtn;
    }

    get(){
        if(!this.rootHeap) return null;
        return [this.rootHeap.key, this.rootHeap.weight];
    }
}
/*
var h = new heap()
h.insert("A", 5)
h.insert("B", 8)
h.insert("C", 4)
h.insert("D", 10)
h.insert("E", 6)
h.insert("F", 7)
h.insert("G", 5)
console.log(minVertexHeap, minVertexHeapTop)
*/


class SMMH{
    constructor(){
        this.rootHeap = {
            key: null,
            weight: null,
            children: [],
            childrenNum: [0, 0],
            parent: null,
        }
    }

    insert(pointNowKey, pointNowWeight = 0){
        var tmpHeap = this.rootHeap, chn, insertIdx;

        var nowVertexHeap = {
            key: pointNowKey,
            weight: pointNowWeight,
            children: [],
            childrenNum: [0, 0],
            parent: null,
        };

        while(tmpHeap.children.length == 2){
            chn = tmpHeap.childrenNum;
            insertIdx = chn[0] <= chn[1] ? 0 : 1;

            chn[insertIdx]++;
            tmpHeap = tmpHeap.children[insertIdx];
        }

        for(var i=0; i<2; i++){
            if(!tmpHeap.children[i]){
                tmpHeap.children[i] = nowVertexHeap;
                tmpHeap.childrenNum[i]++;
                nowVertexHeap.parent = tmpHeap;
                insertIdx = i;
                break;
            }
        }
        tmpHeap = nowVertexHeap;

        if(tmpHeap.parent.children.length == 2 && tmpHeap.weight * Math.pow(-1, insertIdx) > tmpHeap.parent.children[insertIdx?0:1].weight * Math.pow(-1, insertIdx)){
            [tmpHeap.parent.children[0].weight, tmpHeap.parent.children[1].weight] = [tmpHeap.parent.children[1].weight, tmpHeap.parent.children[0].weight];
            [tmpHeap.parent.children[0].key, tmpHeap.parent.children[1].key] = [tmpHeap.parent.children[1].key, tmpHeap.parent.children[0].key];
            tmpHeap = tmpHeap.parent.children[insertIdx?0:1];
        }
        
        while(tmpHeap.parent.parent && (tmpHeap.weight < tmpHeap.parent.parent.children[0].weight || tmpHeap.parent.parent.children[1] && tmpHeap.weight > tmpHeap.parent.parent.children[1].weight)){
            if(tmpHeap.weight < tmpHeap.parent.parent.children[0].weight){
                [tmpHeap.weight, tmpHeap.parent.parent.children[0].weight] = [tmpHeap.parent.parent.children[0].weight, tmpHeap.weight];
                [tmpHeap.key, tmpHeap.parent.parent.children[0].key] = [tmpHeap.parent.parent.children[0].key, tmpHeap.key];
                tmpHeap = tmpHeap.parent.parent.children[0];
            }
            else{
                [tmpHeap.weight, tmpHeap.parent.parent.children[1].weight] = [tmpHeap.parent.parent.children[1].weight, tmpHeap.weight];
                [tmpHeap.key, tmpHeap.parent.parent.children[1].key] = [tmpHeap.parent.parent.children[1].key, tmpHeap.key];
                tmpHeap = tmpHeap.parent.parent.children[1];
            }
        }
    }

    pop(popIdx){
        if(!this.rootHeap.children.length) return null;
        popIdx = popIdx ? 1 : 0;
        var minmaxMultiply = popIdx ? -1 : 1;

        var getValue = (list, index) => {
            if(!list) return null;
            return list[Math.min(index, list.length - 1)];
        }

        var tmpHeap = this.rootHeap;
        var rtn = [getValue(tmpHeap.children, popIdx).key, getValue(tmpHeap.children, popIdx).weight];
        var leftNode, rightNode;

        [leftNode, rightNode] = tmpHeap.children;
        while((leftNode && leftNode.children.length) || (rightNode && rightNode.children.length)){
            if(!getValue(leftNode.children, popIdx) || (getValue(rightNode.children, popIdx) && minmaxMultiply * getValue(leftNode.children, popIdx).weight >= minmaxMultiply * getValue(rightNode.children, popIdx).weight)){
                getValue(tmpHeap.children, popIdx).key = getValue(rightNode.children, popIdx).key;
                getValue(tmpHeap.children, popIdx).weight = getValue(rightNode.children, popIdx).weight;
                tmpHeap.childrenNum[1]--;
                tmpHeap = rightNode;
            }
            else if(!getValue(rightNode.children, popIdx) || (getValue(leftNode.children, popIdx) && minmaxMultiply * getValue(leftNode.children, popIdx).weight < minmaxMultiply * getValue(rightNode.children, popIdx).weight)){
                getValue(tmpHeap.children, popIdx).key = getValue(leftNode.children, popIdx).key;
                getValue(tmpHeap.children, popIdx).weight = getValue(leftNode.children, popIdx).weight;
                tmpHeap.childrenNum[0]--;
                tmpHeap = leftNode;
            }
            
            [leftNode, rightNode] = tmpHeap.children;
        }
        
        tmpHeap.children.splice(Math.min(tmpHeap.children.length-1, popIdx),1);
        tmpHeap.childrenNum.splice(Math.min(tmpHeap.childrenNum.length-1, popIdx),1);
        tmpHeap.childrenNum[1] = 0;

        return rtn;
    }

    popMin(){
        return this.pop(0);
    }

    popMax(){
        return this.pop(1);
    }

    getMin(){
        if(!this.rootHeap.children.length) return null;
        return [this.rootHeap.children[0].key, this.rootHeap.children[0].weight];
    }

    getMax(){
        if(!this.rootHeap.children.length) return null;
        return [this.rootHeap.children.slice(-1)[0].key, this.rootHeap.children.slice(-1)[0].weight];
    }
}
/* ----------------------------------- Heap Object ---------------------------------- */