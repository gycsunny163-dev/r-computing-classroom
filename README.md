# R Computing Classroom

中文 R 入门课程：AI 导师讲解，本机 Jupyter 的 R 内核运行代码。12 节课侧重编程基础、物理数据处理和可复现计算，不是 UCL 官方课，也不含官方或独立考官题库。拥有课程不等于掌握。

第一次使用请读 [完整安装上下课与保存指南](CLASSROOM_GUIDE.md)，其中包含日常操作、学习过程记录、备份、换设备和故障处理。

## 第一次使用

下载仓库 ZIP 并完整解压，或用 Git clone 获取仓库。**从解压后的文件夹运行入口，不在 ZIP 中双击。** 首次安装需要联网和较大磁盘空间；后续本地运行不需要 Google API key，也不自动订阅付费服务。

| 系统 | 首次安装 | 打开课堂 | 进入第一课 | 下课 |
|---|---|---|---|---|
| macOS，Apple Silicon / Intel | `setup-mac.command` | `start-mac.command` | `lesson-R01-mac.command` | `stop-mac.command` |
| Windows 10/11，x64 | `setup-windows.cmd` | `start-windows.cmd` | `lesson-R01-windows.cmd` | `stop-windows.cmd` |

这些文件均可双击。Mac 首次打开若系统要求确认软件来源，走系统的正常批准流程；入口没有禁用 Gatekeeper。若解压工具丢失了执行权限，可在该文件夹的终端执行 `chmod +x *.command` 后再双击。Windows 安装器使用系统自带 curl.exe 和 tar.exe，不更改 PowerShell 执行策略。Windows ARM 尚不在本版验收范围。

工具从 Mamba 官方来源与 conda-forge 获取。R、Jupyter 和本机认证状态保存在用户本地应用数据目录，与课程和个人文件分开；不修改系统 R/Python 或 shell 配置。无需先安装另一套 Python 课堂或 RStudio。

浏览器优先 Chrome；没有 Chrome 时尝试系统默认浏览器。第一课入口还会打开 Google AI Studio 和本课启动文字。**请自己把文字完整复制给 Google 后发送。** 新聊天不会自动继承教学规则；本课程没有本机 Notebook 到 Google 的自动读取或聊天归档。

## 上下课

1. 双击打开课堂，在 `START.ipynb` 选择本次的一节小课。实际作答用 `work/Rxx.ipynb`，教材用 `course/lessons/Rxx.ipynb`。
2. 把 `tutor/Rxx.txt` 的全文提供给 Google 或自己选择的导师。按每次一问、先写第一版、逐步提示的规则学习。
3. 在 Notebook 的 Original first attempt 单元格写代码，Shift+Enter 运行。给导师提交当前代码和真实输出或报错。修正写到 Revision 单元格，不覆盖第一版。
4. 下课让导师总结实际教过的内容、帮助和未闭题，把总结保存到 Notebook 的 Session record。按 Mac ⌘S / Windows Ctrl+S 保存。
5. 双击 stop 入口关闭本课程服务。关浏览器标签不会自动停服务。重新打开时需要按依赖顺序建立变量。

课程默认暂停，不自动连续开课；示例输出是教材演示，不是学生作答。正确输出不单独证明掌握。任务解答或提示暴露必须记录。

## 课程清单

| 单元 | 内容 |
|---|---|
| R01 | 计算、赋值与输出 |
| R02 | 向量与逐元素运算 |
| R03 | 类型、转换与缺失值 |
| R04 | 下标与逻辑筛选 |
| R05 | 条件与循环 |
| R06 | 编写函数 |
| R07 | 列表与数据表 |
| R08 | CSV 和数据检查 |
| R09 | 带单位的科学绘图 |
| R10 | 描述统计与重复测量 |
| R11 | 线性拟合与残差 |
| R12 | 随机模拟与可复现记录 |

每课只有一个当前练习。R12 以后再依据学习证据决定是否扩展到 tidyverse、ggplot2 或更深入统计。数学前提不足时补当前任务需要的概念，不自动增加大计划。

## Git 共享与个人作答

`course/`、`tutor/`、`tools/` 和入口脚本是可共享的课程。`work/` 是每位学生自己的代码和学习记录，默认被 Git 忽略；本机环境、令牌和日志保存在仓库外，不发布到 Git。

`git pull` 更新教材不会覆盖 `work/`。首次设置只复制不存在的个人 Notebook。课程有更新时，自己比较模板与旧作答，避免覆盖历史。请不要用 `git add -f work/` 把个人聊天和学习过程加入公共仓库。

跨设备同步与同学共享是两件事：Git 分发教材；你自己的作答可以另用私有仓库或 iCloud/OneDrive 同步 `work/`。同一 Notebook 不要在两台设备同时编辑。默认不会把同学的作答互相同步。

## 运行验证与平台状态

本版约束 R 4.5、IRkernel 1.3.2、Python 3.12、JupyterLab 4.x；不同平台由 `environment.yml` 分别解析二进制，不把 Mac 安装包复制到 Windows。

Mac Apple Silicon、Intel Mac 和 Windows x64 的自动验收均已通过：安装、12 个教材示例、独立环境检查、服务复用与关闭、现有作答文件保留，以及含空格的安装目录。见 [实际三平台运行结果](https://github.com/gycsunny163-dev/r-computing-classroom/actions/runs/37311708777)。本机 Mac 的 Chrome 交互也已检查；CI 不打开浏览器，个人电脑的首次系统批准和 GUI 使用仍由使用者实际核对。详细范围见 [VALIDATION.md](VALIDATION.md)。

维护者在已安装的环境中运行 `python tests/validate.py --runtime <本机运行目录>`；它只执行教材示例与独立环境检查，不读取学生答案。输出保存在 Git 忽略的 `.validation/`。`--save-example-outputs` 是维护者发布教材输出用的选项。

## 来源

基础内容以 [R Core 官方入门手册](https://cran.r-project.org/doc/manuals/r-release/R-intro.html) 与 R 的官方函数帮助为来源。安装依据 [Mamba 官方文档](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html) 和 [IRkernel 文档](https://irkernel.github.io/installation/)。完整范围、版本差异与证据限制见 `course/sources.json` 和 `course/evidence.jsonl`。

CSV 是合成教学数据，不是实际实验记录。所有课程文字、练习和示例新编；引用资料仅以链接列出。没有把 R/Jupyter/Mamba 的二进制或第三方教材版权内容捆绑进仓库。

## 分发许可

本仓库新编的课程内容与工具按 MIT License 分发，允许同学使用、修改和分享，保留 LICENSE 即可。所链接的第三方资料及由安装器下载的工具遵循各自的许可，不因链接或安装而改用本仓库许可。
