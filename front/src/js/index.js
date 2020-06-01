const banner = document.getElementsByClassName('left-banner')[0],
    bContainer = document.getElementsByClassName('banner-container')[0],
    images = banner.getElementsByTagName('li'),
    ul = document.getElementsByClassName('label')[0],
    label = ul.children,
    leftBtn = document.getElementsByClassName('left-btn')[0],
    rightBtn = document.getElementsByClassName('right-btn')[0];

let current = 0;
//设立哨兵
let worker1 = true, worker2 = true;

//初始化
for (let i = 0; i < images.length; i++) {
    // 创建圆点标签
    let li = document.createElement('li');
    li.index = i;
    ul.appendChild(li);

    //初始化图片位置
    if (i !== current) {
        images[i].style.position = 'absolute';
        images[i].style.left = '800px';
        images[i].style.top = 0;
    } else {
        images[i].style.position = 'absolute';
        images[i].style.left = 0;
        images[i].style.top = 0;
        label[i].className = 'active';
    }
}

for (let i = 0; i < label.length; i++) {
    // 添加点击事件
    label[i].onclick = function () {
        label[current].className = '';
        this.className = 'active';
        if (this.index > current) {
            worker1 = false;
            worker2 = false;
            images[this.index].style.left = '800px';
            // 左移
            myTool.multiChange(images[current], {left: -800}, function () {
                worker1 = true;
            });
            myTool.multiChange(images[this.index], {left: 0}, function () {
                worker2 = true;
            });
        }else if(this.index < current){
            worker1 = false;
            worker2 = false;
            images[this.index].style.left = '-800px';
            // 右移
            myTool.multiChange(images[current], {left: 800}, function () {
                worker1 = true;
            });
            myTool.multiChange(images[this.index], {left: 0}, function () {
                worker2 = true;
            });
        }
        current = this.index;
    };
}


// 设置自动轮播
let timer = null;
timer = setInterval(ImageToLeft, 3000);

// 监测鼠标进入轮播图事件
bContainer.addEventListener('mouseover', function () {
    // 显示按钮
    leftBtn.style.display = 'block';
    rightBtn.style.display = 'block';
    // 停止自动滚动
    clearInterval(timer);
});

// 监测鼠标退出轮播图事件
bContainer.addEventListener('mouseout', function () {
    // 隐藏按钮
    leftBtn.style.display = 'none';
    rightBtn.style.display = 'none';
    // 开启自动滚动
    clearInterval(timer);
    timer = setInterval(ImageToLeft, 3000);
});

// 监听按钮点击事件
leftBtn.onclick = function () {
    ImageToRight();
};
rightBtn.onclick = function () {
    ImageToLeft();
};

function ImageToLeft() {
    if (worker1 && worker2) {
        worker1 = false;
        worker2 = false;
        label[current].className = '';
        const ready = (current + 1) % images.length;
        images[ready].style.left = '800px';
        myTool.multiChange(images[current], {left: -800}, function () {
            worker1 = true;
        });
        current = (current + 1) % images.length;
        myTool.multiChange(images[current], {left: 0}, function () {
            worker2 = true;
        });
        label[current].className = 'active';
    }
}

function ImageToRight() {
    if (worker1 && worker2) {
        worker1 = false;
        worker2 = false;
        label[current].className = '';
        const ready = (current + images.length - 1) % images.length;
        images[ready].style.left = '-800px';
        myTool.multiChange(images[current], {left: 800}, function () {
            worker1 = true;
        });
        current = (current + images.length - 1) % images.length;
        myTool.multiChange(images[current], {left: 0}, function () {
            worker2 = true;
        });
        label[current].className = 'active';
    }
}