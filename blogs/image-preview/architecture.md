 
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](../images/img_cf375330.png)

#  Harmonyos NEXT 图片预览组件架构设计与实现原理

## 效果预览

![](../images/img_0cb0cbb1.png)

## 一、组件架构概述

图片预览组件是一个用于展示和交互图片的高级组件，采用分层设计模式，将复杂功能拆分为多个独立模块，提高代码的可维护性和复用性。组件架构如下：

### 1. 核心组件层次结构

```
PicturePreview (外层容器)
  └── PicturePreviewImage (内层图片组件)
      └── Image (基础图片渲染)
```

### 2. 组件职责划分

| 组件名称 | 主要职责 | 核心技术 |
| --- | --- | --- |
| PicturePreview | 图片列表管理、切换控制 | List、LazyForEach、ListScroller |
| PicturePreviewImage | 单张图片交互、手势处理 | matrix4、手势识别、偏移计算 |

### 3. 数据模型设计

图片预览组件使用多个数据模型来管理不同的状态：

- **ScaleModel**: 管理图片缩放状态
- **RotateModel**: 管理图片旋转状态
- **OffsetModel**: 管理图片位移状态
- **CommonLazyDataSourceModel**: 实现图片的懒加载

## 二、PicturePreview组件实现

### 1. 组件定义

```typescript
@Component
export struct PicturePreview {
    // 滑动方向
    @Prop listDirection: Axis = Axis.Vertical;
    // 外部传入的图片数据
    @Link @Watch('getListMaxLength') imageList: string[];
    // 背景颜色
    @State listBGColor: Color = Color.White;
    // 图片懒加载数据源
    @State lazyImageList: CommonLazyDataSourceModel<string> = new CommonLazyDataSourceModel();
    // ...
}
```

### 2. 核心功能实现

#### 2.1 图片列表管理

```typescript
// 获取图片数量和设置懒加载图片数据
getListMaxLength() {
    this.listMaxLength = this.imageList.length;
    this.lazyImageList.clearAndPushAll(this.imageList)
}
```

这段代码实现了图片数据的初始化，将外部传入的图片列表转换为懒加载数据源，提高性能。

#### 2.2 图片切换控制

```typescript
// 改变到具体页面
setListToIndex = (index: number) => {
    const WIN_SIZE = windowSizeManager.get();
    let nIndex = index;
    if (nIndex < 0) {
        nIndex = 0
    } else if (nIndex >= this.listMaxLength) {
        nIndex = this.listMaxLength - 1
    }
    this.listIndex = nIndex;
    let principalAxisSize = this.listDirection === Axis.Horizontal ? WIN_SIZE.width : WIN_SIZE.height
    let calculatedOffset = Math.abs(nIndex * principalAxisSize) + this.listSpace * nIndex;
    this.listScroll.scrollTo({
        yOffset: this.listDirection === Axis.Horizontal ? 0 : calculatedOffset,
        xOffset: this.listDirection === Axis.Horizontal ? calculatedOffset : 0,
        animation: {
            duration: this.listAnimationDuration
        }
    })
}
```

这段代码实现了图片切换功能，通过计算偏移量并使用ListScroller控制滚动位置，实现图片的平滑切换。

### 3. 布局实现

```typescript
build() {
    NavDestination() {
        List({ scroller: this.listScroll, space: this.listSpace }) {
            LazyForEach(this.lazyImageList, (imageUrl: string, index: number) => {
                ListItem() {
                    PicturePreviewImage({
                        imageUrl: imageUrl,
                        listDirection: this.listDirection,
                        setListOffset: this.setListOffset,
                        setListToIndex: this.setListToIndex,
                        imageIndex: index,
                        imageMaxLength: this.listMaxLength,
                        listBGColor: this.listBGColor
                    })
                }
                .width("100%")
            })
        }
        .enableScrollInteraction(false) // 禁止List本身的滑动，避免滑动冲突
        // ...
    }
}
```

布局实现使用List组件和LazyForEach实现图片列表的渲染，通过禁用List的滚动交互，将滚动控制权交给PicturePreviewImage组件处理。

## 三、技术要点分析

### 1. 懒加载实现

图片预览组件使用CommonLazyDataSourceModel实现懒加载，只加载当前可见的图片，提高性能和内存利用率。

### 2. 主轴与交叉轴处理

组件支持水平和垂直两种滑动方向，通过listDirection属性控制：

```typescript
let principalAxisSize = this.listDirection === Axis.Horizontal ? WIN_SIZE.width : WIN_SIZE.height
```

### 3. 安全区域适配

```typescript
.expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP, SafeAreaEdge.BOTTOM])
```

通过expandSafeArea属性，确保组件在不同设备上的安全区域适配。

## 四、使用示例

```typescript
@Entry
@Component
struct PicturePreviewSample {
    @State imageList: string[] = [];
    @State listDirection: Axis = Axis.Horizontal;

    aboutToAppear(): void {
        let imageSource:string = $r("app.media.02") as ESObject;
        this.imageList.push(
            imageSource,
            imageSource,
            imageSource
        )
    }

    build() {
        RelativeContainer() {
            PicturePreview({ imageList: this.imageList, listDirection: this.listDirection })
        }
        .height('100%')
        .width('100%')
    }
}
```

## 五、总结

图片预览组件通过分层设计和数据模型抽象，实现了高性能、高可用性的图片预览体验。PicturePreview作为外层容器，负责图片列表的管理和切换，而内部的交互细节则由PicturePreviewImage组件处理，形成了清晰的职责划分。

组件的核心技术包括：

1. 使用List和LazyForEach实现图片列表的高效渲染
2. 通过ListScroller控制图片的切换
3. 支持水平和垂直两种滑动方向
4. 安全区域适配，确保在不同设备上的显示效果

在下一篇教程中，我们将深入探讨PicturePreviewImage组件的实现，了解图片的缩放、旋转和手势处理等功能的实现原理。
