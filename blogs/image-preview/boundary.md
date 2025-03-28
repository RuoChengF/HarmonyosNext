> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/7708a83b-ed38-4e2f-adc4-cfc1b2d191c0.png)

# Harmonyos NEXT 图片预览组件之边界处理与图片切换

## 效果预览

![](https://files.mdnice.com/user/47561/d8d2c370-46fe-4ef5-a985-5961f413f927.jpg)

## 一、边界处理概述

在图片预览组件中，边界处理是一个核心功能，它确保了图片在缩放、旋转和拖动过程中的合理显示，并实现了多图片之间的平滑切换。本文将详细介绍 PicturePreviewImage 组件中的边界处理与图片切换实现原理。

### 1. 边界处理的核心问题

图片预览组件在处理边界时需要解决以下几个核心问题：

1. **偏移约束**：确保图片不会被拖动到视口之外
2. **切换条件**：判断何时触发图片切换
3. **主轴与交叉轴**：处理不同滑动方向的边界情况
4. **动画过渡**：提供平滑的视觉体验

## 二、边界约束实现

### 1. 最大偏移量计算

```typescript
// 获取最大偏移量
export function getMaxAllowedOffset(winSize: number, imageSize: number, scale: number) {
    const maxNum = Math.max(imageSize * scale, winSize);
    const minNum = Math.min(imageSize * scale, winSize);
    return (maxNum - minNum) / 2;
}
```

这个函数计算图片在特定方向上可以移动的最大距离。当图片尺寸大于窗口尺寸时，允许图片在窗口内移动；当图片尺寸小于窗口尺寸时，限制图片移动范围，确保图片不会完全移出窗口。

### 2. 偏移约束函数

```typescript
function constrainOffset(offset: number, winSize: number, imageSize: number, scale: number): number {
    let maxAllowedOffset = getMaxAllowedOffset(winSize, imageSize, scale);
    return Math.min(Math.max(offset, -maxAllowedOffset), maxAllowedOffset);
}
```

这个函数确保图片的偏移量不会超出允许的范围，通过 Math.min 和 Math.max 函数将偏移量限制在[-maxAllowedOffset, maxAllowedOffset]区间内。

## 三、图片切换判断

### 1. 切换条件判断

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

这个函数判断是否需要切换图片，通过计算当前偏移量与最大允许偏移量的差值，并与切换阈值（窗口尺寸 \* TogglePercent）进行比较。当差值大于阈值时，触发图片切换。

### 2. 边界评估与图片切换

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
    const yBol = constrainOffsetAndAnimation({
        dimensionWH: ImageFitType.TYPE_HEIGHT,
        imageDefaultSize: this.imageDefaultSize,
        imageOffsetInfo: this.imageOffsetInfo,
        scaleValue: this.imageScaleInfo.scaleValue,
        rotate: this.imageRotateInfo.lastRotate,
        TogglePercent: this.TogglePercent,
        imageListOffset: this.imageListOffset,
        listDirection: this.listDirection
    });
    if (this.listDirection === Axis.Horizontal) {
        if (xBol[0] || xBol[1]) {
            if (xBol[0]) {
                this.setListToIndex(this.imageIndex - 1);
                if (this.imageIndex !== 0) {
                    this.resetCurrentImageInfo();
                }
            }
            if (xBol[1]) {
                this.setListToIndex(this.imageIndex + 1);
                if (this.imageIndex < this.imageMaxLength - 1) {
                    this.resetCurrentImageInfo();
                }
            }
        } else {
            this.setListToIndex(this.imageIndex);
        }
    } else if (this.listDirection === Axis.Vertical) {
        // 垂直方向的处理逻辑类似
        // ...
    }
    this.imageListOffset = 0;
    this.isMoveCrossAxis = true;
}
```

这个方法是边界处理的核心，它通过调用 constrainOffsetAndAnimation 函数评估水平和垂直方向的边界情况，并根据返回结果决定是否切换图片。

## 四、主轴与交叉轴处理

### 1. 主轴处理

```typescript
// 设置主轴位置
setPrincipalAxis(event: GestureEvent) {
    // 获取主轴方向
    let direction: "X" | "Y" = this.listDirection === Axis.Horizontal ? "X" : "Y";
    // 获取主轴中对应的是 width 还是 height
    let imageWH = this.listDirection === Axis.Horizontal ? ImageFitType.TYPE_WIDTH : ImageFitType.TYPE_HEIGHT;
    // 获取手指在主轴移动偏移量
    let offset = event[`offset${direction}`];
    // 获取图片最后一次在主轴移动的数据
    let lastOffset = imageWH === ImageFitType.TYPE_WIDTH ? this.imageOffsetInfo.lastX : this.imageOffsetInfo.lastY;
    // 获取主轴上图片的尺寸
    const IMG_SIZE = getImgSize(this.imageDefaultSize, this.imageRotateInfo.lastRotate, imageWH);
    const WIN_SIZE = windowSizeManager.get();
    // 获取窗口对应轴的尺寸
    const WIN_AXIS_SIZE = WIN_SIZE[imageWH];
    // 当前最大移动距离
    let maxAllowedOffset = getMaxAllowedOffset(WIN_AXIS_SIZE, IMG_SIZE, this.imageScaleInfo.scaleValue);
    // 计算当前移动后偏移量结果
    let calculatedOffset = lastOffset + offset;

    // 处理左右滑动边界
    if (offset < 0) {
        // 左滑
        if ((this.imageIndex >= this.imageMaxLength - 1) || (calculatedOffset >= -maxAllowedOffset)) {
            // 当是最后一个元素 或者 当前移动没有抵达边缘时候触发
            this.setCurrentOffsetXY(imageWH, calculatedOffset)
        }
    } else if (offset > 0) {
        // 右滑
        if ((this.imageIndex === 0) || (calculatedOffset <= maxAllowedOffset)) {
            // 当是第一个元素 或者 当前移动没有抵达边缘时候触发
            this.setCurrentOffsetXY(imageWH, calculatedOffset)
        }
    }

    // 处理图片切换预览
    if ((calculatedOffset > maxAllowedOffset) && (this.imageIndex !== 0)) {
        // 右滑 -- 当前滑动超过最大值时 并且 不是第一个元素去设置list偏移量显"下一张"图片
        let listOffset = calculatedOffset - maxAllowedOffset;
        this.setListOffset(-listOffset)
        this.imageListOffset = listOffset;
    } else if ((calculatedOffset < -maxAllowedOffset) && (this.imageIndex < this.imageMaxLength - 1)) {
        // 左滑 -- 当前滑动超过最大值时 并且 不是最后一个元素去设置list偏移量显"下一张"图片
        let listOffset = calculatedOffset + maxAllowedOffset;
        this.setListOffset(Math.abs(listOffset))
        this.imageListOffset = listOffset;
    }
}
```

主轴处理负责处理图片在主滑动方向上的移动，包括边界约束和图片切换预览。当图片被拖动到边缘时，会显示下一张图片的预览，提供良好的视觉反馈。

### 2. 交叉轴处理

```typescript
// 设置交叉轴位置
setCrossAxis(event: GestureEvent) {
    // list当前没有在移动 &&  交叉轴时候如果没有放大也不移动
    let isScale = this.imageScaleInfo.scaleValue !== this.imageScaleInfo.defaultScaleValue;
    let listOffset = Math.abs(this.imageListOffset);
    if (listOffset > this.moveMaxOffset) {
        this.isMoveCrossAxis = false;
    }
    if (this.isMoveCrossAxis && isScale) {
        // 获取交叉轴方向
        let direction: "X" | "Y" = this.listDirection === Axis.Horizontal ? "Y" : "X";
        // 获取交叉轴中对应的是 width 还是 height
        let imageWH = this.listDirection === Axis.Horizontal ? ImageFitType.TYPE_HEIGHT : ImageFitType.TYPE_WIDTH;
        // 获取手指在主轴移动偏移量
        let offset = event[`offset${direction}`];
        // 获取图片最后一次在主轴移动的数据
        let lastOffset = imageWH === ImageFitType.TYPE_WIDTH ? this.imageOffsetInfo.lastX : this.imageOffsetInfo.lastY;
        // 计算当前移动后偏移量结果
        let calculatedOffset = lastOffset + offset;
        // 设置交叉轴数据
        this.setCurrentOffsetXY(imageWH, calculatedOffset)
    }
}
```

交叉轴处理负责处理图片在非主滑动方向上的移动。当图片被放大时，允许在交叉轴方向上移动；当图片处于切换预览状态时，禁止交叉轴移动，避免干扰图片切换操作。

## 五、综合约束与动画处理

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

这个函数是边界处理的核心，它综合了偏移约束和动画处理，并返回是否需要切换图片的判断结果。通过 runWithAnimation 函数，确保偏移修正过程有平滑的动画效果。

## 六、总结

图片预览组件的边界处理与图片切换功能是提供良好用户体验的关键。通过精确的偏移计算、合理的切换条件判断以及平滑的动画过渡，实现了图片在预览过程中的自然交互效果。

边界处理的核心技术包括：

1. 最大偏移量计算，确保图片不会完全移出视口
2. 切换条件判断，基于偏移量和阈值决定是否切换图片
3. 主轴与交叉轴分离处理，适应不同的滑动方向
4. 动画处理，确保偏移修正过程有平滑的动画效果
