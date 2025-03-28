 
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](../images/img_8ab299da.png)


# Harmonyos NEXT 图片预览组件之工具类实现
## 效果预览

![](../images/img_bd971de3.png)
## 一、工具类概述

图片预览组件中的工具类是支撑组件功能实现的重要基础设施，它们提供了约束计算、动画效果、窗口管理等核心功能。本文将详细介绍图片预览组件中的三个核心工具类：Constrain、FuncUtils和Managers。

### 1. 工具类的作用

在图片预览组件中，工具类主要承担以下职责：

1. **约束计算**：确保图片在缩放和移动过程中不会超出合理范围
2. **动画处理**：提供平滑的动画效果，提升用户体验
3. **窗口管理**：提供窗口尺寸信息，用于计算图片的适配大小
4. **旋转计算**：提供旋转角度的计算和简化功能

### 2. 工具类的设计原则

| 设计原则 | 说明 | 实现方式 |
| --- | --- | --- |
| 功能聚焦 | 每个工具类专注于特定的功能领域 | 按功能划分为不同的工具类 |
| 无状态设计 | 工具类方法不依赖于内部状态 | 使用纯函数实现核心功能 |
| 参数明确 | 明确定义参数类型和返回值 | 使用TypeScript类型系统 |
| 复用性高 | 工具类方法可在多处复用 | 提供通用的功能接口 |

## 二、Constrain - 约束工具

### 1. 功能概述

Constrain工具类主要负责图片的边界约束和切换判断，确保图片在交互过程中的合理显示。

### 2. 核心枚举和接口

```typescript
// 图片适配类型枚举
export enum ImageFitType {
    TYPE_WIDTH = 'width',
    TYPE_HEIGHT = 'height',
    TYPE_DEFAULT = 'default'
}

// 约束偏移计算接口
export interface ConstrainOffsetAndAnimationType {
    // 此次计算的方向 宽或者高
    dimensionWH: ImageFitType,
    // 此次图片的默认尺寸
    imageDefaultSize: image.Size,
    // 此次图片相对应的偏移信息
    imageOffsetInfo: OffsetModel,
    // 此次图片的放大尺寸
    scaleValue: number,
    // 当前图片的旋转角度
    rotate: number,
    // 当超出限制多少时去判断，取值：0 ~ 1
    TogglePercent: number,
    // List 偏移量
    imageListOffset: number,
    // 主轴方向
    listDirection: Axis
}
```

### 3. 最大偏移量计算

```typescript
// 获取最大偏移量
export function getMaxAllowedOffset(winSize: number, imageSize: number, scale: number) {
    const maxNum = Math.max(imageSize * scale, winSize);
    const minNum = Math.min(imageSize * scale, winSize);
    return (maxNum - minNum) / 2;
}
```

这个函数计算图片在特定方向上可以移动的最大距离。计算逻辑如下：

1. 当图片尺寸大于窗口尺寸时（imageSize * scale > winSize）：
   - maxNum = imageSize * scale
   - minNum = winSize
   - 最大偏移量 = (imageSize * scale - winSize) / 2

2. 当图片尺寸小于窗口尺寸时（imageSize * scale < winSize）：
   - maxNum = winSize
   - minNum = imageSize * scale
   - 最大偏移量 = (winSize - imageSize * scale) / 2

### 4. 偏移约束函数

```typescript
function constrainOffset(offset: number, winSize: number, imageSize: number, scale: number): number {
    let maxAllowedOffset = getMaxAllowedOffset(winSize, imageSize, scale);
    return Math.min(Math.max(offset, -maxAllowedOffset), maxAllowedOffset);
}
```

这个函数确保图片的偏移量不会超出允许的范围，通过Math.min和Math.max函数将偏移量限制在[-maxAllowedOffset, maxAllowedOffset]区间内。

### 5. 切换判断函数

```typescript
function isToggle(offset: number, winSize: number, imageSize: number, scale: number, TogglePercent: number): boolean {
    let maxAllowedOffset = getMaxAllowedOffset(winSize, imageSize, scale);
    const deviation = Math.abs(offset) - maxAllowedOffset;
    const switchThreshold = winSize * TogglePercent;

    if (deviation > switchThreshold) {
        return true
    }
    return false
}
```

这个函数判断是否需要切换图片，通过计算当前偏移量与最大允许偏移量的差值，并与切换阈值（窗口尺寸 * TogglePercent）进行比较。当差值大于阈值时，触发图片切换。

### 6. 综合约束与动画处理

```typescript
export function constrainOffsetAndAnimation(info: ConstrainOffsetAndAnimationType): [boolean, boolean] {
    if (info.dimensionWH === ImageFitType.TYPE_DEFAULT) {
        return [false, false]
    }
    const WIN_SIZE = windowSizeManager.get();
    const IMG_SIZE = getImgSize(info.imageDefaultSize, info.rotate, info.dimensionWH);
    const WIN_AXIS_SIZE = WIN_SIZE[info.dimensionWH];
    let currentOffset = (info.imageOffsetInfo as object)[`last${info.dimensionWH === ImageFitType.TYPE_WIDTH ? 'X' : 'Y'}`];
    
    // 计算最后的图片偏移量
    if (info.dimensionWH === (info.listDirection === Axis.Horizontal ? ImageFitType.TYPE_WIDTH : ImageFitType.TYPE_HEIGHT)) {
        currentOffset += info.imageListOffset;
    }
    
    const CLAMPED_OFFSET = constrainOffset(currentOffset, WIN_AXIS_SIZE, IMG_SIZE, info.scaleValue);
    
    // 如果偏移量发生了变化（即需要修正）
    if (CLAMPED_OFFSET !== currentOffset) {
        let updateFn = () => {
            (info.imageOffsetInfo as object)[`current${info.dimensionWH == ImageFitType.TYPE_WIDTH ? 'X' : 'Y'}`] = CLAMPED_OFFSET;
            info.imageOffsetInfo.stash();
        }
        runWithAnimation(updateFn);
        
        // 判断是否需要切换图片
        let bol = isToggle(currentOffset, WIN_AXIS_SIZE, IMG_SIZE, info.scaleValue, info.TogglePercent);
        if (bol) {
            const BOL = currentOffset >= 0 ? true : false
            return [BOL, !BOL]
        }
    }
    return [false, false]
}
```

