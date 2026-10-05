# 本版验收记录

验收日期：2026-10-04 至 2026-10-05。课程准备与环境验收不代表学生已上课或掌握。

| 项目 | 实际证据 | 状态 |
|---|---|---|
| macOS Apple Silicon | 本机 R 4.5.3、Python 3.12.14；12 个教材 Notebook 全部由 R 内核执行，无报错 | 通过 |
| 独立环境检查 | R 下标、逐元素运算、NA、样本标准差、已知直线的最小二乘、固定种子和 CSV 读写 | 通过 |
| 科学绘图 | R09 实际执行的图像；白底、坐标名称和 SI 单位已目视检查 | 通过 |
| 浏览器入口 | Chrome 显示 START 首页，点击 R01 进入个人作答副本，识别 R 内核 | 通过 |
| 课堂启停 | Mac 下课入口关闭；重复启动复用服务；再次关闭；现有 work 文件的 SHA-256 全部保持相同 | 通过 |
| Windows x64 依赖 | conda-forge win-64 解析成功，221 个包；未执行 Windows 二进制 | 解析通过，运行待验证 |
| Windows x64 课堂 | GitHub Windows CI 中 setup-windows.cmd 安装成功；12 个示例、独立检查和启停、现有 work 文件保留检查均通过 | CI 通过，个人电脑 GUI 待验证 |
| macOS Apple Silicon CI | GitHub macos-26-arm64 上安装、12 个示例及启停、文件保留检查均通过 | CI 通过 |
| macOS Intel | GitHub macos-15-intel 上安装、12 个示例及启停、文件保留检查均通过 | CI 通过 |
| 含空格的安装目录 | 三种 CI 环境均在 R classroom 目录中安装并完整运行；Unix R 启动路径已修复 | 通过 |
| Windows ARM / Linux | 本版未提供相应原生入口或运行验收 | 不在本版验收范围 |
| Google 导师 | 提供可复制启动文字；没有自动发消息或读取聊天 | 配置已准备，教学效果未测 |

本地原始运行证据放在 `.validation/`，其中含执行后的 Notebook、环境报告与启停报告。该目录默认不进入公共 Git；GitHub CI 每次运行独立生成报告。最终 [三平台完整运行记录](https://github.com/gycsunny163-dev/r-computing-classroom/actions/runs/37311708777) 已通过，覆盖运行代码提交 2bff52592ea72c48db49bccbf780b3902e3a3fea；之后的文档更新不改变这些运行代码。Mac ARM、Mac Intel、Windows 各有可下载的 validation artifact，其中包括 report.json、lifecycle.json、12 个执行后的教材 Notebook 和环境检查 Notebook。

[含空格目录的首轮补测](https://github.com/gycsunny163-dev/r-computing-classroom/actions/runs/37311005234) 发现 conda R 的 Unix 启动脚本把安装路径直接写成未加引号的赋值，导致两种 Mac 架构安装后启动失败；Windows 测试引用了不一致的运行目录。安装设置已增加课程自有 R 环境的路径引号修复，保留原始脚本备份，并拒绝修改环境外的 R。Windows 的测试路径也已统一；修复后的三平台完整检查与报告下载均已通过。

CI 的 Windows 环境是 GitHub 托管 Windows runner，浏览器不打开。它验证真实 Windows 安装、R 内核执行和本机服务生命周期，不替代 Windows 10 或 11 上双击入口、浏览器交互和首次系统来源批准的人工验收。Mac 本机 Chrome 交互已另行检查；Intel 机型及第三方个人设备以自身实际运行结果为准。

维护者的验证方式：在本课程环境中执行 `python tests/validate.py --runtime <本机运行目录>` 和 `python tests/lifecycle.py --runtime <本机运行目录>`。后者会关闭当前仓库的课堂服务；运行前请先保存个人作答。两项检查不打开 AI 网站、不上传作答、不执行学生答案。

R 在线手册与函数帮助的版本范围见 `course/sources.json`。合成 CSV 只用于教学；独立环境检查不是考试题。初始学习状态全部为 unassessed。
