Object.__proto__.isDict = function (e) {
    return e?.constructor?.name == 'Object';
}

Function.__proto__.do = function (callback, n, ...args) {
	var res = [];
	for(var i=0; i<Math.abs(n); i++) res.push(callback(...args));
	return res;
}

Array.__proto__.range = (a, b, step=1) => {
    if(b==undefined) {
        b=a;
        a=0;
    }
    return Array.from({length: (b-a-1)/step+1}, (_, i) => a+i*step);
}

Array.__proto__.vector = (m, value=0) => {
    return Array.from({length: m}, (_, x) => (typeof value == "function" ? value(x): value));
}
Array.__proto__.matrix = (m, n, value=0) => {
    return Array.from({length: m}, (_, x) => Array.from({length: n}, (_, y) => (typeof value == "function" ? value(x, y): value)));
}

Array.__proto__.matrixN = (dim, value=0) => {
    var qwe = (l, v) => {
        return Array.from({length: l[0]}, (_, _v) => {
            if(v.length+1 == dim.length) return (typeof value == "function" ? value(...v, _v): value);
            else return qwe([dim[v.length+1], ...l], [...v, _v]);
        });
    };
    return qwe([dim[0]], []);
}

// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// Boolean @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Object.defineProperty(
    Boolean.prototype,
    'duplicate',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            return this.valueOf();
        }
    }
);

// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// Object @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Object.defineProperty(
    Object.prototype,
    'getFloorNum',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            function getD(e, n) {
                var tmp = [], r = n ? n : 1;
                for (var i in e) {
                    if (typeof e[i] == 'object') {
                        tmp.push(getD(e[i], r + 1));
                    }
                    else {
                        tmp.push(r);
                    }
                }
                return [tmp];
            }

            function findEx(a, Ex) {
                if (!Array.isArray(a)) return [NaN, NaN];
                if (a.length == 0) return [0, 0]
                if (!Ex) Ex = [];
                for (var i in a) {
                    if (!Array.isArray(a[i])) {
                        Ex[0] = Ex[0] == undefined ? a[i] : Ex[0] > a[i] ? Ex[0] : a[i];
                        Ex[1] = Ex[1] == undefined ? a[i] : Ex[1] < a[i] ? Ex[1] : a[i];
                    }
                    else {
                        var t = findEx(a[i], Ex);
                        Ex[0] = Ex[0] == undefined ? t[0] : Ex[0] > t[0] ? Ex[0] : t[0];
                        Ex[1] = Ex[1] == undefined ? t[1] : Ex[1] < t[1] ? Ex[1] : t[1];
                    }
                }
                return Ex;
            }

            return findEx(getD(this))
        }
    }
);

Object.defineProperty(
    Object.prototype,
    'lengthX',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            return Object.keys(this).length;
        }
    }
);

Object.defineProperty(
    Object.prototype,
    'duplicate',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            var r = {}
            for(var i in this){
                r[i] = this[i]?.duplicate();
            }
            return r;
        }
    }
);

Object.defineProperty(
    Object.prototype,
    'getV',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (tar, def) {
            var r = typeof this.get == "function" ? this.get(tar) : this[tar];
            return r === undefined ? def : r;
        }
    }
);

Object.defineProperty(
    Object.prototype,
    'getVF',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (tar, def, ...args) {
            var r = typeof this[tar] == "function" ? this[tar](...args) : this[tar];
            return r === undefined ? def : r;
        }
    }
);

Object.defineProperty(
    Object.prototype,
    'setV',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (tar, value, isForce) {
            if(tar in this || isForce) {
                if(value == undefined && isForce) delete this[tar];
                else this[tar] = value;
            }
            return this;
        }
    }
);

Object.defineProperty(
    Object.prototype,
    'reduce',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (f, init) {
            for(var i in this){
                init = f(init, this[i], i);
            }
            return init;
        }
    }
);

Object.defineProperty(
    Object.prototype,
    'clear',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            for(var i in this){
                delete this[i];
            }
            return this;
        }
    }
);

// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// Array @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Object.defineProperty(
    Array.prototype,
    'insert_idx2',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (e) {
            if (e == undefined) e = 0;
            var a = 0, b = this.length - 1, tmp;
            while (b - a > 1) {
                tmp = Math.floor((a + b) / 2);
                if (this[tmp] > e) b = tmp;
                else if (this[tmp] < e) a = tmp;
                else {
                    for (var i = tmp; i >= -1; i--) {
                        if (this[i] != e) return i + 1.5;
                    }
                }
            }
            if (this[a] < e) return b + (this[b] == e ? 0.5 : 0);
            return a + (this[a] == e ? 0.5 : 0);
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'insert',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (e, _IDX) {
            if(!Array.isArray(e)) e = [e];
            _IDX = Math.min(Math.max(_IDX ? _IDX : 0, 0), this.length);
            var L = this.length = this.length + e.length, eL = e.length;
            for (var i = L - 1; i >= eL + _IDX; i--) {
                this[i] = this[i - eL];
            }
            for (var i = 0; i < eL; i++) {
                this[_IDX + i] = e[i]
            }
            return L;
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'remove',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (..._IDX) {
            _IDX = Object.keys(_IDX.reduce(function (a, e) { var x = parseInt(typeof e == 'string' ? (e.match(/\d/g) || []).join('') : e); if (!isNaN(x)) a[x] = 1; return a }, {})).sort().reverse();
            var l = 0;
            for (var i in this) {
                if (i == _IDX[_IDX.length - 1]) _IDX.pop();
                else this[l++] = this[i];
            }
            this.length = l;
            
            return this.length;
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'removeE',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (items) {
            var ditems = {}, L = this.length, n = 0;
            var f = {};
            if (Array.isArray(items)) {
                for(var i in items) ditems[items[i]] = 1;
            }
            else {
                ditems[items] = 1;
            }
            for(var i=0; i<L; i++){
                if(this[i] in ditems)this[i] = f;
            }
            for(var i=0; i<L; i++){
                while(this[i+n] == f)n++;
                this[i] = this[i+n];
            }
            this.length = this.length - n;
            return this.length;
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'last',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            return this[this.length - 1];
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'index',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (x) {
            x = x%this.length;
            return this[x < 0 ? x+this.length : x];
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'max',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            var x = this[0];
            for (i in this) if (this[i] > x) x = this[i];
            return x;
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'min',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            var x = this[0];
            for (i in this) if (this[i] < x) x = this[i];
            return x;
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'moveft',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (from, to) {
            if(from == undefined) return -1;
            to = to == undefined ? this.length - 1 : to;
            this.splice(to, 0, this.splice(from, 1)[0]);
            return this;
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'switch',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (a, b) {
            if(a == undefined || b == undefined || this[a] == undefined || this[b] == undefined) return -1;
            var tmp = this[a];
            this[a] = this[b];
            this[b] = tmp;
            return this;
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'duplicate',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            var r = []
            for(var i in this){
                r[i] = this[i]?.duplicate();
            }
            return r;
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'random',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            return this[Math.floor(Math.random() * this.length)];
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'containNum',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (argw) {
            if(Array.isArray(argw)){
                var n = 0, tmp = {};
                for(var i in this) tmp[this[i]] = 1;
                for(var i in argw) if(argw[i] in tmp) n++;
                return n;
            }
            return this.includes(argw) ? 1 : 0;
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'containNumOnce',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (argw) {
            var tmp = {};
            for(i in argw) tmp[argw[i]] = 1;
            argw = [];
            for(i in tmp) argw.push(i);

            return this.containNum(argw);
        }
    }
);

Object.defineProperty(
    Array.prototype,
    'shuffle',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            var l = this.length, tmp, a, b;
            for(var i=0; i<l-1; i++){
                if(Math.random()<0.5){
                    a = Math.floor(Math.random() * l);
                    b = Math.floor(Math.random() * l);
                    tmp = this[a];
                    this[a] = this[b];
                    this[b] = tmp;
                }
            }

            return this.valueOf();
        }
    }
);
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// Number @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Object.defineProperty(
    Number.prototype,
    'duplicate',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            return this.valueOf();
        }
    }
);

Object.defineProperty(
    Number.prototype,
    'minmax',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (m, M) {
            m = parseFloat(m);
            M = parseFloat(M);
            if(isNaN(m)) m = Math.min(isNaN(M)?orig:M, this.valueOf());
            if(isNaN(M)) M = Math.max(isNaN(m)?orig:m, this.valueOf());
            if(m>M) {
                var tmp;
                tmp=m; m=M; M=tmp;
            }
            return Math.min(Math.max(this, m), M);
        }
    }
);

Object.defineProperty(
    Number.prototype,
    'format',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            var mm = this<0? "-":"", tmp = Math.abs(this).toString(), L = Math.floor((tmp.length-1)/3);
            for(var i=0; i<L; i++) tmp = tmp.splice(1-4*(i+1), 0, ',');
            return mm + tmp;
        }
    }
);

