 
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](../images/img_6f49328b.png)

#  Harmonyos NEXT图片预览组件应用实践（二）：电商、内容与办公场景
## 效果预览

![](../images/img_bd971de3.png)
## 一、电商应用最佳实践

### 1. 功能需求

电商应用中的商品图片预览需求包括：

1. 支持商品多角度图片查看
2. 高清缩放查看商品细节
3. 商品参数标注和热点标记
4. 与商品信息面板的联动
5. 支持视频和图片混合展示

### 2. 实现示例与代码解析

```typescript
@Entry
@Component
struct ProductImageViewer {
    @State imageList: string[] = [];  // 商品图片列表
    @State currentIndex: number = 0;  // 当前图片索引
    @State hotspots: Array<{x: number, y: number, text: string}> = [];  // 热点标记数据
    
    aboutToAppear(): void {
        this.loadProductImages();  // 加载商品图片
        this.setupHotspots();  // 设置热点标记
    }
    
    loadProductImages() {
        // 加载商品图片示例
        let imageSource1: string = $r("app.media.product1") as ESObject;
        let imageSource2: string = $r("app.media.product2") as ESObject;
        let imageSource3: string = $r("app.media.product3") as ESObject;
        
        this.imageList.push(imageSource1, imageSource2, imageSource3);
    }
    
    setupHotspots() {
        // 配置商品特点标记
        this.hotspots = [
            {x: 0.3, y: 0.4, text: "优质面料"},
            {x: 0.7, y: 0.6, text: "精细缝线"},
            {x: 0.5, y: 0.2, text: "时尚设计"}
        ];
    }
    
    build() {
        Stack() {
            // 核心预览组件
            PicturePreview({ 
                imageList: this.imageList, 
                listDirection: Axis.Horizontal 
            })
            
            // 热点标记渲染
            ForEach(this.hotspots, (hotspot) => {
                Button(hotspot.text)
                    .position({
                        x: `${hotspot.x * 100}%`,
                        y: `${hotspot.y * 100}%`
                    })
                    .backgroundColor('rgba(255, 255, 255, 0.7)')
                    .borderRadius(15)
            })
            
            // 底部缩略图导航
            Row() {
                ForEach(this.imageList, (image, index) => {
                    Image(image)
                        .width(60)
                        .height(60)
                        .margin(5)
                        .borderWidth(index === this.currentIndex ? 2 : 0)
                        .borderColor(Color.Blue)
                        .onClick(() => {
                            // 切换到对应图片
                        })
                })
            }
            .width('100%')
            .justifyContent(FlexAlign.Center)
            .position({ x: 0, y: '90%' })
        }
        .width('100%')
        .height('100%')
    }
}
```

#### 代码要点解析：

1. **数据结构设计**
   - 使用数组存储热点标记信息
   - 支持图片列表和缩略图管理

2. **布局实现**
   - 热点标记使用绝对定位
   - 缩略图导航固定在底部

3. **交互处理**
   - 支持缩略图切换
   - 热点标记点击响应

4. **样式优化**
   - 热点标记使用半透明背景
   - 当前选中缩略图高亮显示

### 3. 功能扩展建议

电商应用中的图片预览可以考虑以下功能扩展：

1. **AR试用**：结合AR技术，实现虚拟试穿、试用功能
2. **360度全景**：支持商品360度全景查看
3. **对比功能**：支持多商品图片对比
4. **颜色切换**：支持同一商品不同颜色的快速切换

## 二、内容平台最佳实践

### 1. 功能需求

内容平台中的图片预览需求包括：

1. 从文章内容中点击图片进入预览
2. 支持图片说明文字显示
3. 返回文章时恢复阅读位置
4. 支持保存和分享功能

### 2. 实现示例与代码解析

```typescript
@Entry
@Component
struct ArticleImageViewer {
    @State imageList: string[] = [];  // 文章图片列表
    @State captions: string[] = [];  // 图片说明列表
    @State isPreviewMode: boolean = false;  // 预览模式状态
    @State currentImageIndex: number = 0;  // 当前图片索引
    
    aboutToAppear(): void {
        this.loadArticleImages();  // 加载文章图片
    }
    
    loadArticleImages() {
        // 加载文章图片和说明
        let imageSource1: string = $r("app.media.article1") as ESObject;
        let imageSource2: string = $r("app.media.article2") as ESObject;
        
        this.imageList.push(imageSource1, imageSource2);
        this.captions.push("图1：项目概览图", "图2：详细设计图");
    }
    
    build() {
        Stack() {
            if (this.isPreviewMode) {
                // 图片预览模式
                Stack() {
                    PicturePreview({ 
                        imageList: this.imageList, 
                        listDirection: Axis.Horizontal 
                    })
                    
                    // 图片说明
                    Text(this.captions[this.currentImageIndex])
                        .fontSize(16)
                        .fontColor(Color.White)
                        .backgroundColor('rgba(0, 0, 0, 0.5)')
                        .padding(10)
                        .position({ x: 0, y: '90%' })
                        .width('100%')
                        .textAlign(TextAlign.Center)
                }
            } else {
                // 文章内容模式
                Column() {
                    // ... 文章内容渲染 ...
                }
            }
        }
    }
}
```

