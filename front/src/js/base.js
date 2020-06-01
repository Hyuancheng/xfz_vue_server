function Auth() {
    const self = this;
    self.mask = document.getElementsByClassName('mask')[0];
    self.wrapper = self.mask.getElementsByClassName('inner-wrapper')[0];
    self.head = document.getElementById('header');
    self.register_form = self.mask.getElementsByClassName('register-form')[0];
}

Auth.prototype.run = function () {
    const self = this;
    self.showHideEvent();
    self.loginEvent();
    self.loginRegChange();
    self.showHideBackend();
    self.changeCaptcha();
    self.GetCodeEvent();
    self.RegisterEvent();
};

Auth.prototype.showHideEvent = function () {
    const self = this;
    self.login_btn = self.head.getElementsByClassName('login-btn')[0];
    self.register_btn = self.head.getElementsByClassName('register-btn')[0];
    self.close_btn = self.mask.getElementsByClassName('close-btn')[0];

    //监听登录/注册的点击
    if (self.login_btn) {
        self.login_btn.addEventListener('click', function () {
            self.showEvent();
            self.wrapper.style.left = '0';
        });
    }

    if (self.register_btn) {
        self.register_btn.addEventListener('click', function () {
            self.showEvent();
            self.wrapper.style.left = '-400px';
        });
    }

    // 监听关闭按钮的点击
    self.close_btn.addEventListener('click', function () {
        self.hideEvent();
    });
};

Auth.prototype.showEvent = function () {
    const self = this;
    self.mask.style.display = 'block';
};

Auth.prototype.hideEvent = function () {
    const self = this;
    self.mask.style.display = 'none';
};

Auth.prototype.loginEvent = function () {
    const self = this;
    const login_form = self.mask.getElementsByClassName('login-form')[0];
    const login_submit = login_form.getElementsByClassName('login-btn')[0];
    const login_phone = login_form.getElementsByClassName('phone-input')[0];
    const login_password = login_form.getElementsByClassName('password-input')[0];

    login_submit.addEventListener('click', function () {
        const phone = login_phone.value, password = login_password.value;
        const params = 'telephone=' + phone + '&password=' + password;
        const xhr = new XMLHttpRequest();

        xhr.open('post', 'http://127.0.0.1:8000/user/login/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.send(params);
        xhr.addEventListener('readystatechange', function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    console.log('success');
                    console.log(xhr.response);
                    window.location.reload();
                } else {
                    console.log('failed');
                    console.log(xhr.response);
                }
            }
        })
    });
};

Auth.prototype.loginRegChange = function () {
    const self = this;
    const inner_wrapper = self.mask.getElementsByClassName('inner-wrapper')[0];
    const login_form = self.mask.getElementsByClassName('login-form')[0];
    const login_change = login_form.getElementsByClassName('change')[0];
    const register_form = self.mask.getElementsByClassName('register-form')[0];
    const register_change = register_form.getElementsByClassName('change')[0];

    login_change.addEventListener('click', function () {
        inner_wrapper.style.left = '-400px';
    });

    register_change.addEventListener('click', function () {
        inner_wrapper.style.left = '0';
    })
};

Auth.prototype.showHideBackend = function () {
    const self = this;
    const right = self.head.getElementsByClassName('right')[0];
    const auth_wrapper = right.getElementsByClassName('auth-wrapper')[0];

    if (auth_wrapper) {
        right.addEventListener('mouseover', function () {
            auth_wrapper.style.display = 'block';
        });

        right.addEventListener('mouseout', function () {
            auth_wrapper.style.display = 'none';
        });
    }
};

Auth.prototype.changeCaptcha = function () {
    const self = this;
    const captcha = self.mask.getElementsByClassName('captcha')[0];
    const src = captcha.name;

    captcha.addEventListener('click', function () {
        let ran = '?random=' + Math.random().toString().substr(-5);
        this.src = src + ran;
    })
};

Auth.prototype.GetCodeEvent = function () {
    const self = this;
    const phone_btn = self.mask.getElementsByClassName('phone-btn')[0];
    const phone_input = self.register_form.getElementsByClassName('telephone')[0];

    phone_btn.addEventListener('click', function () {
        const phone = phone_input.value;
        const paramsObject = {
            "method": "post",
            "url": "http://127.0.0.1:8000/user/code/",
            "params": {
                "telephone": phone
            }
        };
        Tool.ajaxRequest(paramsObject, successFunc);

        function successFunc(xhr) {
            console.log(xhr.response);
        }
    });
};

Auth.prototype.RegisterEvent = function () {
    const self = this;
    const username_box = self.register_form.getElementsByClassName('username')[0];
    const telephone_box = self.register_form.getElementsByClassName('telephone')[0];
    const password1_box = self.register_form.getElementsByClassName('password1')[0];
    const password2_box = self.register_form.getElementsByClassName('password2')[0];
    const img_code_box = self.register_form.getElementsByClassName('auth-number')[0];
    const sms_code_box = self.register_form.getElementsByClassName('phone-number')[0];
    const register_btn = self.register_form.getElementsByClassName('register')[0];

    register_btn.addEventListener('click', function () {
        const username = username_box.value;
        const telephone = telephone_box.value;
        const password1 = password1_box.value;
        const password2 = password2_box.value;
        const img_code = img_code_box.value;
        const sms_code = sms_code_box.value;
        const url = register_btn.name;
        const paramsObject = {
            'method': 'post',
            'url': url,
            'params': {
                'username': username,
                'telephone': telephone,
                'password1': password1,
                'password2': password2,
                'img_code': img_code,
                'sms_code': sms_code,
            }
        };
        Tool.ajaxRequest(paramsObject, successFunc);

        function successFunc(xhr) {
            console.log(xhr.response);
        }
    })
};

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

window.auth = new Auth();
window.auth.run();


