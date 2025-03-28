> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](../images/img_ebd152fa.png)
# HarmonyOS NEXT系列教程之列表切换案例数据管理详解
## 效果演示

![](../images/img_f8c8cab3.png)
## 1. 数据模型设计

### 1.1 ListInfo类
```typescript
@Observed
export class ListInfo {
    // 列表项数据结构
    icon: ResourceStr = '';    // 图标资源
    name: ResourceStr = '';    // 显示名称

    constructor(icon: ResourceStr = '', name: ResourceStr = '') {
        this.icon = icon;
        this.name = name;
    }
}
```

关键点解析：
1. @Observed装饰器：使类变成可观察对象，当属性变化时自动触发UI更新
2. ResourceStr类型：使用资源引用而不是直接字符串，支持多语言
3. 构造函数：提供默认值，方便创建实例

### 1.2 模拟数据
```typescript
// Mock数据示例
export const MEMO_DATA: ListInfo[] = [
    new ListInfo($r("app.media.list_exchange_ic_public_cards_filled"), '账户余额'),
    new ListInfo($r("app.media.list_exchange_ic_public_cards_filled2"), 'xx银行储蓄卡（1234）'),
    // ...更多数据
];
```

## 2. 状态控制器

### 2.1 ListExchangeCtrl类
```typescript
@Observed
export class ListExchangeCtrl<T> {
    // 内部状态
    private deductionData: Array<T> = [];      // 列表数据
    private modifier: Array<ListItemModifier> = []; // 属性修改器
    private dragRefOffset: number = 0;          // 拖拽参考偏移量
    
    // 公开状态
    offsetY: number = 0;                       // 当前偏移量
    state: OperationStatus = OperationStatus.IDLE; // 操作状态
}
```

关键点解析：
1. 泛型设计：支持不同类型的列表项
2. 状态管理：维护列表数据和UI状态
3. 修改器数组：每个列表项对应一个修改器

### 2.2 操作状态枚举
```typescript
enum OperationStatus {
    IDLE,       // 空闲状态
    PRESSING,   // 长按状态
    MOVING,     // 移动状态
    DROPPING,   // 放置状态
    DELETE      // 删除状态
}
```

## 3. 数据操作实现

### 3.1 初始化数据
```typescript
initData(deductionData: Array<T>) {
    // 设置列表数据
    this.deductionData = deductionData;
    // 为每个列表项创建修改器
    deductionData.forEach(() => {
        this.modifier.push(new ListItemModifier());
    })
}
```

### 3.2 数据交换
```typescript
changeItem(index: number, newIndex: number): void {
    // 交换数据
    const tmp: Array<T> = this.deductionData.splice(index, 1);
    this.deductionData.splice(newIndex, 0, tmp[0]);
    
    // 交换修改器
    const tmp2: Array<ListItemModifier> = this.modifier.splice(index, 1);
    this.modifier.splice(newIndex, 0, tmp2[0]);
}
```

## 4. 属性修改器

### 4.1 ListItemModifier类
```typescript
export class ListItemModifier implements AttributeModifier<ListItemAttribute> {
    // UI属性
    public hasShadow: boolean = false;  // 阴影效果
    public scale: number = 1;           // 缩放比例
    public offsetY: number = 0;         // 垂直偏移
    public offsetX: number = 0;         // 水平偏移
    public opacity: number = 1;         // 透明度
    public isDeleted: boolean = false;  // 删除状态
}
```

### 4.2 属性应用
```typescript
applyNormalAttribute(instance: ListItemAttribute): void {
    // 应用阴影效果
    if (this.hasShadow) {
        instance.shadow({
            radius: $r('app.integer.list_exchange_shadow_radius'),
            color: $r('app.color.list_exchange_box_shadow')
        });
        instance.zIndex(1);
        instance.opacity(0.5);
    } else {
        instance.opacity(this.opacity);
    }

    // 应用变换
    instance.translate({ x: this.offsetX, y: this.offsetY });
    instance.scale({ x: this.scale, y: this.scale });
}
```

## 5. 状态同步机制

### 5.1 数据绑定
```typescript
@Component
export struct ListExchangeViewComponent {
    // 数据绑定
    @State appInfoList: ListInfo[] = MEMO_DATA;
    @State listExchangeCtrl: ListExchangeCtrl<ListInfo>;

    // 初始化
    aboutToAppear(): void {
        this.listExchangeCtrl.initData(this.appInfoList);
    }
}
```

### 5.2 状态更新
```typescript
// 删除操作
deleteItem(item: T): void {
    try {
        const index: number = this.deductionData.indexOf(item);
        // 更新状态
        this.state = OperationStatus.DELETE;
        // 更新UI属性
        this.modifier[index].offsetX = 150;
        this.modifier[index].opacity = 0;
        // 删除数据
        this.modifier.splice(index, 1);
        this.deductionData.splice(index, 1);
    } catch (err) {
        console.error(`delete err:${JSON.stringify(err)}`);
    }
}
```

## 6. 性能优化

### 6.1 数据处理优化
```typescript
// 使用索引优化查找
getModifier(item: T): ListItemModifier {
    const index: number = this.deductionData.indexOf(item);
    return this.modifier[index];
}

// 批量更新处理
private batchUpdate(updates: Array<() => void>): void {
    updates.forEach(update => update());
}
```

### 6.2 状态管理优化
1. 使用@Observed减少不必要的更新
2. 合理使用状态枚举控制流程
3. 优化数据结构提高性能
4. 实现错误处理机制

## 7. 小结

本篇教程详细介绍了：
1. 数据模型的设计实现
2. 状态控制器的工作机制
3. 属性修改器的使用方法
4. 状态同步的实现方案
5. 性能优化的策略

这些内容帮助你理解列表切换案例的数据管理机制。下一篇将详细介绍列表交互和手势处理的实现。
