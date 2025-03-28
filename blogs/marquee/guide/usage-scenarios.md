> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](../images/img_5ebd9778.png)

# HarmonyOS NEXT跑马灯组件教程：实际应用与场景示例

## 1. 跑马灯组件应用概述

跑马灯组件在HarmonyOS NEXT应用中有着广泛的应用场景，特别是在需要在有限空间内展示较长文本内容的情况下。本文将介绍跑马灯组件的实际应用场景和使用方法，帮助开发者更好地理解和使用这一组件。

### 1.1 常见应用场景

| 应用场景 | 使用特点 | 配置建议 |
|------|------|------|
| 消息通知 | 短时间内展示重要信息 | 适中速度，从右到左滚动 |
| 票务信息 | 展示检票口、登机口等信息 | 较慢速度，无限循环 |
| 促销广告 | 吸引用户注意力 | 较快速度，有停顿效果 |
| 新闻标题 | 展示多条新闻标题 | 适中速度，多次循环 |
| 股票行情 | 实时展示多支股票信息 | 较快速度，从右到左滚动 |

## 2. 在MarqueeDemo中使用跑马灯组件

### 2.1 基本使用方法

在HarmonyOS NEXT中，使用跑马灯组件非常简单。以MarqueeDemo.ets为例：

```typescript
import { MarqueeViewComponent } from "../../components/Marquee/Marquee";
@Entry
@Component
struct MarqueeDemo {
    build() {
        RelativeContainer() {
            MarqueeViewComponent()
        }
        .height('100%')
        .width('100%')
    }
}
```

这段代码展示了跑马灯组件的基本使用方法：

1. 首先导入MarqueeViewComponent组件
2. 在页面的build方法中创建一个RelativeContainer作为容器
3. 在容器中添加MarqueeViewComponent组件
4. 设置容器的宽高为100%，使其填满整个页面

### 2.2 组件层次结构

在实际应用中，跑马灯组件通常嵌套在多层组件中使用。以MarqueeViewComponent为例，其内部结构如下：

```typescript
@Component
export struct MarqueeViewComponent {
  build() {
    Column() {
      // 场景介绍组件
      FunctionDescription({
        title: $r('app.string.marquee_title'),
        content: $r('app.string.marquee_content')
      })
      // 行程信息组件
      TripView()
    }
    .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])
    .width('100%')
    .height('100%')
    .padding($r('app.string.ohos_id_card_padding_start'))
    .linearGradient({
      angle: Constants.ANGLE,
      colors: [[$r('app.color.marquee_bg_color1'), 0], [$r('app.color.marquee_bg_color2'), 1]]
    })
  }
}
```

这段代码中，MarqueeViewComponent包含两个子组件：

1. FunctionDescription：用于展示功能描述
2. TripView：包含实际的跑马灯组件

## 3. 票务信息场景示例

### 3.1 TripView组件实现

TripView组件是一个典型的票务信息展示场景，它使用跑马灯组件展示检票口信息：

```typescript
@Component
struct TripView {
  @State tripData: TripDataSource = new TripDataSource();

  build() {
    Column() {
      // 行程信息列表
      List({ space: 12 }) {
        LazyForEach(this.tripData, (item: TripDataType) => {
          ListItem() {
            TripItem({ tripDataItem: item })
          }
        }, (item: TripDataType) => item.id.toString())
      }
      .width('100%')
      .layoutWeight(1)
    }
    .width('100%')
    .height('100%')
  }
}
```

### 3.2 TripItem组件中使用跑马灯

TripItem组件中使用MarqueeSection组件展示检票口信息：

