> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/2f8d522f-949e-42c9-9936-10921b18abfa.png)

# HarmonyOS NEXT 数字滚动动画详解(一)：基础结构与原理

## 效果演示

![](https://files.mdnice.com/user/47561/3c439d97-e02c-4488-be35-fd0735537c95.gif)


## 1. 组件概述

DigitalScrollDetail是一个实现数字滚动动画效果的组件，主要用于展示数字变化的动态效果，类似于计数器或者股票价格显示。

## 2. 基本原理

组件通过以下步骤实现数字滚动效果：
1. 双重ForEach循环渲染数字
2. 随机数生成更新数据
3. 动画控制数字滚动
4. 视图裁剪控制显示

## 3. 核心属性

```typescript
@Component
export struct DigitalScrollDetail {
  // 可选数字数组
  private dataItem: number[] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
  
  // Y轴滚动位移数组
  @State scrollYList: number[] = [];
  
  // 当前显示的数字数组
  private currentData: number[] = new Array(DATA_CONFIG.NUMBER_LEN).fill(0);
  
  // 上一次显示的数字数组
  private preData: number[] = new Array(DATA_CONFIG.NUMBER_LEN).fill(0);
  
  // 是否需要刷新的状态标记
  @Prop @Watch('onDataRefresh') isRefresh: boolean;
}
```

## 4. 属性说明

### 4.1 dataItem
- 类型：number[]
- 作用：存储0-9的数字，用于垂直方向的数字显示
- 使用：作为基础数字源进行渲染

### 4.2 scrollYList
- 类型：number[]
- 装饰器：@State
- 作用：存储每个数字位的Y轴偏移量
- 特点：状态变化会触发视图更新

### 4.3 currentData和preData
- 类型：number[]
- 作用：分别存储当前和上一次的数字值
- 用途：用于计算动画时长和更新显示

### 4.4 isRefresh
- 装饰器：@Prop @Watch
- 作用：控制数据刷新的触发器
- 特点：值变化时会触发onDataRefresh回调

## 5. 配置常量

```typescript
// 从ConstData.ts导入的配置
const DATA_CONFIG = {
  NUMBER_LEN: 6,        // 显示的数字位数
  MILLENNIAL_LEN: 3,    // 千分位长度
  DURATION_TIME: 100    // 基础动画时长
}

const STYLE_CONFIG = {
  ITEM_HEIGHT: 32      // 数字项高度
}
```

## 6. 工作流程

1. 初始化
   - 创建数字源数组(0-9)
   - 初始化当前和历史数据数组
   - 准备Y轴偏移量数组

2. 数据更新触发
   - 监听isRefresh变化
   - 触发onDataRefresh回调
   - 执行refreshData方法

3. 视图渲染
   - 横向遍历显示位数
   - 纵向遍历显示数字
   - 应用Y轴偏移实现滚动

## 7. 使用示例

```typescript
// 创建组件实例
DigitalScrollDetail({
  isRefresh: true
})
```

## 8. 注意事项

1. 性能考虑
   - 使用ForEach而不是map
   - 控制动画对象数量
   - 及时清理资源

2. 数据处理
   - 注意数组长度一致性
   - 处理边界情况
   - 合理使用状态管理

3. 视图更新
   - 合理使用@State
   - 控制更新频率
   - 优化渲染性能

通过以上详细讲解，你应该能够理解这个数字滚动组件的基本结构和工作原理。在接下来的文章中，我们将深入探讨动画实现、布局处理等具体细节。
