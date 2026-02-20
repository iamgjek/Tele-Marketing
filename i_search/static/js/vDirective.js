/*
    v-focus                 focus onload
    v-preload               replace noimg when image not found
    v-sticker               sticker like memo
    v-stickerShadow         opened sticker
    v-contextmenu           rightclick menu
    v-reactfont             autosizing to fit container's width
    v-tagchange             change outer HTML
    v-reactinput            extend input width when text overflow
    v-clickcopy             click to copy content
    v-dropdownmenu          dropdown floating block
    v-dropdownmenublock     dropdown block
    v-biphasic              on off btuuon
    v-title                 hover show title text
    v-movehome              move itself to another node
    v-scrollload            simulate loading when scrolling items into sight
    v-relativepos           move animate when scroll
    v-number                set number if out of range
    v-stick                 fix at specific position
    v-textarea              autosizing height for textarea
    v-password              click or hover to see password
    v-edit                  create edit enter cancel button
    v-elasticinput          focus extend and blur retract
*/

baseapp.directive('focus', {
    mounted(el) {
        el.focus();
    }
});

// ------------------------------------------------------------------------------------- //
let imageIsExist = function (url) {
    return new Promise((resolve) => {
        var img = new Image();
        img.onload = function () {
            if (this.complete == true) {
                resolve([img.width, img.height]);
                img = null;
            }
        }
        img.onerror = function () {
            resolve([0, 0]);
            img = null;
        }
        img.src = url;
    });
}

// ------------------------------------------------------------------------------------- //
async function preload(el, binding) {
    let defaultImg = '/system/noimg'; //預設圖片
    let newLoadImg = binding.value; //欲載入的新圖片
    var type = binding.modifiers.backgroundimage ? "backgroundimage" : "src";
    
    let exist = await imageIsExist(defaultImg);
    if (exist[0] && exist[1]) {
        el.w = exist[0];
        el.h = exist[1];
    }

    switch(type){
        case "src":
        el.setAttribute("src", defaultImg);
            break;
        case "backgroundimage":
            el.style.backgroundImage = "url(" + defaultImg + ")";
    }

    if (newLoadImg) {
        //await : 等待判斷結果回傳
        let exist = await imageIsExist(newLoadImg);
        if (exist[0] && exist[1]) {
            switch(type){
                case "src":
                    el.setAttribute("src", newLoadImg);
                    el.w = exist[0];
                    el.h = exist[1];
                    break;
                case "backgroundimage":
                    el.style.backgroundImage = "url(" + newLoadImg + ")";
            }
        }
        else {
            // el.setAttribute(binding.type, defaultImg);
            el.setAttribute('title', 'image not found');
        }
    }


    if(typeof el.preloadSetRatio == "function"){
        el.container.style.width = "";
        el.container.style.height = "";
        el.div.style.width = "";
        el.div.style.height = "";
        // Vue.nextTick(()=>{
            el.preloadSetRatio();
        // });
    }
}

baseapp.directive('preload', {
    mounted: function (el, binding) {
        var size = (binding.arg || "").match(/^[hw]\d+(\:?\d+)?$/), dir, rate;
        if(size){
            el.container = supfnc.createElement("div", {style:{ display: "inline-block", overflow: "hidden"}, class:["align-middle"]});
            el.div = supfnc.createElement("div", {style:{display: "inline-block", overflow: "hidden"}});
            var idx = Array.prototype.slice.call(el.parentElement.children).indexOf(el);

            el.parentElement.insertBefore(el.container, el.parentElement.children[idx]);
            el.container.appendChild(el.div);
            el.div.appendChild(el);

            size = (size || [""])
            size = size[0];
            dir = size[0];
            rate = size.slice(1).split(":");
            rate = rate[0] / rate[1]; // 0 == w, 1 == h

            el.preloadSetRatio = () => {
                var W = el.offsetWidth, H = el.offsetHeight;
                if(size){ 
                    if(dir == "h"){
                        el.container.style.width = H * rate + "px";
                        el.div.style.width = H * rate + "px";
                        el.div.style.transform = "translateX(-" + Math.max(50*(rate-1), 0) + "%)";
                        el.style.transform = "translateX(" + Math.max(25*(rate-1), 0) + "%)";
                    }
                    else{
                        el.container.style.height = W / rate + "px";
                        el.div.style.height = W / rate + "px";
                        el.div.style.transform = "translateY(-" + Math.max(50*(rate-1), 0) + "%)";
                        el.style.transform = "translateY(" + Math.max(25*(rate-1), 0) + "%)";
                    }
                    console.log(W, H, rate)
                }
            }
            window.addEventListener("resize", el.preloadSetRatio);
        }
        
        preload(el, binding);
    },
    updated: function (el, binding) {
        if (_.isEqual(binding.value, binding.oldValue)) return 0;
        preload(el, binding);
    }
});

