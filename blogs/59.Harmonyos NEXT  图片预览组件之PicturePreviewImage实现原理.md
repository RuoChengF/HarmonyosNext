 
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/af11f342-5073-4b3d-a923-cbfdf4737b3d.png)

#   Harmonyos NEXT  图片预览组件之PicturePreviewImage实现原理

## 效果预览

![](https://files.mdnice.com/user/47561/e4fc23ba-5598-466e-98a8-56fc5f9cedce.jpg)

## 一、组件概述

`PicturePreviewImage`是图片预览组件的核心内层组件，负责单张图片的展示和交互处理。该组件实现了图片的缩放、旋转、拖动等丰富的交互功能，为用户提供流畅的图片预览体验。

### 1. 组件定义

```typescript
@Reusable
@Component
export struct PicturePreviewImage {
    // 当前背景色
    @Link listBGColor: Color;
    // 图片显示的地址
    @Require @Prop imageUrl: string = '';
    // 图片滑动方向
    @Require @Prop listDirection: Axis;
    // 图片滑动多大距离需要切换图片
    @Prop TogglePercent: number = 0.2;
    // 当前图片下标
    @Prop imageIndex: number = 0;
    // 最多几张图片
    @Prop imageMaxLength: number = 0;
    // 设置偏移尺寸
    setListOffset: (offset: number, animationDuration?: number) => void;
    // 切换图片
    setListToIndex: (index: number) => void;
    // ...
}
```

### 2. 核心状态管理

组件使用多个状态模型来管理图片的不同交互状态：

```typescript
// 图片旋转信息
@State imageRotateInfo: RotateModel = new RotateModel();
// 图片缩放信息
@State imageScaleInfo: ScaleModel = new ScaleModel(1.0, 1.0, 1.5, 0.3);
// 图片默认大小 -- 是转化后的大小
@State imageDefaultSize: image.Size = { width: 0, height: 0 };
// 表示当前图片是根据宽度适配还是高度适配
@State imageWH: ImageFitType = ImageFitType.TYPE_DEFAULT;
// 本模块提供矩阵变换功能，可对图形进行平移、旋转和缩放等
@State matrix: matrix4.Matrix4Transit = matrix4.identity().copy();
// 图片偏移信息
@State imageOffsetInfo: OffsetModel = new OffsetModel(0, 0);
```

## 二、核心功能实现

### 1. 图片尺寸计算

组件会根据图片原始宽高比和窗口大小，计算图片的默认显示尺寸：

```typescript
calcImageDefaultSize(imageWHRatio: number, windowSize: window.Size): image.Size {
    let width = 0
    let height = 0;
    if (imageWHRatio > windowSize.width / windowSize.height) {
        // 图片宽高比大于屏幕宽高比，图片默认以屏幕宽度进行显示
        width = windowSize.width;
        height = windowSize.width / imageWHRatio;
    } else {
        height = windowSize.height;
        width = windowSize.height * imageWHRatio;
    }
    return { width: width, height: height };
}
```

这段代码根据图片和屏幕的宽高比，决定图片是以屏幕宽度还是高度为基准进行适配显示。

### 2. 图片信息初始化

当图片加载完成后，组件会初始化图片的相关信息：

```typescript
initCurrentImageInfo(event: ImageLoadResult): void {
    let imageW = event.width;
    let imageH = event.height;
    let windowSize = windowSizeManager.get();
    // 图片宽高比
    this.imageWHRatio = imageW / imageH;
    // 图片默认大小
    this.imageDefaultSize = this.calcImageDefaultSize(this.imageWHRatio, windowSize);
    // 图片宽度 等于 视口宽度 则图片使用宽度适配 否则 使用 高度适配
    if (this.imageDefaultSize.width === windowSize.width) {
        this.imageWH = ImageFitType.TYPE_WIDTH;
    } else {
        this.imageWH = ImageFitType.TYPE_HEIGHT;
    }
    // 设置最大缩放值
    this.imageScaleInfo.maxScaleValue += this.imageWH === ImageFitType.TYPE_WIDTH ?
        (windowSize.height / this.imageDefaultSize.height) :
        (windowSize.width / this.imageDefaultSize.width);
}
```

这段代码完成了图片适配类型的判断和最大缩放值的计算，为后续的交互操作做准备。

### 3. 矩阵变换实现

组件使用matrix4矩阵变换实现图片的缩放和旋转效果：

```typescript
// 缩放矩阵示例
this.matrix = matrix4.identity().scale({
    x: this.imageScaleInfo.scaleValue,
    y: this.imageScaleInfo.scaleValue,
}).rotate({
    x: 0,
    y: 0,
    z: 1,
    angle: this.imageRotateInfo.currentRotate,
}).copy();
```

矩阵变换是实现图片缩放和旋转的核心技术，通过matrix4.identity()创建单位矩阵，然后应用缩放和旋转变换。

## 三、手势处理实现

### 1. 单指拖动

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

单指拖动手势用于移动图片，分为主轴和交叉轴两个方向的处理。当手指释放时，会评估边界并决定是否需要切换图片。

### 2. 双指缩放

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
```

双指缩放手势用于放大缩小图片，通过event.scale获取缩放比例，并应用到矩阵变换中。

### 3. 双指旋转

```typescript
RotationGesture({ angle: this.imageRotateInfo.startAngle })
    .onActionUpdate((event: GestureEvent) => {
        let angle = this.imageRotateInfo.lastRotate + event.angle
        if (event.angle > 0) {
            angle -= this.imageRotateInfo.startAngle;
        } else {
            angle += this.imageRotateInfo.startAngle;
        }
        this.matrix = matrix4.identity()
            .scale({
                x: this.imageScaleInfo.scaleValue,
                y: this.imageScaleInfo.scaleValue
            })
            .rotate({
                x: 0,
                y: 0,
                z: 1,
                angle: angle,
            }).copy();
        this.imageRotateInfo.currentRotate = angle;
    })
```

双指旋转手势用于旋转图片，通过event.angle获取旋转角度，并应用到矩阵变换中。

### 4. 双击缩放

```typescript
TapGesture({ count: 2 })
    .onAction(() => {
        let fn: Function;
        // 当前大小倍数 大于 默认的倍数，则是放大状态需要缩小
        if (this.imageScaleInfo.scaleValue > this.imageScaleInfo.defaultScaleValue) {
            fn = () => {
                // 恢复默认大小
                this.imageScaleInfo.reset();
                // 重置偏移量
                this.imageOffsetInfo.reset();
                // 设置一个新的矩阵
                this.matrix = matrix4.identity().copy().rotate({
                    z: 1,
                    angle: this.imageRotateInfo.lastRotate
                });
            }
        } else {
            fn = () => {
                // 这里是正常状态 -- 需要放大
                // 获取放大倍数
                const ratio: number = this.calcFitScaleRatio(this.imageDefaultSize, windowSizeManager.get());
                // 设置当前放大倍数
                this.imageScaleInfo.scaleValue = ratio;
                // 重置偏移量
                this.imageOffsetInfo.reset();
                // 设置矩阵元素
                this.matrix = matrix4.identity().scale({
                    x: ratio,
                    y: ratio,
                }).rotate({
                    z: 1,
                    angle: this.imageRotateInfo.lastRotate
                }).copy();
                // 设置最后放大倍数设置为当前的倍数
                this.imageScaleInfo.stash();
            }
        }
        runWithAnimation(fn);
    })
```

双击缩放功能实现了图片在默认大小和适配屏幕大小之间的切换，提供了便捷的缩放操作。
 
 ## 四、总结
 
 本文介绍了图片浏览器的核心功能，包括图片的加载、缩放、旋转、拖动、双指缩放、双指旋转、双击缩放等。通过这些功能，我们可以实现一个功能完善的图片浏览器。同时，本文也提供了详细的代码实现，包括核心逻辑、事件处理、动画效果等。通过阅读本文，读者可以更好地理解和掌握图片浏览器的实现原理和技巧。
