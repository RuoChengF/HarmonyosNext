> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！


![](https://files.mdnice.com/user/47561/bb8c0fa6-50b1-42b6-8383-6df862e262ce.png)

# HarmonyOS NEXT跑马灯组件教程：MarqueeSection组件实现原理

## 1. MarqueeSection组件概述

MarqueeSection组件是HarmonyOS NEXT跑马灯功能的核心实现，它负责处理文本的滚动动画、宽度检测和循环控制。本文将深入分析MarqueeSection组件的实现原理和核心功能。

### 1.1 组件定位

MarqueeSection组件位于utils/marquee目录下，是一个功能性组件，主要用于实现文本的自动滚动效果。它通过以下机制实现跑马灯效果：

1. 检测文本宽度是否超出显示区域
2. 根据配置参数控制文本滚动方向、速度和循环次数
3. 使用动画API实现平滑滚动效果
4. 通过定时器控制滚动间隔

### 1.2 组件结构

```typescript
@Component
export struct MarqueeSection {
    // 对外暴露的属性
    @BuilderParam marqueeTextBuilder: () => void;
    marqueeAnimationModifier: MarqueeAnimationModifier;
    marqueeScrollModifier: MarqueeScrollModifier;
    
    // 私有属性
    @State ticketCheckTextOffset: number;
    @State ticketCheckTextWidth: number;
    @State ticketCheckScrollWidth: number;
    count: number;
    timer: number;
    
    // 方法
    scrollAnimation() {...}
    aboutToAppear() {...}
    build() {...}
}
```

## 2. 组件属性详解

### 2.1 对外暴露的属性

| 属性名 | 类型 | 说明 | 默认值 |
|------|------|------|------|
| marqueeTextBuilder | () => void | 跑马灯文本内容构建器 | defaultMarqueeBuilder |
| marqueeAnimationModifier | MarqueeAnimationModifier | 跑马灯动画属性配置 | new MarqueeAnimationModifier() |
| marqueeScrollModifier | MarqueeScrollModifier | 跑马灯滚动属性配置 | new MarqueeScrollModifier() |

这些属性允许开发者自定义跑马灯的文本内容、动画效果和滚动行为：

```typescript
// 源码中的属性定义
@Builder
defaultMarqueeBuilder() {
    Text('')
}
// 跑马灯文本视图
@BuilderParam marqueeTextBuilder: () => void = this.defaultMarqueeBuilder;
// 跑马灯动画属性
marqueeAnimationModifier: MarqueeAnimationModifier = new MarqueeAnimationModifier();
// 跑马灯文本滚动属性
marqueeScrollModifier: MarqueeScrollModifier = new MarqueeScrollModifier();
```

### 2.2 私有属性

| 属性名 | 类型 | 说明 | 初始值 |
|------|------|------|------|
| ticketCheckTextOffset | number | 文本偏移量 | 0 |
| ticketCheckTextWidth | number | 文本组件宽度 | 0 |
| ticketCheckScrollWidth | number | 滚动区域宽度 | 0 |
| count | number | 滚动计数器 | 1 |
| timer | number | 定时器句柄 | -1 |

这些私有属性用于内部状态管理和动画控制：

```typescript
// 源码中的私有属性定义
// 初始化文本偏移量
@State ticketCheckTextOffset: number = 0;
// 初始化文本组件所占的宽度
@State ticketCheckTextWidth: number = 0;
// 初始化Scroll组件所占的宽度
@State ticketCheckScrollWidth: number = 0;
// 记滚动次数
count: number = 1;
// 定时器句柄
timer: number = -1;
```

## 3. 核心方法实现

### 3.1 scrollAnimation方法

scrollAnimation方法是跑马灯组件的核心，负责实现文本滚动动画：

```typescript
// 文本滚动函数
scrollAnimation() {
    // 文本宽度小于Scroll组件宽度，不执行滚动操作
    if (this.ticketCheckTextWidth < this.ticketCheckScrollWidth) {
        return;
    }
    /**
     * 文本跑马灯动画。可以控制文本向左或者向右滚动，每隔1s再次滚动。
     */
    animateTo({
        duration: this.marqueeAnimationModifier.duration,
        tempo: this.marqueeAnimationModifier.tempo,
        curve: Curve.Linear,
        onFinish: () => {
            // 动画完成时的处理逻辑
            this.ticketCheckTextOffset =
                this.marqueeAnimationModifier.playMode === PlayMode.Normal ? 0 :
                    -(2 * this.ticketCheckTextWidth + this.marqueeScrollModifier.space - this.ticketCheckScrollWidth);
            // 处理循环次数逻辑
            if (this.marqueeAnimationModifier.iterations > 1) {
                if (this.count === this.marqueeAnimationModifier.iterations) {
                    this.count = 1;
                    return;
                }
                this.count++;
            } else if (this.marqueeAnimationModifier.iterations === 0 || this.marqueeAnimationModifier.iterations === 1) {
                return;
            }
            // 设置定时器，延迟执行下一次动画
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

这个方法的实现可以分为以下几个关键部分：

1. **条件判断**：首先检查文本宽度是否超出滚动区域宽度，只有超出时才执行滚动动画
2. **动画配置**：使用animateTo方法创建动画，设置持续时间、速度和动画曲线
3. **动画完成回调**：在动画完成后，根据配置重置文本位置，处理循环次数，并设置定时器延迟执行下一次动画
4. **动画执行函数**：设置文本偏移量，根据滚动方向(PlayMode)决定偏移方向和距离

### 3.2 build方法

build方法负责构建组件的UI结构：

```typescript
build() {
    // 使用Scroll组件和文本内容组件结合来判断文本宽度过宽时执行文本滚动
    Scroll() {
        Row() {
            Column() {
                this.marqueeTextBuilder()
            }
            .onAreaChange((oldValue, newValue) => {
                logger.info(`TextArea oldValue:${JSON.stringify(oldValue)},newValue:${JSON.stringify(newValue)}`);
                // 获取当前文本内容宽度
                let modePosition: componentUtils.ComponentInfo = componentUtils.getRectangleById('marquee');
                this.ticketCheckScrollWidth = Number(px2vp(modePosition.size.width));
                this.ticketCheckTextWidth = Number(newValue.width);
                if (this.ticketCheckTextWidth < this.ticketCheckScrollWidth) {
                    return;
                }
                this.ticketCheckTextOffset =
                    this.marqueeAnimationModifier.playMode === PlayMode.Normal ? 0 :
                        -(2 * this.ticketCheckTextWidth + this.marqueeScrollModifier.space - this.ticketCheckScrollWidth);
            })

            // 文本宽度大于Scroll组件宽度时显示。在偏移过程中可实现文本接替并显示在同一显示区的效果
            if (this.ticketCheckTextWidth >= this.ticketCheckScrollWidth) {
                Blank()
                    .width(this.marqueeScrollModifier.space)
                this.marqueeTextBuilder()
            }
        }.offset({ x: this.ticketCheckTextOffset })
        .onAppear(() => {
            // 执行动画函数
            this.scrollAnimation();
        })
    }
    .width(this.marqueeScrollModifier.scrollWidth)
    .id('marquee')
    .alignRules({
        top: { anchor: '__container__', align: VerticalAlign.Top },
        left: { anchor: 'ticketEntrance', align: HorizontalAlign.End }
    })
    .align(Alignment.Start)
    .enableScrollInteraction(false)
    .scrollable(ScrollDirection.Horizontal)
    .scrollBar(BarState.Off)
}
```

这个方法的实现包含以下关键部分：

1. **滚动容器**：使用Scroll组件作为容器，设置宽度、对齐方式和滚动行为
2. **文本内容**：使用Row和Column组件布局文本内容，并通过marqueeTextBuilder构建具体文本
3. **宽度检测**：通过onAreaChange事件监听文本区域变化，获取文本宽度和滚动区域宽度
4. **文本复制**：当文本宽度超出滚动区域时，复制一份文本并添加间隔，实现文本接替效果
5. **动画触发**：通过onAppear事件在组件出现时触发scrollAnimation方法开始动画

## 4. 动画实现原理

### 4.1 文本宽度检测

跑马灯组件首先需要检测文本是否超出显示区域，这通过以下代码实现：

```typescript
.onAreaChange((oldValue, newValue) => {
    // 获取当前文本内容宽度
    let modePosition: componentUtils.ComponentInfo = componentUtils.getRectangleById('marquee');
    this.ticketCheckScrollWidth = Number(px2vp(modePosition.size.width));
    this.ticketCheckTextWidth = Number(newValue.width);
    if (this.ticketCheckTextWidth < this.ticketCheckScrollWidth) {
        return;
    }
    // 设置初始偏移量
    this.ticketCheckTextOffset =
        this.marqueeAnimationModifier.playMode === PlayMode.Normal ? 0 :
            -(2 * this.ticketCheckTextWidth + this.marqueeScrollModifier.space - this.ticketCheckScrollWidth);
})
```

这段代码通过onAreaChange事件获取文本区域的宽度变化，并使用componentUtils.getRectangleById获取滚动区域的宽度。然后比较两者，只有当文本宽度大于滚动区域宽度时，才需要设置初始偏移量并启动滚动动画。

### 4.2 文本滚动动画

文本滚动动画通过animateTo方法实现：

```typescript
animateTo({
    duration: this.marqueeAnimationModifier.duration,
    tempo: this.marqueeAnimationModifier.tempo,
    curve: Curve.Linear,
    onFinish: () => {
        // 动画完成后的处理...
    }
}, () => {
    // 设置文本偏移量
    this.ticketCheckTextOffset = this.marqueeAnimationModifier.playMode === PlayMode.Normal ?
        -(this.ticketCheckTextWidth + this.marqueeScrollModifier.space) :
        -(this.ticketCheckTextWidth - this.ticketCheckScrollWidth)
})
```

animateTo方法接受两个参数：
1. **动画配置对象**：包含duration(持续时间)、tempo(速度)、curve(动画曲线)和onFinish(完成回调)等属性
2. **动画执行函数**：定义动画的具体行为，这里是改变ticketCheckTextOffset属性值，实现文本偏移

### 4.3 循环控制

跑马灯组件支持设置动画循环次数，通过以下代码实现：

```typescript
// 处理循环次数逻辑
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

这段代码根据marqueeAnimationModifier.iterations属性控制动画的循环次数：
- 当iterations > 1时，表示指定循环次数，通过count计数器控制
- 当iterations = 0或1时，表示不循环或只播放一次
- 当iterations = -1时(默认值)，表示无限循环

### 4.4 停顿效果

每次滚动完成后的停顿效果通过setTimeout实现：

```typescript
this.timer = setTimeout(() => {
    this.scrollAnimation();
}, this.marqueeAnimationModifier.delayTime)
```

这段代码在动画完成后，通过setTimeout设置一个延时任务，延时时间由marqueeAnimationModifier.delayTime属性控制（默认为1000毫秒），延时结束后再次调用scrollAnimation方法开始下一次动画，从而实现停顿效果。

### 4.5 文本接替效果

为了实现文本的无缝接替效果，MarqueeSection组件采用了一个巧妙的设计：当文本宽度超出滚动区域时，在原文本后面添加一个相同的文本副本，并在两个文本之间添加一定的间隔：

```typescript
// 文本宽度大于Scroll组件宽度时显示。在偏移过程中可实现文本接替并显示在同一显示区的效果
if (this.ticketCheckTextWidth >= this.ticketCheckScrollWidth) {
    Blank()
        .width(this.marqueeScrollModifier.space)
    this.marqueeTextBuilder()
}
```

这段代码的工作原理是：

1. 首先判断文本宽度是否超出滚动区域
2. 如果超出，则添加一个空白间隔（Blank组件），宽度由marqueeScrollModifier.space属性控制
3. 然后再次调用marqueeTextBuilder添加一个相同的文本副本
4. 当第一个文本滚动到末尾时，第二个文本正好进入视野，实现无缝接替

## 5. 组件生命周期管理

### 5.1 aboutToAppear方法

MarqueeSection组件实现了aboutToAppear生命周期方法，用于在组件即将出现时进行初始化工作：

```typescript
aboutToAppear(): void {
    // 清除定时器
    clearTimeout(this.timer);
}
```

这个方法主要用于清除可能存在的定时器，防止内存泄漏和重复执行动画。

### 5.2 资源释放

组件在使用定时器时，需要注意资源的释放。在aboutToAppear方法中清除定时器是一个良好的实践，可以防止组件重新创建时出现问题。

## 6. 性能优化

### 6.1 条件渲染

MarqueeSection组件使用条件渲染优化性能，只有当文本宽度超出滚动区域时才启动动画和添加文本副本：

```typescript
if (this.ticketCheckTextWidth < this.ticketCheckScrollWidth) {
    return;
}
```

这样可以避免不必要的动画和渲染，提高组件的性能。

### 6.2 动画性能

组件使用系统提供的animateTo方法实现动画，而不是自己实现动画逻辑，这可以充分利用系统的优化，提高动画性能：

```typescript
/**
 * 文本跑马灯动画。可以控制文本向左或者向右滚动，每隔1s再次滚动。
 *
 * 性能：播放动画时，系统需要在一个刷新周期内完成动画变化曲线的计算，完成组件布局绘制等操作。建议使用系统提供的动画接口，
 * 只需设置曲线类型、终点位置、时长等信息，就能够满足常用的动画功能，减少UI主线程的负载。
 */
animateTo({
    // 动画配置...
})
```

## 7. 总结

MarqueeSection组件是HarmonyOS NEXT中实现跑马灯效果的核心组件，它通过以下机制实现文本的自动滚动：

1. 使用onAreaChange事件检测文本宽度是否超出显示区域
2. 使用animateTo方法实现平滑的文本滚动动画
3. 通过添加文本副本和间隔实现文本的无缝接替
4. 使用定时器控制动画的循环和停顿
5. 支持自定义动画持续时间、速度、方向和循环次数

通过这些机制，MarqueeSection组件可以在有限的空间内展示超出显示区域的文本内容，提高用户体验和界面美观度。

在下一篇教程中，我们将深入探讨MarqueeAnimationModifier和MarqueeScrollModifier类的实现，了解如何自定义跑马灯组件的动画效果和滚动行为。
