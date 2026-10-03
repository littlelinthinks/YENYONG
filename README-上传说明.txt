YENYONG v31 Fixpack 3 — 2026-10-03 (含法/俄博客正文补全)
==================================================
本次修复内容：
1. Insights 逻辑统一：全站所有指向旧 news.html 的链接改为 insights.html，news.html 变为自动跳转页。
   （此前从首页 Products 下拉进入的"Insights"其实是旧页面 news.html，里面有跳首页的产品链接和高亮的 Contact——你看到的所有怪现象的根源）
2. 文章页恢复导航栏：每篇文章顶部导航含 INSIGHTS 高亮链接 + Home/Insights 面包屑 + 文章底部"返回文章列表"按钮（5 种语言）。
3. Insights 卡片：缩略图加链接、整卡可点击、悬停放大效果（5 种语言）。
4. 导航文字改为宝蓝色（assets/css/base.css）：Projects / Downloads 等所有页面的导航不再是黑灰色。
5. 首页导航不再随滚动变色：全站导航统一白底宝蓝字（5 种语言首页）。
6. 死链清理：各语言 FAQ 404 → 占位跳转；语言版隐私/条款链接修正；首页两张新闻卡死链修正。
7. 翻译补全：法/俄 carbon-crystal-explained.html 文章正文此前漏翻（仍为英文），本次补全。

上传方法（共 91 个文件，按文件夹对应上传到仓库）：
- assets/css/base.css        -> assets/css/
- 根目录 *.html              -> 仓库根目录
- blog/*.html (10 个)        -> blog/
- de|fr|ru|zh/*.html         -> 对应语言文件夹
- de|fr|ru|zh/blog/*.html    -> 对应语言 blog 文件夹
- de|fr|ru|zh/faq.html       -> 对应语言文件夹（新文件）
上传后等 1-2 分钟构建，强刷（Ctrl+Shift+R）验证。