// ------------------------------------------------------------------------------------- //
baseapp.directive('sticker', {
    mounted(el, binding) {
        var rotate = (parseInt(Math.random() * 13) - 6);
        el.style.background = '#' + ["ccf", "cfc", "fcc", "fcf", "ffc"][parseInt(Math.random() * 5)];
        el.style.transform = "rotate(" + rotate + "deg)";
        el.style.height = "";
        el.style.width = "";
        el.style.transition = "all 0.5s ease";
        el.addEventListener('mouseover', function () {
            if (window.innerWidth < 1000) return;
            el.style.transform = "scale(1.2)";
        });
        el.addEventListener('mouseleave', function () {
            if (window.innerWidth < 1000) return;
            el.style.transform = "rotate(" + rotate + "deg)";
        });

        if (binding.arg[binding.value]) {
            binding.arg[binding.value].orig = el;
            for (var i in el.style) {
                if (i == "display") { binding.arg[binding.value].shadow.style[i] = "none"; }
                else binding.arg[binding.value].shadow.style[i] = el.style[i];
            }
            binding.arg[binding.value].shadow.style.display = "none";
        }
        else {
            binding.arg[binding.value] = {};
            binding.arg[binding.value].orig = el;
        }
    },
    beforeUpdate(el, binding){
        if (_.isEqual(binding.value, binding.oldValue)) return 0;
        delete binding.arg[binding.oldValue];
        if (binding.arg[binding.value]) {
            binding.arg[binding.value].orig = el;
            for (var i in el.style) {
                if (i == "display") { binding.arg[binding.value].shadow.style[i] = "none"; }
                else binding.arg[binding.value].shadow.style[i] = el.style[i];
            }
            binding.arg[binding.value].shadow.style.display = "none";
        }
        else {
            binding.arg[binding.value] = {};
            binding.arg[binding.value].orig = el;
        }
    }
});

// ------------------------------------------------------------------------------------- //
baseapp.directive('stickerShadow', {
    mounted(el, binding) {
        if (binding.arg[binding.value]) {
            binding.arg[binding.value].shadow = el;
            for (var i in el.style) {
                if (i == "display") el.style[i] = "none";
                else el.style[i] = binding.arg[binding.value].orig.style[i];
            }
        }
        else {
            el.style["display"] = "none";
            binding.arg[binding.value] = {};
            binding.arg[binding.value].shadow = el;
        }
    },
    beforeUpdate(el, binding){
        if (_.isEqual(binding.value, binding.oldValue)) return 0;
        delete binding.arg[binding.oldValue];
        if (binding.arg[binding.value]) {
            binding.arg[binding.value].shadow = el;
            for (var i in el.style) {
                if (i == "display") el.style[i] = "none";
                else el.style[i] = binding.arg[binding.value].orig.style[i];
            }
        }
        else {
            el.style["display"] = "none";
            binding.arg[binding.value] = {};
            binding.arg[binding.value].shadow = el;
        }
    }
});

// ------------------------------------------------------------------------------------- //
function contextmenu(el, binding, update) {
    if(binding.value == null) return;
    if (binding.value.url == "BACKAPAGE") {
        var a = window.location.href.split('/');
        a.pop();
        binding.value.url = a.join("/");
    }

    if (binding.value.args != undefined) {
        var nowarg = window.location.href.split("?")[1];
        if (nowarg) nowarg = nowarg.split("&");
        var args = {};
        for (var i in nowarg) {
            if (nowarg[i] == "") continue;
            nowarg[i] = nowarg[i].split("=");
            args[nowarg[i][0]] = nowarg[i][1];
        }
        for (var i in binding.value.args) {
            if (binding.value.args[i] != undefined) {
                args[i] = binding.value.args[i];
            }
            else {
                delete args[i]
            }
        }
        if(args.lengthX()) binding.value.url += "?";
        for (var i in args) {
            binding.value.url += i + "=" + args[i] + "&";
        }
        if (binding.value.url.length > 1) binding.value.url = binding.value.url.slice(0, binding.value.url.length - 1);
        else binding.value.url = window.location.href.split("/").last().split("?")[0];
    }

    if (update) {
        if (binding.arg == "link") el.removeEventListener("click", el.clickE_contextmenu);
        el.removeEventListener("contextmenu", el.contextmenuE_contextmenu);
    }

    var a=document.createElement("a");
    a.href = binding.value.url;
    if(binding.arg == "link") el.setAttribute("custom-title", a.href);
    
    el.clickE_contextmenu = function (e) {
        binding.instance.$root.goto(binding.value.url);
    }
    el.contextmenuE_contextmenu = function (e) {
        e.preventDefault();
        binding.instance.$root.rightClickMenuOpen(e, binding.arg, binding.value);
    }

    if (binding.arg == "link") el.addEventListener("click", el.clickE_contextmenu);
    el.addEventListener("contextmenu", el.contextmenuE_contextmenu);
}

