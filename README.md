# Share

由多个独立子项目组成的静态页面集合，直接通过 GitHub Pages 发布。

- 在线站点：<https://hanops.github.io/share/>
- 源码仓库：<https://github.com/hanops/share>

## 子项目

| 目录 | 页面 | 项目说明 |
| --- | --- | --- |
| `ergonomic-chair/` | SPINAIR S9 Pro 电商详情页 | [README](ergonomic-chair/README.md) |
| `kakeya/` | 挂谷猜想交互可视化 | [README](kakeya/README.md) |

每个子项目以自己的目录作为边界，并在目录内维护项目说明和 Agent 约定。根目录只负责页面索引、共享检查和仓库级配置。

## 仓库级命令

要求 Python 3.9 或更高版本。站点本身不需要安装依赖。

```bash
make serve
make check
```

本地入口为 <http://127.0.0.1:8000/>。检查会验证所有 HTML 的基本结构、重复 ID、本地资源引用，以及首页是否收录全部一级页面。

## 发布

`main` 分支是 GitHub Pages 发布源，仓库不维护单独的构建产物。
