> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/d93f261a-86cc-4416-a309-fa69fedffc39.png)

# HarmonyOS NEXT跑马灯组件教程：基础概念与架构设计

## 1. 跑马灯组件概述

跑马灯（Marquee）是一种常见的UI组件，主要用于在有限的空间内展示超出显示区域的文本内容。当文本内容过长无法在固定宽度内完整显示时，跑马灯组件会使文本自动滚动，以便用户可以查看全部内容。在HarmonyOS NEXT中，跑马灯组件被广泛应用于消息通知、公告栏等场景。

### 1.1 应用场景

| 场景 | 描述 | 优势 |
|------|------|------|
| 消息通知 | 展示系统或应用的通知消息 | 节省空间，吸引用户注意 |
| 公告栏 | 展示重要公告或活动信息 | 内容可循环播放，不遗漏信息 |
| 票务信息 | 展示车票、机票等检票口信息 | 动态效果明显，易于识别 |
| 商品促销 | 展示促销信息或折扣活动 | 增强视觉吸引力 |

### 1.2 基本功能

跑马灯组件的核心功能是实现文本的自动滚动，具体包括：

1. **文本滚动**：当文本宽度超过显示区域时，自动进行水平滚动
2. **循环播放**：支持设置滚动次数，可以无限循环或指定次数
3. **滚动方向**：支持从左到右或从右到左滚动
4. **滚动速度**：可调整滚动速度和动画持续时间
5. **滚动间隔**：每次滚动完成后可设置停顿时间

## 2. 组件架构设计

### 2.1 整体架构

跑马灯组件采用了模块化的设计思想，将功能划分为多个模块，每个模块负责不同的功能。整体架构如下：

```
跑马灯组件
├── 组件层（Component）
│   ├── MarqueeViewComponent - 跑马灯视图组件
│   └── MarqueeSection - 跑马灯核心实现组件
├── 模型层（Model）
│   ├── DataType - 数据类型定义
│   ├── Constants - 常量定义
│   └── DataSource - 数据源实现
└── 工具层（Utils）
    └── Logger - 日志工具
```

### 2.2 核心文件说明

| 文件名 | 路径 | 功能描述 |
|------|------|------|
| MarqueeDemo.ets | pages/StudyHo/ | 跑马灯组件使用入口 |
| Marquee.ets | components/Marquee/ | 跑马灯视图组件定义 |
| MarqueeSection.ets | utils/marquee/ | 跑马灯核心实现 |
| DataType.ets | model/marquee/ | 数据类型和配置选项定义 |
| Constants.ets | model/marquee/ | 常量定义 |
| DataSource.ets | model/marquee/ | 数据源实现 |
| Logger.ets | utils/marquee/ | 日志工具 |

## 3. 组件使用方式

### 3.1 基本使用

跑马灯组件的使用非常简单，只需要在页面中引入并使用即可：

```typescript
// MarqueeDemo.ets
import { MarqueeViewComponent } from "../../components/Marquee/Marquee";
@Entry
@Component
struct MarqueeDemo {
    build() {
        RelativeContainer() {
            MarqueeViewComponent()
        }
        .height('100%')
        .width('100%')
    }
}
```

这段代码展示了跑马灯组件的基本使用方式：

1. 首先导入`MarqueeViewComponent`组件
2. 在页面的`build`方法中使用`RelativeContainer`作为容器
3. 在容器中添加`MarqueeViewComponent`组件
4. 设置容器的宽高为100%，使其填满整个页面

### 3.2 自定义配置

跑马灯组件支持多种自定义配置，可以通过传入不同的参数来实现：

```typescript
// 自定义跑马灯动画属性
MarqueeSection({
  marqueeTextBuilder: () => {
    this.marqueeTextBuilder(this.tripDataItem.ticketEntrance)
  },
  marqueeAnimationModifier: new MarqueeAnimationModifier(
    -1,                    // 无限循环
    5000,                  // 动画持续时间5秒
    1.5,                   // 动画速度1.5倍
    PlayMode.Normal,       // 从左到右滚动
    2000                   // 停顿时间2秒
  ),
  marqueeScrollModifier: new MarqueeScrollModifier(
    '30%',                // 滚动区域宽度为30%
    80                     // 文本间隔80像素
  )
})
```

## 4. 组件实现原理

### 4.1 基本原理

跑马灯组件的实现原理主要基于以下几点：

1. **文本宽度检测**：通过`onAreaChange`事件获取文本实际宽度和滚动区域宽度
2. **条件判断**：当文本宽度大于滚动区域宽度时，才启动滚动动画
3. **动画实现**：使用`animateTo`方法实现文本的平滑滚动
4. **循环控制**：通过计数器和定时器控制动画的循环次数和间隔时间

### 4.2 关键代码分析

```typescript
// MarqueeSection.ets中的核心实现
scrollAnimation() {
    // 文本宽度小于Scroll组件宽度，不执行滚动操作
    if (this.ticketCheckTextWidth < this.ticketCheckScrollWidth) {
        return;
    }
    
    animateTo({
        duration: this.marqueeAnimationModifier.duration,
        tempo: this.marqueeAnimationModifier.tempo,
        curve: Curve.Linear,
        onFinish: () => {
            // 动画完成后的处理...
            
            // 使用定时器实现停顿效果
            this.timer = setTimeout(() => {
                this.scrollAnimation();
            }, this.marqueeAnimationModifier.delayTime)
        }
    }, () => {
        // 设置文本偏移量，实现滚动效果
        this.ticketCheckTextOffset = this.marqueeAnimationModifier.playMode === PlayMode.Normal ?
            -(this.ticketCheckTextWidth + this.marqueeScrollModifier.space) :
            -(this.ticketCheckTextWidth - this.ticketCheckScrollWidth)
    })
}
```

## 5. 总结

本文介绍了HarmonyOS NEXT跑马灯组件的基础概念和架构设计，包括组件的应用场景、基本功能、整体架构、使用方式和实现原理。通过本文的学习，读者可以了解跑马灯组件的基本结构和工作原理，为后续深入学习组件的具体实现打下基础。

在下一篇教程中，我们将深入探讨跑马灯组件的核心实现——MarqueeSection组件，详细分析其属性、方法和实现细节。