baseapp.directive('contextmenu', {
    mounted(el, binding) {
        contextmenu(el, binding, 0);
        if(binding.modifiers.default) {
            el.classList.add("btn");
            el.classList.add("btn-light");
        }
    },
    updated(el, binding) {
        if (_.isEqual(binding.value, binding.oldValue)) return 0;
        contextmenu(el, binding, 1);
    }
});

// ------------------------------------------------------------------------------------- //
function reactfont(el, binding) {
    var maxSize = binding.value ? binding.value : 28;
    var containerW = el.parentElement.offsetWidth, ctxW = el.offsetWidth;
    var fs = parseInt(window.getComputedStyle(el, null).getPropertyValue('font-size'));
    fs = Math.min(maxSize, parseInt((containerW / ctxW) * fs));
    el.style.fontSize = fs + 'px';
}

baseapp.directive('reactfont', {
    mounted(el, binding) {
        reactfont(el, binding);
    },
    updated(el, binding) {
        if (_.isEqual(binding.value, binding.oldValue)) return 0;
        reactfont(el, binding);
    }
});

// ------------------------------------------------------------------------------------- //
function tagchange(el, binding) {
    var outerHtmlTag = el.outerHTML.match(new RegExp("(?<=\\<)[\\w]+(?=(\\>|\\s))"))[0];
    var reg = new RegExp("^(\<)" + outerHtmlTag + "|" + outerHtmlTag + "(\>)$", "g");
    el.outerHTML = el.outerHTML.replace(reg, "$1" + binding.value + "$2");
}

baseapp.directive('tagchange', {
    mounted(el, binding) {
        tagchange(el, binding);
    },
    updated(el, binding) {
        if (_.isEqual(binding.value, binding.oldValue)) return 0;
        tagchange(el, binding);
    }
});

// ------------------------------------------------------------------------------------- //
baseapp.directive('reactinput', {
    mounted(el, binding) {
        var div = document.createElement("div");
        var span = document.createElement("span");
        div.style.height = "0";
        div.style.overflow = "hidden";
        span.innerText = binding.value;
        div.appendChild(span);
        el.parentElement.appendChild(div);
        el.defaultWidth = el.offsetWidth;
        el.bindingID = supfnc.randAlphabet(10);
        span.setAttribute("id", el.bindingID)
    },
    updated(el, binding) {
        if (_.isEqual(binding.value, binding.oldValue)) return 0;
        var span = document.getElementById(el.bindingID);
        span.innerText = binding.value;
        el.style.width = "min(" + Math.max(span.offsetWidth + 10, el.defaultWidth) + "px, 100%)";
    }
});

// ------------------------------------------------------------------------------------- //
baseapp.directive('clickcopy', {
    mounted(el, binding) {
        if(!binding.value) binding.value = {};
        binding.value.hoverTxt = binding.value.hoverTxt || "點擊複製!";
        binding.value.copyTxt = binding.value.copyTxt || "已複製!";
        
        var origColor = el.style.color || "currentColor";
        var type = document.createAttribute(binding.value.type);
        el.style.cursor = "pointer";
        el.style.transition = ".3s";
        el.inter = -1;
        el.style.zIndex = "999";
        el.origColor = window.getComputedStyle(el, null).getPropertyValue("color");

        type.textContent = binding.value.hoverTxt;
        el.attributes.setNamedItem(type);

        el.addEventListener("mouseenter", function(){
            el.style.color = "#4263eb";
        });
        el.addEventListener("mouseleave", function(){
            el.style.color = el.origColor;
        });
        el.addEventListener("click", function(){
            var t = 0;
            supfnc.clickCopy(el);

            type.textContent = binding.value.copyTxt;
            el.attributes.setNamedItem(type);
            type.style.zIndex = "999";

            if(el.inter == -1){
                el.inter = setInterval(() => {
                    el.style.transform = "scale(" + (1 + 2 * Math.exp(-t/20) * Math.cos(20 * (Math.PI/360) * t)) +")";
                    t++;
                    if(t>100) {
                        clearInterval(el.inter);
                        el.inter = -1;
                        el.style.transform = "";
                        
                        type.textContent = binding.value.hoverTxt;
                        el.attributes.setNamedItem(type);
                        type.style.zIndex = "";
                    }
                }, 10);
            }
        });
        
    }
});

