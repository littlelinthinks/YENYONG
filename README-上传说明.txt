YENYONG v31 Fixpack 4 — 2026-10-03
==================================
内容：恢复首页导航"滚动变色"原设计（此前被误当作 bug 移除）。
- 页面未滚动：白底 + 宝蓝字
- 滚动超过 80px：宝蓝底 + 白字（logo 反色、按钮变白底蓝字）
仅改动 5 个文件：index.html、de/index.html、fr/index.html、ru/index.html、zh/index.html
其余页面（projects/downloads 等）保持白底宝蓝字静态导航，不受影响。

上传方法：5 个 index.html 按路径对应覆盖上传到仓库根目录及 de/fr/ru/zh 文件夹。
上传后等 1-2 分钟构建，强刷（Ctrl+Shift+R）验证。
