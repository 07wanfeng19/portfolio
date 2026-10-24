# 个人作品集 · Personal Portfolio

> 一个纯技术作品展示仓库：在线工具箱、网页数据抓取工具、Android 生态移植案例。

## 作品一览

| 作品 | 类型 | 说明 | 在线 |
|---|---|---|---|
| 在线工具箱 | 前端网页 | 5 个实用小工具，零依赖、单文件、离线可用 | [在线演示](https://07wanfeng19.github.io/portfolio/) |
| 网页抓取工具 | Python 脚本 | 零依赖、自动解析、导出 CSV/JSON | 见 [`scraper/`](scraper/) |
| Android 生态移植 | 桌面宠物 | 开源项目 dsh-pet 的 Android 端适配（见下方说明） | [whale-girl-pet](https://github.com/07wanfeng19/whale-girl-pet) |

## 作品详情

### 1. 在线工具箱（toolbox/）

纯前端实现的实用工具集，单文件、零依赖、数据完全在浏览器内处理：

- JSON 格式化 / 校验 / 压缩
- Unix 时间戳 ↔ 日期互转
- Base64 编解码
- 文本哈希（MD5 / SHA-1 / SHA-256）
- 字数 / 字符统计

在线演示：<https://07wanfeng19.github.io/portfolio/>

### 2. 网页数据抓取工具（scraper/）

零依赖 Python 脚本，自动解析网页并导出 CSV/JSON。详见 [`scraper/README.md`](scraper/README.md)。

### 3. Android 生态移植案例（whale-girl-pet）

一个跑在 Android 上的桌面宠物：悬浮窗 + 24fps 视频渲染 + 可接 DSH 工作台 / 任意 OpenAI 兼容接口。

> **作品边界声明（重要）**
> 该项目的角色素材（webm 动画、表情包、立绘、字体、人设文案）全部来自开源项目
> [`dsh-pet`](https://github.com/PC2005-cloud/dsh-pet)（npm 包 [`dsh-pet`](https://www.npmjs.com/package/dsh-pet)，MIT）。
> 本作品**只负责 Android 端生态适配**（悬浮窗与前台服务、GL 渲染、动画调度、气泡/面板交互、
> DSH 桥接、无障碍自动发送、打包签名安装），不制作、不主张这些素材的著作权。
>
> **本项目仅作为「Android 生态移植」的成功案例展示，不进行任何非授权收益行为，尊重上游开源项目。**
> 素材的使用、二次分发与商用，请遵守上游许可及实际权利人要求。

代码仓库：<https://github.com/07wanfeng19/whale-girl-pet>

## 仓库结构

```
portfolio/
├── index.html          # 在线工具箱（GitHub Pages 首页）
├── toolbox/            # 工具箱源码副本
├── scraper/            # 网页抓取工具
├── 案例图1_工具箱.png    # 作品配图
├── 案例图2_抓取脚本.png  # 作品配图
└── README.md           # 本文件
```

## License

代码：MIT。鲸鱼娘素材版权归上游 `dsh-pet` 及实际权利人所有，不随本仓库 MIT 重新授权。