```typescript
@Component
struct TripItem {
  @Prop tripDataItem: TripDataType;

  @Builder
  marqueeTextBuilder(marqueeText: ResourceStr) {
    Text(marqueeText)
      .fontSize($r('app.float.trip_item_font_size'))
      .fontColor($r('app.color.trip_item_font_color'))
  }

  build() {
    RelativeContainer() {
      // 其他票务信息...
      
      // 检票口信息（使用跑马灯）
      Text($r('app.string.ticket_entrance'))
        .fontSize($r('app.float.trip_item_font_size'))
        .fontColor($r('app.color.trip_item_font_color'))
        .id('ticketEntrance')
        .alignRules({
          top: { anchor: 'vehicleModel', align: VerticalAlign.Bottom },
          left: { anchor: '__container__', align: HorizontalAlign.Start }
        })
        .margin({ top: 12 })
      
      // 跑马灯组件
      MarqueeSection({
        marqueeTextBuilder: () => {
          this.marqueeTextBuilder(this.tripDataItem.ticketEntrance)
        },
        marqueeAnimationModifier: new MarqueeAnimationModifier(),
        marqueeScrollModifier: new MarqueeScrollModifier(display.isFoldable() ?
          $r('app.string.marquee_scroll_phone_width') : $r('app.string.marquee_scroll_tablet_width'),
          Constants.BLANK_SPACE)
      })
    }
    .width('100%')
    .height($r('app.float.trip_item_height'))
    .borderRadius($r('app.float.trip_item_radius'))
    .backgroundColor(Color.White)
    .padding({
      left: $r('app.float.trip_item_padding_left'),
      right: $r('app.float.trip_item_padding_right'),
      top: $r('app.float.trip_item_padding_top'),
      bottom: $r('app.float.trip_item_padding_bottom')
    })
  }
}
```

这段代码展示了在票务信息场景中使用跑马灯组件的方法：

1. 定义marqueeTextBuilder方法，用于构建跑马灯文本内容
2. 在RelativeContainer中添加检票口标签和跑马灯组件
3. 配置MarqueeSection组件，传入文本构建器和动画配置
4. 根据设备类型（折叠屏或平板）设置不同的滚动区域宽度

## 4. 消息通知场景示例

### 4.1 消息通知组件实现

在消息通知场景中，跑马灯组件通常用于展示重要通知信息：

```typescript
@Component
struct NotificationBar {
  @Prop notificationText: string;
  
  @Builder
  notificationTextBuilder() {
    Text(this.notificationText)
      .fontSize(14)
      .fontColor('#FFFFFF')
  }
  
  build() {
    Row() {
      Image($r('app.media.ic_notification'))
        .width(20)
        .height(20)
        .margin({ right: 8 })
      
      // 跑马灯组件
      MarqueeSection({
        marqueeTextBuilder: () => {
          this.notificationTextBuilder()
        },
        // 配置从右到左滚动，适中速度
        marqueeAnimationModifier: new MarqueeAnimationModifier(
          -1,                    // 无限循环
          8000,                  // 动画持续时间8秒
          1.2,                   // 动画速度1.2倍
          PlayMode.Reverse,      // 从右到左滚动
          1500                   // 停顿时间1.5秒
        ),
        // 配置较宽的滚动区域
        marqueeScrollModifier: new MarqueeScrollModifier(
          '80%',                // 滚动区域宽度为80%
          40                     // 文本间隔40像素
        )
      })
    }
    .width('100%')
    .height(40)
    .backgroundColor('#FF5722')
    .padding({ left: 16, right: 16 })
  }
}
```

这个示例展示了消息通知场景中的跑马灯配置：

1. 使用较宽的滚动区域（80%）
2. 从右到左滚动（PlayMode.Reverse）
3. 适中的动画速度（tempo=1.2）
4. 适当的停顿时间（delayTime=1500ms）

## 5. 新闻标题场景示例

### 5.1 新闻标题组件实现

在新闻应用中，跑马灯组件可用于展示多条新闻标题：

