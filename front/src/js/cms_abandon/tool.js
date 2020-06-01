(function (window) {
    window.Tool = {
        getCookie: function (cname) {
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
        },
        getErrorMsg: function (data) {
            if (typeof data === 'string') {
                return data
            } else {
                return Tool.getMsg(data);
            }
        },
        getMsg: function (data) {
            let array = [];
            for (let key in data) {
                if (!data.hasOwnProperty(key)) {
                    continue;
                }
                for (let i = 0; i < data[key].length; i++) {
                    let label = `<span>${data[key][i]}</span>`;
                    array.push(label);
                }
            }
            return array.join('<br/>');
        }
    }
})(window);