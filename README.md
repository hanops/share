# Share

个人静态页面集合，直接由 GitHub Pages 发布，不需要构建步骤。

- 在线站点：<https://hanops.github.io/share/>
- 源码仓库：<https://github.com/hanops/share>

## 页面

| 路径 | 内容 | 实现 |
| --- | --- | --- |
| `/` | 页面索引 | HTML + CSS |
| `/ergonomic-chair/` | SPINAIR S9 Pro 电商详情页 | HTML + CSS + SVG + 原生 JavaScript |
| `/kakeya/` | 挂谷猜想交互可视化 | HTML + CSS + Canvas + Three.js |

每个页面都是可独立部署的 `index.html`。样式和业务脚本以内联方式维护；字体来自 Google Fonts，挂谷页面额外从 jsDelivr 加载 Three.js 和 OrbitControls。

## 本地开发

要求 Python 3.9 或更高版本，无需安装项目依赖。

```bash
make serve
```

然后访问 <http://127.0.0.1:8000/>。

提交前运行：

```bash
make check
```

检查会验证 HTML 基本结构、重复 ID、本地资源引用，以及首页是否收录所有一级页面。

## 发布

`main` 分支是发布源。推送后由 GitHub Pages 直接提供仓库中的静态文件；本仓库不维护单独的构建产物。

## 内容注意事项

页面中的产品参数、用户数据、认证信息、数学史和奖项信息属于需要来源支撑的事实性内容。修改此类内容时，应同步核验权威来源，并避免把演示数据表述为已验证事实。