// ------------------------------------------------------------------------------------- //
// 在target內的按鈕 加上cblur="1" => 點完清單消失
// modifiers hideonlymobile absolute (top bottom)*(left right) (left right)*(up down)
function dropdownmenu(el, binding, update) {
    if (update) {
        el.removeEventListener("click", el.clickE_dropdownmenu);
        el.removeEventListener("contextmenu", el.contextmenuE_dropdownmenu);
        el.target.removeEventListener("blur", el.blurE_dropdownmenu);
    }

    el.blurE_dropdownmenu = function(e){
        // e.stopPropagation();
        // console.log(e.relatedTarget)
        if(e.relatedTarget && !('display' in e.relatedTarget)){
            e.relatedTarget.addEventListener("blur", function(ee){
                if(ee.relatedTarget != el.target){
                    el.clickE_dropdownmenu(e, 0);
                    // el.target.focus();
                    // setTimeout(function(){el.target.blur();}, 1);
                }
            });
            return;
        }
        el.display = 0;
        el.target.classList.add(binding.modifiers.hideonlymobile ? "dropdownMenuHideMobile":"dropdownMenuHide");
        
        el.isBlur = true;
        setTimeout(function(){
            el.isBlur = false;
        }, 200);
    }
    el.clickE_dropdownmenu = function (e, option) {
        e.stopPropagation();
        var clickInTarget = 0, offsetElTarget = [0, 0], ex = el.target, trX, trY;
        for(var i in e.path) if(e.path[i] == el.target) {clickInTarget = 1; break;}
        if((!el.isBlur && !clickInTarget) || e.path[0].getAttribute("cblur") || option != undefined){
            if(option != undefined) el.display = option;
            else el.display ^= 1;
            if(el.display){
                el.target.classList.remove(binding.modifiers.hideonlymobile ? "dropdownMenuHideMobile":"dropdownMenuHide");
                while(ex != el){
                    // console.log(ex, ex.offsetLeft, el.target, el.target.offsetLeft)
                    offsetElTarget[0] += ex.offsetLeft;
                    offsetElTarget[1] += ex.offsetTop;
                    ex = ex.parentElement;
                }
                // console.log(offsetElTarget,  el.target.offsetWidth, el.getBoundingClientRect().x, el.target.offsetWidth, window.innerWidth);
                // var trX = Math.max(-offsetElTarget[0] - el.target.offsetWidth, el.getBoundingClientRect().x + el.target.offsetWidth - window.innerWidth);
                // var trY = -offsetElTarget[1];
                
                if(binding.modifiers.leftup){
                    trX = - offsetElTarget[0] - el.target.offsetWidth;
                    trY = - offsetElTarget[1] - el.target.offsetHeight + el.offsetHeight;
                }
                else if(binding.modifiers.leftdown){
                    trX = - offsetElTarget[0] - el.target.offsetWidth;
                    trY = - offsetElTarget[1];
                }
                else if(binding.modifiers.rightup){
                    trX = - offsetElTarget[0] - el.offsetWidth;
                    trY = - offsetElTarget[1] - el.target.offsetHeight + el.offsetHeight;
                }
                else if(binding.modifiers.rightdown){
                    trX = - offsetElTarget[0] - el.offsetWidth;
                    trY = - offsetElTarget[1];
                }
                else if(binding.modifiers.topleft){
                    trX = - offsetElTarget[0] - el.target.offsetWidth + el.offsetWidth;
                    trY = - offsetElTarget[1] - el.target.offsetHeight;
                }
                else if(binding.modifiers.topright){
                    trX = - offsetElTarget[0];
                    trY = - offsetElTarget[1] - el.target.offsetHeight;
                }
                else if(binding.modifiers.bottomleft){
                    trX = - offsetElTarget[0] - el.target.offsetWidth + el.offsetWidth;
                    trY = - offsetElTarget[1] + el.offsetHeight;
                }
                else if(binding.modifiers.bottomright){
                    trX = - offsetElTarget[0];
                    trY = - offsetElTarget[1] + el.offsetHeight;
                }

                el.target.style.transform = "translate(" + trX + "px, " + trY + "px)";
            }
            else{
                el.target.classList.add(binding.modifiers.hideonlymobile ? "dropdownMenuHideMobile":"dropdownMenuHide");
            }
        }
        if(el.display) el.target.focus();
    }
    el.contextmenuE_dropdownmenu = function (e) {
        e.preventDefault();
    }

    el.addEventListener("click", el.clickE_dropdownmenu);
    el.addEventListener("contextmenu", el.contextmenuE_dropdownmenu);
    el.target.addEventListener("blur", el.blurE_dropdownmenu);
}

baseapp.directive('dropdownmenu', {
    mounted(el, binding) {
        el.display = 0;
        
        el.target = document.getElementById(binding.value);
        el.target.style.userSelect = "none";
        el.target.style.cursor = "default";
        el.target.parentElement.style.position = "relative";
        el.target.setAttribute("tabindex", 10);
        el.target.classList.add(binding.modifiers.hideonlymobile ? "dropdownMenuHideMobile":"dropdownMenuHide");
        el.target.classList.add("dropdownMenu");
        if(binding.modifiers.absolute) el.target.style.position = "absolute";
        dropdownmenu(el, binding, 0);
    },
    updated(el, binding) {
        if (_.isEqual(binding.value, binding.oldValue)) return 0;
        dropdownmenu(el, binding, 1);
    }
});

