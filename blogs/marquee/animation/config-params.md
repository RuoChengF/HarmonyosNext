> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/0dbfa651-8a8d-4edd-9058-59933abeb107.png)

# HarmonyOS NEXT跑马灯组件教程：动画配置与参数详解

## 1. 跑马灯动画配置概述

跑马灯组件的动画效果和滚动行为可以通过两个核心配置类进行自定义：MarqueeAnimationModifier和MarqueeScrollModifier。这两个类分别控制动画的播放方式和滚动区域的尺寸，为开发者提供了灵活的配置选项。本文将详细介绍这两个类的实现和使用方法。

### 1.1 配置类的作用

| 配置类 | 作用 | 主要参数 |
|------|------|------|
| MarqueeAnimationModifier | 控制动画的播放方式 | 播放次数、持续时间、速度、方向、延迟时间 |
| MarqueeScrollModifier | 控制滚动区域的尺寸 | 滚动区域宽度、文本间隔 |

这两个配置类的组合使用，可以实现各种不同效果的跑马灯动画，满足不同场景的需求。

## 2. MarqueeAnimationModifier类详解

### 2.1 类定义

MarqueeAnimationModifier类定义在model/marquee/DataType.ets文件中，用于控制跑马灯动画的播放方式：

```typescript
/**
 * 跑马灯滚动动画属性
 * @param {number} [iterations] - 动画播放次数。默认播放一次，设置为-1时表示无限次播放。设置为0时表示无动画效果
 * @param {number} [duration] - 动画持续时间，单位为毫秒
 * @param {number} [tempo] - 动画播放速度，值越大动画播放越快，值越小播放越慢，为0时无动画效果
 * @param {PlayMode} [playMode] - 控制跑马灯向左还是向右滚动。方向向右的时候，文本需要取反，如牌匾 -> 匾牌，这样可以给用户良好的阅读体验
 * @param {number} [delayTime] - 动画延迟播放时间，单位为ms(毫秒)，默认延时1s播放
 */
export class MarqueeAnimationModifier {
  iterations: number;
  duration: number;
  tempo: number;
  playMode: PlayMode;
  delayTime: number;

  constructor(iterations: number = -1, duration: number = Constants.ANIMATION_DURATION, tempo: number = 1,
    playMode: PlayMode = PlayMode.Normal, delayTime: number = Constants.DELAY_TIME) {
    this.iterations = iterations;
    this.duration = duration;
    this.tempo = tempo;
    this.playMode = playMode;
    this.delayTime = delayTime;
  }
}
```

### 2.2 参数详解

| 参数名 | 类型 | 说明 | 默认值 |
|------|------|------|------|
| iterations | number | 动画播放次数 | -1（无限循环） |
| duration | number | 动画持续时间（毫秒） | Constants.ANIMATION_DURATION（10000ms） |
| tempo | number | 动画播放速度 | 1 |
| playMode | PlayMode | 滚动方向 | PlayMode.Normal |
| delayTime | number | 动画延迟时间（毫秒） | Constants.DELAY_TIME（1000ms） |

#### 2.2.1 iterations参数

iterations参数控制动画的播放次数：

- **-1**：表示无限循环播放
- **0**：表示不播放动画
- **1**：表示只播放一次
- **>1**：表示播放指定次数

在MarqueeSection组件中，通过以下代码实现循环控制：

```typescript
if (this.marqueeAnimationModifier.iterations > 1) {
    if (this.count === this.marqueeAnimationModifier.iterations) {
        this.count = 1;
        return;
    }
    this.count++;
} else if (this.marqueeAnimationModifier.iterations === 0 || this.marqueeAnimationModifier.iterations === 1) {
    return;
}
```

#### 2.2.2 duration参数

duration参数控制动画的持续时间，单位为毫秒。默认值为Constants.ANIMATION_DURATION（10000ms），即10秒。这个参数决定了文本从开始位置滚动到结束位置需要的时间。

在Constants.ets文件中定义：

```typescript
// 动画总时长10s
static readonly ANIMATION_DURATION: number = 10000;
```

#### 2.2.3 tempo参数

tempo参数控制动画的播放速度：

- **>1**：加快动画速度
- **=1**：正常速度
- **<1**：减慢动画速度
- **=0**：无动画效果

这个参数与duration参数配合使用，可以更精细地控制动画速度。

#### 2.2.4 playMode参数

playMode参数控制文本的滚动方向，是一个枚举类型：

- **PlayMode.Normal**：从左到右滚动
- **PlayMode.Reverse**：从右到左滚动

在MarqueeSection组件中，根据playMode参数计算不同的偏移量：

```typescript
this.ticketCheckTextOffset = this.marqueeAnimationModifier.playMode === PlayMode.Normal ?
    -(this.ticketCheckTextWidth + this.marqueeScrollModifier.space) :
    -(this.ticketCheckTextWidth - this.ticketCheckScrollWidth)
```