```typescript
@Component
struct NewsTickerBar {
  @State currentNewsIndex: number = 0;
  private newsList: string[] = [
    "华为发布最新HarmonyOS NEXT系统，带来全新体验",
    "国内科技企业加速布局人工智能领域",
    "全球气候变化会议将于下月在北京举行",
    "新能源汽车销量持续增长，市场份额突破30%"
  ];
  
  @Builder
  newsTextBuilder() {
    Text(this.newsList[this.currentNewsIndex])
      .fontSize(16)
      .fontColor('#333333')
      .fontWeight(FontWeight.Medium)
  }
  
  build() {
    Row() {
      Text("最新消息：")
        .fontSize(16)
        .fontColor('#FF0000')
        .fontWeight(FontWeight.Bold)
        .margin({ right: 8 })
      
      // 跑马灯组件
      MarqueeSection({
        marqueeTextBuilder: () => {
          this.newsTextBuilder()
        },
        // 配置单次播放，播放完成后切换到下一条新闻
        marqueeAnimationModifier: new MarqueeAnimationModifier(
          1,                     // 单次播放
          12000,                 // 动画持续时间12秒
          1,                     // 正常速度
          PlayMode.Reverse,      // 从右到左滚动
          500                    // 停顿时间0.5秒
        ),
        marqueeScrollModifier: new MarqueeScrollModifier(
          '70%',                // 滚动区域宽度为70%
          60                     // 文本间隔60像素
        )
      })
    }
    .width('100%')
    .height(50)
    .backgroundColor('#F5F5F5')
    .padding({ left: 16, right: 16 })
    .onAppear(() => {
      // 定时切换新闻标题
      setInterval(() => {
        this.currentNewsIndex = (this.currentNewsIndex + 1) % this.newsList.length;
      }, 15000); // 每15秒切换一次
    })
  }
}
```

这个示例展示了新闻标题场景中的跑马灯配置：

1. 使用单次播放（iterations=1）
2. 较长的动画持续时间（duration=12000ms）
3. 从右到左滚动（PlayMode.Reverse）
4. 较短的停顿时间（delayTime=500ms）
5. 通过定时器定期切换新闻标题

## 6. 设备适配与响应式设计

### 6.1 折叠屏与平板适配

跑马灯组件可以根据不同设备类型进行适配：

```typescript
MarqueeSection({
  // ...
  marqueeScrollModifier: new MarqueeScrollModifier(display.isFoldable() ?
    $r('app.string.marquee_scroll_phone_width') : $r('app.string.marquee_scroll_tablet_width'),
    Constants.BLANK_SPACE)
})
```

这段代码通过display.isFoldable()方法检测设备是否为折叠屏，然后根据设备类型选择不同的滚动区域宽度：

- 对于折叠屏设备，使用app.string.marquee_scroll_phone_width资源
- 对于平板设备，使用app.string.marquee_scroll_tablet_width资源

### 6.2 横竖屏适配

跑马灯组件也可以根据屏幕方向进行适配：

```typescript
@Component
struct AdaptiveMarquee {
  @State isPortrait: boolean = true;
  
  aboutToAppear() {
    // 监听屏幕方向变化
    display.on('change', (data) => {
      this.isPortrait = data.width < data.height;
    });
  }
  
  @Builder
  marqueeTextBuilder(text: string) {
    Text(text)
      .fontSize(16)
      .fontColor('#333333')
  }
  
  build() {
    Column() {
      // 跑马灯组件
      MarqueeSection({
        marqueeTextBuilder: () => {
          this.marqueeTextBuilder("这是一段需要使用跑马灯效果展示的长文本内容")
        },
        marqueeAnimationModifier: new MarqueeAnimationModifier(),
        // 根据屏幕方向设置不同的滚动区域宽度
        marqueeScrollModifier: new MarqueeScrollModifier(
          this.isPortrait ? '80%' : '50%',
          Constants.BLANK_SPACE
        )
      })
    }
    .width('100%')
  }
}
```

这个示例展示了如何根据屏幕方向调整跑马灯组件的配置：

1. 使用display.on('change')监听屏幕方向变化
2. 根据屏幕宽高比判断是否为竖屏模式
3. 在竖屏模式下使用较宽的滚动区域（80%）
4. 在横屏模式下使用较窄的滚动区域（50%）

## 7. 数据绑定与动态更新

### 7.1 数据绑定

跑马灯组件可以与数据源绑定，实现动态内容更新：

```typescript
@Component
struct DynamicMarquee {
  @State message: string = "初始消息内容";
  
  @Builder
  messageTextBuilder() {
    Text(this.message)
      .fontSize(16)
      .fontColor('#333333')
  }
  
  build() {
    Column() {
      // 跑马灯组件
      MarqueeSection({
        marqueeTextBuilder: () => {
          this.messageTextBuilder()
        },
        marqueeAnimationModifier: new MarqueeAnimationModifier(),
        marqueeScrollModifier: new MarqueeScrollModifier()
      })
      
      // 更新按钮
      Button("更新消息")
        .onClick(() => {
          this.message = "这是更新后的消息内容 - " + new Date().toLocaleTimeString();
        })
        .margin({ top: 20 })
    }
    .width('100%')
    .padding(16)
  }
}
```

