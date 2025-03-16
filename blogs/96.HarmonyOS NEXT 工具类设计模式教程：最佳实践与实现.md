 
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/5d0746f9-f5aa-4cf2-9d5f-204947b67238.png)

# HarmonyOS NEXT工具类设计模式教程：最佳实践与实现

## 1. 工具类设计原则

### 1.1 基本原则

| 原则 | 说明 | 示例 |
|------|------|------|
| 单一职责 | 每个类只负责一个功能 | WindowSizeManager只管理窗口尺寸 |
| 高内聚 | 相关功能集中在一起 | FuncUtils集中处理动画和旋转 |
| 低耦合 | 减少类之间的依赖 | Constrain独立处理图片约束 |

### 1.2 代码组织

```typescript
// 相关功能集中在一个文件中
// FuncUtils.ets
export function runWithAnimation(...) { ... }
export function simplestRotationQuarter(...) { ... }

// 单一职责示例
// WindowSizeManager.ets
class WindowSizeManager {
    private size: window.Size;
    // 只处理窗口尺寸相关功能
}
```

## 2. 单例模式实现

### 2.1 基本实现

```typescript
// 经典单例模式
class WindowSizeManager {
    private static instance: WindowSizeManager;
    private size: window.Size = { width: 0, height: 0 };
    
    private constructor() {
        // 私有构造函数
    }
    
    static getInstance(): WindowSizeManager {
        if (!this.instance) {
            this.instance = new WindowSizeManager();
        }
        return this.instance;
    }
}
```

### 2.2 导出单例

```typescript
// 直接导出实例
export const windowSizeManager = new WindowSizeManager();

// 使用示例
const size = windowSizeManager.get();
```

## 3. 工具函数设计

### 3.1 函数设计原则

1. **参数设计**
```typescript
// 使用默认参数
export function runWithAnimation(
    fn: Function,
    duration: number = DEFAULT_DURATION,
    curve: Curve = Curve.Smooth
) { ... }

// 使用接口定义复杂参数
interface AnimationOptions {
    duration?: number;
    curve?: Curve;
    delay?: number;
}
```

2. **返回值设计**
```typescript
// 返回元组表示多个结果
function constrainOffsetAndAnimation(
    info: ConstrainOffsetAndAnimationType
): [boolean, boolean] { ... }

// 使用类型别名简化复杂返回值
type ConstrainResult = {
    exceeded: boolean;
    direction: 'left' | 'right';
};
```

### 3.2 错误处理

```typescript
// 统一的错误处理
function safeExecute<T>(
    operation: () => T,
    fallback: T,
    errorMessage: string
): T {
    try {
        return operation();
    } catch (error) {
        console.error(errorMessage, error);
        return fallback;
    }
}

// 使用示例
const size = safeExecute(
    () => windowSizeManager.get(),
    { width: 0, height: 0 },
    'Failed to get window size'
);
```

## 4. 接口设计

### 4.1 类型定义

```typescript
// 明确的类型定义
export interface ConstrainOffsetAndAnimationType {
    dimensionWH: ImageFitType;
    imageDefaultSize: image.Size;
    imageOffsetInfo: OffsetModel;
    scaleValue: number;
    rotate: number;
    TogglePercent: number;
    imageListOffset: number;
    listDirection: Axis;
}

// 枚举类型
export enum ImageFitType {
    TYPE_WIDTH = 'width',
    TYPE_HEIGHT = 'height',
    TYPE_DEFAULT = 'default'
}
```

### 4.2 接口使用

```typescript
// 实现接口
class ImageConstrainer implements ImageConstrainer {
    constrainOffset(info: ConstrainOffsetAndAnimationType): [boolean, boolean] {
        return constrainOffsetAndAnimation(info);
    }
}

// 使用接口
function processImage(constrainer: ImageConstrainer) {
    const result = constrainer.constrainOffset({...});
}
```

## 5. 实践应用

### 5.1 组合使用示例

```typescript
// 图片查看器组件
@Component
struct ImageViewer {
    // 使用工具类
    private sizeManager = windowSizeManager;
    
    build() {
        Stack() {
            Image(this.source)
                .width(this.sizeManager.get().width)
                .height(this.sizeManager.get().height)
                .onTouch((event: TouchEvent) => {
                    // 处理触摸事件
                    this.handleImageTouch(event);
                })
        }
    }
    
    private handleImageTouch(event: TouchEvent) {
        // 使用工具函数处理动画
        runWithAnimation(() => {
            // 计算约束
            const [exceeded, direction] = constrainOffsetAndAnimation({
                // 配置参数
            });
            
            // 处理结果
            if (exceeded) {
                this.handleExceeded(direction);
            }
        });
    }
}
```

### 5.2 性能优化

```typescript
// 缓存计算结果
class CachedCalculator {
    private cache = new Map<string, any>();
    
    calculate(key: string, computer: () => any): any {
        if (!this.cache.has(key)) {
            this.cache.set(key, computer());
        }
        return this.cache.get(key);
    }
    
    clearCache(): void {
        this.cache.clear();
    }
}

// 使用示例
const calculator = new CachedCalculator();
const maxOffset = calculator.calculate(
    `offset_${winSize}_${imageSize}_${scale}`,
    () => getMaxAllowedOffset(winSize, imageSize, scale)
);
```

## 6. 测试与维护

### 6.1 单元测试

```typescript
// 工具函数测试
describe('WindowSizeManager', () => {
    it('should return correct window size', () => {
        const size = windowSizeManager.get();
        expect(size.width).toBeGreaterThan(0);
        expect(size.height).toBeGreaterThan(0);
    });
});

// 约束函数测试
describe('constrainOffset', () => {
    it('should constrain offset within bounds', () => {
        const result = constrainOffset(100, 50, 200, 1);
        expect(result).toBeLessThanOrEqual(75);
    });
});
```

### 6.2 文档维护

```typescript
/**
 * 运行带动画的函数
 * @param fn 要执行的函数
 * @param duration 动画持续时间（毫秒）
 * @param curve 动画曲线
 */
export function runWithAnimation(
    fn: Function,
    duration: number = DEFAULT_DURATION,
    curve: Curve = Curve.Smooth
): void {
    // 实现...
}
```

通过合理的工具类设计，可以提高代码的可维护性和复用性。在实际开发中，要注意遵循设计原则，做好错误处理和性能优化，确保工具类的可靠性和效率。
