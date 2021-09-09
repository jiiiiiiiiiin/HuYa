# 虎粮自动发放

用于虎牙直播平台，自动发放用户虎粮。

## 使用说明

```python
hy.login(username="", password="")  #  填写账号
hy.into_room(518512, 70)			#  房间号， 发放虎粮数目
hy.into_room(518511, 20)			#  房间号， 发放虎粮数目
```

- 第一次登陆会需要进行扫码登陆，二维码保存在代码路径下，名为`qr-username.png`，打开扫码登陆即可；或者打开输出的`QR-code url:xxxxx`也可以。

- 如果需要多个账号登陆，需要把这里的代码。(自己看着改吧

  ```python
  path_chrome_data = os.getcwd() + '\\chromeData'
  if not Path(path_chrome_data).exists():
      os.mkdir(path_chrome_data)
  chrome_options.add_argument(r'user-data-dir=' + path_chrome_data)
  ```

- 运行需要`chromedriver`。

- 定时使用`crontab`， `0 8 * * * python main.py >> huya.log >> 2>&1`。

- linux下selenium环境

  ```sh
  # 安装 google-chrome
  yum install -y https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
  yum install -y mesa-libOSMesa-devel gnu-free-sans-fonts wqy-zenhei-fonts
  # 这里根据安装的chrome版本选择chromedriver
  wget https://npm.taobao.org/mirrors/chromedriver/94.0.4606.41/chromedriver_linux64.zip
  unzip chromedriver_linux64.zip
  mv chromedriver /usr/bin/
  chmod +x /usr/bin/chromedriver
  #安装selenium
  pip install selenium 
  ```

  > [**518512 nb**](https://huya.com/518512)
