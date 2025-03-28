> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/09115456-e88b-4578-9a77-4d81737069dc.png)

# HarmonyOS NEXT 登录模块开发教程（一）：模态窗口登录概述

## 效果预览

![](https://files.mdnice.com/user/47561/0ce72fe6-f1af-4f1d-8b10-689fe69a3e9a.jpg)

## 1. 引言

在移动应用开发中，登录功能是几乎所有应用必不可少的组成部分。一个设计良好的登录界面不仅能提升用户体验，还能增强应用的安全性和可用性。本系列教程将详细讲解如何使用 HarmonyOS NEXT（API12+）开发一个功能完善、体验良好的登录模块。

本教程是系列的第一篇，我们将从整体上介绍登录模块的架构设计和核心组件，并重点讲解模态窗口（ModalWindow）的实现原理。

## 2. 登录模块整体架构

我们的登录模块采用组件化设计，主要包含以下核心组件：

| 组件名称             | 文件路径             | 主要功能                                 |
| -------------------- | -------------------- | ---------------------------------------- |
| ModalWindowComponent | ModalWindow.ets      | 提供全屏模态窗口容器，作为登录界面的载体 |
| DefaultLogin         | DefaultLogin.ets     | 实现默认的一键登录页面                   |
| OtherWaysToLogin     | OtherWaysToLogin.ets | 提供短信验证码登录和第三方登录方式       |
| ReadAgreement        | OtherWaysToLogin.ets | 用户协议和隐私政策展示组件               |

这些组件之间的关系如下：

1. ModalWindowComponent 作为容器组件，负责控制登录模态窗口的显示和隐藏
2. DefaultLogin 和 OtherWaysToLogin 作为内容组件，在模态窗口中进行切换展示
3. ReadAgreement 作为公共组件，在不同登录方式中复用

## 3. 模态窗口组件详解

### 3.1 什么是模态窗口？

模态窗口（Modal Window）是一种特殊的 UI 元素，它会临时阻断与主界面的交互，强制用户完成某项操作后才能返回主界面。在登录场景中，模态窗口能够集中用户注意力，提供更专注的登录体验。

在 HarmonyOS NEXT 中，模态窗口通过`bindContentCover`属性实现，它能够在当前页面上覆盖一个新的内容层，而不需要跳转到新页面。

### 3.2 ModalWindow 组件实现

下面是 ModalWindowComponent 的完整代码：

```typescript
import { DefaultLogin } from './DefaultLogin';

/**
 *
 * 功能描述：全屏登录页面：在主页面点击跳转到全屏登录页后，显示全屏模态页面，全屏模态页面从下方滑出并覆盖整个屏幕，模态页面内容自定义，此处分为默认一键登录方式和其他登录方式。
 *
 * 推荐场景：需要登录场景的app
 *
 * 核心组件：
 * 1. DefaultLogin
 *
 * 实现步骤：
 * 1. 模态转场是新的界面覆盖在旧的界面上，旧的界面不消失的一种转场方式。
 * 2. 通过bindContentCover属性为Button组件绑定全屏模态页面，点击Button后显示模态页面，模态页面内容自定义，包含默认一键登录页面和其他登录方式页面。
 */

@Component
export struct ModalWindowComponent {
    // 是否显示全屏模态页面
    @State isPresent: boolean = false;

    @Builder
    loginBuilder() {
        Column() {
            DefaultLogin({ isPresentInLoginView: this.isPresent }) // 通过@State和@Link使isPresentInLoginView和isPresent产生关联
        }
    }

    build() {
        Column() {
            // TODO：需求：增加其他登录方式，如半模态窗口
            Button($r('app.string.modalwindow_full_screen_modal_login_description'))
                .fontColor(Color.White)
                .borderRadius($r('app.integer.modalwindow_border_radius'))
                    /**
                     * ButtonType为Normal时，按钮圆角通过通用属性borderRadius设置。不同ButtonType下borderRadius属性是否生效，详见：
                     * https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/ts-basic-components-button-0000001815086854-V5#ZH-CN_TOPIC_0000001815086854__buttontype枚举说明
                     */
                .type(ButtonType.Normal)
                .backgroundColor($r('app.color.modalwindow_grey_2'))
                .width($r('app.string.modalwindow_size_full'))
                    /**
                     * TODO: 知识点: 通过bindContentCover属性为组件绑定全屏模态页面
                     * isPresent：是否显示全屏模态页面
                     * loginBuilder：配置全屏模态页面内容
                     */
                .bindContentCover($$this.isPresent, this.loginBuilder)
                .onClick(() => {
                    this.isPresent = true; // 当isPresent为true时显示模态页面，反之不显示
                })
        }
        .size({ width: $r('app.string.modalwindow_size_full'), height: $r('app.string.modalwindow_size_full') })
        .padding($r('app.integer.modalwindow_padding_default'))
        .justifyContent(FlexAlign.Center)
    }
}
```

### 3.3 核心知识点解析

#### 3.3.1 @Component 装饰器

`@Component`装饰器用于声明一个自定义组件，使其可以在其他组件中使用。在 HarmonyOS NEXT 中，所有 UI 组件都需要使用@Component 装饰器进行声明。

```typescript
@Component
export struct ModalWindowComponent {
    // 组件实现
}
```

#### 3.3.2 @State 装饰器

`@State`装饰器用于声明组件的内部状态，当状态变化时会自动触发 UI 刷新。在 ModalWindowComponent 中，我们使用@State 装饰 isPresent 变量，用于控制模态窗口的显示和隐藏。

```typescript
@State isPresent: boolean = false;
```

当 isPresent 变为 true 时，模态窗口显示；当 isPresent 变为 false 时，模态窗口隐藏。

#### 3.3.3 @Builder 装饰器

`@Builder`装饰器用于定义一个 UI 构建函数，可以在 build()方法中复用。在 ModalWindowComponent 中，我们使用@Builder 定义了 loginBuilder()函数，用于构建模态窗口的内容。

```typescript
@Builder
loginBuilder() {
    Column() {
        DefaultLogin({ isPresentInLoginView: this.isPresent })
    }
}
```

#### 3.3.4 bindContentCover 属性

`bindContentCover`是 HarmonyOS NEXT 中实现模态窗口的核心属性，它接收两个参数：

1. 控制模态窗口显示/隐藏的状态变量（需要使用\$\$ 运算符）
2. 构建模态窗口内容的 Builder 函数

```typescript
.bindContentCover($$this.isPresent, this.loginBuilder)
```

这里的`$$`运算符用于创建状态变量的引用，使得系统组件可以同步修改状态变量的值。

#### 3.3.5 资源引用

在代码中，我们使用`$r()`函数引用应用资源，这是 HarmonyOS 推荐的资源管理方式，有利于应用的国际化和主题适配。

```typescript
Button($r('app.string.modalwindow_full_screen_modal_login_description'))
    .borderRadius($r('app.integer.modalwindow_border_radius'))
    .backgroundColor($r('app.color.modalwindow_grey_2'))
    .width($r('app.string.modalwindow_size_full'))
```

## 4. 模态窗口的交互流程

模态窗口的完整交互流程如下：

1. 用户点击主页面上的登录按钮
2. 系统触发按钮的 onClick 事件，将 isPresent 设置为 true
3. bindContentCover 检测到 isPresent 变为 true，显示模态窗口
4. 模态窗口从底部滑入，覆盖整个屏幕
5. 用户在模态窗口中完成登录操作或点击返回按钮
6. 如果用户点击返回按钮，系统将 isPresent 设置为 false
7. bindContentCover 检测到 isPresent 变为 false，隐藏模态窗口
8. 模态窗口滑出，显示主页面

## 5. 最佳实践与注意事项

在使用模态窗口实现登录功能时，有以下几点最佳实践和注意事项：

1. **状态管理**：使用@State 和@Link 装饰器管理组件状态，确保状态变化能正确触发 UI 刷新
2. **资源管理**：使用\$r()函数引用应用资源，避免硬编码字符串和数值
3. **组件复用**：将可复用的 UI 部分抽取为独立组件，提高代码可维护性
4. **交互体验**：添加适当的转场动画，提升用户体验
5. **安全考虑**：在登录成功后及时清理敏感信息，避免内存泄露

## 6. 小结

本文介绍了 HarmonyOS NEXT 中模态窗口登录的实现原理和核心组件。通过 ModalWindowComponent，我们可以创建一个全屏模态窗口，为用户提供专注的登录体验。在下一篇教程中，我们将详细讲解 DefaultLogin 组件的实现，包括一键登录的 UI 布局和交互逻辑。

## 7. 参考资源

- [HarmonyOS 开发者文档 - bindContentCover 属性](https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-universal-attributes-modal-0000001428061700)
- [HarmonyOS 开发者文档 - @Component 装饰器](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-component-0000001473537046)
- [HarmonyOS 开发者文档 - @State 装饰器](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-state-0000001474017162)
- [HarmonyOS 开发者文档 - @Builder 装饰器](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-builder-0000001473697338)
