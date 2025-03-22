> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！


![](https://files.mdnice.com/user/47561/43fb25b6-24ac-4afa-939f-920df777c44d.png)

# HarmonyOS NEXT跑马灯组件教程：Logger日志工具详解

## 效果演示

![](https://files.mdnice.com/user/47561/515b84cc-bcf8-48d2-97d2-06bc62b51180.jpg)

## 1. Logger工具概述

在HarmonyOS NEXT跑马灯组件的实现中，Logger工具类扮演着重要的角色，它负责记录组件运行过程中的各种日志信息，帮助开发者调试和排查问题。本文将详细介绍Logger工具类的实现和使用方法。

### 1.1 Logger工具的作用

Logger工具主要有以下作用：

1. **记录调试信息**：记录组件运行过程中的调试信息，帮助开发者了解组件的运行状态
2. **错误追踪**：记录错误和异常信息，帮助开发者定位和解决问题
3. **性能监控**：记录组件的性能相关信息，帮助开发者优化组件性能

### 1.2 Logger工具的位置

Logger工具类定义在utils/marquee/Logger.ets文件中，是跑马灯组件工具层的一部分。

## 2. Logger类详解

### 2.1 类定义

Logger类的定义如下：

```typescript
import hilog from '@ohos.hilog';

/**
 * 日志打印类
 */
class Logger {
  private domain: number;
  private prefix: string;
  private format: string = '%{public}s, %{public}s';

  constructor(prefix: string) {
    this.prefix = prefix;
    this.domain = 0xFF00;
    this.format.toUpperCase();
  }

  debug(...args: string[]) {
    hilog.debug(this.domain, this.prefix, this.format, args);
  }

  info(...args: string[]) {
    hilog.info(this.domain, this.prefix, this.format, args);
  }

  warn(...args: string[]) {
    hilog.warn(this.domain, this.prefix, this.format, args);
  }

  error(...args: string[]) {
    hilog.error(this.domain, this.prefix, this.format, args);
  }
}

export let logger = new Logger('[CommonAppDevelopment]')
```

### 2.2 属性详解

| 属性名 | 类型 | 说明 | 默认值 |
|------|------|------|------|
| domain | number | 日志域，用于标识日志来源 | 0xFF00 |
| prefix | string | 日志前缀，用于标识日志模块 | 构造函数传入 |
| format | string | 日志格式，定义日志内容的格式 | '%{public}s, %{public}s' |

#### 2.2.1 domain属性

domain属性是一个数字，用于标识日志的来源域。在HarmonyOS中，不同的应用或模块可以使用不同的domain值，便于日志的过滤和查询。在Logger类中，domain值设置为0xFF00。

#### 2.2.2 prefix属性

prefix属性是一个字符串，用于标识日志的模块。在Logger类的构造函数中，需要传入一个prefix参数，用于设置日志前缀。在跑马灯组件中，prefix值设置为'[CommonAppDevelopment]'。

#### 2.2.3 format属性

format属性是一个字符串，用于定义日志内容的格式。在Logger类中，format值设置为'%{public}s, %{public}s'，表示日志内容包含两个公开的字符串参数。

### 2.3 方法详解

| 方法名 | 参数 | 返回值 | 说明 |
|------|------|------|------|
| constructor | prefix: string | 无 | 构造函数，初始化Logger实例 |
| debug | ...args: string[] | 无 | 记录调试级别的日志 |
| info | ...args: string[] | 无 | 记录信息级别的日志 |
| warn | ...args: string[] | 无 | 记录警告级别的日志 |
| error | ...args: string[] | 无 | 记录错误级别的日志 |

#### 2.3.1 constructor方法

constructor方法是Logger类的构造函数，用于初始化Logger实例：

```typescript
constructor(prefix: string) {
  this.prefix = prefix;
  this.domain = 0xFF00;
  this.format.toUpperCase();
}
```

这个方法接受一个prefix参数，用于设置日志前缀，同时初始化domain属性和format属性。

#### 2.3.2 日志记录方法

Logger类提供了四个日志记录方法，分别对应不同的日志级别：

```typescript
debug(...args: string[]) {
  hilog.debug(this.domain, this.prefix, this.format, args);
}

info(...args: string[]) {
  hilog.info(this.domain, this.prefix, this.format, args);
}

warn(...args: string[]) {
  hilog.warn(this.domain, this.prefix, this.format, args);
}

error(...args: string[]) {
  hilog.error(this.domain, this.prefix, this.format, args);
}
```

这些方法都接受可变数量的字符串参数，并调用hilog模块的相应方法记录日志。

### 2.4 导出实例

Logger.ets文件最后导出了一个Logger实例：

```typescript
export let logger = new Logger('[CommonAppDevelopment]')
```

这个实例使用'[CommonAppDevelopment]'作为前缀，可以在跑马灯组件的其他文件中直接导入和使用。

## 3. hilog模块

### 3.1 hilog模块概述

Logger类内部使用了HarmonyOS提供的hilog模块，这是一个用于记录日志的系统模块。hilog模块提供了不同级别的日志记录方法，如debug、info、warn、error等。

```typescript
import hilog from '@ohos.hilog';
```

### 3.2 hilog方法参数

hilog模块的日志记录方法接受以下参数：

1. **domain**：日志域，用于标识日志来源
2. **tag**：日志标签，用于标识日志模块
3. **format**：日志格式，定义日志内容的格式
4. **args**：日志参数，根据format格式填充日志内容

```typescript
hilog.debug(this.domain, this.prefix, this.format, args);
```

### 3.3 日志级别

hilog模块支持不同级别的日志：

| 级别 | 方法 | 说明 |
|------|------|------|
| DEBUG | hilog.debug | 调试级别，用于记录详细的调试信息 |
| INFO | hilog.info | 信息级别，用于记录一般的信息 |
| WARN | hilog.warn | 警告级别，用于记录可能的问题 |
| ERROR | hilog.error | 错误级别，用于记录错误和异常 |
| FATAL | hilog.fatal | 致命级别，用于记录严重错误 |

## 4. 在跑马灯组件中使用Logger

### 4.1 导入Logger

在跑马灯组件的其他文件中，可以通过以下方式导入Logger：

```typescript
import { logger } from './Logger';
```

### 4.2 记录日志

导入Logger后，可以使用不同级别的方法记录日志：

```typescript
// 记录调试信息
logger.debug('MarqueeSection', 'scrollAnimation called');

// 记录一般信息
logger.info('MarqueeSection', `TextArea oldValue:${JSON.stringify(oldValue)},newValue:${JSON.stringify(newValue)}`);

// 记录警告信息
logger.warn('MarqueeSection', 'Text width is too large');

// 记录错误信息
logger.error('MarqueeSection', 'Failed to get component size');
```

### 4.3 实际应用示例

在MarqueeSection组件中，Logger被用于记录文本区域变化的信息：

```typescript
.onAreaChange((oldValue, newValue) => {
  logger.info(`TextArea oldValue:${JSON.stringify(oldValue)},newValue:${JSON.stringify(newValue)}`);
  // 获取当前文本内容宽度
  let modePosition: componentUtils.ComponentInfo = componentUtils.getRectangleById('marquee');
  this.ticketCheckScrollWidth = Number(px2vp(modePosition.size.width));
  this.ticketCheckTextWidth = Number(newValue.width);
  if (this.ticketCheckTextWidth < this.ticketCheckScrollWidth) {
    return;
  }
  this.ticketCheckTextOffset =
    this.marqueeAnimationModifier.playMode === PlayMode.Normal ? 0 :
      -(2 * this.ticketCheckTextWidth + this.marqueeScrollModifier.space - this.ticketCheckScrollWidth);
})
```

这段代码使用logger.info方法记录了文本区域变化的详细信息，包括oldValue和newValue，帮助开发者了解文本区域的变化情况。

## 5. 日志最佳实践

### 5.1 选择合适的日志级别

在使用Logger记录日志时，应根据日志的重要性选择合适的日志级别：

- **debug**：用于记录详细的调试信息，通常只在开发阶段启用
- **info**：用于记录一般的信息，如组件的状态变化、用户操作等
- **warn**：用于记录可能的问题，但不影响组件的正常运行
- **error**：用于记录错误和异常，可能导致组件无法正常运行

### 5.2 提供有用的上下文信息

在记录日志时，应提供足够的上下文信息，帮助开发者理解日志：

```typescript
// 不好的示例
logger.info('width changed');

// 好的示例
logger.info('MarqueeSection', `Text width changed from ${oldWidth} to ${newWidth}`);
```

### 5.3 避免过多的日志

过多的日志会影响应用的性能，应避免在关键路径上记录过多的日志：

```typescript
// 不好的示例：在循环中记录日志
for (let i = 0; i < 1000; i++) {
  logger.debug('MarqueeSection', `Loop iteration ${i}`);
}

// 好的示例：只记录关键信息
logger.debug('MarqueeSection', `Loop started with ${iterations} iterations`);
// 循环代码...
logger.debug('MarqueeSection', `Loop completed in ${time}ms`);
```

### 5.4 使用条件日志

在生产环境中，可以使用条件日志减少日志输出：

```typescript
// 定义一个调试标志
const DEBUG = false;

// 条件日志
if (DEBUG) {
  logger.debug('MarqueeSection', 'Detailed debug information');
}
```

## 6. 总结

本文详细介绍了HarmonyOS NEXT跑马灯组件中的Logger工具类，包括其实现原理、属性方法和使用方式。Logger工具类基于HarmonyOS的hilog模块，提供了不同级别的日志记录功能，帮助开发者调试和排查问题。

在跑马灯组件的开发过程中，合理使用Logger工具类可以提高开发效率和代码质量。开发者应根据日志的重要性选择合适的日志级别，提供足够的上下文信息，避免过多的日志输出，使用条件日志减少生产环境中的日志量。

通过本文的学习，读者应该能够理解Logger工具类的实现原理和使用方法，能够在自己的HarmonyOS应用中实现类似的日志记录功能，提高应用的可维护性和可调试性。