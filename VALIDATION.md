# 本版验收记录

验收日期：2026-10-04。课程准备与环境验收不代表学生已上课或掌握。

| 项目 | 实际证据 | 状态 |
|---|---|---|
| macOS Apple Silicon | 本机 R 4.5.3、Python 3.12.14；12 个教材 Notebook 全部由 R 内核执行，无报错 | 通过 |
| 独立环境检查 | R 下标、逐元素运算、NA、样本标准差、已知直线的最小二乘、固定种子和 CSV 读写 | 通过 |
| 科学绘图 | R09 实际执行的图像；白底、坐标名称和 SI 单位已目视检查 | 通过 |
| 浏览器入口 | Chrome 显示 START 首页，点击 R01 进入个人作答副本，识别 R 内核 | 通过 |
| 课堂启停 | Mac 下课入口关闭；重复启动复用服务；再次关闭；现有 work 文件的 SHA-256 全部保持相同 | 通过 |
| Windows x64 依赖 | conda-forge win-64 解析成功，221 个包；未执行 Windows 二进制 | 解析通过，运行待验证 |
| Windows x64 课堂 | 本版提供 .cmd 入口和 GitHub Actions 示例、启停测试 | 待 CI 或实机验证 |
| macOS Intel | 安装入口按架构选择 osx-64 包 | 待 CI 或实机验证 |
| Windows ARM / Linux | 本版未提供相应原生入口或运行验收 | 不在本版验收范围 |
| Google 导师 | 提供可复制启动文字；没有自动发消息或读取聊天 | 配置已准备，教学效果未测 |

本地原始运行证据放在 `.validation/`，其中含执行后的 Notebook、环境报告与启停报告。该目录默认不进入公共 Git；GitHub CI 每次运行可独立生成证据并作为 artifact 保存。仓库中的 workflow 尚未上传运行，不能将它当作 Windows 测试已经通过。

维护者的验证方式：在本课程环境中执行 `python tests/validate.py --runtime <本机运行目录>` 和 `python tests/lifecycle.py --runtime <本机运行目录>`。后者会关闭当前仓库的课堂服务；运行前请先保存个人作答。两项检查不打开 AI 网站、不上传作答、不执行学生答案。

R 在线手册与函数帮助的版本范围见 `course/sources.json`。合成 CSV 只用于教学；独立环境检查不是考试题。初始学习状态全部为 unassessed。
