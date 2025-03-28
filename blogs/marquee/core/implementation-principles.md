> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](../images/img_a4529613.png)

# HarmonyOS NEXT 跑马灯组件详解(三)：核心组件实现原理
## 效果演示

![](../images/img_97896a98.png)
## 1. MarqueeViewComponent 组件概述

MarqueeViewComponent 是跑马灯组件的主要容器组件，负责整体布局和功能组织。

### 1.1 基础结构

```typescript
@Component
export struct MarqueeViewComponent {
  @State tripData: TripDataSource = new TripDataSource();

  build() {
    Column() {
      // 功能描述部分
      FunctionDescription({
        title: $r('app.string.marquee_title'),
        content: $r('app.string.marquee_content')
      })
      // 行程信息展示部分
      TripView()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F1F3F5')
  }
}
```

## 2. TripView 组件详解

### 2.1 组件定义

```typescript
@Component
struct TripView {
  @State tripData: TripDataSource = new TripDataSource();

  build() {
    Column() {
      Text($r('app.string.marquee_plan_title'))
        .fontSize($r('app.float.ohos_id_text_size_headline8'))
        .fontWeight(FontWeight.Medium)
        .margin({ top: 16, bottom: 16 })

      // 使用LazyForEach渲染行程信息
      LazyForEach(this.tripData, (item: TripDataType) => {
        TripMessage({ tripDataItem: item })
      }, (item: TripDataType) => JSON.stringify(item))
    }
    .width('100%')
    .padding({ left: 12, right: 12 })
  }
}
```

### 2.2 LazyForEach 实现原理

- 按需加载数据
- 提高性能和内存使用效率
- 支持大量数据渲染

## 3. TripMessage 组件实现

### 3.1 基础结构

```typescript
@Component
struct TripMessage {
  private tripDataItem: TripDataType;

  build() {
    Column() {
      this.BuildTrainInfo()
      this.BuildTimeInfo()
      this.BuildLocationInfo()
    }
    .width('100%')
    .padding(12)
    .backgroundColor(Color.White)
    .borderRadius(8)
    .margin({ bottom: 12 })
  }
}
```

### 3.2 列车信息构建

```typescript
@Builder
BuildTrainInfo() {
  Row() {
    Text(this.tripDataItem.trainNumber)
      .fontSize(16)
      .fontWeight(FontWeight.Medium)
    
    Text(this.tripDataItem.wholeCourse)
      .fontSize(14)
      .margin({ left: 8 })
  }
  .width('100%')
  .justifyContent(FlexAlign.SpaceBetween)
}
```

### 3.3 时间信息构建

```typescript
@Builder
BuildTimeInfo() {
  Row() {
    Text(this.tripDataItem.startingTime)
    Text($r('app.string.marquee_time_separator'))
    Text(this.tripDataItem.endingTime)
    Text(this.tripDataItem.timeDifference)
  }
  .width('100%')
  .margin({ top: 8 })
  .justifyContent(FlexAlign.SpaceBetween)
}
```

## 4. MarqueeSection 核心实现

### 4.1 组件定义

```typescript
@Component
struct MarqueeSection {
  // 文本构建器
  private marqueeTextBuilder: () => void;
  // 动画配置
  private marqueeAnimationModifier: MarqueeAnimationModifier;
  // 滚动配置
  private marqueeScrollModifier: MarqueeScrollModifier;

  build() {
    Row() {
      this.marqueeTextBuilder()
    }
    .width(this.marqueeScrollModifier.scrollWidth)
    .animation({
      duration: this.marqueeAnimationModifier.duration,
      tempo: this.marqueeAnimationModifier.tempo,
      delay: this.marqueeAnimationModifier.delayTime,
      iterations: this.marqueeAnimationModifier.iterations,
      playMode: this.marqueeAnimationModifier.playMode
    })
  }
}
```

### 4.2 动画配置详解

```typescript
private marqueeAnimationModifier: MarqueeAnimationModifier = new MarqueeAnimationModifier(
  -1,                           // 无限循环
  Constants.ANIMATION_DURATION, // 动画持续时间
  1,                           // 正常速度
  PlayMode.Reverse,           // 反向播放
  Constants.DELAY_TIME        // 延迟时间
);
```

## 5. 状态管理

### 5.1 组件状态

```typescript
@State private isPlaying: boolean = true;
@State private currentIndex: number = 0;
@State private contentWidth: number = 0;
```

### 5.2 状态更新

```typescript
private updateState(index: number) {
  this.currentIndex = index;
  this.isPlaying = true;
  this.notifyStateChange();
}

private notifyStateChange() {
  // 触发状态变化监听器
}
```

## 6. 事件处理

### 6.1 点击事件

```typescript
onClick: () => {
  this.isPlaying = !this.isPlaying;
  if (this.isPlaying) {
    this.resumeMarquee();
  } else {
    this.pauseMarquee();
  }
}
```

### 6.2 生命周期事件

```typescript
aboutToAppear() {
  // 组件即将出现时的处理
  this.initializeMarquee();
}

aboutToDisappear() {
  // 组件即将消失时的处理
  this.cleanupMarquee();
}
```

## 7. 性能优化

### 7.1 渲染优化

```typescript
// 使用条件渲染避免不必要的更新
if (this.contentWidth > this.containerWidth) {
  MarqueeSection({
    marqueeTextBuilder: this.buildMarqueeText,
    marqueeAnimationModifier: this.animationConfig,
    marqueeScrollModifier: this.scrollConfig
  })
} else {
  Text(this.content)
}
```

### 7.2 内存优化

```typescript
// 及时清理不需要的资源
private cleanup() {
  this.stopAnimation();
  this.clearCache();
  this.removeListeners();
}
```

## 8. 最佳实践

1. 组件封装
   - 保持组件的独立性
   - 提供清晰的接口
   - 遵循单一职责原则

2. 性能考虑
   - 使用懒加载
   - 避免不必要的渲染
   - 及时清理资源

3. 错误处理
   - 参数验证
   - 异常捕获
   - 降级处理

4. 代码组织
   - 逻辑分离
   - 复用公共代码
   - 保持代码简洁

通过以上详细讲解，你应该能够理解跑马灯组件的核心实现原理和各个部分的作用。这些知识将帮助你更好地使用和定制组件。