#### 2.2.5 delayTime参数

delayTime参数控制每次动画完成后的停顿时间，单位为毫秒。默认值为Constants.DELAY_TIME（1000ms），即1秒。

在Constants.ets文件中定义：

```typescript
// 延时时间1s
static readonly DELAY_TIME: number = 1000;
```

在MarqueeSection组件中，通过setTimeout实现停顿效果：

```typescript
this.timer = setTimeout(() => {
    this.scrollAnimation();
}, this.marqueeAnimationModifier.delayTime)
```

### 2.3 使用示例

```typescript
// 创建一个自定义的动画配置
const animationModifier = new MarqueeAnimationModifier(
    -1,                    // 无限循环
    5000,                  // 动画持续时间5秒
    1.5,                   // 动画速度1.5倍
    PlayMode.Normal,       // 从左到右滚动
    2000                   // 停顿时间2秒
);

// 使用配置创建跑马灯组件
MarqueeSection({
    marqueeTextBuilder: () => {
        Text("这是一段长文本，需要使用跑马灯效果展示")
    },
    marqueeAnimationModifier: animationModifier,
    marqueeScrollModifier: new MarqueeScrollModifier()
})
```

## 3. MarqueeScrollModifier类详解

### 3.1 类定义

MarqueeScrollModifier类也定义在model/marquee/DataType.ets文件中，用于控制滚动区域的尺寸：

```typescript
/**
 * 跑马灯滚动文本属性
 * @param {Length} [scrollWidth] - 滚动轴宽度
 * @param {number} [space] - 文本间隔
 */
export class MarqueeScrollModifier {
  scrollWidth: Length;
  space: number;

  constructor(scrollWidth: Length = Constants.DEFAULT_SCROLL_WIDTH, space: number = Constants.BLANK_SPACE) {
    this.scrollWidth = scrollWidth;
    this.space = space;
  }
}
```

### 3.2 参数详解

| 参数名 | 类型 | 说明 | 默认值 |
|------|------|------|------|
| scrollWidth | Length | 滚动区域宽度 | Constants.DEFAULT_SCROLL_WIDTH（'25%'） |
| space | number | 文本间隔 | Constants.BLANK_SPACE（50） |

#### 3.2.1 scrollWidth参数

scrollWidth参数控制滚动区域的宽度，可以使用像素值或百分比。默认值为Constants.DEFAULT_SCROLL_WIDTH（'25%'）。

在Constants.ets文件中定义：

```typescript
// 默认滚动轴宽度
static readonly DEFAULT_SCROLL_WIDTH: string = '25%';
```

在MarqueeSection组件中，通过以下代码设置滚动区域宽度：

```typescript
Scroll() {
    // ...
}
.width(this.marqueeScrollModifier.scrollWidth)
```

#### 3.2.2 space参数

space参数控制两个文本之间的间隔，单位为像素。默认值为Constants.BLANK_SPACE（50）。

在Constants.ets文件中定义：

```typescript
// 间隔距离
static readonly BLANK_SPACE: number = 50;
```

在MarqueeSection组件中，通过以下代码设置文本间隔：

```typescript
if (this.ticketCheckTextWidth >= this.ticketCheckScrollWidth) {
    Blank()
        .width(this.marqueeScrollModifier.space)
    this.marqueeTextBuilder()
}
```

### 3.3 使用示例

```typescript
// 创建一个自定义的滚动配置
const scrollModifier = new MarqueeScrollModifier(
    '30%',                // 滚动区域宽度为30%
    80                     // 文本间隔80像素
);

// 使用配置创建跑马灯组件
MarqueeSection({
    marqueeTextBuilder: () => {
        Text("这是一段长文本，需要使用跑马灯效果展示")
    },
    marqueeAnimationModifier: new MarqueeAnimationModifier(),
    marqueeScrollModifier: scrollModifier
})
```

## 4. 常量定义

跑马灯组件使用的常量定义在model/marquee/Constants.ets文件中：

```typescript
export default class Constants {
  // 动画总时长10s
  static readonly ANIMATION_DURATION: number = 10000;
  // 延时时间1s
  static readonly DELAY_TIME: number = 1000;
  // 间隔距离
  static readonly BLANK_SPACE: number = 50;
  // 间隔距离
  static readonly ANGLE: number = 180;
  // 默认文本字体颜色
  static readonly DEFAULT_FONT_COLOR: string = '#000';
  // 默认文本字体大小
  static readonly DEFAULT_FONT_SIZE: number = 16;
  // 默认跑马灯动画时间
  static readonly DEFAULT_ANIMATION_DURATION: number = 500;
  // 默认滚动轴宽度
  static readonly DEFAULT_SCROLL_WIDTH: string = '25%';
}
```