这个函数是边界处理的核心，它综合了偏移约束和动画处理，并返回是否需要切换图片的判断结果。返回值是一个布尔数组：

- 如果dimensionWH是"width"，返回值为[左边超出，右边超出]
- 如果dimensionWH是"height"，返回值为[上边超出，下边超出]

## 三、FuncUtils - 功能工具

### 1. 动画执行函数

```typescript
export function runWithAnimation(fn: Function, duration: number = 300) {
    animateTo({
        duration: duration,
        curve: Curve.Ease,
        iterations: 1,
        playMode: PlayMode.Normal,
    }, fn);
}
```

这个函数为其他函数执行添加动画效果，使用animateTo API实现平滑的动画过渡。参数说明：

- fn：需要执行的函数
- duration：动画持续时间，默认300毫秒

### 2. 旋转角度简化函数

```typescript
export function simplestRotationQuarter(angle: number): number {
    // 将角度转换为0-360范围内
    let normalizedAngle = angle % 360;
    if (normalizedAngle < 0) {
        normalizedAngle += 360;
    }
    
    // 计算最接近的90度倍数
    let quarter = Math.round(normalizedAngle / 90) * 90;
    return quarter;
}
```

这个函数将任意角度转换为最接近的90度倍数（0°、90°、180°、270°），用于图片旋转时的角度对齐。实现步骤：

1. 将角度归一化到0-360度范围内
2. 计算最接近的90度倍数

## 四、Managers - 窗口管理器

### 1. 窗口尺寸管理器

```typescript
class WindowSizeManager {
    private size: window.Size = { width: 0, height: 0 };
    
    constructor() {
        // 初始化窗口尺寸
        this.size = { 
            width: window.getLastWindowSize().width, 
            height: window.getLastWindowSize().height 
        };
        
        // 监听窗口尺寸变化
        window.on('sizeChange', (size: window.Size) => {
            this.size = size;
        });
    }
    
    get(): window.Size {
        return this.size;
    }
}

// 创建单例实例
export const windowSizeManager = new WindowSizeManager();
```

窗口尺寸管理器是一个单例类，用于获取和管理窗口尺寸信息。它的主要功能包括：

1. 初始化时获取当前窗口尺寸
2. 监听窗口尺寸变化事件，实时更新尺寸信息
3. 提供get()方法获取当前窗口尺寸

## 五、工具类在组件中的应用

### 1. 约束工具在边界处理中的应用

```typescript
evaluateBound(): void {
    const xBol = constrainOffsetAndAnimation({
        dimensionWH: ImageFitType.TYPE_WIDTH,
        imageDefaultSize: this.imageDefaultSize,
        imageOffsetInfo: this.imageOffsetInfo,
        scaleValue: this.imageScaleInfo.scaleValue,
        rotate: this.imageRotateInfo.lastRotate,
        TogglePercent: this.TogglePercent,
        imageListOffset: this.imageListOffset,
        listDirection: this.listDirection
    });
    
    // 根据返回结果决定是否切换图片
    if (this.listDirection === Axis.Horizontal) {
        if (xBol[0] || xBol[1]) {
            if (xBol[0]) {
                this.setListToIndex(this.imageIndex - 1);
            }
            if (xBol[1]) {
                this.setListToIndex(this.imageIndex + 1);
            }
        }
    }
}
```

### 2. 动画工具在状态重置中的应用

```typescript
resetCurrentImageInfo(): void {
    runWithAnimation(() => {
        this.imageScaleInfo.reset();
        this.imageOffsetInfo.reset();
        this.imageRotateInfo.reset();
        this.matrix = matrix4.identity().copy();
    }, this.restImageAnimation);
}
```

### 3. 窗口管理器在尺寸计算中的应用

```typescript
initCurrentImageInfo(event: ImageLoadResult): void {
    let imageW = event.width;
    let imageH = event.height;
    let windowSize = windowSizeManager.get();
    
    // 图片宽高比
    this.imageWHRatio = imageW / imageH;
    
    // 图片默认大小
    this.imageDefaultSize = this.calcImageDefaultSize(this.imageWHRatio, windowSize);
}
```

## 六、总结

图片预览组件中的工具类是组件功能实现的重要支撑，它们通过提供约束计算、动画效果、窗口管理等核心功能，确保了组件的高性能和良好用户体验。

工具类的设计遵循了功能聚焦、无状态设计、参数明确和复用性高的原则，使得代码结构清晰、易于维护。通过合理的工具类抽象，图片预览组件实现了复杂交互逻辑的模块化和可复用性。

在实际应用中，这些工具类不仅服务于图片预览组件，还可以在其他需要类似功能的组件中复用，提高了代码的复用率和开发效率。
