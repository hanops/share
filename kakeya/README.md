# 挂谷猜想 · KAKEYA 3D LAB

挂谷猜想的交互式数学可视化，发布路径为 `/kakeya/`。

## 实现

- 单文件页面：`index.html`
- Three.js 0.128.0 与 OrbitControls 通过 jsDelivr 加载
- Scene 01：转针问题与三类容器
- Scene 02：Perron 树、面积衰减和切割平移动画
- Scene 03：三维方向填充
- Scene 04：历史年表
- 桌面端使用左右 HUD，手机端使用底部抽屉

页面依赖 WebGL 和外部 CDN。Three.js 无法加载时，启动层会显示网络错误提示。

## 本地检查

从仓库根目录运行：

```bash
make serve
make check
```

访问 <http://127.0.0.1:8000/kakeya/>。应逐一切换四个场景，操作播放按钮和滑块，并检查 390 × 844 手机视口中的底部抽屉。

## 墨问 GIF 导出

`scripts/export_mowen_gifs.py` 是该子项目的可选内容导出工具。它需要 Pillow 和 macOS 系统字体，生成文件写入被忽略的 `output/mowen/`，不属于 GitHub Pages 运行依赖。

从仓库根目录运行：

```bash
python3 kakeya/scripts/export_mowen_gifs.py
```

## 内容边界

数学定理、证明归属、人物履历、年份、奖项与开放问题状态都需要权威来源。结构检查和可视化运行成功不代表这些事实已经核验。
