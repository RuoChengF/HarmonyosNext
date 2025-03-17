> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/b3af4f4e-d4c6-49ff-9e16-82d8af7e34c9.png)

# HarmonyOS NEXT 跑马灯组件详解(三)：MarqueeSection基础结构
## 效果演示

![](https://files.mdnice.com/user/47561/515b84cc-bcf8-48d2-97d2-06bc62b51180.jpg)
## 1. 组件概述

MarqueeSection是一个实现文本滚动效果的自定义组件，主要用于显示超出显示区域的文本内容。

### 1.1 基本结构

```typescript
@Component
export struct MarqueeSection {
  // 构建器参数
  @BuilderParam marqueeTextBuilder: () => void;
  
  // 动画配置
  marqueeAnimationModifier: MarqueeAnimationModifier;
  
  // 滚动配置
  marqueeScrollModifier: MarqueeScrollModifier;
}
```

## 2. 属性详解

### 2.1 构建器参数

```typescript
@Builder
defaultMarqueeBuilder() {
    Text('')
}

@BuilderParam marqueeTextBuilder: () => void = this.defaultMarqueeBuilder;
```

- @Builder：声明一个自定义构建函数
- @BuilderParam：声明一个构建器参数
- defaultMarqueeBuilder：默认的构建器实现

### 2.2 状态属性

```typescript
// 文本偏移量
@State ticketCheckTextOffset: number = 0;

// 文本宽度
@State ticketCheckTextWidth: number = 0;

// 滚动区域宽度
@State ticketCheckScrollWidth: number = 0;
```

### 2.3 其他属性

```typescript
// 滚动计数
count: number = 1;

// 定时器句柄
timer: number = -1;
```

## 3. 配置对象

### 3.1 动画配置

```typescript
marqueeAnimationModifier: MarqueeAnimationModifier = new MarqueeAnimationModifier();
```

包含：
- 动画持续时间
- 播放速度
- 播放模式
- 延迟时间

### 3.2 滚动配置

```typescript
marqueeScrollModifier: MarqueeScrollModifier = new MarqueeScrollModifier();
```

包含：
- 滚动区域宽度
- 文本间距

## 4. 生命周期处理

```typescript
aboutToAppear(): void {
    // 清除定时器
    clearTimeout(this.timer);
}
```

## 5. 关键知识点

1. 装饰器使用
   - @Component：声明自定义组件
   - @BuilderParam：声明构建器参数
   - @State：声明状态变量

2. 默认值处理
   - 为构建器参数提供默认实现
   - 配置对象使用默认构造

3. 状态管理
   - 使用@State管理动态数据
   - 确保状态变化触发视图更新

4. 生命周期
   - aboutToAppear：组件即将出现
   - 资源清理和初始化

## 6. 使用示例

### 6.1 基本使用

```typescript
MarqueeSection({
  marqueeTextBuilder: () => {
    Text('滚动文本内容')
      .fontSize(16)
      .fontColor('#333333')
  },
  marqueeAnimationModifier: new MarqueeAnimationModifier(),
  marqueeScrollModifier: new MarqueeScrollModifier()
})
```

### 6.2 自定义配置

```typescript
MarqueeSection({
  marqueeTextBuilder: () => {
    Row() {
      Text('自定义内容')
      Image('icon.png')
    }
  },
  marqueeAnimationModifier: new MarqueeAnimationModifier(
    -1,    // 无限循环
    5000,  // 5秒一次
    1.5    // 1.5倍速
  ),
  marqueeScrollModifier: new MarqueeScrollModifier(
    '80%',  // 宽度
    20      // 间距
  )
})
```

## 7. 注意事项

1. 构建器参数
   - 必须提供有效的构建函数
   - 考虑性能影响
   - 保持视图简洁

2. 状态管理
   - 合理使用状态变量
   - 避免不必要的状态更新
   - 注意状态依赖关系

3. 配置对象
   - 提供合理的默认值
   - 验证配置参数
   - 考虑边界情况

通过以上详细讲解，你应该能够理解MarqueeSection组件的基本结构和配置方式。这为后续深入理解组件的动画实现和滚动逻辑打下了基础。
