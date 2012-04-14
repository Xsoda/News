/**
 * i use closure to simulate private method in OOP,because i don't wanna disturb the others js libraris you may use like jQuery,which uses $
 * remember the only variable i inject to window is Slider
 *
 * (c)logan liu
 * Email:hellouniverse@qq.com
 * if you find bugs,Don't hesitate contacting me.
 */
(function(window){

    function Slider(contentID, handlerID, pageNum, onePageWidth, direction, step, speed){
        if (arguments.length<4) {
            alert("init error,you must have at least 4 parameters:contentId,handlerId,pageNum and onePageWidth");
        }
        this.contentID = contentID;
        this.handlerID = handlerID;
        this.pageNum = pageNum;
        this.onePageWidth = onePageWidth;
        this.step = step || 10;
        this.direction = direction;
        this.speed = speed || 1;
    }
    var $ = function(id){
        return document.getElementById(id);
    }
    
    var style = function(sid, key, value){
        if (value) 
            $(sid).style[key] = value;
        else 
            return $(sid).style[key];
    };
    /**
     *
     * @param {Object} id
     * @param {Object} i
     *	0-100
     */
    var fade = function(id, i){
        style(id, "filter", "alpha(opacity=" + i + ")");
        i = i / 100;
        style(id, "-moz-opacity", i);
        style(id, "-khtml-opacity", i);
        style(id, "opacity", i);
    };
    
    var log = function(){
        if (!window.console) 
            return;
        // console.log(arguments.callee.caller.toString());
        for (var i in arguments) {
            console.log(i + ":" + arguments[i]);
        }
        
    }
    var addEvent = function(elm, evType, fn, useCapture){
        if (elm.addEventListener) {
            elm.addEventListener(evType, fn, useCapture);
        }
        else 
            if (elm.attachEvent) {
                elm.attachEvent('on' + evType, fn);
            }
            else {
                elm['on' + evType] = fn;
            }
    };
    var dump = function(o){
        for (var i in o) {
            log(i + ":" + o[i]);
        }
    };
    
    Slider.prototype = {
        changeEvent: "onclick",
        leftAndRightArrow: false,
        pageHandler: true,
        currentPage: 0,
        transformEffect: "",
        intervalId: 0,
        duration: 6000,
        /**
         * anything can case to false stands for horizontal.and the others are vertical.
         */
        direction: 0,
        /**
         * rend page navigator like 1,2...,so you can override it with you method such as page1,page2..or just empty.
         * @param {Object} i
         */
        rendPageNav: function(i){
            return i == -1 || i == this.pageNum ? "" : (i + 1);
        },
        /**
         * set navigator's class when clicked.add "current" to this.currentPage
         * @param {Object} i
         */
        rendNav: function(j){
            var c = $(this.handlerID).children;
            j = this.leftAndRightArrow ? (j + 1) : j;
            for (var i = (this.leftAndRightArrow ? 1 : 0), l = (this.leftAndRightArrow ? c.length - 1 : c.length); i < l; i++) {
                c[i].className = (i == j ? "current" : "");
            }
        },
        initHandler: function(){
            var tempThis = this;
            for (var i = (this.leftAndRightArrow ? -1 : 0), len = (this.leftAndRightArrow ? this.pageNum + 1 : this.pageNum); i < len; i++) {
                if ((!tempThis.pageHandler) && i != -1 && i != tempThis.pageNum) 
                    continue;
                var a = document.createElement("a");
                a.href = "#nogo";
                a.className = (i == -1 ? "left" : (i == 0 ? "current" : (i == this.pageNum ? "right" : "")));
                
                /**
                 * must use closure here to keep i.
                 * inspired by:Listing 2-16,page 29,<Pro JavaScript Techniques>,John Resig
                 */
                (function(){
                    var tempI = i;
                    a[tempThis.changeEvent] = function(){
                        this.blur();
                        tempThis.toPage(tempI == -1 ? "-1" : (tempI == tempThis.pageNum ? "+1" : tempI));
                    };
                })();
                a.innerHTML = tempThis.rendPageNav(i);
                $(this.handlerID).appendChild(a);
            }
        },
        toPage: function(toNum){
            if (toNum === "+1") 
                toNum = this.currentPage + 1;
            if (toNum === "-1") 
                toNum = this.currentPage - 1;
            
            if (this.currentPage == toNum) 
                return;
            if (toNum >= this.pageNum) 
                toNum = toNum % this.pageNum;
            if (toNum < 0) 
                toNum = this.pageNum - 1;
            this.rendNav(toNum);
            
            var toPos = -toNum * this.onePageWidth;
            var currentPos = -this.currentPage * this.onePageWidth;
            this.stopAutoSwitch();
            var value = this.direction ? "top" : "left";
            this.transformFn(this.contentID, value, currentPos, toPos, this.startAutoSwitch);
            //fix some pix
            if (style(this.contentID, value) != toPos) 
                style(this.contentID, value, toPos + "px");
            this.currentPage = toNum;
        },
        /**
         * all the transform funcitons must set value(left,top) from x to y.
         * i don't care how you transfrom but the start stat and the end stat.
         * @param {Object} id
         * @param {Object} value
         * @param {Object} from
         * @param {Object} to
         */
        transformFn: function(id, value, from, to, callback){
            //            log(this.transformEffect,id, value, from, to);
            switch (this.transformEffect) {
                case "fade":
                    var tempThis = this;
                    //fade from 1 to 0 to 1,i change from 1 to 0 to -1
                    (function fadeEffect(i){
                        i = i - 5;
                        if (i == -100) {
                            fade(id, 100);
                            callback.call(tempThis);
                        }
                        else {
                            if (i == 0) {
                                style(id, value, to + "px");
                            }
                            fade(id, i >= 0 ? i : -i);
                            
                            window.setTimeout(function(){
                                fadeEffect(i);
                            }, tempThis.speed);
                        }
                        
                    })(100);
                    break;
                case "slide":
                    var neg = (to - from > 0) ? "1" : "-1";
                    var tempThis = this;
                    (function slideEffect(toTemp){
                        style(tempThis.contentID, value, toTemp + "px");
                        if ((to - toTemp) * neg > 0) {
                            window.setTimeout(function(){
                                slideEffect(toTemp + neg * tempThis.step);
                            }, tempThis.speed);
                        }
                        else {
							style(id, value, to + "px");//add at version 11.419.
                            callback.call(tempThis);
                        }
                        
                    })(from + neg * tempThis.step);
                    break;
                default:
                    style(id, value, to + "px");
                    callback();
                    break;
            }
            
        },
        
        winonload: function(duration){
            style(this.contentID, "position", "absolute");
            this.initHandler();
            this.startAutoSwitch();
            return {};//it's necessary for IE6
        },
        startAutoSwitch: function(){
            if (this.duration > 0) {
                var tempThis = this;
                this.intervalId = window.setInterval(function(){
                    tempThis.toPage(tempThis.currentPage + 1)
                }, tempThis.duration);
            }
        },
        stopAutoSwitch: function(){
            if (this.intervalId) 
                window.clearInterval(this.intervalId);
        },
        start: function(duration, transformEffect){
            this.duration = duration || 3000;
            this.transformEffect = transformEffect || "slide";
            addEvent(window, 'load', this.winonload(), false);
        }
    };
    window.Slider = Slider;
})(window)