这个示例展示了如何实现数据绑定和动态更新：

1. 使用@State装饰器定义响应式数据
2. 在marqueeTextBuilder中使用响应式数据
3. 通过按钮点击事件更新数据
4. 当数据更新时，跑马灯组件会自动更新显示内容

### 7.2 列表数据绑定

跑马灯组件也可以与列表数据绑定，实现多条数据的展示：

```typescript
@Component
struct ListMarquee {
  @State dataList: TripDataSource = new TripDataSource();
  
  build() {
    Column() {
      List({ space: 12 }) {
        LazyForEach(this.dataList, (item: TripDataType) => {
          ListItem() {
            // 为每个列表项创建一个跑马灯组件
            Row() {
              Text(item.trainNumber)
                .width('30%')
              
              MarqueeSection({
                marqueeTextBuilder: () => {
                  Text(item.ticketEntrance)
                    .fontSize(14)
                },
                marqueeAnimationModifier: new MarqueeAnimationModifier(),
                marqueeScrollModifier: new MarqueeScrollModifier('60%', 30)
              })
            }
            .width('100%')
            .height(50)
            .backgroundColor(Color.White)
            .borderRadius(8)
            .padding(10)
          }
        }, (item: TripDataType) => item.id.toString())
      }
      .width('100%')
    }
    .width('100%')
    .padding(16)
  }
}
```

这个示例展示了如何将跑马灯组件与列表数据绑定：

1. 使用LazyForEach遍历数据源
2. 为每个列表项创建一个跑马灯组件
3. 将列表项的数据传递给跑马灯组件

## 8. 性能优化建议

### 8.1 减少实例数量

在使用跑马灯组件时，应尽量减少实例数量，特别是在列表中使用时：

```typescript
// 不推荐：为所有列表项创建跑马灯组件
LazyForEach(this.dataList, (item) => {
  ListItem() {
    MarqueeSection({ /* ... */ })
  }
})

// 推荐：只为需要跑马灯效果的列表项创建跑马灯组件
LazyForEach(this.dataList, (item) => {
  ListItem() {
    if (needMarquee(item)) { // 判断是否需要跑马灯效果
      MarqueeSection({ /* ... */ })
    } else {
      Text(item.text)
    }
  }
})
```

### 8.2 延迟加载

对于不在视口内的跑马灯组件，可以使用延迟加载策略：

```typescript
@Component
struct LazyMarquee {
  @State isVisible: boolean = false;
  
  build() {
    Column() {
      if (this.isVisible) {
        MarqueeSection({ /* ... */ })
      } else {
        Text("加载中...")
      }
    }
    .onAppear(() => {
      setTimeout(() => {
        this.isVisible = true;
      }, 200); // 延迟200ms加载
    })
  }
}
```

### 8.3 合理设置动画参数

为了提高性能，应合理设置动画参数：

1. 避免过短的动画持续时间（duration不宜小于3000ms）
2. 避免过高的动画速度（tempo不宜大于2）
3. 避免过小的停顿时间（delayTime不宜小于500ms）

## 9. 总结

本文详细介绍了HarmonyOS NEXT跑马灯组件的实际应用场景和使用方法，包括票务信息、消息通知、新闻标题等典型场景的实现示例。通过这些示例，我们可以看到跑马灯组件在不同场景下的配置和使用方式，以及如何根据设备类型和屏幕方向进行适配。

跑马灯组件的灵活性使其能够适应各种应用场景，通过合理配置MarqueeAnimationModifier和MarqueeScrollModifier，可以实现不同的滚动效果和视觉体验。在实际应用中，应根据具体需求选择合适的配置参数，并注意性能优化，提供最佳的用户体验。

通过本系列教程的学习，相信读者已经掌握了HarmonyOS NEXT跑马灯组件的基本概念、实现原理、配置参数和实际应用方法，能够在自己的项目中灵活运用这一组件，实现各种文本滚动效果。
