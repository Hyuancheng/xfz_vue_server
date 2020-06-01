(function (window) {
    window.Tool = {
        /**
         * 发送ajax请求
         * {
         * 'method': 'get',
         * 'url': 'http:....',
         * 'params': {'username':'xiaoming', 'password':'123456'}
         * }
         * @param paramsObj json格式。包含url, 请求方法(默认为get)，以及参数字典。
         * @param successFunc 请求成功后执行的函数，默认传入xhr对象
         * @param failFunc 请求失败后执行的函数，默认传入xhr对象
         */
        'ajaxRequest': function (paramsObj, successFunc, failFunc) {
            const xhr = new XMLHttpRequest();
            const method = paramsObj['method'].toLowerCase() || 'get';
            const url = paramsObj['url'];
            const params = paramsObj['params'] || null;
            if (method === 'get') {
                let myUrl = url + '?' + getParamStr(params);
                xhr.open('get', myUrl, true);
                xhr.send();
            } else {
                xhr.open('post', url, true);
                // post方法必须设置请求头
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                //设置csrftoken
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                xhr.send(getParamStr(params));
            }
            xhr.addEventListener('readystatechange', function () {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        if (successFunc) {
                            successFunc(xhr);
                            //因为此处ajax为异步执行
                            // 以下返回值来不及被调用者接收，会导致接收的变量为undefined
                            return xhr;
                        }
                    } else {
                        if (failFunc) {
                            failFunc(xhr);
                        }
                    }
                }
            })
        },

        /*
        *jsonp({
        * url: http://127.0.0.1:8000/
        * success: function(data)
        * })
        */
        'jsonp': function (json) {
            //生成动态函数名
            const callback = 'getData' + Math.random().toString().substr(-5);
            // 将该函数名绑定到window上，以便回调时能调用该函数。
            window[callback] = function (data) {
                // 调用回调函数，然后删除掉加在body后面的script标签
                json.success(data);
                script.remove();
            };

            // 新建标签
            let script = document.createElement('script');
            script.src = json.url + `?caller=${callback}`;
            document.body.appendChild(script);
        }
    };

    function getParamStr(params) {
        let strArray = [];
        // 遍历参数
        if (params) {
            for (let key in params) {
                let p = key + '=' + params[key];
                strArray.push(p);
            }
        }
        const randomStr = Date.now().toString().substr(-5, 5);
        let r = 'random' + '=' + randomStr;
        strArray.push(r);
        return strArray.join('&');
    }

    /**
     * 用于获取cookie中指定键的值
     * @param cname 键的名称
     * @returns {string}
     */
    function getCookie(cname) {
        const name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        const ca = decodedCookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

})(window);