> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](../images/img_ebd152fa.png)
# HarmonyOS NEXT系列教程之 TabBar工具函数与Canvas绘制实现解析

本文将详细解析TabBar中的工具函数和Canvas绘制实现，包括图片处理、尺寸计算和Canvas绘制等核心功能。
## 效果演示

![](../images/img_e3a9fa89.png)
## 1. 图片资源处理

```typescript
export function getImageUrl(item: TabMenusInterfaceIRequired, index: number,
  selectIndex: number): PixelMap | ResourceStr | DrawableDescriptor {
  if (index === selectIndex) {
    if (item.selectImage) {
      return item.selectImage;
    }
  }
  return item.image!;
}
```

### 图片处理说明：
1. 参数解析：
   - `item`: 菜单项配置
   - `index`: 当前项索引
   - `selectIndex`: 选中项索引

2. 图片选择逻辑：
   - 判断是否选中状态
   - 检查是否有选中态图片
   - 返回适当的图片资源

3. 返回类型：
   - `PixelMap`: 像素图
   - `ResourceStr`: 资源字符串
   - `DrawableDescriptor`: 可绘制描述符

## 2. 尺寸计算工具

```typescript
export function getMinWidth(width: number, height: number, menuLength: number = 0): number {
  return Math.min(width / menuLength, height);
}

export function getChamferXY(itemHeight: number, r: number = 30): [number, number] {
  let topH = itemHeight / 3;
  let center = itemHeight / 2;
  let cenToTop = center - topH;
  let chamferY = cenToTop + r;
  let sr = r + center;
  let chamferX = Math.sqrt(Math.pow(sr, 2) - Math.pow(chamferY, 2));
  return [chamferX, chamferY];
}
```

### 计算工具说明：
1. `getMinWidth`函数：
   - 计算最小兼容宽度
   - 考虑菜单数量
   - 确保合适的显示比例

2. `getChamferXY`函数：
   - 计算倒角坐标
   - 使用数学公式
   - 返回[x,y]坐标对

3. 数学计算：
   - 使用三角函数
   - 精确计算位置
   - 确保视觉效果

## 3. Canvas矩形绘制

```typescript
export function CanvasCreateRectangle(canvasInfo: CanvasCreateRectangleType) {
  let ctx = canvasInfo.context;
  let cW = canvasInfo.context.width;
  let cH = canvasInfo.context.height;

  ctx.clearRect(0, 0, cW, cH);
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(cW, 0);
  ctx.lineTo(cW, cH);
  ctx.lineTo(0, cH);
  ctx.closePath();
  ctx.fillStyle = canvasInfo.tabsBgColor;
  ctx.fill();
  ctx.closePath();
}
```

### Canvas绘制流程：
1. 准备工作：
   - 获取上下文
   - 获取画布尺寸
   - 清除旧内容

2. 路径绘制：
   - 开始新路径
   - 绘制四个顶点
   - 闭合路径

3. 样式设置：
   - 设置填充颜色
   - 执行填充
   - 完成绘制

## 4. Canvas凹槽效果

```typescript
export function CanvasClipGroove(canvasInfo: CanvasClipGrooveType) {
  let ctx = canvasInfo.context;
  let cW = ctx.width;
  let cH = ctx.height;
  let radius = getMinWidth(cW, cH, canvasInfo.menuLength) / 2;
  let Center = canvasInfo.center || cW / 2;
  let aroundCenter = Math.sqrt(Math.pow(radius * 2, 2) - Math.pow(radius, 2));

  const chamferDegrees1 = Math.PI / 180;
  const chamferDegrees330 = chamferDegrees1 * 330;
  const chamferDegrees270 = chamferDegrees1 * 270;
  const chamferDegrees210 = chamferDegrees1 * 210;
  const chamferDegrees150 = chamferDegrees1 * 150;
  const chamferDegrees30 = chamferDegrees1 * 30;

  ctx.beginPath();
  ctx.arc(Center - aroundCenter, radius, radius, chamferDegrees270, chamferDegrees330);
  ctx.arc(Center, 0, radius, chamferDegrees30, chamferDegrees150);
  ctx.arc(Center + aroundCenter, radius, radius, chamferDegrees210, chamferDegrees270);
  ctx.closePath();
  ctx.clip();
  ctx.clearRect(0, 0, cW, cH);
}
```

### 凹槽实现说明：
1. 参数计算：
   - 计算半径
   - 确定中心点
   - 计算辅助参数

2. 角度定义：
   - 定义关键角度
   - 使用弧度制
   - 确保圆滑过渡

3. 路径绘制：
   - 绘制左侧圆弧
   - 绘制中间圆弧
   - 绘制右侧圆弧

4. 剪裁处理：
   - 应用剪裁路径
   - 清除剪裁区域
   - 完成凹槽效果

## 总结

工具函数和Canvas绘制通过：
1. 精确的数学计算
2. 清晰的绘制流程
3. 优雅的函数封装
4. 灵活的参数配置

实现了：
- 准确的图片处理
- 精确的尺寸计算
- 平滑的视觉效果
- 高效的Canvas渲染

这些实现为TabBar提供了强大的底层支持，确保了组件的视觉效果和性能表现。