// ------------------------------------------------------------------------------------- //
function dropdownmenublock(el, binding, update) {
    function ddmbSetHeight(el, binding){
        var child = el.target.children, chNum = child.length, h=0, cNum, offsetY;
        var eltProperty = window.getComputedStyle(el.target, null);
        var colNum = eltProperty.getPropertyValue('grid-template-columns').split(' ').length;
        offsetY = parseInt(eltProperty.getPropertyValue("padding-top")) + parseInt(eltProperty.getPropertyValue("padding-bottom")) + parseInt(eltProperty.getPropertyValue("border-top-width")) + parseInt(eltProperty.getPropertyValue("border-bottom-width"));
        
        if(el.display || window.innerWidth > binding.arg){
            for(var i=0; i<parseFloat(chNum/colNum); i++){
                var tmp = window.getComputedStyle(child[i*colNum], null);
                h += child[i*colNum].offsetHeight + parseInt(tmp.getPropertyValue("margin-top")) + parseInt(tmp.getPropertyValue("margin-bottom"));
            }
            el.target.style.maxHeight = offsetY + h + "px";
            setTimeout(()=>{
                if(el.display || window.innerWidth > binding.arg) el.target.style.overflow = "";
            },300);
        }
        else{
            if(el.retractH.match(/\d+c/)){
                cNum = parseFloat(el.retractH);
                for(var i=0; i<Math.min(Math.ceil(cNum)*colNum, chNum); i+=colNum){
                    h += child[i*colNum].offsetHeight * (cNum - i < 1 ? cNum - i : 1);
                }
                el.target.style.maxHeight = offsetY + h + "px";
            }
            else{
                el.target.style.maxHeight = el.retractH;
            }
            el.target.style.overflow = "hidden";
        }
        var pE = window.getComputedStyle(el.parentElement, null);
        var posY = parseInt(pE.getPropertyValue("padding-top")) + child[0].getBoundingClientRect().height/2 - el.getBoundingClientRect().height/2;
        if(pE.getPropertyValue("position") == "relative"){
            el.style.top = posY + "px";
        }
        else{
            el.style.top = posY + el.parentElement.offsetTop + "px";
        }
        
        el.style.right = "16px"; // @@@@
    }
    
    if(typeof binding.value == "string"){
        el.targetID = binding.value;
        el.retractH = "1c"; // 1c = 1 child height
    }
    else if(Object.isDict(binding.value)){
        el.targetID = binding.value.targetID;
        el.retractH = binding.value.retractH;
    }
    el.target = document.getElementById(el.targetID);

    if (update) {
        el.removeEventListener("click", el.clickE_dropdownmenublock);
        window.removeEventListener("resize", el.resizeE_dropdownmenublock);
    }

    el.clickE_dropdownmenublock = function (e) {
        el.display ^= 1;
        ddmbSetHeight(el, binding);
    }
    el.resizeE_dropdownmenublock = function(e){
        ddmbSetHeight(el, binding);
    }
    el.addEventListener("click", el.clickE_dropdownmenublock);
    window.addEventListener("resize", el.resizeE_dropdownmenublock);
}

baseapp.directive('dropdownmenublock', {
    mounted(el, binding) {
        el.display = 1;
        dropdownmenublock(el, binding, 0);
        el.target.style.transition = ".3s linear";
        Vue.nextTick(()=>{
            el.clickE_dropdownmenublock();
        });
    },
    updated(el, binding) {
        if (_.isEqual(binding.value, binding.oldValue)) return 0;
        dropdownmenublock(el, binding, 1);
    }
});

// ------------------------------------------------------------------------------------- //
function biphasic(el, binding){
    function setBarPos(enable){
        if(Array.isArray(enable)) enable = enable[0];
        el.children[0].style.transform = enable ? "translateX(0px)" : "translateX(-" + (el.txtW - el.switchBarW) + "px)";
        el.children[1].style.left = enable ? el.txtW + "px" : "0";
    }
    binding.arg = binding.arg.split(",");
    binding.arg = {
        on: binding.arg[0],
        off: binding.arg[1],
        title: binding.arg[2],
    }

    el.removeEventListener("click", el.clickE_biphasic);
    el.children[0].children[0].innerText = binding.arg.on;
    el.children[0].children[1].innerText = binding.arg.off;
    el.children[0].children[0].classList.add("biphasicOn");
    el.children[0].children[1].classList.add("biphasicOff");

    var div = document.createElement("div"), p;
    div.style.opacity = 0;
    div.classList.add("d-inline-block");
    document.getElementsByTagName("body")[0].appendChild(div);

    div.innerText = binding.arg.on;
    p = window.getComputedStyle(el.children[0].children[0], null);
    el.txtW = div.offsetWidth + parseInt(p.getPropertyValue("padding-left")) + parseInt(p.getPropertyValue("padding-right"));

    div.innerText = binding.arg.off;
    p = window.getComputedStyle(el.children[0].children[1], null);
    el.txtW = Math.max(el.txtW, div.offsetWidth + parseInt(p.getPropertyValue("padding-left")) + parseInt(p.getPropertyValue("padding-right")));
    div.remove();

    Vue.nextTick(()=>{
        el.style.width = (el.txtW + el.switchBarW) + "px";
        el.children[0].style.width = 2 * el.txtW + "px";
        el.children[0].children[0].style.width = el.children[0].children[1].style.width = el.txtW + "px";
        setTimeout(()=>{
            setBarPos(el.switch);
        },10);
    });
    
    el.clickE_biphasic = function (e, value) {
        if(binding.modifiers.indep){
            el.switch = binding.value;
        }
        else{
            if(Array.isArray(el.switch)) {
                if(value == undefined) el.switch[0] ^= 1;
                else el.switch[0] = value;
            }
            else{
                if(value == undefined) el.switch ^= 1;
                else el.switch = value;
            }
        }
        
        setBarPos(el.switch)
    }
    el.addEventListener("click", el.clickE_biphasic);
}

