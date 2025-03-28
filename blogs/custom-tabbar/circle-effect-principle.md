> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/e7866215-2919-4450-90eb-21112b7974a1.png)
# HarmonyOS NEXT系列教程之 CircleClass基础类与圆形效果实现原理解析

本文将详细解析CircleClass基础类及其子类的实现原理，这些类是实现TabBar圆形效果的核心。
## 效果演示

![](https://files.mdnice.com/user/47561/c2894823-0343-4de9-a551-e971b3e8daff.gif)
## 1. CircleClass基础类实现

```typescript
@Observed
class CircleClass {
  @Track
  width: number;
  @Track
  height: number;
  @Track
  menuLength: number = 0;

  constructor(options: CircleClassConstructorType) {
    this.width = options.width;
    this.height = options.height;
    this.menuLength = options.menuLength;
  }
}
```

### 核心属性说明：
1. `@Observed`装饰器：
   - 标记类为可观察对象
   - 支持属性变化监听
   - 用于状态管理

2. `@Track`装饰器：
   - 标记属性为可追踪
   - 属性变化时触发更新
   - 实现响应式更新

3. 基础属性：
   - `width`: 组件宽度
   - `height`: 组件高度
   - `menuLength`: 菜单项数量

## 2. 核心方法实现

```typescript
getMinWidth(): number {
  return utilGetMinWidth(this.width, this.height, this.menuLength);
}

getMenuCenterX(index: number): number {
  let itemWidth = this.width / this.menuLength;
  let basicsX = itemWidth * index;
  let centerWidth = itemWidth / 2;
  return basicsX + centerWidth;
}
```

### 方法解析：
1. `getMinWidth()`：
   - 计算兼容性宽度
   - 确保圆形效果的适配性
   - 返回最小宽度值

2. `getMenuCenterX()`：
   - 计算菜单项中心点位置
   - 参数`index`：当前菜单项索引
   - 返回X轴坐标位置

## 3. ConcaveCircle凹陷效果实现

```typescript
@Observed
export class ConcaveCircle extends CircleClass {
  @Track
  positionX: number = 0;
  @Track
  positionY: number = 0;
  oldPositionX: number = 0;
  oldPositionY: number = 0;
  @Track
  circleRadius: number = 0;
  @Track
  circleDiameter: number = 0;

  constructor(context: CanvasRenderingContext2D, menuLength: number) {
    super({
      width: context.width,
      height: context.height,
      menuLength: menuLength
    });
    this.initCircleRadius();
    this.resetXY();
  }
}
```

### 凹陷效果关键点：
1. 位置管理：
   - `positionX/Y`: 当前位置
   - `oldPositionX/Y`: 上一次位置
   - 用于动画过渡效果

2. 圆形参数：
   - `circleRadius`: 圆形半径
   - `circleDiameter`: 圆形直径
   - 控制凹陷大小

3. 初始化流程：
   ```typescript
   initCircleRadius(): void {
     this.circleRadius = this.getMinWidth() / 2 - SURPLUSRADIUS;
     this.circleDiameter = this.circleRadius * 2;
   }

   resetXY(): void {
     this.positionY = -this.circleRadius;
     this.positionX = this.getAutoPositionX(0);
     this.oldPositionX = 0;
     this.oldPositionY = 0;
   }
   ```
   - 计算圆形尺寸
   - 设置初始位置
   - 重置位置记录

## 4. 位置计算与更新

```typescript
getAutoPositionX(index: number): number {
  return this.getMenuCenterX(index) - this.circleRadius;
}

setPositionXY(position: RaisedCircleSetPostionXYType): void {
  if (position.x || position.x === 0) {
    this.oldPositionX = this.positionX;
    this.positionX = position.x;
  }
  if (position.y || position.y === 0) {
    this.oldPositionY = this.positionY;
    this.positionY = position.y;
  }
}
```

### 位置处理说明：
1. 自动定位：
   - 根据索引计算位置
   - 考虑圆形半径偏移
   - 确保居中显示

2. 位置更新：
   - 记录旧位置
   - 更新新位置
   - 支持单轴更新

## 总结

CircleClass及其子类通过：
1. 响应式状态管理
2. 精确的位置计算
3. 完善的参数配置
4. 灵活的更新机制

实现了：
- 准确的圆形效果
- 流畅的动画过渡
- 精确的位置控制
- 良好的扩展性

这些类为TabBar的圆形效果提供了坚实的基础实现。
