 
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/c18147ef-6c89-4908-96f9-17b757244d87.png)

# Harmonyos NEXT 图片预览组件之手势处理实现
## 效果预览

![](https://files.mdnice.com/user/47561/d8d2c370-46fe-4ef5-a985-5961f413f927.jpg)
## 一、手势处理概述

手势处理是图片预览组件的核心交互功能，通过识别和响应用户的各种触摸操作，实现图片的缩放、旋转、拖动和切换等功能。本文将详细介绍PicturePreviewImage组件中的手势处理实现原理。

### 1. 手势类型

图片预览组件支持以下几种手势类型：

| 手势类型 | 触发方式 | 功能 |
| --- | --- | --- |
| 单指拖动 | 单指在屏幕上滑动 | 移动图片、触发图片切换 |
| 双指缩放 | 两指捏合或分开 | 放大或缩小图片 |
| 双指旋转 | 两指旋转 | 旋转图片 |
| 双击 | 快速点击两次 | 在默认大小和适配屏幕大小之间切换 |

### 2. 手势处理架构

图片预览组件采用了组合手势的处理架构，通过GestureGroup将多种手势组合在一起，实现复杂的交互效果：

```typescript
// 单指手势组
GestureGroup(
    GestureMode.Parallel,
    TapGesture({ count: 2 }),  // 双击手势
    PanGesture({ fingers: 1 })  // 单指拖动手势
)

// 双指手势组
GestureGroup(
    GestureMode.Parallel,
    RotationGesture({ angle: this.imageRotateInfo.startAngle }),  // 旋转手势
    PinchGesture({ fingers: 2, distance: 1 })  // 缩放手势
)
```

## 二、单指拖动手势实现

### 1. 手势定义

```typescript
PanGesture({ fingers: 1 })
    .onActionUpdate((event: GestureEvent) => {
        if (this.imageWH != ImageFitType.TYPE_DEFAULT) {
            if (this.eventOffsetX != event.offsetX || event.offsetY != this.eventOffsetY) {
                this.eventOffsetX = event.offsetX;
                this.eventOffsetY = event.offsetY;
                this.setCrossAxis(event);
                this.setPrincipalAxis(event);
            }
        }
    })
    .onActionEnd((event: GestureEvent) => {
        this.imageOffsetInfo.stash();
        this.evaluateBound();
    })
```

### 2. 主轴处理

主轴处理是单指拖动手势的核心，它负责处理图片在主滑动方向上的移动：

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

主轴处理的核心逻辑包括：

1. 根据listDirection确定主轴方向（X或Y）
2. 计算图片在主轴方向上的最大允许偏移量
3. 处理边界情况，确保图片不会超出合理范围
4. 当图片达到边缘时，显示下一张图片的预览

### 3. 交叉轴处理

交叉轴处理负责图片在非主滑动方向上的移动：

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

交叉轴处理的核心逻辑包括：

1. 只有当图片被放大时，才允许在交叉轴方向上移动
2. 当图片处于切换预览状态时（imageListOffset > moveMaxOffset），禁止交叉轴移动
3. 根据listDirection确定交叉轴方向（与主轴相反）

## 三、双指缩放手势实现

### 1. 手势定义

```typescript
PinchGesture({ fingers: 2, distance: 1 })
    .onActionUpdate((event: GestureEvent) => {
        let scale = this.imageScaleInfo.lastValue * event.scale;
        // 限制缩放范围
        if (scale > this.imageScaleInfo.maxScaleValue * (1 + this.imageScaleInfo.extraScaleValue)) {
            scale = this.imageScaleInfo.maxScaleValue * (1 + this.imageScaleInfo.extraScaleValue);
        }
        if (scale < this.imageScaleInfo.defaultScaleValue * (1 - this.imageScaleInfo.extraScaleValue)) {
            scale = this.imageScaleInfo.defaultScaleValue * (1 - this.imageScaleInfo.extraScaleValue);
        }
        this.imageScaleInfo.scaleValue = scale;
        // 应用矩阵变换
        this.matrix = matrix4.identity().scale({
            x: this.imageScaleInfo.scaleValue,
            y: this.imageScaleInfo.scaleValue,
        }).rotate({
            x: 0,
            y: 0,
            z: 1,
            angle: this.imageRotateInfo.currentRotate,
        }).copy();
    })
    .onActionEnd((event: GestureEvent) => {
        // 当小于默认大小时，恢复为默认大小
        if (this.imageScaleInfo.scaleValue < this.imageScaleInfo.defaultScaleValue) {
            runWithAnimation(() => {
                this.imageScaleInfo.reset();
                this.imageOffsetInfo.reset();
                this.matrix = matrix4.identity().rotate({
                    x: 0,
                    y: 0,
                    z: 1,
                    angle: this.imageRotateInfo.currentRotate,
                }).copy();
            })
        }
        // 当大于最大缩放因子时，恢复到最大
        if (this.imageScaleInfo.scaleValue > this.imageScaleInfo.maxScaleValue) {
            runWithAnimation(() => {
                this.imageScaleInfo.scaleValue = this.imageScaleInfo.maxScaleValue;
                this.matrix = matrix4.identity()
                    .scale({
                        x: this.imageScaleInfo.maxScaleValue,
                        y: this.imageScaleInfo.maxScaleValue
                    }).rotate({
                        x: 0,
                        y: 0,
                        z: 1,
                        angle: this.imageRotateInfo.currentRotate,
                    });
            })
        }
        this.imageScaleInfo.stash();
    })
```

### 2. 缩放处理逻辑

双指缩放手势的核心逻辑包括：

1. 根据event.scale计算新的缩放值，基于上次缩放的结果（lastValue）
2. 限制缩放范围，防止过度放大或缩小
3. 应用矩阵变换，实现图片的缩放效果
4. 手势结束时，处理边界情况：
   - 如果缩放值小于默认值，恢复到默认大小
   - 如果缩放值大于最大值，恢复到最大值
5. 保存当前缩放值为最后缩放值，用于下次缩放的基准计算

### 3. 弹性缩放体验

组件通过extraScaleValue属性提供了弹性缩放体验，允许用户在手势过程中临时超出缩放限制，但在手势结束时会恢复到合理范围：

```typescript
// 允许的最大缩放范围
let maxScale = this.imageScaleInfo.maxScaleValue * (1 + this.imageScaleInfo.extraScaleValue);
// 允许的最小缩放范围
let minScale = this.imageScaleInfo.defaultScaleValue * (1 - this.imageScaleInfo.extraScaleValue);
```
 ## 四、总结
 通过上述代码，实现了一个具有手势交互的图片预览组件，实现了图片的缩放、旋转、移动、切换预览等功能。通过使用手势库，实现了对图片的交互，并实现了各种手势的响应。