baseapp.directive('biphasic', {
    mounted(el, binding) {
        el.switch = binding.value;
        el.classList.add("biphasicBtn");
        for(var i=0; i<2; i++) el.appendChild(document.createElement("div"));
        for(var i=0; i<2; i++) el.children[0].appendChild(document.createElement("p"));

        var div = document.createElement("div");
        div.style.opacity = 0;
        div.classList.add("biphasicBtnSwitchBar");
        document.getElementsByTagName("body")[0].appendChild(div);
        el.switchBarW = div.offsetWidth;

        setTimeout(()=>{
            div.remove();
            el.children[0].style.transition = "0s";
            
            el.children[0].style.transform = "translateX(-" + (el.txtW - el.switchBarW) + "px)";
            setTimeout(()=>{
                el.children[0].style.transition = "";
            },10);
        },10);
        el.children[1].classList.add("biphasicBtnSwitchBar");
        biphasic(el, binding);
    },
    updated(el, binding) {
        if (_.isEqual(binding.value, binding.oldValue)) return 0;
        el.switch = binding.value;
        // console.log(el, binding.value)
        biphasic(el, binding);
    }
});

// ------------------------------------------------------------------------------------- //
baseapp.directive('title', {
    mounted(el, binding) {
        el.setAttribute(binding.value.type, binding.value.text);
    },
    beforeUpdate(el, binding) {
        el.setAttribute(binding.value.type, binding.value.text);
    }
});

// ------------------------------------------------------------------------------------- //
baseapp.directive('movehome', {
    mounted(el, binding) {
        var target = document.getElementById(binding.value);
        target.appendChild(el);
    },
    beforeUpdate(el, binding) {
        if(binding.value == binding.oldValue) return 0;
        var target = document.getElementById(binding.value);
        target.appendChild(el);
    }
});

// ------------------------------------------------------------------------------------- //
var scrollload = (el, binding)=>{
    var target = document.getElementById(binding.value);
    if(target != el.target){
        el.target = target;
        el.target.removeEventListener("scroll", el.scrollE_scrollload);
    }
    
    el.scrollE_scrollload = (event) => {
        var range = el.target.offsetHeight;
        var nowDY = el.getBoundingClientRect().y - parseInt(window.getComputedStyle(el, null).getPropertyValue("margin-top")) - el.target.getBoundingClientRect().y - parseInt(window.getComputedStyle(el.target, null).getPropertyValue("padding-top"));
        
        if(-30 - 0.8 * el.offsetHeight < nowDY && nowDY < range - 50){
            if(!el.show){
                el.show = 1;
                if(el.preDY < nowDY){
                    TweenMax.to(el, 1, {y: 0, opacity: 1}, 0.5);
                }
                else {
                    TweenMax.to(el, 1, {y: 0, opacity: 1}, 0.5);
                }
            }
        }
        else{
            if(el.show){
                el.show = 0;
                if(el.preDY < nowDY){
                    TweenMax.to(el, 1, {y: 30, opacity: 0}, 0.5);
                }
                else {
                    TweenMax.to(el, 1, {y: -30, opacity: 0}, 0.5);
                }
            }
        }
        el.preDY = nowDY;
    }
    
    el.target.addEventListener("scroll", el.scrollE_scrollload);
}
baseapp.directive('scrollload', {
    mounted(el, binding) {
        el.show = 0;
        el.target = document.getElementById(binding.value);
        el.preDY = el.getBoundingClientRect().y - parseInt(window.getComputedStyle(el, null).getPropertyValue("padding-top")) - el.target.getBoundingClientRect().y - parseInt(window.getComputedStyle(el.target, null).getPropertyValue("margin-top"));
        scrollload(el, binding);
        TweenMax.to(el, 0, {y: 30, opacity: 0});
        setTimeout(()=>{
            el.target.dispatchEvent(new CustomEvent("scroll"))
        },10)
        
    },
    beforeUpdate(el, binding) {
        if(binding.value == binding.oldValue) return 0;
        scrollload(el, binding);
    }
});

