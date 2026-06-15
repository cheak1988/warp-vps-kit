# 安装方式

## 方式一：从 GitHub 直接安装 CLI

适合只想使用 `warp-vps-kit` 命令的用户。

```bash
python -m pip install "git+https://github.com/cheak1988/warp-vps-kit.git"
warp-vps-kit --help
```

升级：

```bash
python -m pip install --upgrade "git+https://github.com/cheak1988/warp-vps-kit.git"
```

## 方式二：克隆仓库本地运行

适合想改脚本、看文档、提交 PR 的用户。

```bash
git clone https://github.com/cheak1988/warp-vps-kit.git
cd warp-vps-kit
python -m venv .venv
source .venv/bin/activate
pip install -e .
warp-vps-kit --help
```

Windows PowerShell：

```powershell
git clone https://github.com/cheak1988/warp-vps-kit.git
cd warp-vps-kit
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
warp-vps-kit --help
```

## Windows 中文显示乱码

如果 PowerShell 里 `Get-Content README.md` 显示乱码，通常是终端编码问题，不是文件损坏。

可以用：

```powershell
Get-Content README.md -Encoding UTF8
```

或在 Python 中验证：

```powershell
python -c "from pathlib import Path; print(Path('README.md').read_text(encoding='utf-8')[:80])"
```

GitHub 网页会按 UTF-8 正常渲染。

## 方式三：只复制 VPS 脚本

如果 VPS 上还没装 Git，可以先在本地生成配置，再通过 VNC 或控制台执行脚本内容。

脚本默认 dry run，不会直接修改系统：

```bash
bash scripts/install-xray-ws.sh
bash scripts/install-warp-proxy.sh
```

确认要执行时加 `RUN=1`：

```bash
VLESS_UUID=VLESS_UUID_HERE WS_PATH=/ws RUN=1 bash scripts/install-xray-ws.sh
RUN=1 bash scripts/install-warp-proxy.sh
```
