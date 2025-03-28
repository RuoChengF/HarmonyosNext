> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/b1ff4b28-98f6-477c-b870-ec8d17df4697.png)

# HarmonyOS NEXT 跑马灯组件数据类型详解：理解数据结构
## 效果演示

![](https://files.mdnice.com/user/47561/515b84cc-bcf8-48d2-97d2-06bc62b51180.jpg)
## 1. 数据类型概述

在跑马灯组件中，定义了三个主要的数据类型：
- TripDataType：行程信息接口
- MarqueeAnimationModifier：动画属性类
- MarqueeScrollModifier：滚动属性类

## 2. 行程信息接口（TripDataType）

```typescript
export interface TripDataType {
  id: number;                    // 唯一标识
  trainNumber: string;           // 列车号
  wholeCourse: ResourceStr;      // 全程
  startingTime: string;         // 起始时间
  endingTime: string;           // 终止时间
  timeDifference: ResourceStr;   // 距出发时间
  origin: ResourceStr;          // 起始位置
  destination: ResourceStr;     // 目的地
  ticketEntrance: ResourceStr;  // 检票口
  vehicleModel: ResourceStr;    // 车型
}
```

### 2.1 属性说明

- `id`：数字类型，用于唯一标识每条行程信息
- `trainNumber`：字符串类型，表示列车编号
- `wholeCourse`：资源字符串类型，表示完整行程
- `startingTime`和`endingTime`：字符串类型，表示发车和到达时间
- `timeDifference`：资源字符串类型，表示距离发车的时间
- `origin`和`destination`：资源字符串类型，表示起点和终点
- `ticketEntrance`：资源字符串类型，表示检票口信息
- `vehicleModel`：资源字符串类型，表示车辆型号

### 2.2 ResourceStr类型说明

ResourceStr是HarmonyOS中的资源引用类型，用于支持多语言和资源管理：
```typescript
// 使用示例
wholeCourse: $r('app.string.marquee_whole_course_data_1')
```

## 3. 动画属性类（MarqueeAnimationModifier）

```typescript
export class MarqueeAnimationModifier {
  iterations: number;    // 动画播放次数
  duration: number;      // 动画持续时间
  tempo: number;        // 动画播放速度
  playMode: PlayMode;   // 播放模式
  delayTime: number;    // 延迟时间

  constructor(
    iterations: number = -1,
    duration: number = Constants.ANIMATION_DURATION,
    tempo: number = 1,
    playMode: PlayMode = PlayMode.Normal,
    delayTime: number = Constants.DELAY_TIME
  ) {
    // 构造函数实现
  }
}
```

### 3.1 属性详解

- `iterations`：
  - -1：无限循环
  - 0：无动画效果
  - 正数：指定播放次数

- `duration`：动画持续时间（毫秒）
- `tempo`：播放速度系数
  - >1：加速
  - <1：减速
  - 0：停止

- `playMode`：播放方向
  - Normal：正常方向
  - Reverse：反向播放

- `delayTime`：动画开始前的延迟时间

## 4. 滚动属性类（MarqueeScrollModifier）

```typescript
export class MarqueeScrollModifier {
  scrollWidth: Length;   // 滚动区域宽度
  space: number;        // 文本间隔

  constructor(
    scrollWidth: Length = Constants.DEFAULT_SCROLL_WIDTH,
    space: number = Constants.BLANK_SPACE
  ) {
    this.scrollWidth = scrollWidth;
    this.space = space;
  }
}
```

### 4.1 属性说明

- `scrollWidth`：
  - 类型：Length（可以是具体数值或百分比）
  - 默认值：'25%'
  - 用途：定义滚动区域的宽度

- `space`：
  - 类型：number
  - 默认值：50
  - 用途：定义文本之间的间隔距离

## 5. 使用示例

### 5.1 创建行程数据

```typescript
const tripData: TripDataType = {
  id: 1,
  trainNumber: "G101",
  wholeCourse: $r('app.string.course_beijing_shanghai'),
  startingTime: "09:00",
  endingTime: "14:00",
  timeDifference: $r('app.string.time_1_hour'),
  origin: $r('app.string.beijing'),
  destination: $r('app.string.shanghai'),
  ticketEntrance: $r('app.string.gate_a1'),
  vehicleModel: $r('app.string.high_speed')
};
```

### 5.2 配置动画属性

```typescript
const animation = new MarqueeAnimationModifier(
  -1,                    // 无限循环
  10000,                // 10秒一次循环
  1.5,                  // 1.5倍速
  PlayMode.Normal,      // 正常方向
  1000                  // 延迟1秒
);
```

### 5.3 配置滚动属性

```typescript
const scroll = new MarqueeScrollModifier(
  '30%',    // 滚动区域宽度为容器的30%
  60        // 文本间隔60单位
);
```

## 6. 最佳实践

1. 类型检查
```typescript
function isValidTripData(data: any): data is TripDataType {
  return data 
    && typeof data.id === 'number'
    && typeof data.trainNumber === 'string'
    // ... 其他属性检查
}
```

2. 默认值处理
```typescript
const defaultAnimation = new MarqueeAnimationModifier();
const defaultScroll = new MarqueeScrollModifier();
```

3. 参数验证
```typescript
if (tempo <= 0) {
  console.warn('Animation tempo should be greater than 0');
  tempo = 1;
}
```

## 7. 小结

这些数据类型定义：
- 提供了清晰的数据结构
- 支持类型检查
- 包含默认值处理
- 便于代码维护和扩展

通过合理使用这些数据类型，可以：
- 提高代码的可读性
- 减少运行时错误
- 便于后期维护
- 提供更好的开发体验
