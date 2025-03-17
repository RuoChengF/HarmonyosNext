> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/4206b79e-a950-403e-810a-61b2d474e6dd.png)

# HarmonyOS NEXT  跑马灯组件详解(一): 组件概述与架构设计
## 效果演示

![](https://files.mdnice.com/user/47561/515b84cc-bcf8-48d2-97d2-06bc62b51180.jpg)
## 1. 组件简介

跑马灯(Marquee)组件是一个用于展示滚动文本的UI组件，主要用于处理文本内容超出显示区域时的展示问题。当文本内容过长时，组件会自动实现文本的循环滚动效果，并在每次循环结束后暂停一定时间。

## 2. 核心功能

- 文本自动滚动展示
- 支持自定义滚动速度和方向
- 可配置滚动间隔和动画效果
- 适配不同屏幕尺寸(手机/平板)
- 支持自定义文本样式

## 3. 基础架构

整个跑马灯组件由以下几个主要部分组成：

```typescript
@Component
export struct MarqueeViewComponent {
  // 主容器组件
}

@Component
struct TripView {
  // 行程信息容器
}

@Component
struct TripMessage {
  // 单条行程信息展示
}

@Component
export struct FunctionDescription {
  // 功能描述组件
}
```

## 4. 关键类和接口

### 4.1 动画配置类

```typescript
export class MarqueeAnimationModifier {
  iterations: number;    // 动画播放次数
  duration: number;      // 动画持续时间
  tempo: number;        // 动画播放速度
  playMode: PlayMode;   // 播放模式
  delayTime: number;    // 延迟时间
}
```

### 4.2 滚动配置类

```typescript
export class MarqueeScrollModifier {
  scrollWidth: Length;  // 滚动区域宽度
  space: number;       // 文本间距
}
```

## 5. 组件层级结构

```
MarqueeViewComponent (根组件)
├── FunctionDescription (功能描述)
└── TripView (行程视图)
    └── TripMessage (行程信息)
        └── MarqueeSection (跑马灯核心组件)
```

## 6. 使用场景

该组件特别适用于以下场景：

- 新闻公告滚动展示
- 长文本信息展示
- 消息通知展示
- 实时信息更新展示

## 7. 代码示例

基本使用方式：

```typescript
MarqueeSection({
  marqueeTextBuilder: () => {
    this.marqueeTextBuilder(this.tripDataItem.ticketEntrance)
  },
  marqueeAnimationModifier: new MarqueeAnimationModifier(),
  marqueeScrollModifier: new MarqueeScrollModifier(
    display.isFoldable() ? 
    $r('app.string.marquee_scroll_phone_width') : 
    $r('app.string.marquee_scroll_tablet_width'),
    Constants.BLANK_SPACE
  )
})
```

## 8. 关键知识点解析

### 8.1 装饰器使用
- `@Component`: 声明一个自定义组件
- `@State`: 组件状态管理
- `@Builder`: 自定义构建函数

### 8.2 响应式设计
- 使用`display.isFoldable()`判断设备类型
- 通过资源引用(`$r`)实现不同设备适配

### 8.3 布局设计
- 使用`Column`和`Row`进行弹性布局
- 通过`RelativeContainer`实现相对定位

## 9. 小结

跑马灯组件是一个功能完整、易于使用的UI组件，通过合理的架构设计和模块化的代码组织，使得组件具有良好的可维护性和扩展性。在后续的文章中，我们将深入探讨每个模块的具体实现细节。
