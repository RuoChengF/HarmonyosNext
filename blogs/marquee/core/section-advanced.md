> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/8723e0ab-d0a9-4b0c-a2bb-4ca8a6c5ae99.png)

# HarmonyOS NEXT  跑马灯组件详解(二): MarqueeSection核心实现
## 效果演示

![](https://files.mdnice.com/user/47561/515b84cc-bcf8-48d2-97d2-06bc62b51180.jpg)
## 1. MarqueeSection组件概述

MarqueeSection是跑马灯组件的核心，负责实现文本的滚动效果。它通过配置动画参数和滚动属性，实现了流畅的文本滚动展示效果。

## 2. 核心配置类详解

### 2.1 MarqueeAnimationModifier类

```typescript
export class MarqueeAnimationModifier {
  iterations: number;     // 动画循环次数
  duration: number;       // 持续时间(ms)
  tempo: number;         // 播放速度
  playMode: PlayMode;    // 播放模式
  delayTime: number;     // 延迟时间(ms)

  constructor(
    iterations: number = -1,                    // 默认无限循环
    duration: number = Constants.ANIMATION_DURATION,
    tempo: number = 1,                         // 默认速度
    playMode: PlayMode = PlayMode.Reverse,     // 默认反向播放
    delayTime: number = Constants.DELAY_TIME   // 默认延迟时间
  ) {
    // 初始化配置
  }
}
```

参数说明：
- `iterations`: -1表示无限循环，0表示不动画，正数表示具体循环次数
- `duration`: 一次完整动画的持续时间
- `tempo`: 动画速度系数，值越大速度越快
- `playMode`: 控制滚动方向
- `delayTime`: 每次滚动后的停顿时间

### 2.2 MarqueeScrollModifier类

```typescript
export class MarqueeScrollModifier {
  scrollWidth: Length;    // 滚动区域宽度
  space: number;         // 文本间距

  constructor(
    scrollWidth: Length = Constants.DEFAULT_SCROLL_WIDTH,
    space: number = Constants.BLANK_SPACE
  ) {
    this.scrollWidth = scrollWidth;
    this.space = space;
  }
}
```

参数说明：
- `scrollWidth`: 定义滚动区域的宽度，支持响应式配置
- `space`: 定义文本之间的间隔距离

## 3. 组件使用示例

### 3.1 基础使用方式

```typescript
MarqueeSection({
  // 定义文本内容构建器
  marqueeTextBuilder: () => {
    this.marqueeTextBuilder(this.tripDataItem.ticketEntrance)
  },
  // 配置动画属性
  marqueeAnimationModifier: new MarqueeAnimationModifier(),
  // 配置滚动属性
  marqueeScrollModifier: new MarqueeScrollModifier(
    display.isFoldable() ? 
      $r('app.string.marquee_scroll_phone_width') : 
      $r('app.string.marquee_scroll_tablet_width'),
    Constants.BLANK_SPACE
  )
})
```

### 3.2 自定义文本构建器

```typescript
@Builder
marqueeTextBuilder(marqueeText: ResourceStr) {
  Text(marqueeText)
    .fontSize(16)
    .fontColor('#333333')
    // 可以添加更多文本样式
}
```

## 4. 适配处理

### 4.1 设备类型适配

```typescript
display.isFoldable() ? 
  $r('app.string.marquee_scroll_phone_width') : // 手机宽度
  $r('app.string.marquee_scroll_tablet_width')  // 平板宽度
```

### 4.2 资源引用

```typescript
// 在resources目录下定义不同设备的宽度
// phone.json
{
  "marquee_scroll_phone_width": "300vp"
}

// tablet.json
{
  "marquee_scroll_tablet_width": "500vp"
}
```

## 5. 动画效果实现

### 5.1 动画流程

1. 初始化：文本位于起始位置
2. 延迟：等待delayTime时间
3. 滚动：按照设定的速度和方向滚动
4. 停顿：完成一次滚动后暂停
5. 循环：重复以上步骤

### 5.2 关键参数配置

```typescript
const Constants = {
  ANIMATION_DURATION: 8000,  // 动画持续8秒
  DELAY_TIME: 1000,         // 延迟1秒
  BLANK_SPACE: 100,         // 文本间距100
  DEFAULT_SCROLL_WIDTH: '300vp'  // 默认滚动宽度
}
```

## 6. 性能优化

### 6.1 动态加载

使用LazyForEach实现数据的按需加载：

```typescript
LazyForEach(this.tripData, (item: TripDataType) => {
  TripMessage({
    tripDataItem: item
  })
}, (item: TripDataType) => JSON.stringify(item))
```

### 6.2 资源复用

通过Builder装饰器复用文本构建逻辑：

```typescript
@Builder
marqueeTextBuilder(marqueeText: ResourceStr) {
  Text(marqueeText)
}
```

## 7. 常见问题解决

1. 文本不滚动
   - 检查scrollWidth是否合适
   - 确认iterations不为0
   - 验证文本内容是否超出显示区域

2. 滚动效果不流畅
   - 调整duration值
   - 优化tempo参数
   - 检查设备性能状态

3. 适配问题
   - 使用响应式单位(vp)
   - 根据设备类型设置不同参数
   - 测试不同屏幕尺寸

## 8. 最佳实践

1. 合理设置动画参数
2. 注意性能优化
3. 做好设备适配
4. 保持代码简洁
5. 遵循组件设计规范

通过以上详细讲解，相信你已经对MarqueeSection组件的实现原理和使用方法有了深入的了解。在实际开发中，可以根据具体需求调整相关参数，实现最佳的展示效果。
