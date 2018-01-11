## 帮助文档

**注意**：此脚本还属于内测中。很多功能都没有经过严格测试。<br>
**测试前请备份好V2Ray-core配置文件**<br>
**测试前请备份好V2Ray-core配置文件**<br>
**测试前请备份好V2Ray-core配置文件**

### 目标人群
由于脚本还在内测中。所以目前脚本针对的目标人群不是所有人。<br>
如果你是下列人群，欢迎测试这个脚本帮助改进。
   * 对技术感觉兴趣，愿意学习新技术
   * 熟悉Qt程序，可以指正脚本中的错误地方
   * 脚本使用过程中出错，知道如何修改相应的代码解决问题
   * 脚本使用过程中出错，知道如何复现出错问题，定位出错原因
   * 脚本导入导出JSON配置错误，并知道如何修改成正确配置
   * 熟习[V2Ray官方文档](https://www.v2ray.com/chapter_02/01_overview.html)，并且知道如何配置v2ray-core JSON配置文件
   * 不怕被冷落

### BUG提交
如果你[提交一个BUG](https://www.chiark.greenend.org.uk/~sgtatham/bugs-cn.html)，但无法提供复现方法与步骤或者解决方法。不会得到优先处理。<br>
任何要求增加新功能的要求将不会被优生处理。<br>
复现步骤时，请把icons, translations, config.v2rayshell这个三个文件放到src/bridgehouse/目录中。<br>
在命令行运行`python3 bridge.py`,以便获得Python Traceback数据。<br>

* 编辑器不支持编辑带有注释的JSON文件。请自行移除注释。 [原因](https://plus.google.com/+DouglasCrockfordEsq/posts/RK8qyGVaGSr)
* 编辑器生成的配置只能保证符合文档规范，无法保证配置是否有用。
* 使用编辑器生成的配置文件之前请使用如下命令检查配置是否正确 `v2ray -test config.json` (暂无计划将此功能集成在脚本中)
* 编辑JSON文档暂无错误提示。
* 编辑器不对输入的数据做合法验证。比如IP地址可以输入IPv4,IPv6,域名,或者其他任意数据
* 如果想直接使用编辑器，可以在src/bridgehouse/editMap/ 目录找到 nauticalChartPanel.py
* 代理服务器延迟测试，并非为本地计算机到VPS的延迟。这个延迟是访问http://www.google.com的延迟。
* 如果频繁测试google.com服务器可能会引起DDOS。VPS有被拉黑的风险。最小测试时间间隔为60秒。
对此，你可以在自己的VPS开启http协议用作代理连接状态检查。(当然检查V2Ray-core的日志文件也是个有效的方法,同样暂无计划将此功能集成在脚本中。)
* 代理服务器无法连接时自动切换到另一个配置，可能不太稳定。暂时还没有很好的解决方案。
* 编辑JSON文档时，不会自动分析in/outbound(Detour)已有的policy level。<br>在面板中添加新的in/outbound(Detour)时,所有的policy level会出现在PolicyTAB列表中(V2Ray-core V3.1之前的配置文件会有此问题)。
* 如果v2ray-shell崩溃关闭，会可能导致正在运行的v2ray进程变成[孤儿进程](https://zh.wikipedia.org/wiki/%E5%AD%A4%E5%84%BF%E8%BF%9B%E7%A8%8B),这时需要手动关闭v2ray。
* 测试服务器连接状态功能关闭，服务器延迟测试也会自己关闭。
* 编译二进制文件，使用二进制文件的一切问题无法处理。
* build.py文件为开发人员使用，可以删除。

### 参与开发
欢迎任何对此脚本感兴趣的开发者参与开发。<br>
但请知道，参与这个脚本的开发者必须放弃对脚本的一切权利(开发者同样也包括原始作者)。<br>
如果你无法接受这个条件，你可以自由复制这个脚本单独发行。<br>
但请注意如果使用PyQt请遵循Riverbank公司的[协议](https://www.riverbankcomputing.com/commercial/license-faq)。<br>
或者使用PySide请遵循Qt公司[相应协议](http://code.qt.io/cgit/pyside/pyside-setup.git/tree/?h=5.9)<br>
为了兼顾两家公司的协议，所以此脚本才会使用[公有领域协议](https://zh.wikipedia.org/wiki/%E5%85%AC%E6%9C%89%E9%A2%86%E5%9F%9F)<br>
如果你购买了Riverbank或Qt的商业授权。闭源是被允许。

### 维护
由于作者还有其他工作。只能用业余时间去维护这个项目。<br>
有一年的有效维护保证。<br>
每个季度维护一次(致命错误，其他重要情况除外)。<br>
到2018年12月会视下一年安排，会作出如何接着维护这个项目的决定。<br>
一但项目稳定版本发行，需要维护的地方将很少。

### 新功能增加
由于这个脚本支持多平台运行。为了减少维护成本，很多功能不增加。<br>
如开机自启动，设置系统代理，向导生成配置，自动生成配置，配置模板，二维码等等...<br>
也无法提供[负载均衡](https://zh.wikipedia.org/wiki/%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1)，[服务质量](https://zh.wikipedia.org/wiki/%E6%9C%8D%E5%8A%A1%E8%B4%A8%E9%87%8F)等等...<br>
脚本中路由配置的编辑暂时不支持,坑太大暂时不填...<br>
后续的维护主要针对v2ray-core JSON配置文件编辑器进行修改。减少很多不必要的控件。

### 二进制文件
此脚本不直接提供二进制文件。请自行编译。<br>
编译方法:<br>
先安装pyinstaller,安装方法之一 `pip install pyinstaller`<br>
然后到/src/bridgehouse/目录，在命令行中执行如下编译命令:<br>

`pyinstaller -F --noconsole -name v2ray-shell bridge.py` <br>
或者使用 `pyinstaller v2ray-shell.spec` 生成可独立运行的二进制文件可在dist目录中找到。<br>
windows平台亦可直接使用build.py直接生成二进制文件,有可能失败。
windows平台确保有libeay32.dll与ssleay32.dll与安装包同目录。<br>
这两个文件可以在Python PyQt5安装目录中找到(../Lib/site-packages/PyQt5/Qt/bin/)<br>
请确保icons与translations与二进制文件同一个目录，以便使用相应功能。<br>

ubuntu-17.10测试时，pyinstaller使用的是python2.7。请改为python3.6运行。<br>
命令行中使用which pyinstaller找到pyinstaller文件。<br>
修改 `#!/usr/bin/python` 为 `#!/usr/bin/python3` <br>

发布二进制文件时，请附带此脚本的源代码与相应协议。<br>
**备注** :*这个测试在windows 10 平台通过，其他平台未知。对于编译二进制文件， 与其出现的一切问题无法处理*<br>
**谨慎使用第三方发布的二进制文件**<br>
**谨慎使用第三方发布的二进制文件**<br>
**谨慎使用第三方发布的二进制文件**

### 翻译
欢迎有能力与时间的朋友参与脚本的翻译与修正。<br>
或者帮助设计无版权图标(带Alpha通道的PSD或者TIF文件受欢迎)。
翻译方法：<br> 
> 1. [注册QT账号](https://login.qt.io/login) [下载QT开发包](https://www.qt.io/download-qt-for-application-development) 或者下载在线安装包<br>
>[Linux Host](http://download.qt.io/official_releases/online_installers/qt-unified-linux-x64-online.run)<br>
>[macOS Host](http://download.qt.io/official_releases/online_installers/qt-unified-mac-x64-online.dmg)<br>
>[Windows Host](http://download.qt.io/official_releases/online_installers/qt-unified-windows-x86-online.exe)<br>
> 2. 打开v2rayshell.pro文件，在TRANSLATIONS项目里增加相应语言。<br>
> 3. 命令行中找到v2ray-shell的v2rayshell.pro文件。执行此命令`pylupdate5 v2rayshell.pro`生成ts文件。<br>
> 4. 到translations目录找到相应的ts目标文件。<br>
> 5. 找到QT开发包的Qt Linguist，使用Linguist打开ts文件并开始翻译。Qt Linguist的使用方法可以查看帮助文档Qt Linguist Manual。<br>
> 6. 翻译好后文件后，在Qt Linguist中找到File->Release As 发布翻译好的qm文件。<br>
> 7. 最后打开v2ray-shell脚本，在Option->Preference设置相应的翻译文件并重新启动脚本测试。

### PyQt5学习
此脚本是自底向上开发，几乎所有的脚本都可以单独运行并测试。<br>
开发者也是第一次接触QT编程。学习过程并不困难。欢迎大家一起来学习，交流指正代码中的错误地方。<br>
在学习的过程中请善用[搜索引擎](https://en.wikipedia.org/wiki/Category:Internet_search_engines)，与使用[stackoverflow](https://stackoverflow.com/) [提问](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md)。<br>
其中QT开发文档是最有力的助手。虽然使用的编程语言不同，但并不影响文档的使用。<br>
[PyQt5的Demo代码参考](https://riverbankcomputing.com/software/pyqt/download5)。<br>
一些学习网站:
* [Pythonspot](https://pythonspot.com/en/pyqt5/)
* [zetcode](http://zetcode.com/gui/pyqt5/)
* [PythonBlogs](http://pythonthusiast.pythonblogs.com/index.php?op=Search&blogId=230&searchTerms=pyqt)
* [Python wiki](https://wiki.python.org/moin/PyQt)
* [PySide for Android](http://wiki.qt.io/PySide_for_Android_guide)
* [Archi的中文教程](http://www.cnblogs.com/archisama/tag/PyQt5/)
* [皮皮blog](http://blog.csdn.net/column/details/py-qt.html)

### 其他
这个脚本在2017年10月1日开始编写。使用PyQt5的原因是比较熟悉Python语言。选择QT是因为跨平台友好。<br>
原计划只做个v2ray-core的JSON配置编辑器,写着写着又写了个启动器，现在变成坑了。精力有限，不想搞太深...<br>
在将来的版本中可能会改写成C++与QML结合(有点渺茫)......