#### 代码要点解析：

1. **模式切换**
   - 使用`isPreviewMode`控制显示模式
   - 支持文章模式和预览模式切换

2. **UI布局**
   - 预览模式下使用全屏显示
   - 文章模式下保持正常排版

3. **图片说明**
   - 使用半透明背景增加可读性
   - 固定在底部显示

### 3. 优化建议

内容平台的图片预览优化建议：

1. **阅读位置记录**
   - 使用 ScrollController 记录位置
   - 返回时自动恢复阅读进度

2. **懒加载优化**
   - 仅加载可视区域图片
   - 滚动时动态加载新图片

3. **预加载策略**
   - 预加载相邻图片资源
   - 根据用户行为预测加载

4. **手势优化**
   - 支持左右滑动切换
   - 添加缩放和旋转手势

## 三、办公应用最佳实践

### 1. 功能需求详解

办公应用中的图片预览具有以下特点：

1. **文档集成**
   - 支持多种文档格式
   - 保持文档排版一致性

2. **协作功能**
   - 多人实时批注
   - 版本历史管理

3. **专业工具**
   - 测量和标注工具
   - 图片对比功能

4. **权限管理**
   - 查看权限控制
   - 编辑权限分级

### 2. 实现示例与代码解析

```typescript
@Entry
@Component
struct OfficeImageViewer {
    @State imageList: string[] = [];
    @State annotations: Array<{x: number, y: number, text: string}> = [];
    @State isEditMode: boolean = false;
    @State currentUser: string = "用户A";
    @State userPermission: string = "edit"; // edit, view
    
    aboutToAppear(): void {
        this.loadOfficeImages();
        this.loadAnnotations();
        this.checkUserPermission();
    }
    
    checkUserPermission() {
        // 检查用户权限
        // 实际应用中应该从服务器获取
        this.userPermission = "edit";
    }
    
    addAnnotation(x: number, y: number) {
        if (this.userPermission !== "edit") return;
        
        this.annotations.push({
            x: x,
            y: y,
            text: "新批注"
        });
    }
    
    build() {
        Stack() {
            // 图片预览基础组件
            PicturePreview({ 
                imageList: this.imageList,
                listDirection: Axis.Horizontal
            })
            
            if (this.isEditMode && this.userPermission === "edit") {
                // 编辑模式UI
                Column() {
                    // 批注列表
                    ForEach(this.annotations, (item) => {
                        Button(item.text)
                            .position({
                                x: `${item.x * 100}%`,
                                y: `${item.y * 100}%`
                            })
                            .backgroundColor('rgba(255, 255, 0, 0.7)')
                            .borderRadius(15)
                    })
                    
                    // 工具栏
                    Row() {
                        Button('添加批注')
                            .onClick(() => {
                                // 进入添加批注模式
                            })
                        Button('保存')
                        Button('分享')
                    }
                    .width('100%')
                    .justifyContent(FlexAlign.SpaceAround)
                    .position({ x: 0, y: '90%' })
                    .backgroundColor('rgba(0, 0, 0, 0.5)')
                    .padding(10)
                }
            }
            
            // 用户信息和权限提示
            Text(this.currentUser + (this.userPermission === "edit" ? " (可编辑)" : " (只读)"))
                .fontSize(14)
                .fontColor(Color.White)
                .backgroundColor('rgba(0, 0, 0, 0.5)')
                .padding(5)
                .position({ x: 10, y: 10 })
        }
        .width('100%')
        .height('100%')
        .gesture(
            TapGesture()
                .onAction((event: GestureEvent) => {
                    if (this.isEditMode) {
                        this.addAnnotation(
                            event.x / this.width,
                            event.y / this.height
                        );
                    }
                })
        )
    }
}
```

#### 代码要点解析：

1. **权限控制**
   - 用户权限状态管理
   - 基于权限的UI条件渲染

2. **批注功能**
   - 支持点击添加批注
   - 批注位置使用相对坐标

3. **手势处理**
   - 编辑模式下支持点击添加批注
   - 可扩展更多手势操作

4. **用户界面**
   - 清晰的权限提示
   - 直观的操作工具栏

### 3. 协作功能实现建议

1. **实时同步**
```typescript
class SyncManager {
    syncAnnotations(annotations: Array<any>) {
        // 向服务器同步批注数据
    }
    
    onAnnotationUpdate(callback: Function) {
        // 监听其他用户的更新
    }
}
```

2. **版本控制**
```typescript
class VersionControl {
    saveVersion() {
        // 保存当前版本
    }
    
    rollback(version: string) {
        // 回滚到指定版本
    }
}
```

## 四、总结 

通过以上最佳实践，开发者可以根据具体场景需求，灵活运用HarmonyOS图片预览组件，构建出功能丰富、性能优异的图片预览功能。
 