Object.defineProperty(
    Number.prototype,
    'chUnit',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (type, rnum = 0) {
            var un = [], num = this, rtn = "", unitCh = ["", "萬", "億", "兆", "京", "垓", "秭", "穰", "溝", "澗", "正", "載", "極"];
            while(num >= 1){
                un.push(num%1E4);
                num = Math.floor(num/1E4);
            }
            if(type == 1){
                for(var i=un.length; i>=0; i--){
                    if(un[i]){
                        rtn = ((un[i] + (un[i-1]||0)/1E4).round(rnum)) + unitCh[i];
                        break;
                    }
                }
            }
            else{
                for(var i in un){
                    if(un[i]) rtn = un[i] + unitCh[i] + rtn;
                }
            }
            return rtn;
        }
    }
);

Object.defineProperty(
    Number.prototype,
    'zfill',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (n) {
            var r="", L = Math.max(n - this.toString().length, 0);
            if(parseInt(this) == this){
                for(var i=0;i<L;i++) r+="0";
            }
            else{
                for(var i=0;i<L;i++) r+="*";
            }
            
            return r+this.toString();
        }
    }
);

Object.defineProperty(
    Number.prototype,
    'round',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (n) {
            n = parseInt(n);
            return Math.round(this * 10**n) / 10**n;
        }
    }
);

Object.defineProperty(
    Number.prototype,
    'floor',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (n) {
            n = parseInt(n);
            return Math.floor(this * 10**n) / 10**n;
        }
    }
);

Object.defineProperty(
    Number.prototype,
    'ceil',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (n) {
            n = parseInt(n);
            return Math.ceil(this * 10**n) / 10**n;
        }
    }
);
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// String @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Object.defineProperty(
    String.prototype,
    'minmax',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (m, M, d) {
            var orig = parseFloat(this.valueOf());
            orig = isNaN(orig) ? d == undefined ? 0..minmax(m,M): d : orig;
            m = parseFloat(m);
            M = parseFloat(M);
            if(isNaN(m)) m = Math.min(isNaN(M)?orig:M, orig);
            if(isNaN(M)) M = Math.max(isNaN(m)?orig:m, orig);
            if(m>M) {
                var tmp;
                tmp=m; m=M; M=tmp;
            }
            return Math.min(Math.max(orig, m), M);
        }
    }
);

Object.defineProperty(
    String.prototype,
    'duplicate',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            return this.slice();
        }
    }
);

Object.defineProperty(
    String.prototype,
    'format',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            return parseFloat(this).format();
        }
    }
);

Object.defineProperty(
    String.prototype,
    'chUnit',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (type, num) {
            return parseFloat(this).chUnit(type, num);
        }
    }
);

Object.defineProperty(
    String.prototype,
    'splice',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (start, delCount, newSubStr) {
            if (start == undefined) start = 0;
            if (delCount == undefined) delCount = this.length - start - 1;
            if (newSubStr == undefined) newSubStr = "";
            return this.slice(0, start) + newSubStr + this.slice(start + Math.abs(delCount));
        }
    }
);

Object.defineProperty(
    String.prototype,
    'strip',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (char) {
            if (char == undefined) char = '\\s';
            var reg = "^" + char + "+|" + char + "+$";
            return this.replace(new RegExp(reg, "g"), '');
        }
    }
);

Object.defineProperty(
    String.prototype,
    'last',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            return this[this.length - 1];
        }
    }
);


Object.defineProperty(
    String.prototype,
    'lengthB',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            var l = 0;
            for(var i in this){
                l += Math.ceil(Math.log(this.charCodeAt(i))/Math.log(256));
            }
            return l;
        }
    }
);


Object.defineProperty(
    String.prototype,
    'reverse',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            return this.split("").reverse().join("");
        }
    }
);
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// Function @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Object.defineProperty(
    Function.prototype,
    'fire',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (n, ...argw) {
            var res = [];
			for(var i=0; i<Math.abs(n); i++) res.push(this(...argw));
            return res;
        }
    }
);

Object.defineProperty(
    Function.prototype,
    'duplicate',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function () {
            return this.bind({});;
        }
    }
);

// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
// HTMLCollection @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Object.defineProperty(
    HTMLCollection.prototype,
    'switch',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (a, b) {
            if(a == undefined || b == undefined || this[a] == undefined || this[b] == undefined) return -1;
            this[b].parentElement.insertBefore(this[a], this[b].nextElementSibling);
            this[a].parentElement.insertBefore(this[b], this[a+1]);
            return this;
        }
    }
);

Object.defineProperty(
    HTMLElement.prototype,
    'switch',
    {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function (a, b) {
            if(a == undefined || b == undefined || this.children[a] == undefined || this.children[b] == undefined) return -1;
            this.insertBefore(this.children[a], this.children[b].nextElementSibling);
            this.insertBefore(this.children[b], this.children[a+1]);
            return this;
        }
    }
);