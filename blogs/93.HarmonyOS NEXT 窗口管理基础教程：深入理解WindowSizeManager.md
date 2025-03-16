 
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/24135a73-3d2b-480c-a7ae-587b4a4e1bc9.png)

# HarmonyOS NEXT窗口管理基础教程：深入理解WindowSizeManager

## 1. 窗口管理概述

### 1.1 基本概念

| 概念 | 说明 | 使用场景 |
|------|------|----------|
| 窗口尺寸 | 应用窗口的宽高信息 | 布局计算、UI适配 |
| 物理像素 | 设备实际像素点 | 设备显示 |
| 视口像素 | 逻辑显示单位 | UI开发 |

### 1.2 WindowSizeManager类解析

```typescript
class WindowSizeManager {
  // 存储窗口尺寸信息
  private size: window.Size = { width: 0, height: 0 };
 
  constructor() {
    // 获取当前窗口实例
    window.getLastWindow(getContext()).then((value: window.Window) => {
      // 获取窗口属性中的矩形信息
      const rect: window.Rect = value.getWindowProperties().windowRect;
      // 转换物理像素到视口像素
      this.size.width = px2vp(rect.width);
      this.size.height = px2vp(rect.height);
      console.log(`[windowWidth]${this.size.width} [windowHeight]${this.size.height}`);
    })
  }

  // 获取窗口尺寸
  get(): window.Size {
    return this.size;
  }
}
```

## 2. 核心功能解析

### 2.1 单例模式实现

```typescript
// 导出单例实例
export const windowSizeManager: WindowSizeManager = new WindowSizeManager();
```

**为什么使用单例模式？**
1. 确保全局只有一个窗口管理器实例
2. 避免重复创建和资源浪费
3. 提供统一的访问点

### 2.2 异步窗口获取

```typescript
window.getLastWindow(getContext()).then((value: window.Window) => {
  // 处理窗口信息
})
```

**异步操作的必要性：**
1. 窗口信息可能不会立即可用
2. 避免阻塞主线程
3. 确保数据准确性

### 2.3 像素转换

```typescript
this.size.width = px2vp(rect.width);
this.size.height = px2vp(rect.height);
```

**px2vp转换的重要性：**
1. 物理像素到视口像素的转换
2. 确保跨设备显示一致性
3. 适应不同屏幕密度

## 3. 实践应用

### 3.1 基本使用方式

```typescript
// 获取窗口尺寸
const windowSize = windowSizeManager.get();
console.log(`Window size: ${windowSize.width} x ${windowSize.height}`);
```

### 3.2 常见应用场景

| 场景 | 使用方式 | 示例代码 |
|------|----------|----------|
| 布局计算 | 获取可用空间 | `const availableWidth = windowSize.width;` |
| 居中定位 | 计算居中坐标 | `const centerX = windowSize.width / 2;` |
| 响应式布局 | 根据窗口大小调整 | `if (windowSize.width > 600) { ... }` |

## 4. 最佳实践

### 4.1 初始化时机

```typescript
// 推荐在组件初始化时获取窗口尺寸
aboutToAppear() {
  const size = windowSizeManager.get();
  // 使用窗口尺寸进行初始化
}
```

### 4.2 监听变化

```typescript
// 在需要响应窗口变化的地方
onWindowResize(size: window.Size) {
  // 更新布局或其他处理
}
```

### 4.3 错误处理

```typescript
try {
  const size = windowSizeManager.get();
  // 使用尺寸信息
} catch (error) {
  console.error('Failed to get window size:', error);
  // 使用默认值或错误处理
}
```

## 5. 注意事项

1. **初始化时序**
   - 确保在使用前完成初始化
   - 处理初始值为0的情况
   - 考虑异步加载的影响

2. **性能考虑**
   - 避免频繁获取窗口尺寸
   - 缓存计算结果
   - 合理使用防抖/节流

3. **兼容性处理**
   - 考虑不同设备的差异
   - 处理异常情况
   - 提供降级方案

## 6. 调试技巧

1. **日志输出**
```typescript
console.log(`Window size updated: ${this.size.width} x ${this.size.height}`);
```

2. **断点调试**
- 在尺寸更新处设置断点
- 监控异步操作完成
- 检查转换结果

3. **错误排查**
- 检查Context是否正确
- 验证异步操作结果
- 确认像素转换准确性

通过合理使用WindowSizeManager，可以有效管理应用的窗口尺寸信息，为UI布局和适配提供可靠的基础。在实际开发中，要注意异步操作和像素转换的处理，确保应用在不同设备上都能正常显示。
