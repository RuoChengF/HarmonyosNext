> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/ddc3e07a-128b-4e5b-8fb1-10557ef34674.png)

# HarmonyOS NEXT 登录模块开发教程（二）：一键登录页面实现

## 效果预览

![](https://files.mdnice.com/user/47561/0ce72fe6-f1af-4f1d-8b10-689fe69a3e9a.jpg)

## 1. 引言

在上一篇教程中，我们介绍了 HarmonyOS NEXT 登录模块的整体架构和模态窗口的实现原理。本篇教程将深入讲解 DefaultLogin 组件的实现，这是登录模块中最核心的组件之一，负责提供默认的一键登录页面。

一键登录是现代移动应用中常见的登录方式，它能够简化用户的登录流程，提高用户体验。在 HarmonyOS NEXT 中，我们可以通过 ArkTS 语言和声明式 UI 框架，轻松实现一个功能完善的一键登录页面。

## 2. DefaultLogin 组件概述

### 2.1 组件功能

DefaultLogin 组件主要提供以下功能：

1. 显示用户头像和欢迎信息
2. 展示用户手机号（预设或从系统获取）
3. 提供服务协议阅读和同意选项
4. 实现一键登录按钮及其交互逻辑
5. 提供其他登录方式的入口
6. 支持返回按钮，控制模态窗口的显示/隐藏

### 2.2 组件结构

| 部分             | 描述                                 |
| ---------------- | ------------------------------------ |
| 状态变量         | 控制组件内部状态和 UI 展示           |
| DefaultLoginPage | 构建一键登录页面 UI 的 Builder 函数  |
| build 方法       | 组件的主要构建方法，处理页面切换逻辑 |

## 3. DefaultLogin 组件实现

### 3.1 完整代码

```typescript
import promptAction from '@ohos.promptAction';
import { OtherWaysToLogin, ReadAgreement } from './OtherWaysToLogin';

const EFFECT_DURATION = 800;
const EFFECT_OPACITY = 0.4;
const SPACE_TEN = 10;

@Component
export struct DefaultLogin {
    /**
     * isPresentInLoginView控制登录页面是否显示
     * 子组件中被@Link装饰的变量与其父组件中@State装饰的对应数据源建立双向数据绑定，详见：
     * https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-link-0000001820999565
     */
    @Link isPresentInLoginView: boolean;
    // 是否是默认一键登录方式
    @State isDefaultLogin: boolean = true;
    // 用户名
    userName: string = '18888888888';
    // 判断是否同意协议
    isConfirmed: boolean = false;
    private effect: TransitionEffect = TransitionEffect.OPACITY
        .animation({ duration: EFFECT_DURATION })
        .combine(TransitionEffect.opacity(EFFECT_OPACITY))

    // 默认一键登录方式
    @Builder
    DefaultLoginPage() {
        Column({ space: SPACE_TEN }) {
            Row({ space: SPACE_TEN }) {
                Image($r('app.media.batman'))
                    .width($r('app.integer.modalwindow_user_image_height'))
                    .height($r('app.integer.modalwindow_user_image_height'))
                Column({ space: SPACE_TEN }) {
                    Text($r('app.string.modalwindow_welcome_back'))
                        .fontWeight(FontWeight.Bold)
                        .fontSize($r('app.integer.modalwindow_font_size_mid'))
                        .fontColor(Color.Black)

                    Text($r('app.string.modalwindow_more_wonderful_after_login'))
                        .fontColor($r('app.color.modalwindow_grey_3'))
                }
                .alignItems(HorizontalAlign.Start)
            }
            .alignItems(VerticalAlign.Center)
            .width($r('app.string.modalwindow_size_full'))

            Text(this.userName)
                .fontColor($r('app.color.modalwindow_grey_3'))
                .fontWeight(FontWeight.Bold)
                .padding({ left: $r('app.integer.modalwindow_padding_default') })
                .height($r('app.integer.modalwindow_user_image_height'))
                .width($r('app.string.modalwindow_size_full'))
                .borderRadius($r('app.integer.modalwindow_border_radius'))
                .backgroundColor($r('app.color.modalwindow_grey_e'))

            Text($r('app.string.modalwindow_verify_server_tip'))
                .fontColor($r('app.color.modalwindow_grey_6'))
                .width($r('app.string.modalwindow_size_full'))
                .textAlign(TextAlign.Start)

            Row() {
                Checkbox({ name: 'checkbox1' })
                    .id('default_agreement')
                    .select(this.isConfirmed)
                    .onChange((value: boolean) => {
                        this.isConfirmed = value
                    })
                ReadAgreement()
            }
            .width($r('app.string.modalwindow_size_full'))
            .alignItems(VerticalAlign.Center)

            Button($r('app.string.modalwindow_phone_start_login'))
                .fontColor(Color.White)
                .borderRadius($r('app.integer.modalwindow_border_radius'))
                .type(ButtonType.Normal)
                .backgroundColor($r('app.color.modalwindow_grey_2'))
                .onClick(() => {
                    if (this.isConfirmed) {
                        // 调用Toast显示登录成功提示
                        promptAction.showToast({ message: $r('app.string.modalwindow_login_success') });
                    } else {
                        // 调用Toast显示请先阅读并同意协议提示
                        promptAction.showToast({ message: $r('app.string.modalwindow_please_read_and_agree') });
                    }
                })
                .width($r('app.string.modalwindow_size_full'))
                .height($r('app.integer.modalwindow_height_fifty'))
            Row() {
                Text($r('app.string.modalwindow_other_way_login'))
                    .fontColor($r('app.color.modalwindow_grey_7'))
                    .backgroundColor($r('app.color.modalwindow_transparent_7'))
                    .onClick(() => {
                        this.isDefaultLogin = false;
                    })

                Blank() // 在容器主轴方向上自动填充容器空余部分

                Text($r('app.string.modalwindow_login_problems'))
                    .fontColor($r('app.color.modalwindow_grey_7'))
                    .backgroundColor($r('app.color.modalwindow_transparent_7'))
                    .onClick(() => {
                        // 调用Toast显示遇到问题提示
                        promptAction.showToast({ message: $r('app.string.modalwindow_login_problems') });
                    })
            }
            .width($r('app.string.modalwindow_size_full'))
        }
        .width($r('app.string.modalwindow_size_full'))
        .height($r('app.string.modalwindow_size_full'))
        .backgroundColor(Color.White)
        .justifyContent(FlexAlign.Center)
    }

    build() {
        Stack({ alignContent: Alignment.TopStart }) {
            // 登录方式有两种(默认一键登录方式和其他方式登录)，需要在一个模态窗口中切换，使用if进行条件渲染
            if (this.isDefaultLogin) {
                this.DefaultLoginPage() // 默认一键登录方式
            } else {
                OtherWaysToLogin()// 其他登录方式
                    .transition(this.effect) // 此处涉及到组件的显示和消失，所以使用transition属性设置出现/消失转场
            }
            Image($r('app.media.arrow_back'))// 通过Stack组件，两个页面只实现一个back
                .id('login_back')
                .width($r('app.integer.modalwindow_height_twenty_five')).height($r('app.integer.modalwindow_height_twenty_five'))
                .margin({ top: $r('app.integer.modalwindow_margin_mid') })
                .onClick(() => {
                    if (this.isDefaultLogin) {
                        this.isPresentInLoginView = false;
                    } else {
                        this.isDefaultLogin = true
                    }
                })
        }
        .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])
        .size({ width: $r('app.string.modalwindow_size_full'), height: $r('app.string.modalwindow_size_full') })
        .padding({
            top: $r('app.integer.modalwindow_padding_default'),
            left: $r('app.integer.modalwindow_padding_default'),
            right: $r('app.integer.modalwindow_padding_default')
        })
        .backgroundColor(Color.White) // 将模态页面背景设置为白色，以避免模态页面内组件发生显隐变化时露出下层页面
    }
}
```

### 3.2 状态变量解析

在 DefaultLogin 组件中，我们定义了以下状态变量：

```typescript
@Link isPresentInLoginView: boolean;
@State isDefaultLogin: boolean = true;
userName: string = '18888888888';
isConfirmed: boolean = false;
private effect: TransitionEffect = TransitionEffect.OPACITY
    .animation({ duration: EFFECT_DURATION })
    .combine(TransitionEffect.opacity(EFFECT_OPACITY))
```

| 变量名               | 装饰器  | 类型             | 作用                                              |
| -------------------- | ------- | ---------------- | ------------------------------------------------- |
| isPresentInLoginView | @Link   | boolean          | 与父组件建立双向数据绑定，控制模态窗口的显示/隐藏 |
| isDefaultLogin       | @State  | boolean          | 控制当前显示的是默认登录页面还是其他登录方式页面  |
| userName             | 无      | string           | 存储用户手机号，此处为预设值                      |
| isConfirmed          | 无      | boolean          | 记录用户是否同意服务协议                          |
| effect               | private | TransitionEffect | 定义页面切换时的转场效果                          |

#### 3.2.1 @Link 装饰器

`@Link`装饰器用于在父子组件之间建立双向数据绑定。在我们的例子中，DefaultLogin 组件通过@Link 装饰的 isPresentInLoginView 变量与 ModalWindowComponent 中的 isPresent 变量建立了双向绑定。

当 DefaultLogin 组件中修改 isPresentInLoginView 的值时，ModalWindowComponent 中的 isPresent 也会同步更新，反之亦然。这种机制使得子组件可以控制父组件中的状态，实现更灵活的组件通信。

#### 3.2.2 @State 装饰器

`@State`装饰器用于声明组件的内部状态。当@State 装饰的变量值发生变化时，框架会自动重新渲染组件。在 DefaultLogin 组件中，isDefaultLogin 变量控制显示默认登录页面还是其他登录方式页面。

#### 3.2.3 TransitionEffect

TransitionEffect 用于定义组件的转场效果。在 DefaultLogin 组件中，我们定义了一个组合转场效果，包括透明度变化和动画持续时间：

```typescript
private effect: TransitionEffect = TransitionEffect.OPACITY
    .animation({ duration: EFFECT_DURATION })
    .combine(TransitionEffect.opacity(EFFECT_OPACITY))
```

这个转场效果会在默认登录页面和其他登录方式页面之间切换时应用，提供平滑的视觉过渡。

## 4. UI 布局详解

### 4.1 整体布局

DefaultLogin 组件的 UI 布局采用嵌套的容器组件实现，主要包括：

1. 最外层使用 Stack 组件，实现页面切换和返回按钮的叠加布局
2. 内部使用 Column 组件作为主要容器，垂直排列各个 UI 元素
3. 使用 Row 组件实现水平排列的元素，如用户头像和欢迎信息

### 4.2 用户信息区域

让我详细讲解这段用户信息区域的代码：

```typescript
Row({ space: SPACE_TEN }) {  // 创建水平布局，设置子元素间距为10
    // 1. 用户头像
    Image($r('app.media.batman'))  // 加载本地图片资源
        .width($r('app.integer.modalwindow_user_image_height'))  // 设置图片宽度
        .height($r('app.integer.modalwindow_user_image_height')) // 设置图片高度

    // 2. 欢迎信息区域
    Column({ space: SPACE_TEN }) {  // 创建垂直布局，子元素间距为10
        // 2.1 欢迎回来文本
        Text($r('app.string.modalwindow_welcome_back'))
            .fontWeight(FontWeight.Bold)    // 设置字体粗细为粗体
            .fontSize($r('app.integer.modalwindow_font_size_mid'))  // 设置字体大小
            .fontColor(Color.Black)         // 设置字体颜色为黑色

        // 2.2 登录后更精彩提示文本
        Text($r('app.string.modalwindow_more_wonderful_after_login'))
            .fontColor($r('app.color.modalwindow_grey_3'))  // 设置字体颜色为灰色
    }
    .alignItems(HorizontalAlign.Start)  // 将Column内的文本左对齐
}
.alignItems(VerticalAlign.Center)  // Row内的元素垂直居中对齐
.width($r('app.string.modalwindow_size_full'))  // 设置整个Row的宽度为100%
```

代码结构分析：

1. **外层容器**：

   - 使用 `Row` 组件创建水平布局
   - `space: SPACE_TEN` 设置子元素间距为 10 像素
   - `.alignItems(VerticalAlign.Center)` 使子元素垂直居中
   - `.width($r('app.string.modalwindow_size_full'))` 使容器宽度占满父容器

2. **头像部分**：

   - 使用 `Image` 组件显示用户头像
   - 通过 `$r('app.media.batman')` 引用本地图片资源
   - 使用资源引用设置宽高，保证在不同设备上的一致性

3. **文字信息部分**：
   - 使用 `Column` 组件创建垂直布局
   - 包含两个 `Text` 组件：
     - 欢迎语：粗体显示，黑色
     - 提示语：使用灰色显示
   - `.alignItems(HorizontalAlign.Start)` 确保文本左对齐

布局效果：

- 左侧显示圆形头像
- 右侧垂直排列两行文本
- 整体垂直居中对齐
- 文本左对齐排列
- 组件间保持统一的间距

## 总结

本文详细介绍了 HarmonyOS NEXT 登录模块中 DefaultLogin 组件的实现，主要包括以下几个方面：

1. **组件架构设计**

   - 采用 ArkTS 声明式开发范式
   - 使用装饰器（@Link、@State）管理组件状态
   - 实现页面间平滑切换的转场效果

2. **UI 布局实现**

   - 使用 Stack、Column、Row 等布局组件构建界面
   - 运用资源引用（\$r）确保界面在不同设备上的一致性
   - 实现了用户信息展示、协议确认、登录按钮等核心功能

3. **交互功能**

   - 实现一键登录和其他登录方式的切换
   - 添加服务协议确认机制
   - 集成返回按钮和页面导航功能

4. **最佳实践**
   - 组件状态管理的规范使用
   - UI 布局的模块化设计
   - 代码复用和维护性的考虑

通过本教程，开发者可以了解如何在 HarmonyOS NEXT 中实现一个功能完整、交互友好的登录页面，同时掌握 ArkTS 组件开发的核心概念和最佳实践。这些知识和技能可以应用到其他类似的组件开发中，帮助开发者构建更好的 HarmonyOS 应用。
