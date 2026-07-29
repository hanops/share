# SPINAIR S9 Pro

面向电商详情场景的单页长图设计，发布路径为 `/ergonomic-chair/`。

## 实现

- 单文件入口：`index.html`
- HTML、CSS、SVG 和原生 JavaScript 全部内联
- Google Fonts 提供 Archivo、DM Sans、Noto Sans SC 和 Noto Serif SC
- 页面宽度以 790 px 的长页画布为基准
- 包含 12 个内容章节、滚动揭示、计数动画、悬浮反馈和底部购买栏

页面没有构建步骤，也不依赖本地图片资源。产品主体、结构示意和图标主要使用内联 SVG 与 CSS 绘制。

## 本地检查

从仓库根目录运行：

```bash
make serve
make check
```

访问 <http://127.0.0.1:8000/ergonomic-chair/>。视觉改动应同时检查桌面端与 390 × 844 手机视口，并完整滚动一次页面以触发延迟动画和底部购买栏。

## 内容边界

价格、调节范围、承重、认证、用户数量、评分和评价均属于事实性或营销性声明。修改前需要核验来源，演示内容不得表述为已验证的真实销售数据。
