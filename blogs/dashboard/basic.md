![](../images/img_cb1ff158.png)

> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

[toc]
# HarmonyOS Next仪表盘案例详解（一）：基础篇

## 1. 项目概述

本文将详细分析 HarmonyOS 应用中的仪表盘(Dashboard)示例，该示例展示了一个业务数据概览页面，包含数据卡片和趋势图表区域。通过这个案例，我们可以学习 HarmonyOS 应用开发的核心技术和最佳实践。

## 2. 技术架构

### 2.1 文件结构

仪表盘示例位于`entry/src/main/ets/pages/StudyHo/DashboardExample.ets`，是一个完整的页面组件。该组件引用了自定义的 Navbar 组件，展示了 HarmonyOS 组件化开发的思想。

```typescript
import { router } from '@kit.ArkUI';
import { Navbar as MyNavbar } from "../../components/NavBar"
```

### 2.2 ArkTS 语言特性

该案例充分利用了 ArkTS 语言的特性，主要包括：

#### 装饰器的使用

```typescript
@Entry  // 标记组件为页面入口
@Component  // 定义自定义组件
struct DashboardExample {
    @State desc: string = '';  // 组件内部状态变量
    @State title: string = ''
    // ...
}
```

- **@Entry**：标记 DashboardExample 为页面入口组件
- **@Component**：声明 DashboardExample 为自定义组件
- **@State**：定义组件内部状态变量，当这些变量发生变化时，UI 会自动刷新

## 3. 数据结构设计

### 3.1 接口定义

案例中定义了`DashboardCardItem`接口，用于描述仪表盘数据卡片的数据结构：

```typescript
export interface DashboardCardItem {
    /**
     * 卡片标题
     */
    title: string;

    /**
     * 数值内容
     */
    value: string;

    /**
     * 数值单位
     */
    unit: string;

    /**
     * 趋势变化，如'+12.5%'或'-0.3s'
     */
    trend: string;

    /**
     * 卡片主题颜色，十六进制颜色代码
     */
    color: string;
}
```

这种接口定义方式体现了 TypeScript 的类型系统优势，使代码更加健壮，同时提高了开发效率和代码可维护性。

### 3.2 数据初始化

组件内部使用@State 装饰器定义了 dataCards 数组，初始化了四个数据卡片：

```typescript
@State dataCards:DashboardCardItem[] = [
    {title: '今日销售额', value: '8,846', unit: '元', trend: '+12.5%', color: '#2A9D8F'},
    {title: '活跃用户数', value: '1,286', unit: '人', trend: '+6.8%', color: '#E9C46A'},
    {title: '订单完成率', value: '92.6', unit: '%', trend: '+2.4%', color: '#F4A261'},
    {title: '平均响应时间', value: '1.2', unit: '秒', trend: '-0.3s', color: '#E76F51'}
]
```

每个卡片都有不同的主题颜色，使界面更加丰富多彩，同时通过 trend 字段显示数据的变化趋势。

## 4. 生命周期与页面路由

### 4.1 组件生命周期

```typescript
aboutToAppear() {
    // 获取屏幕宽度，用于响应式布局
    this.screenWidth = px2vp(AppStorage.Get<number>('windowWidth') || 720)
}
```

`aboutToAppear()`是组件的生命周期函数，在组件即将出现时调用。这里用于获取屏幕宽度，为响应式布局做准备。

### 4.2 页面参数传递

```typescript
onPageShow(): void {
    // 获取传递过来的参数对象
    const params = router.getParams() as Record<string, string>;
    //   获取传递的值
    if (params) {
        this.desc = params.desc as string
        this.title = params.value as string
    }
}
```

`onPageShow()`在页面显示时调用，用于接收页面路由传递的参数。这里通过`router.getParams()`获取参数，并将参数值赋给组件的状态变量。

## 5. UI 布局与组件

### 5.1 整体布局结构

DashboardExample 的 UI 结构如下：

```
Column (根容器)
├── MyNavbar (导航栏)
├── Flex (顶部标题栏)
│   ├── Text (标题文本)
│   └── Flex (筛选器)
├── Flex (数据卡片网格)
│   └── ForEach (循环渲染数据卡片)
└── Column (图表区域)
    ├── Flex (图表标题栏)
    └── Column (图表占位区域)
```

这种嵌套结构清晰地展示了 HarmonyOS 声明式 UI 的特点，通过组合不同的容器组件和基础组件，构建复杂的界面。

### 5.2 基础组件使用

案例中使用了多种基础 UI 组件：

- **Text**：文本显示组件，用于显示标题、数值等
- **Image**：图片显示组件，用于显示图标
- **Column**：垂直布局容器
- **Flex**：弹性布局容器，支持更灵活的布局方式
- **ForEach**：循环渲染组件，用于批量创建数据卡片

### 5.3 样式与主题

ArkTS 支持链式调用设置组件样式，使 UI 代码更加简洁：

```typescript
Text(card.value)
    .fontSize(28)
    .fontWeight(FontWeight.Bold)
    .fontColor(card.color)
```

数据卡片的样式设置：

```typescript
.width(this.screenWidth > 600 ? '22%' : '45%')
.height(120)
.padding(16)
.margin(8)
.borderRadius(12)
.backgroundColor(Color.White)
// 添加卡片阴影效果
.shadow({radius: 4, color: '#1A000000', offsetY: 2})
```

这种链式调用方式使代码更加简洁易读，同时通过设置 borderRadius、shadow 等属性实现丰富的视觉效果。

## 总结

本文介绍了 HarmonyOS 仪表盘示例的基础部分，包括项目概述、技术架构、数据结构设计、生命周期与页面路由以及 UI 布局与组件等内容。通过这些基础知识，开发者可以了解 HarmonyOS 应用开发的核心概念和基本结构。在下一篇文章中，我们将继续探讨响应式设计、数据展示与交互、事件处理机制、性能优化技巧、数据流管理和最佳实践等高级内容。