// ------------------------------------------------------------------------------------- //
var relativepos = (el, binding) => {
    var target = document.getElementById(binding.value);
    if(target != el.target){
        el.target = target;
        el.target.removeEventListener("scroll", el.scrollE_relativepos);
    }

    el.scrollE_relativepos = (event) => {
        el.nowY = el.target.scrollTop;
        el.Timeline.clear().to(el, 0.01, {y: "+=" + (el.befY - el.nowY)}).to(el, 0.8, {y: 0}).play();
        el.befY = el.target.scrollTop;
    }

    el.target.addEventListener("scroll", el.scrollE_relativepos);
}
baseapp.directive('relativepos', {
    mounted(el, binding) {
        el.target = document.getElementById(binding.value);
        el.Timeline = new TimelineMax();
        el.nowY = 0;
        el.befY = 0;
        relativepos(el, binding);
    },
    beforeUpdate(el, binding) {
        if(binding.value == binding.oldValue) return 0;
        relativepos(el, binding);
    }
});
// ------------------------------------------------------------------------------------- //
function vnumber(el, binding){
    var numfy = binding.modifiers.float ? parseFloat : parseInt;
    var range = (binding.value.toString() || "").split(","), min = numfy(range[0] || "-1"), max =  numfy(range[1] || "-1");

    el.removeEventListener("input", el.inputE_number);
    el.inputE_number = () => {
        var value = el.value.length ? numfy((el.value.match(/(^\-)?\d+(\.\d+)?/g) || []).join("") || "0") : null;
        if(min != -1) value = Math.max(min, value);
        if(max != -1) value = Math.min(max, value);
        if(value != el.value && value != null) {
            el.value = value;
            el.dispatchEvent(new CustomEvent("input"));
        }
    }
    el.addEventListener("input", el.inputE_number);
}
baseapp.directive('number', {
    mounted(el, binding) {
        vnumber(el, binding);
    },
    beforeUpdate(el, binding) {
        if(binding.value == binding.oldValue) return 0;
        vnumber(el, binding);
    }
});
// ------------------------------------------------------------------------------------- //
// fixed at a position
baseapp.directive('stick', {
    mounted(el, binding) {
        el.style.display = "block";
        el.attr = el.getBoundingClientRect();
        var dx, dy;
        if("L" in binding.value){
            dx = (binding.value.L - el.attr.x) + "px";
        }
        else if("R" in binding.value){
            dx = (binding.value.R + window.innerWidth - el.attr.width - el.attr.x) + "px";
        }
        if("T" in binding.value){
            dy = (binding.value.T - el.attr.y) + "px";
        }
        else if("B" in binding.value){
            dy = (binding.value.B + window.innerHeight - el.attr.height - el.attr.y) + "px";
        }
        el.style.transform = "translate(" + dx + "," + dy + ")";
        el.style.display = "";
    },
    beforeUpdate(el, binding) {
        if(binding.value == binding.oldValue) return 0;
    }
});
// ------------------------------------------------------------------------------------- //
// textarea autosize height

baseapp.directive('textarea', {
    mounted(el, binding) {
        if(el.tagName != "TEXTAREA") return;
        el.listenFnc = (event) => {
            if(event && event.keyCode == 13 && !event.shiftKey && binding.modifiers.clear) {
                event.preventDefault();
                el.value = "";
            }
            el.style.height = "1px";
            var style = window.getComputedStyle(el, null);
            el.style.height = parseInt(style.getPropertyValue("border-top-width")) + parseInt(style.getPropertyValue("border-bottom-width")) + el.scrollHeight + "px";
        }
        el.addEventListener("keypress", el.listenFnc);
        el.addEventListener("input", el.listenFnc);
    },
    beforeUpdate(el, binding) {
        if(binding.value == binding.oldValue || el.tagName != "TEXTAREA") return 0;
    }
});
// ------------------------------------------------------------------------------------- //
// input password see

