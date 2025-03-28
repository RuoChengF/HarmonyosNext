  
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！


![](https://files.mdnice.com/user/47561/41bd1890-42d3-4708-87e1-c9a907532042.png)

# HarmonyOS NEXT 登录模块开发教程（三）上：短信验证码登录基础实现

## 效果预览


![](https://files.mdnice.com/user/47561/d9af2abd-eefd-406a-a41e-7fa3942195d7.jpg)

## 1. 引言

在前两篇教程中，我们介绍了HarmonyOS NEXT登录模块的整体架构、模态窗口的实现原理以及一键登录页面的实现。本篇教程将深入讲解短信验证码登录的基础功能实现，包括手机号输入、验证码发送等核心功能。

## 2. OtherWaysToLogin组件概述

### 2.1 组件功能

OtherWaysToLogin组件的基础功能包括：

1. 手机号输入框，支持输入过滤和长度限制
2. 发送验证码按钮，支持基础交互
3. 基础UI布局实现

### 2.2 基础状态变量

```typescript
@Component
export struct OtherWaysToLogin {
    // 发送验证码按钮的颜色
    @State buttonColor: ResourceColor = Color.Grey;
    // 发送验证码按钮的内容
    @State buttonContent: ResourceStr = $r('app.string.modalwindow_verify');
    // 手机号是否可用
    phoneNumberAvailable: boolean = false;
}
```

## 3. 基础UI实现

### 3.1 顶部标题区域

```typescript
Column({ space: SPACE_TEN }) {
    Row({ space: SPACE_TEN }) {
        Image($r('app.media.phone'))
            .width($r('app.integer.modalwindow_user_image_height'))
            .borderRadius($r('app.integer.modalwindow_border_radius_mid'))
        Text($r('app.string.modalwindow_phone_login'))
            .fontSize($r('app.integer.modalwindow_font_size_mid'))
    }
    .width($r('app.string.modalwindow_size_full'))

    Text($r('app.string.modalwindow_new'))
        .width($r('app.string.modalwindow_size_full'))
}
.width($r('app.string.modalwindow_size_full'))
.alignItems(HorizontalAlign.Start)
```

#### 代码讲解  

 

1. **外层布局容器**
```typescript
Column({ space: SPACE_TEN }) {
    // 内容
}
.width($r('app.string.modalwindow_size_full'))
.alignItems(HorizontalAlign.Start)
```
- 使用 Column 组件创建垂直布局
- `space: SPACE_TEN` 设置子元素间垂直间距为10
- 通过 `width` 设置宽度占满父容器
- `alignItems` 设置子元素水平左对齐

2. **标题行布局**
```typescript
Row({ space: SPACE_TEN }) {
    Image($r('app.media.phone'))
        .width($r('app.integer.modalwindow_user_image_height'))
        .borderRadius($r('app.integer.modalwindow_border_radius_mid'))
    Text($r('app.string.modalwindow_phone_login'))
        .fontSize($r('app.integer.modalwindow_font_size_mid'))
}
.width($r('app.string.modalwindow_size_full'))
```
- 使用 Row 组件创建水平布局
- `space: SPACE_TEN` 设置子元素间水平间距为10
- 包含手机图标和标题文本两个子元素
- 设置宽度占满父容器

3. **手机图标**
```typescript
Image($r('app.media.phone'))
    .width($r('app.integer.modalwindow_user_image_height'))
    .borderRadius($r('app.integer.modalwindow_border_radius_mid'))
```
- 使用资源引用加载手机图标
- 设置图标宽度
- 添加圆角效果

4. **标题文本**
```typescript
Text($r('app.string.modalwindow_phone_login'))
    .fontSize($r('app.integer.modalwindow_font_size_mid'))
```
- 使用资源引用显示"手机号登录"文本
- 设置文字大小

5. **提示文本**
```typescript
Text($r('app.string.modalwindow_new'))
    .width($r('app.string.modalwindow_size_full'))
```
- 使用资源引用显示提示文本
- 设置宽度占满父容器

 

### 3.2 手机号输入区域

```typescript
Row() {
    Text($r('app.string.modalwindow_86'))
    Image($r('app.media.arrow_right'))
        .size({
            width: $r('app.integer.modalwindow_arrow_right_height'),
            height: $r('app.integer.modalwindow_arrow_right_height')
        })
        .margin($r('app.integer.modalwindow_margin_default'))
    TextInput({ placeholder: $r('app.string.modalwindow_input_phone_number') })
        .inputFilter('[0-9]')
        .backgroundColor(Color.Transparent)
        .caretColor(Color.Grey)
        .width($r('app.string.modalwindow_size_full'))
        .maxLength(PHONE_NUMBER_LENGTH)
        .onChange((value: string) => {
            if (value.length === PHONE_NUMBER_LENGTH) {
                this.phoneNumberAvailable = true;
                this.buttonColor = Color.Blue;
            } else {
                this.phoneNumberAvailable = false;
                this.buttonColor = Color.Grey;
            }
        })
}
```

### 3.3 发送验证码按钮

```typescript
Button(this.buttonContent)
    .type(ButtonType.Normal)
    .border({ radius: $r('app.integer.modalwindow_border_radius') })
    .width($r('app.string.modalwindow_size_full'))
    .backgroundColor(this.buttonColor)
    .onClick(() => {
        if (!this.phoneNumberAvailable) {
            promptAction.showToast({ 
                message: $r('app.string.modalwindow_message_right_phone_number') 
            });
            return;
        }
        promptAction.showToast({ 
            message: $r('app.string.modalwindow_message_verify_code_send') 
        });
    })
```

## 4. 基础交互逻辑

### 4.1 手机号输入验证

手机号输入验证主要包括：
1. 限制只能输入数字
2. 限制最大长度为11位
3. 实时验证输入长度，控制按钮状态

### 4.2 发送验证码基础逻辑

发送验证码的基础逻辑包括：
1. 验证手机号是否有效
2. 提供适当的交互反馈
3. 基础按钮状态管理

## 5. 小结

本篇教程介绍了短信验证码登录的基础功能实现，包括：
1. 基础UI布局
2. 手机号输入验证
3. 发送验证码按钮的基础功能

在下一篇教程中，我们将介绍更多进阶功能的实现。
 