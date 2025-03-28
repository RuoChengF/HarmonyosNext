> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/765d1c73-a0ba-4230-8cc0-513bc0590378.png)

# HarmonyOS NEXT 日志工具类详解(一)：Logger类基础结构
## 效果演示

![](https://files.mdnice.com/user/47561/515b84cc-bcf8-48d2-97d2-06bc62b51180.jpg)
## 1. Logger类概述

Logger类是一个用于打印日志的工具类，它封装了HarmonyOS的hilog模块，提供了更便捷的日志打印方法。

### 1.1 基本结构

```typescript
class Logger {
  private domain: number;        // 日志域
  private prefix: string;        // 日志前缀
  private format: string;        // 日志格式
}
```

## 2. 类属性详解

### 2.1 domain属性

```typescript
private domain: number = 0xFF00;
```
- 作用：定义日志的域标识
- 取值：0xFF00（十六进制）
- 用途：用于区分不同模块的日志

### 2.2 prefix属性

```typescript
private prefix: string;
```
- 作用：定义日志的前缀标识
- 用途：用于标识日志来源
- 示例：'[CommonAppDevelopment]'

### 2.3 format属性

```typescript
private format: string = '%{public}s, %{public}s';
```
- 作用：定义日志的格式模板
- 说明：'%{public}s'表示公共可见的字符串参数
- 用途：控制日志的输出格式

## 3. 构造函数解析

```typescript
constructor(prefix: string) {
  this.prefix = prefix;
  this.domain = 0xFF00;
  this.format.toUpperCase();
}
```

构造函数的作用：
1. 接收前缀参数并初始化
2. 设置默认的域值
3. 将格式字符串转换为大写

## 4. 使用示例

### 4.1 创建Logger实例

```typescript
export let logger = new Logger('[CommonAppDevelopment]');
```

### 4.2 使用Logger打印日志

```typescript
logger.info('Module name', 'This is an info message');
logger.error('Error type', 'This is an error message');
```

## 5. 知识点总结

1. 私有属性声明
   - 使用private关键字
   - 类型明确声明
   - 初始值设置

2. 构造函数设计
   - 参数验证
   - 属性初始化
   - 格式处理

3. 模块导出
   - 单例模式
   - 统一导出
   - 全局可用

## 6. 最佳实践建议

1. 日志级别使用
   - debug：开发调试信息
   - info：普通信息
   - warn：警告信息
   - error：错误信息

2. 日志前缀规范
   - 使用方括号[]
   - 简明扼要
   - 模块标识清晰

3. 日志内容规范
   - 信息完整
   - 简洁明了
   - 便于定位问题

通过以上详细讲解，你应该能够理解Logger类的基本结构和使用方法。这个类为应用提供了统一的日志打印接口，便于调试和问题定位。
