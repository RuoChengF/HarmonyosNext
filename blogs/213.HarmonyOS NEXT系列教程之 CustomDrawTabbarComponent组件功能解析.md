> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/e7866215-2919-4450-90eb-21112b7974a1.png)
# HarmonyOS NEXT系列教程之 CustomDrawTabbarComponent组件功能解析

本文将详细解析CustomDrawTabbarComponent组件的实现，这是一个自定义的TabBar容器组件。
## 效果演示

![](https://files.mdnice.com/user/47561/c2894823-0343-4de9-a551-e971b3e8daff.gif)
## 1. 组件功能概述

```typescript
/**
 * 功能描述: 通过canvas，clipShape，radialGradient实现自定义TabBar选择时凸起点交界处的圆滑过渡动效以及扩展了一个凹陷选择时不遮挡原本内容的功能。
 *
 * 推荐场景: 自定义TabBar页签需要实现一圈圆弧外轮廓或者凹陷轮廓，点击TabBar页签之后需要改变图标显示，并有平移滑动切换页签动效的场景。
 */
@Component
export struct CustomDrawTabbarComponent {
  @State currentIndex: number = 0;
  @State TabsMenu: TabMenusInterfaceIRequired[] = [
    // 菜单配置
  ];
}
```

### 功能特点说明：

1. 核心功能：
   - 自定义TabBar实现
   - 支持凸起和凹陷效果
   - 平滑的过渡动画

2. 适用场景：
   - 需要圆弧外轮廓
   - 需要凹陷轮廓
   - 需要动态图标
   - 需要切换动画

## 2. 菜单数据结构

```typescript
@State TabsMenu: TabMenusInterfaceIRequired[] = [
  {
    text: $r("app.string.custom_tab_home"),
    image: $r("app.media.tab_home"),
    selectImage: $r("app.media.tab_community")
  },
  {
    text: $r("app.string.custom_tab_friend"),
    image: $r("app.media.tab_cart"),
    selectImage: $r("app.media.tab_community")
  }
  // ... 其他菜单项
];
```

### 数据结构说明：

1. 菜单项配置：
   - `text`: 显示文本
   - `image`: 默认图标
   - `selectImage`: 选中状态图标

2. 资源引用：
   - 使用`$r()`引用资源
   - 支持多语言
   - 支持图片资源

## 3. 布局实现

```typescript
build() {
  Column() {
    Divider()
      .margin(30)
    TabsConcaveCircle({
      tabsMenu: this.TabsMenu,
      selectIndex: this.currentIndex,
    });
  }
  .width('100%')
  .height("100%")
  .justifyContent(FlexAlign.Center)
  .linearGradient({
    direction: GradientDirection.Left,
    repeating: false,
    colors: [[Color.White, 0.0], [Color.Pink, 1]]
  })
}
```

### 布局结构说明：

1. 容器设置：
   - 使用Column布局
   - 全屏显示
   - 居中对齐

2. 分隔线：
   ```typescript
   Divider()
     .margin(30)
   ```
   - 添加视觉分隔
   - 设置外边距

3. TabBar组件：
   ```typescript
   TabsConcaveCircle({
     tabsMenu: this.TabsMenu,
     selectIndex: this.currentIndex,
   });
   ```
   - 传入菜单数据
   - 传入选中索引

4. 背景效果：
   ```typescript
   .linearGradient({
     direction: GradientDirection.Left,
     repeating: false,
     colors: [[Color.White, 0.0], [Color.Pink, 1]]
   })
   ```
   - 线性渐变
   - 从白色到粉色
   - 左向右渐变

## 4. 组件集成

```typescript
import { TabsConcaveCircle } from '../tabsConcaveCircle/TabsConcaveCircle'
import { TabsRaisedCircle } from '../tabsRaisedCircle/TabsRaisedCircle';
import { TabMenusInterfaceIRequired } from  '../../types/TabMenusInterface'
```

### 集成说明：

1. 组件导入：
   - TabsConcaveCircle: 凹陷效果
   - TabsRaisedCircle: 凸起效果
   - 类型定义导入

2. 组件使用：
   - 可选择使用凹陷或凸起效果
   - 统一的数据接口
   - 一致的交互模式

## 总结

CustomDrawTabbarComponent组件通过：
1. 清晰的功能定位
2. 完整的数据结构
3. 灵活的布局设计
4. 优雅的组件集成

实现了一个：
- 功能丰富
- 使用灵活
- 视觉优美
- 交互流畅

的TabBar容器组件。这个组件为开发者提供了：
- 多种视觉效果选择
- 简单的配置方式
- 统一的使用接口
- 良好的扩展性
