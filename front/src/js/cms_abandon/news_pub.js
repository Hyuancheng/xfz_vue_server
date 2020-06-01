function NewsPublish() {
    const self = this;
    self.pub_btn = $('#pub-news-submit');
    self.pub_img = $('#pub-news-img');
    self.reminder = $('#info-reminder');

    self.news_pub_url = '/cms/news_pub/';
    self.news_img_url = '/cms/news_img/';
}

NewsPublish.prototype.run = function () {
    const self = this;
    // self.uploadImg();
    self.uploadToQiniu();
    self.initUEditor();
    self.publishNews();
};

NewsPublish.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
};

NewsPublish.prototype.uploadToQiniu = function () {
    const self = this;
    const pub_img = $('#pub-news-img');
    pub_img.on('change', function () {
        const img = $(this)[0].files[0];

        $.ajax({
            method: 'get',
            url: self.news_img_url,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', Tool.getCookie('csrftoken'));
            },
            success: success
        });

        function success(data) {
            if (data.code === 200) {
                const token = data.data.token;
                const array = img.name.split('.');
                const format = array[array.length - 1];
                const fname = Date.now() + '.' + format;
                //限制上传文件的类型
                const putExtra = {'mimeType': ["image/png", "image/jpeg", "image/gif", 'video/mp4']};
                //指定文件上传到哪个大区，可不传，会自动检测
                const config = {region: qiniu.region.z2};

                const observer = {
                    'next': function (res) {
                        self.uploadNextAction(res.total);
                    },
                    'error': function (err) {
                        self.uploadErrorAction(err);
                    },
                    'complete': function (res) {
                        self.uploadCompleteAction(res);
                    }
                };

                const observable = qiniu.upload(img, fname, token, putExtra, config);
                const subscription = observable.subscribe(observer)  // 上传开始
            }
        }
    })
};

NewsPublish.prototype.uploadNextAction = function (total) {
    const self = this;
    self.reminder.removeClass('alert-success').addClass('show alert-warning').text(`正在上传...${total.percent.toFixed()}%`);
};

NewsPublish.prototype.uploadErrorAction = function (err) {
    const self = this;
    self.reminder.removeClass('alert-success').addClass('show alert-warning').text('上传失败');
    setTimeout(function () {
        self.reminder.removeClass('show')
    }, 2000)
};

NewsPublish.prototype.uploadCompleteAction = function (res) {
    const self = this;
    const fname = res.key;
    const url = 'http://q9mtei3xj.bkt.clouddn.com/' + fname;
    $('#pub-img-url').val(url);
    self.reminder.removeClass('alert-warning').addClass('show alert-success').text('图片上传成功');
    setTimeout(function () {
        self.reminder.removeClass('show')
    }, 1000)
};

//上传到本地服务器的代码
// NewsPublish.prototype.uploadImg = function () {
//     const self = this;
//     const pub_img = $('#pub-news-img');
//     pub_img.on('change', function () {
//         const img = $(this)[0].files[0];
//         const form_data = new FormData;
//         form_data.append('img', img);
//         form_data.append('name', img.name);
//         $.ajax({
//             method: 'post',
//             url: self.news_img_url,
//             data: form_data,
//             contentType: false,
//             processData: false,
//             beforeSend: function (xhr) {
//                 xhr.setRequestHeader('X-CSRFToken', Tool.getCookie('csrftoken'));
//             },
//             success: success
//         });
//
//         function success(data, string, jqxhr) {
//             if (data.code === 200) {
//                 successAction(data, jqxhr);
//             } else {
//                 failAction(data, jqxhr);
//             }
//         }
//
//         function successAction(data, jqxhr) {
//             // 将url填入输入框
//             const pub_url = $('#pub-img-url');
//             pub_url.val(data.data.url);
//             // 提示成功信息
//             self.reminder.removeClass('alert-warning').addClass('show alert-success').text(data.message);
//             jqxhr.done(function () {
//                 setTimeout(function () {
//                     self.reminder.removeClass('show');
//                 }, 1000)
//             })
//         }
//
//         function failAction(data, jqxhr) {
//             // 显示错误信息
//             self.reminder.removeClass('alert-success').addClass('show alert-warning').html(Tool.getErrorMsg(data.message));
//             jqxhr.done(function () {
//                 setTimeout(function () {
//                     self.reminder.removeClass('show');
//                 }, 1000)
//             })
//         }
//     })
// };

NewsPublish.prototype.publishNews = function () {
    const self = this;

    self.pub_btn.on('click', function () {
        const title = $('#pub-news-title');
        const category = $('#pub-news-type');
        const thumbnail = $('#pub-img-url');
        const des = $('#pub-news-desc');
        const content = window.ue.getContent();
        const params = {
            'title': title,
            'category': category,
            'thumbnail': thumbnail,
            'des': des,
            'content': content
        };
        $.ajax({
            method: 'post',
            url: self.news_pub_url,
            data: params,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', Tool.getCookie('csrftoken'));
            },
            success: success
        });
    });

    function success(data) {
        if (data.code === 200) {
            self.reminder.removeClass('alert-warning').addClass('show alert-success').text('文章发布成功！');
            setTimeout(function () {
                window.location.reload();
            }, 1000)
        } else {
            self.reminder.removeClass('alert-success').addClass('show alert-warning').text(data.getErrorMsg());
            setTimeout(function () {
                self.reminder.removeClass('show');
            }, 1000)
        }
    }

};

const newsPublish = new NewsPublish();
newsPublish.run();