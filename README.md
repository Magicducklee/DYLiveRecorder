<img width="998" height="82" alt="image" src="https://github.com/user-attachments/assets/25e562f9-309a-437d-9c1c-81eb70c9e31d" /><img width="212" height="30" alt="image" src="https://github.com/user-attachments/assets/e17d9375-59a4-4068-871e-7a99165b9bbb" /><img width="561" height="30" alt="image" src="https://github.com/user-attachments/assets/13ab507b-c7d9-4b45-85af-88e41b17fe56" />![video_spider](https://socialify.git.ci/ihmily/DouyinLiveRecorder/image?font=Inter&forks=1&language=1&owner=1&pattern=Circuit%20Board&stargazers=1&theme=Light)

## 💡简介

一款**简易**的可循环值守的直播录制工具，基于FFmpeg实现多平台直播源录制，支持自定义配置录制以及直播状态推送。

</div>

## 😺已支持平台

- [x] 抖音

</div>

## 🎈项目结构

```
.
└── DouyinLiveRecorder/
    ├── /config -> (config record)
    ├── /logs -> (save runing log file)
    ├── /backup_config -> (backup file)
    ├── /douyinliverecorder -> (package)
        ├── initializer.py-> (check and install nodejs)
    	├── spider.py-> (get live data)
    	├── stream.py-> (get live stream address)
    	├── utils.py -> (contains utility functions)
    	├── logger.py -> (logger handdle)
    	├── room.py -> (get room info)
    	├── ab_sign.py-> (generate dy token)
    	├── /javascript -> (some decrypt code)
    ├── main.py -> (main file)
    ├── ffmpeg_install.py -> (ffmpeg install script)
    ├── demo.py -> (call package test demo)
    ├── msg_push.py -> (send live status update message)
    ├── ffmpeg.exe -> (record video)
    ├── index.html -> (play m3u8 and flv video)
    ├── requirements.txt -> (library dependencies)
    ├── docker-compose.yaml -> (Container Orchestration File)
    ├── Dockerfile -> (Application Build Recipe)
    ├── StopRecording.vbs -> (stop recording script on Windows)
    ...
```

</div>

## 🌱使用说明

- 用到了Selenium模块，找到抖音直播时hevc编码的真原画画质

- 最终代码在Selenium_dy_final_OK分支，用：.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onefile --hidden-import=httpx --hidden-import=httpcore --hidden-import=anyio --hidden-import=selenium.webdriver --hidden-import=selenium  --name DYLiveRecorder main.py打包
  
- Windows下测试成功，需要：1、安装Chrome到默认文件夹；2、安装对应版本ChromeDriver（https://chromedriver.chromium.org/downloads），解压文件放到C:\Windows下

- 对于只想使用录制软件的小白用户，[Releases]里直接下载打包好的exe文件，替换ihmily发布的 zip压缩包里的exe即可。

&emsp;



&emsp;

## 🎃源码运行
使用源码运行，可参考下面的步骤。

1.首先拉取或手动下载本仓库项目代码

```bash
git clone https://github.com/ihmily/DouyinLiveRecorder.git
```

2.进入项目文件夹，安装依赖

```bash
cd DouyinLiveRecorder
```

> [!TIP]
> - 不论你是否已安装 **Python>=3.10** 环境, 都推荐使用 [**uv**](https://github.com/astral-sh/uv) 运行, 因为它可以自动管理虚拟环境和方便地管理 **Python** 版本, **不过这完全是可选的**<br />
> 使用以下命令安装
>    ```bash
>    # 在 macOS 和 Linux 上安装 uv
>    curl -LsSf https://astral.sh/uv/install.sh | sh
>    ```
>    ```powershell
>    # 在 Windows 上安装 uv
>    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
>    ```
> - 如果安装依赖速度太慢, 你可以考虑使用国内 pip 镜像源:<br />
> 在 `pip` 命令使用 `-i` 参数指定, 如 `pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`<br />
> 或者在 `uv` 命令 `--index` 选项指定, 如 `uv sync --index https://pypi.tuna.tsinghua.edu.cn/simple`

<details>

  <summary>如果已安装 <b>Python>=3.10</b> 环境</summary>

  - :white_check_mark: 在虚拟环境中安装 (推荐)
  
    1. 创建虚拟环境

       - 使用系统已安装的 Python, 不使用 uv
  
         ```bash
         python -m venv .venv
         ```

       - 使用 uv, 默认使用系统 Python, 你可以添加 `--python` 选项指定 Python 版本而不使用系统 Python [uv官方文档](https://docs.astral.sh/uv/concepts/python-versions/)
       
         ```bash
         uv venv
         ```
    
    2. 在终端激活虚拟环境 (在未安装 uv 或你想要手动激活虚拟环境时执行, 若已安装 uv, 可以跳过这一步, uv 会自动激活并使用虚拟环境)
   
       **Bash** 中
       ```bash
       source .venv/Scripts/activate
       ```

       **Powershell** 中
       ```powershell
       .venv\Scripts\activate.ps1
       ```
       
       **Windows CMD** 中
       ```bat
       .venv\Scripts\activate.bat
       ```

    3. 安装依赖
   
       ```bash
       # 使用 pip (若安装太慢或失败, 可使用 `-i` 指定镜像源)
       pip3 install -U pip && pip3 install -r requirements.txt
       # 或者使用 uv (可使用 `--index` 指定镜像源)
       uv sync
       # 或者
       uv pip sync requirements.txt
       ```

  - :x: 在系统 Python 环境中安装 (不推荐)
  
    ```bash
    pip3 install -U pip && pip3 install -r requirements.txt
    ```

</details>

<details>

  <summary>如果未安装 <b>Python>=3.10</b> 环境</summary>

  你可以使用 [**uv**](https://github.com/astral-sh/uv) 安装依赖
   
  ```bash
  # uv 将使用 3.10 及以上的最新 python 发行版自动创建并使用虚拟环境, 可使用 --python 选项指定 python 版本, 参见 https://docs.astral.sh/uv/reference/cli/#uv-sync--python 和 https://docs.astral.sh/uv/reference/cli/#uv-pip-sync--python
  uv sync
  # 或
  uv pip sync requirements.txt
  ```

</details>

3.安装[FFmpeg](https://ffmpeg.org/download.html#build-linux)，如果是Windows系统，这一步可跳过。对于Linux系统，执行以下命令安装

CentOS执行

```bash
yum install epel-release
yum install ffmpeg
```

Ubuntu则执行

```bash
apt update
apt install ffmpeg
```

macOS 执行

**如果已经安装 Homebrew 请跳过这一步**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
brew install ffmpeg
```

4.运行程序

```python
python main.py

```
或

```bash
uv run main.py
```

其中Linux系统请使用`python3 main.py` 运行。

&emsp;
## 🐋容器运行

在运行命令之前，请确保您的机器上安装了 [Docker](https://docs.docker.com/get-docker/) 和 [Docker Compose](https://docs.docker.com/compose/install/) 

1.快速启动

最简单方法是运行项目中的 [docker-compose.yaml](https://github.com/ihmily/DouyinLiveRecorder/blob/main/docker-compose.yaml) 文件，只需简单执行以下命令：

```bash
docker-compose up
```

可选 `-d` 在后台运行。



2.构建镜像(可选)

如果你只想简单的运行程序，则不需要做这一步。Docker镜像仓库中代码版本可能不是最新的，如果要运行本仓库主分支最新代码，可以本地自定义构建，通过修改 [docker-compose.yaml](https://github.com/ihmily/DouyinLiveRecorder/blob/main/docker-compose.yaml) 文件，如将镜像名修改为 `douyin-live-recorder:latest`，并取消 `# build: .` 注释，然后再执行

```bash
docker build -t douyin-live-recorder:latest .
docker-compose up
```

或者直接使用下面命令进行构建并启动

```bash
docker-compose -f docker-compose.yaml up
```



3.停止容器实例

```bash
docker-compose stop
```



4.注意事项

①在docker容器内运行本程序之前，请先在配置文件中添加要录制的直播间地址。

②在容器内时，如果手动中断容器运行停止录制，会导致正在录制的视频文件损坏！

**无论哪种运行方式，为避免手动中断或者异常中断导致录制的视频文件损坏的情况，推荐使用 `ts` 格式保存**。

&emsp;

## 🤖相关项目

- StreamCap: https://github.com/ihmily/StreamCap
- streamget: https://github.com/ihmily/streamget

&emsp;

## ❤️贡献者

&ensp;&ensp; [![Hmily](https://github.com/ihmily.png?size=50)](https://github.com/ihmily)
[![iridescentGray](https://github.com/iridescentGray.png?size=50)](https://github.com/iridescentGray)
[![annidy](https://github.com/annidy.png?size=50)](https://github.com/annidy)
[![wwkk2580](https://github.com/wwkk2580.png?size=50)](https://github.com/wwkk2580)
[![missuo](https://github.com/missuo.png?size=50)](https://github.com/missuo)
<a href="https://github.com/xueli12" target="_blank"><img src="https://github.com/xueli12.png?size=50" alt="xueli12" style="width:53px; height:51px;" /></a>
<a href="https://github.com/kaine1973" target="_blank"><img src="https://github.com/kaine1973.png?size=50" alt="kaine1973" style="width:53px; height:51px;" /></a>
<a href="https://github.com/yinruiqing" target="_blank"><img src="https://github.com/yinruiqing.png?size=50" alt="yinruiqing" style="width:53px; height:51px;" /></a>
<a href="https://github.com/Max-Tortoise" target="_blank"><img src="https://github.com/Max-Tortoise.png?size=50" alt="Max-Tortoise" style="width:53px; height:51px;" /></a>
[![justdoiting](https://github.com/justdoiting.png?size=50)](https://github.com/justdoiting)
[![dhbxs](https://github.com/dhbxs.png?size=50)](https://github.com/dhbxs)
[![wujiyu115](https://github.com/wujiyu115.png?size=50)](https://github.com/wujiyu115)
[![zhanghao333](https://github.com/zhanghao333.png?size=50)](https://github.com/zhanghao333)
<a href="https://github.com/gyc0123" target="_blank"><img src="https://github.com/gyc0123.png?size=50" alt="gyc0123" style="width:53px; height:51px;" /></a>

&ensp;&ensp; [![HoratioShaw](https://github.com/HoratioShaw.png?size=50)](https://github.com/HoratioShaw)
[![nov30th](https://github.com/nov30th.png?size=50)](https://github.com/nov30th)
[![727155455](https://github.com/727155455.png?size=50)](https://github.com/727155455)
[![nixingshiguang](https://github.com/nixingshiguang.png?size=50)](https://github.com/nixingshiguang)
[![1411430556](https://github.com/1411430556.png?size=50)](https://github.com/1411430556)
[![Ovear](https://github.com/Ovear.png?size=50)](https://github.com/Ovear)
&emsp;

## ⏳提交日志

- 20251024
  - 修复抖音风控无法获取数据问题
  
  - 新增soop.com录制支持
  
  - 修复bigo录制
  
- 20250127
  - 新增淘宝、京东、faceit直播录制
  - 修复小红书直播流录制以及转码问题
  - 修复畅聊、VV星球、flexTV直播录制
  - 修复批量微信直播推送
  - 新增email发送ssl和port配置
  - 新增强制转h264配置
  - 更新ffmpeg版本
  - 重构包为异步函数！

- 20241130
  - 新增shopee、youtube直播录制
  - 新增支持自定义m3u8、flv地址录制
  - 新增自定义执行脚本，支持python、bat、bash等
  - 修复YY直播、花椒直播和小红书直播录制
  - 修复b站标题获取错误
  - 修复log日志错误
- 20241030
  - 新增嗨秀直播、vv星球直播、17Live、浪Live、SOOP、畅聊直播(原时光直播)、飘飘直播、六间房直播、乐嗨直播、花猫直播等10个平台直播录制
  - 修复小红书直播录制，支持小红书作者主页地址录制直播
  - 新增支持ntfy消息推送，以及新增支持批量推送多个地址（逗号分隔多个推送地址)
  - 修复Liveme直播录制、twitch直播录制
  - 新增Windows平台一键停止录制VB脚本程序
- 20241005
  - 新增邮箱和Bark推送
  - 新增直播注释停止录制
  - 优化分段录制
  - 重构部分代码
- 20240928
  - 新增知乎直播、CHZZK直播录制
  - 修复音播直播录制
- 20240903
  - 新增抖音双屏录制、音播直播录制
  - 修复PandaTV、bigo直播录制
- 20240713
  - 新增映客直播录制
- 20240705
  - 新增时光直播录制
- 20240701
  - 修复虎牙直播录制2分钟断流问题
  - 新增自定义直播推送内容
- 20240621
  - 新增Acfun、ShowRoom直播录制
  - 修复微博录制、新增直播源线路
  - 修复斗鱼直播60帧录制
  - 修复酷狗直播录制
  - 修复TikTok部分无法解析直播源
  - 修复抖音无法录制连麦直播
- 20240510
  - 修复部分虎牙直播间录制错误
- 20240508
  - 修复花椒直播录制
  - 更改文件路径解析方式 [@kaine1973](https://github.com/kaine1973)
- 20240506
  - 修复抖音录制画质解析bug
  - 修复虎牙录制 60帧最高画质问题
  - 新增流星直播录制
- 20240427
  - 新增LiveMe、花椒直播录制
- 20240425
  - 新增TwitchTV直播录制
- 20240424
  - 新增酷狗直播录制、优化PopkonTV直播录制
- 20240423
  - 新增百度直播录制、微博直播录制
  - 修复斗鱼录制直播回放的问题
  - 新增直播源地址显示以及输出到日志文件设置
- 20240311
  - 修复海外平台录制bug，增加画质选择，增强录制稳定性
  - 修复虎牙录制bug (虎牙`一起看`频道 有特殊限制，有时无法录制)
- 20240309
  - 修复虎牙直播、小红书直播和B站直播录制
  - 新增5个直播平台录制，包括winktv、flextv、look、popkontv、twitcasting
  - 新增部分海外平台账号密码配置，实现自动登录并更新配置文件中的cookie
  - 新增自定义配置需要使用代理录制的平台
  - 新增只推送开播消息不进行录制设置
  - 修复了一些bug
- 20240209
  - 优化AfreecaTV录制，新增账号密码登录获取cookie以及持久保存
  - 修复了小红书直播因官方更新直播域名，导致无法录制直播的问题
  - 修复了更新URL配置文件的bug
  - 最后，祝大家新年快乐！

<details><summary>点击展开更多提交日志</summary>

- 20240129
  - 新增猫耳FM直播录制
- 20240127
  - 新增千度热播直播录制、新增pandaTV(韩国)直播录制
  - 新增telegram直播状态消息推送，修复了某些bug
  - 新增自定义设置不同直播间的录制画质(即每个直播间录制画质可不同)
  - 修改录制视频保存路径为 `downloads` 文件夹，并且分平台进行保存。
- 20240114
  - 新增网易cc直播录制，优化ffmpeg参数，修改AfreecaTV输入直播地址格式
  - 修改日志记录器 @[iridescentGray](https://github.com/iridescentGray)
- 20240102
  - 修复Linux上运行，新增docker配置文件
- 20231210
  - 修复录制分段bug，修复bigo录制检测bug
  - 新增自定义修改录制主播名
  - 新增AfreecaTV直播录制，修复某些可能会发生的bug
- 20231207
  - 新增blued直播录制，修复YY直播录制，新增直播结束消息推送
- 20231206
  - 新增bigo直播录制
- 20231203
  - 新增小红书直播录制（全网首发），目前小红书官方没有切换清晰度功能，因此直播录制也只有默认画质
  - 小红书录制暂时无法循环监测，每次主播开启直播，都要重新获取一次链接
  - 获取链接的方式为 将直播间转发到微信，在微信中打开后，复制页面的链接。
- 20231030
  - 本次更新只是进行修复，没时间新增功能。
  - 欢迎各位大佬提pr 帮忙更新维护
- 20230930
  - 新增抖音从接口获取直播流，增强稳定性
  - 修改快手获取直播流的方式，改用从官方接口获取
  - 祝大家中秋节快乐！
- 20230919
  - 修复了快手版本更新后录制出错的问题，增加了其自动获取cookie(~~稳定性未知~~)
  - 修复了TikTok显示正在直播但不进行录制的问题
- 20230907
  - 修复了因抖音官方更新了版本导致的录制出错以及短链接转换出错
  - 修复B站无法录制原画视频的bug
  - 修改了配置文件字段，新增各平台自定义设置Cookie
- 20230903
  - 修复了TikTok录制时报644无法录制的问题
  - 新增直播状态推送到钉钉和微信的功能，如有需要请看 [设置推送教程](https://d04vqdiqwr3.feishu.cn/docx/XFPwdDDvfobbzlxhmMYcvouynDh?from=from_copylink)
  - 最近比较忙，其他问题有时间再更新
- 20230816
  - 修复斗鱼直播（官方更新了字段）和快手直播录制出错的问题
- 20230814
  - 新增B站直播录制
  - 写了一个在线播放M3U8和FLV视频的网页源码，打开即可食用
- 20230812
  - 新增YY直播录制
- 20230808
  - 修复主播重新开播无法再次录制的问题
- 20230807
  - 新增了斗鱼直播录制
  - 修复显示录制完成之后会重新开始录制的问题
- 20230805
  - 新增了虎牙直播录制，其暂时只能用flv视频流进行录制
  - Web API 新增了快手和虎牙这两个平台的直播流解析（TikTok要代理）
- 20230804
  - 新增了快手直播录制，优化了部分代码
  - 上传了一个自动化获取抖音直播间页面Cookie的代码，可以用于录制
- 20230803
  - 通宵更新 
  - 新增了国际版抖音TikTok的直播录制，去除冗余 简化了部分代码
- 20230724	
  - 新增了一个通过抖音直播间地址获取直播视频流链接的API接口，上传即可用
  </details>
  &emsp;

## 有问题可以提issue, 我会在这里持续添加更多直播平台的录制 欢迎Star
#### 
