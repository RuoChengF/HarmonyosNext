> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/e7866215-2919-4450-90eb-21112b7974a1.png)
# HarmonyOS NEXT系列教程之 TabsRaisedCircleSelect组件实现解析

本文将详细解析TabsRaisedCircleSelect组件的实现，这是一个用于处理选中状态视觉效果的组件。
## 效果演示

![](https://files.mdnice.com/user/47561/c2894823-0343-4de9-a551-e971b3e8daff.gif)
## 1. 组件结构定义

```typescript
@Builder
export function TabsRaisedCircleSelect(TabItemSelectOptions: TabItemSelectType) {
  RelativeContainer() {
    // 选中时凸起的圆
    Column()
      .aspectRatio(1)
      .height(TabItemSelectOptions.chamfer.circleDiameter)
      .borderRadius(TabItemSelectOptions.chamfer.circleRadius)
      .borderWidth(TabItemSelectOptions.chamfer.circleDiameter * 0.1)
      .borderColor(TabItemSelectOptions.tabsBgColor)
      .radialGradient({
        center: [TabItemSelectOptions.chamfer.circleRadius, TabItemSelectOptions.chamfer.circleRadius],
        radius: TabItemSelectOptions.chamfer.circleRadius,
        colors: [[TabItemSelectOptions.tabsSelectBgColor,
          (TabItemSelectOptions.chamfer.circleDiameter - SURPLUSRADIUS) / TabItemSelectOptions.chamfer.circleDiameter],
          [Color.Transparent,
            (TabItemSelectOptions.chamfer.circleDiameter - SURPLUSRADIUS) /
            TabItemSelectOptions.chamfer.circleDiameter]]
      })
      .id(TabItemSelectOptions.selectBodyId)
    
    // 其他过渡效果
  }
}
```

### 组件结构说明：

1. 组件类型：
   - 使用`@Builder`装饰器
   - 接收配置参数

2. 布局容器：
   - 使用`RelativeContainer`
   - 支持相对定位

3. 样式设置：
   - 保持宽高比1:1
   - 设置圆形边框
   - 应用渐变效果

## 2. 渐变效果实现

```typescript
.radialGradient({
  center: [TabItemSelectOptions.chamfer.circleRadius, TabItemSelectOptions.chamfer.circleRadius],
  radius: TabItemSelectOptions.chamfer.circleRadius,
  colors: [[TabItemSelectOptions.tabsSelectBgColor,
    (TabItemSelectOptions.chamfer.circleDiameter - SURPLUSRADIUS) / TabItemSelectOptions.chamfer.circleDiameter],
    [Color.Transparent,
      (TabItemSelectOptions.chamfer.circleDiameter - SURPLUSRADIUS) /
      TabItemSelectOptions.chamfer.circleDiameter]]
})
```

### 渐变效果说明：

1. 渐变中心：
   - 使用圆心坐标
   - 基于圆半径计算

2. 渐变范围：
   - 使用圆半径作为范围
   - 确保覆盖整个区域

3. 颜色配置：
   - 从选中颜色过渡到透明
   - 计算过渡位置

## 3. 过渡效果实现

```typescript
// 左边过渡
Column()
  .width(TabItemSelectOptions.chamfer.chamferXY[0])
  .height(TabItemSelectOptions.chamfer.chamferXY[1])
  .radialGradient({
    center: [0, 0],
    radius: TabItemSelectOptions.chamfer.chamferRadius,
    colors: [[Color.Transparent, 0.0], [Color.Transparent, 1], [TabItemSelectOptions.tabsBgColor, 1]]
  })
  .clipShape(new PathShape({
    commands: `M0 0 L0 ${vp2px(TabItemSelectOptions.chamfer.chamferXY[1])}   
              L${vp2px(TabItemSelectOptions.chamfer.chamferXY[0])} 
              ${vp2px(TabItemSelectOptions.chamfer.chamferXY[1])} Z`
  }))
```

### 过渡效果说明：

1. 尺寸设置：
   - 根据凸起尺寸计算
   - 保持比例一致

2. 渐变配置：
   - 从边缘向内渐变
   - 使用三个颜色节点

3. 裁切形状：
   - 使用PathShape
   - 创建三角形区域

## 4. 位置对齐

```typescript
.alignRules({
  'right': { 'anchor': TabItemSelectOptions.selectBodyId, 'align': HorizontalAlign.Center },
  "bottom": { 'anchor': TabItemSelectOptions.selectBodyId, 'align': VerticalAlign.Center }
})
```

### 对齐规则说明：

1. 水平对齐：
   - 相对选中项居中
   - 使用right规则

2. 垂直对齐：
   - 相对底部对齐
   - 使用bottom规则

3. 锚点设置：
   - 使用选中项ID
   - 确保精确定位

## 5. 整体定位

```typescript
.offset({
  x: -TabItemSelectOptions.chamfer.circleOffsetX,
  y: -TabItemSelectOptions.chamfer.circleOffsetY
})
.zIndex(-1)
.alignRules({
  'left': {
    'anchor': `${TabItemSelectOptions.tabItemId}${TabItemSelectOptions.selectIndex}`,
    'align': HorizontalAlign.Center
  }
})
```

### 定位实现说明：

1. 偏移设置：
   - 计算X轴偏移
   - 计算Y轴偏移

2. 层级管理：
   - 设置zIndex
   - 确保正确的显示顺序

3. 对齐规则：
   - 相对选中项居中
   - 使用left规则

## 总结

TabsRaisedCircleSelect组件通过：
1. 精确的渐变效果
2. 平滑的过渡处理
3. 准确的位置计算
4. 灵活的对齐规则

实现了一个：
- 视觉效果出色
- 过渡自然流畅
- 位置准确
- 易于集成

的选中状态处理组件。
