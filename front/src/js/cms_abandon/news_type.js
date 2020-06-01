function NewsType() {
    const self = this;
    self.modal = $('.modal');
    self.news_type = $('#news_type');
    self.input = self.modal.find('#add_news_type');
    self.add_btn = self.modal.find('#add_news_submit');
    self.delete = $('#delete');
    self.reminder = $('#info-reminder');

    // 新闻分类的url接口
    self.add_news_type_url = '/cms/news_type/';
}

// 定义入口
NewsType.prototype.run = function () {
    const self = this;
    self.init();
    self.newsTypeAction();
};

//初始化模态框的显示行为
NewsType.prototype.init = function () {
    const self = this;
    //初始化新增/编辑模态框
    self.addModal();
    //初始化删除模态框
    self.deleteModal();
};

NewsType.prototype.addModal = function () {
    const self = this;
    self.modal.on('show.bs.modal', function (e) {
        const name = $(e.relatedTarget).attr('data-whatever');
        const method = $(e.relatedTarget).attr('data-method');
        $(this).find('.modal-title').html(name);
        $(this).find('#add_news_submit').attr('data-method', method);

        //倘若点击的是编辑按钮，则绑定新闻分类的id，将分类名称填入输入框
        const type_id = $(e.relatedTarget).attr('data-id');
        if (type_id) {
            const value = $(e.relatedTarget).attr('data-name');
            $(this).find('#add_news_submit').attr('data-id', type_id);
            self.input.val(value);
        } else {
            self.input.val(null);
        }
    });
};

NewsType.prototype.deleteModal = function () {
    const self = this;
    self.delete.on('show.bs.modal', function (event) {
        const type_id = $(event.relatedTarget).attr('data-id');
        $(this).find('#confirm').attr('data-id', type_id);
    });
    self.delete.find('#cancel').on('click', function () {
        self.delete.modal('hide');
    })
};


/*****************新增，编辑，删除新闻分类接口**************/
NewsType.prototype.newsTypeAction = function () {
    const self = this;
    self.add_btn.on('click', function () {
        const method = $(this).attr('data-method');
        if (method === 'post') {
            self.addNewsType();
        } else if (method === 'put') {
            self.changeNewsType();
        }
    });
    self.delete.find('#confirm').on('click', function () {
        self.deleteNewsType();
    })
};


/******************************新增新闻分类*****************************/

NewsType.prototype.addNewsType = function () {
    const self = this;
    const name = self.input.val();
    self.ajaxRequest('POST', {'name': name});
};


/******************************修改新闻分类*****************************/

NewsType.prototype.changeNewsType = function () {
    const self = this;
    const name = self.input.val();
    const type_id = self.add_btn.attr('data-id');
    const content = {
        'name': name,
        'type_id': type_id
    };
    self.ajaxRequest('PUT', content);
};


/******************************删除新闻分类*****************************/

NewsType.prototype.deleteNewsType = function(){
    const self = this;
    const type_id = self.delete.find('#confirm').attr('data-id');
    self.ajaxRequest('DELETE', {'type_id': type_id});
};


/*************封装ajax请求***********/

NewsType.prototype.ajaxRequest = function (request_method, request_data) {
    const self = this;
    $.ajax({
        method: request_method,
        url: self.add_news_type_url,
        data: request_data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', Tool.getCookie('csrftoken'));
        },
        success: success
    });

    function success(data, string, jqxhr) {
        if (data.code === 200) {
            self.successAction(data, jqxhr);
        } else {
            self.failAction(data, jqxhr);
        }
    }
};

/**************ajax回调函数**************/

//提示成功信息，0.5秒后刷新页面
NewsType.prototype.successAction = function (data, jqxhr) {
    const self = this;
    console.log('hhhh');
    self.reminder.css('display', 'block');
    self.reminder.removeClass('alert-warning').addClass('show alert-success').text(data.message);
    jqxhr.done(function () {
        setTimeout(function () {
            window.location.reload();
        }, 500)
    })
};

//提示错误信息
NewsType.prototype.failAction = function (data, jqxhr) {
    const self = this;
    self.reminder.css('display', 'block');
    self.reminder.addClass('show').html(Tool.getErrorMsg(data.message));
    jqxhr.done(function () {
        setTimeout(function () {
            self.reminder.removeClass('show')
        }, 2000)
    })
};


/******************************实例化开启入口*********************************/

window.newsType = new NewsType();
window.newsType.run();