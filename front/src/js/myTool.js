(function (window) {
    window.myTool = {
        /**
         * 更改指定元素的CSS属性
         * @param obj [element]作用的元素
         * @param attr [string]想要更改的属性
         * @param value [string]更改后的值
         */
        changeStyleAttr: function (obj, attr, value){
                obj.style[attr] = value;
            },

        /**
         * 获取指定元素的CSS属性
         * @param obj [element]作用的元素
         * @param attr  [string]想要获取的属性
         * @returns {string}
         */
        getStyleAttr: function (obj, attr) {
            return window.getComputedStyle(obj, null)[attr];
        },

        /**
         * 实现某元素的多重动画效果，包括位置，大小，颜色，透明度等
         * @param obj 元素对象
         * @param json "{属性(string)：数值(string/number)}"
         * @param fn 定义的下一组动画函数，调用自身，但参数不同。
         */
        multiChange: function (obj, json, fn) {
            let timer = null, speed = 0, begin = 0, target = 0, flag = true;
            clearInterval(timer);
            timer = setInterval(function () {
                flag = true;
                for (let key in json) {
                    if (key === 'opacity') {
                        begin = parseInt(myTool.getStyleAttr(obj, key) * 100);
                        target = parseInt(json[key] * 100);
                    } else {
                        begin = parseInt(myTool.getStyleAttr(obj, key));
                        target = parseInt(json[key]);
                    }
                    speed = (target - begin) * 0.2;
                    // 设置最小速度的绝对值为1
                    speed > 0 ? speed = Math.ceil(speed) : speed = Math.floor(speed);
                    // 移动
                    if (key === 'opacity') {
                        obj.style.opacity = (begin + speed) / 100;
                    } else {
                        obj.style[key] = begin + speed + 'px';
                    }
                    //判断是否到达目标
                    if (begin !== target) {
                        flag = false;
                    }
                }
                //倘若全部抵达目标，则关闭定时器
                if (flag === true) {
                    clearInterval(timer);
                    //若含有另一组动画，则执行下一组
                    if (fn) {
                        fn();
                    }
                }
            }, 20);
        }
    }
})(window);