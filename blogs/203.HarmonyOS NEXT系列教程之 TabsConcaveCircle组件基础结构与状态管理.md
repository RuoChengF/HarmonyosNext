> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/e7866215-2919-4450-90eb-21112b7974a1.png)

# HarmonyOS NEXT系列教程之 TabsConcaveCircle组件基础结构与状态管理

TabsConcaveCircle是一个自定义的底部导航栏组件，它具有独特的凹陷圆形设计。本文将详细介绍该组件的基础结构和状态管理部分。
## 效果演示

![](https://files.mdnice.com/user/47561/c2894823-0343-4de9-a551-e971b3e8daff.gif)
## 1. 组件导入说明

```typescript
import animator, { AnimatorResult } from '@ohos.animator';
import componentUtils from '@ohos.arkui.componentUtils';
import inspector from '@ohos.arkui.inspector';
import { CanvasClipGroove, CanvasCreateRectangle, getImageUrl } from '../../utils/tabbar/Functions';
import { TabMenusInterfaceIRequired } from '../../types/TabMenusInterface';
import { ConcaveCircle } from '../../utils/tabbar/CircleClass';
```

- `animator`: 用于创建和管理动画效果
- `componentUtils`: 提供组件相关的工具函数
- `inspector`: 用于组件观察和监听
- 自定义工具函数：
  - `CanvasClipGroove`: 用于创建凹槽效果
  - `CanvasCreateRectangle`: 用于创建矩形背景
  - `getImageUrl`: 处理图片URL
- `TabMenusInterfaceIRequired`: 定义选项菜单的接口
- `ConcaveCircle`: 处理凹陷圆形的相关计算

## 2. 组件状态管理

```typescript
@Component
export struct TabsConcaveCircle {
  @Link @Watch("getAnimateSelectIndex") selectIndex: number;
  @State animateSelectIndex: number = 0;
  @Prop tabHeight: number = 60;
  @Link tabsMenu: TabMenusInterfaceIRequired[];
  @Prop tabsBgColor: string = "rgb(255, 255, 255)";
  @Prop tabsSelectBgColor: Color | number | string | Resource = "rgba(92, 187, 183,1)";
  @Prop tabsFontColor: Color = Color.Black;
  @Prop tabsSelectFontColor: Color = Color.Black;
}
```

### 状态装饰器说明

1. `@Link`装饰器：
   - `selectIndex`: 当前选中项的索引，支持双向绑定
   - `tabsMenu`: 选项数据集合，支持双向绑定

2. `@State`装饰器：
   - `animateSelectIndex`: 用于控制动画的当前选中项
   - `circleInfo`: 存储凹陷圆球的信息
   - `animationPositionX`: 记录当前凹槽位置
   - `imageOffsetY`: 图片的垂直偏移量
   - `imageWH`: 图片的宽高

3. `@Prop`装饰器：
   - `tabHeight`: 定义Tabs的高度
   - `tabsBgColor`: 背景颜色
   - `tabsSelectBgColor`: 选中球的填充颜色
   - `tabsFontColor`: 字体颜色
   - `tabsSelectFontColor`: 选中时的字体颜色

## 3. Canvas相关配置

```typescript
private settings: RenderingContextSettings = new RenderingContextSettings(true);
private context: CanvasRenderingContext2D = new CanvasRenderingContext2D(this.settings);
```

- `RenderingContextSettings`: 创建Canvas渲染上下文的设置
- `CanvasRenderingContext2D`: Canvas的2D渲染上下文，用于绘制图形

## 4. 动画相关属性

```typescript
private canvasAnimator: AnimatorResult | undefined = undefined;
@State animateTime: number = 1000;
```

- `canvasAnimator`: 存储动画实例
- `animateTime`: 动画执行时长，默认为1000毫秒

## 总结

本文介绍了TabsConcaveCircle组件的基础结构和状态管理部分，包括：
1. 必要的模块导入
2. 组件的状态管理和属性定义
3. Canvas相关配置
4. 动画相关属性

这些基础结构为实现一个具有凹陷圆形效果的底部导航栏提供了必要的框架。在后续文章中，我们将详细介绍组件的动画实现、交互处理和渲染逻辑。