这些常量为跑马灯组件提供了默认配置值，开发者可以通过自定义MarqueeAnimationModifier和MarqueeScrollModifier实例来覆盖这些默认值。

## 5. 配置组合与效果

通过不同的配置组合，可以实现各种不同效果的跑马灯动画：

| 效果 | MarqueeAnimationModifier配置 | MarqueeScrollModifier配置 |
|------|------|------|
| 快速滚动 | duration=5000, tempo=2 | 默认配置 |
| 慢速滚动 | duration=15000, tempo=0.5 | 默认配置 |
| 从左到右 | playMode=PlayMode.Normal | 默认配置 |
| 从右到左 | playMode=PlayMode.Reverse | 默认配置 |
| 单次播放 | iterations=1 | 默认配置 |
| 无限循环 | iterations=-1 | 默认配置 |
| 宽间隔 | 默认配置 | space=100 |
| 窄间隔 | 默认配置 | space=20 |
| 宽显示区域 | 默认配置 | scrollWidth='50%' |
| 窄显示区域 | 默认配置 | scrollWidth='15%' |

## 6. 最佳实践

### 6.1 配置选择

在选择跑马灯配置时，应考虑以下因素：

1. **文本长度**：文本越长，可能需要更长的动画持续时间
2. **显示区域大小**：显示区域越小，可能需要更慢的滚动速度
3. **用户阅读习惯**：考虑用户的阅读方向，选择合适的滚动方向
4. **信息重要性**：重要信息可能需要多次循环播放
5. **用户体验**：停顿时间不宜过长或过短，应根据文本内容和用户阅读速度调整

### 6.2 性能考虑

在使用跑马灯组件时，应注意以下性能问题：

1. **避免过多实例**：在同一页面中避免创建过多的跑马灯实例，以减少资源占用
2. **合理设置动画参数**：过快的动画速度或过短的动画持续时间可能导致动画不流畅
3. **条件渲染**：只在必要时启用跑马灯效果，不需要滚动的文本应使用普通Text组件

### 6.3 适配不同设备

跑马灯组件可以根据不同设备的屏幕尺寸进行适配：

```typescript
MarqueeSection({
  // ...
  marqueeScrollModifier: new MarqueeScrollModifier(display.isFoldable() ?
    $r('app.string.marquee_scroll_phone_width') : $r('app.string.marquee_scroll_tablet_width'),
    Constants.BLANK_SPACE)
})
```

这段代码通过display.isFoldable()方法检测设备是否为折叠屏，然后根据设备类型选择不同的滚动区域宽度。

## 7. 常见问题与解决方案

### 7.1 文本不滚动

如果跑马灯文本不滚动，可能有以下原因：

1. **文本宽度未超出显示区域**：只有当文本宽度大于滚动区域宽度时，才会启动滚动动画
2. **iterations参数设置为0**：iterations=0表示不播放动画
3. **tempo参数设置为0**：tempo=0表示无动画效果

解决方案：

```typescript
// 确保文本宽度超出显示区域
marqueeScrollModifier: new MarqueeScrollModifier('15%', 50),
// 确保iterations不为0
marqueeAnimationModifier: new MarqueeAnimationModifier(-1, 10000, 1, PlayMode.Normal, 1000)
```

### 7.2 动画速度不合适

如果动画速度不合适，可以通过调整duration和tempo参数来解决：

```typescript
// 加快动画速度
marqueeAnimationModifier: new MarqueeAnimationModifier(-1, 5000, 1.5, PlayMode.Normal, 1000)

// 减慢动画速度
marqueeAnimationModifier: new MarqueeAnimationModifier(-1, 15000, 0.8, PlayMode.Normal, 1000)
```

### 7.3 文本接替不流畅

如果文本接替不流畅，可以调整space参数：

```typescript
// 增加文本间隔
marqueeScrollModifier: new MarqueeScrollModifier('25%', 80)

// 减少文本间隔
marqueeScrollModifier: new MarqueeScrollModifier('25%', 30)
```

## 8. 总结

本文详细介绍了HarmonyOS NEXT跑马灯组件的动画配置与参数，包括MarqueeAnimationModifier和MarqueeScrollModifier两个核心配置类的实现和使用方法。通过合理配置这两个类的参数，可以实现各种不同效果的跑马灯动画，满足不同场景的需求。

跑马灯组件的配置灵活性高，可以根据实际需求调整动画的播放次数、持续时间、速度、方向和停顿时间，以及滚动区域的宽度和文本间隔。在实际应用中，应根据文本内容、显示区域大小、用户阅读习惯和信息重要性等因素，选择合适的配置参数，提供最佳的用户体验。

在下一篇教程中，我们将介绍如何在实际项目中使用跑马灯组件，包括组件的集成、数据绑定和事件处理等内容。