baseapp.directive('password', {
    mounted(el, binding) {
        if(el.tagName != "INPUT" || el.type != "password") return;
        var eye = document.createElement("i");
        var eyeL = ["far", "fa-eye", "position-absolute", "end-0", "top-50", "translate-middle"];
        for(var c in eyeL) eye.classList.add(eyeL[c]);
        // eye.style.zIndex = "9999";
        eye.style.marginRight = window.getComputedStyle(el.parentElement, null).getPropertyValue("padding-right");
        eye.setAttribute("role", "button");
        
        el.listenFnc = (event) => {
            if(binding.modifiers.hover) el.type = event.type == "mouseenter" ? "text" : "password";
            else el.type = el.type == "password" ? "text" : "password";
        }

        el.workOnClassAdd = () => {
            eye.style.opacity = "0";
        };
        el.workOnClassRemoval = () => {
            eye.style.opacity = "1";
        };
        el.classWatcher = new ClassWatcher(el, 'is-invalid', el.workOnClassAdd, el.workOnClassRemoval);

        if(binding.modifiers.hover){
            eye.addEventListener("mouseenter", el.listenFnc);
            eye.addEventListener("mouseleave", el.listenFnc);
        }
        else{
            eye.addEventListener("click", el.listenFnc);
        }
        
        el.parentElement.appendChild(eye);
    },
    beforeUpdate(el, binding) {
        if(binding.value == binding.oldValue || el.tagName != "INPUT") return 0;
    }
});
// ------------------------------------------------------------------------------------- //
// input edit button

baseapp.directive('edit', {
    mounted(el, binding) {
        if(el.tagName != "INPUT") return;
        el.disabled = true;
        var edit = supfnc.createElement("i", {
            class: ["far"],
            style: {
                zIndex: 9999, 
                marginRight: window.getComputedStyle(el.parentElement, null).getPropertyValue("padding-right"),
                fontSize: "20px",
            },
            attr: {
                role: "button",
            },
        }), enter, cancel, divOn, divOff;
        enter = edit.cloneNode(1);
        cancel = edit.cloneNode(1);
        divOn = supfnc.createElement("div", {
            class: ["position-absolute", "end-0", "top-50", "me-2"],
            style: {
                transform: "translate(-0%,-50%)",
            },
        });
        divOff = divOn.cloneNode(1);

        edit.classList.add("fa-edit");
        enter.classList.add("fa-check-square");
        cancel.classList.add("fa-window-close");
        enter.classList.add("me-2");
        
        divOff.style.display = "none";
        
        el.editE = (event) => {
            el.disabled = false;
            divOn.style.display = "none";
            divOff.style.display = "block";
        }
        el.enterE = (event) => {
            el.disabled = true;
            divOn.style.display = "block";
            divOff.style.display = "none";
            if(typeof binding.arg == "function") {
                binding.value = Array.isArray(binding.value) ? [1].concat(binding.value) : [1, binding.value];
                binding.arg(...binding.value);
            }
        };
        el.cancelE = (event) => {
            el.disabled = true;
            divOn.style.display = "block";
            divOff.style.display = "none";
            if(typeof binding.arg == "function") {
                binding.value = Array.isArray(binding.value) ? [0].concat(binding.value) : [0, binding.value];
                binding.arg(...binding.value);
            }
        };

        el.workOnClassAdd = () => {
            divOn.style.opacity = "0";
            divOff.style.opacity = "0";
        };
        el.workOnClassRemoval = () => {
            divOn.style.opacity = "1";
            divOff.style.opacity = "1";
        };
        el.classWatcher = new ClassWatcher(el, 'is-invalid', el.workOnClassAdd, el.workOnClassRemoval);

        edit.addEventListener("click", el.editE);
        enter.addEventListener("click", el.enterE);
        cancel.addEventListener("click", el.cancelE);
        el.addEventListener("keydown", (e)=>{
            if (e.key === 'Enter'){
                el.enterE();
            }
            else if (e.key === 'Escape'){
                el.cancelE();
            }
        })
        
        el.parentElement.appendChild(divOn);
        el.parentElement.appendChild(divOff);

        divOn.appendChild(edit);
        divOff.appendChild(enter);
        divOff.appendChild(cancel);
    },
    beforeUpdate(el, binding) {
        if(binding.value == binding.oldValue || el.tagName != "INPUT") return 0;
    }
});
// ------------------------------------------------------------------------------------- //
// input elastic 

baseapp.directive('elasticinput', {
    mounted(el, binding) {
        if(el.tagName != "INPUT") return;
        range = Array.isArray(binding.value) ? binding.value : binding.value.split(",");
        
        el.focusE = (event) => {
            el.style.width = range[1];
        };
        el.blurE = (event) => {
            el.style.width = range[0];
        };

        el.style.width = range[0];
        el.style.transition = ".3s";

        el.addEventListener("focus", el.focusE);
        el.addEventListener("blur", el.blurE);
    },
    beforeUpdate(el, binding) {
        if(binding.value == binding.oldValue || el.tagName != "INPUT") return 0;
    }
});
// ------------------------------------------------------------------------------------- //
// ------------------------------------------------------------------------------------- //
// ------------------------------------------------------------------------------------- //
// ------------------------------------------------------------------------------------- //
// ------------------------------------------------------------------------------------- //
// ------------------------------------------------------------------------------------- //

// v-directive.modifiers:arg="value"
// binding.instance = baseapp
// event.target.selectionStart 取得input textarea輸入點 value = 在它之前有多少字元

// window.getComputedStyle(el, null).getPropertyValue("")
// el.getBoundingClientRect().x y 