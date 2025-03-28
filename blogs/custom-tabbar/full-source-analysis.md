> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](../images/img_ebd152fa.png)
# HarmonyOS NEXT系列教程之 TabsConcaveCircle组件完整源码解析

本文将对TabsConcaveCircle组件的完整源码进行详细解析，帮助开发者深入理解组件的实现原理。
## 效果演示

![](../images/img_e3a9fa89.png)
## 1. 模块导入与依赖

```typescript
import animator, { AnimatorResult } from '@ohos.animator';
import componentUtils from '@ohos.arkui.componentUtils';
import inspector from '@ohos.arkui.inspector';
import { CanvasClipGroove, CanvasCreateRectangle, getImageUrl } from '../../utils/tabbar/Functions';
import { TabMenusInterfaceIRequired } from '../../types/TabMenusInterface';
import { ConcaveCircle } from '../../utils/tabbar/CircleClass';
```

### 导入说明：
1. `animator`: 提供动画相关功能
2. `componentUtils`: 提供组件工具函数
3. `inspector`: 用于组件观察和检查
4. 自定义工具函数：
   - `CanvasClipGroove`: 创建凹槽效果
   - `CanvasCreateRectangle`: 创建矩形背景
   - `getImageUrl`: 处理图片URL
5. 类型定义和工具类：
   - `TabMenusInterfaceIRequired`: 菜单项接口
   - `ConcaveCircle`: 凹陷圆形处理类

## 2. 组件状态与属性定义

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
```

### 状态属性说明：
1. 核心状态：
   - `selectIndex`: 当前选中项索引
   - `animateSelectIndex`: 动画控制索引
   - `tabsMenu`: 菜单数据集合

2. 样式属性：
   - `tabHeight`: 导航栏高度
   - `tabsBgColor`: 背景颜色
   - `tabsSelectBgColor`: 选中状态颜色
   - `tabsFontColor`: 文字颜色
   - `tabsSelectFontColor`: 选中文字颜色

## 3. Canvas相关实现

```typescript
private settings: RenderingContextSettings = new RenderingContextSettings(true);
private context: CanvasRenderingContext2D = new CanvasRenderingContext2D(this.settings);

createCanvas() {
  if (this.circleInfo) {
    this.context.reset()
    CanvasCreateRectangle({
      context: this.context,
      tabsBgColor: this.tabsBgColor
    })
    CanvasClipGroove({
      context: this.context,
      menuLength: this.tabsMenu.length,
      center: this.animationPositionX,
    })
  }
}
```

### Canvas实现说明：
1. 上下文初始化：
   - 创建渲染设置
   - 初始化2D渲染上下文

2. 绘制流程：
   - 重置画布状态
   - 绘制背景矩形
   - 创建凹槽效果

## 4. 动画系统实现

```typescript
createAnimation() {
  if (!this.circleInfo) {
    return;
  }
  this.canvasAnimator = animator.create({
    duration: this.animateTime,
    easing: "ease",
    delay: 0,
    fill: "forwards",
    direction: "normal",
    iterations: 1,
    begin: this.animationPositionX,
    end: this.circleInfo?.getMenuCenterX(this.selectIndex)
  })
  
  this.canvasAnimator.onFrame = (value: number) => {
    this.animationPositionX = value;
    this.circleInfo?.setPositionXY({ x: value - this.circleInfo.circleRadius })
    this.createCanvas()
  }
  
  this.canvasAnimator.play()
}
```

### 动画实现说明：
1. 动画配置：
   - 设置动画时长和缓动函数
   - 配置动画方向和循环次数
   - 设置起始和结束位置

2. 帧动画处理：
   - 更新位置信息
   - 重新计算圆球位置
   - 重绘Canvas内容

## 总结

TabsConcaveCircle组件通过以下几个关键部分实现了独特的视觉效果：
1. 状态管理系统
2. Canvas渲染系统
3. 动画控制系统
4. 交互响应系统

这些系统协同工作，创造出了一个既美观又实用的底部导航栏组件。通过合理的代码组织和模块化设计，使得组件易于维护和扩展。
