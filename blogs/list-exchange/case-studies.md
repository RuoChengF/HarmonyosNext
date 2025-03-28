> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/e7866215-2919-4450-90eb-21112b7974a1.png)
# HarmonyOS NEXT系列教程之列表交换组件实战应用案例
## 效果演示

![](https://files.mdnice.com/user/47561/82592202-671d-445a-8eee-e36ca4d748dc.gif)
## 1. 银行卡管理场景

### 1.1 基础实现
```typescript
@Component
struct BankCardManager {
    @State cardList: BankCard[] = [];
    private cardController: ListExchangeCtrl<BankCard> = new ListExchangeCtrl();

    build() {
        Column() {
            ListExchange({
                items: this.cardList,
                listExchangeCtrl: this.cardController,
                deductionView: this.cardItemBuilder
            })
        }
    }

    @Builder
    cardItemBuilder(card: BankCard) {
        Row() {
            Image(card.bankIcon)
                .width(40)
                .height(40)
            Column() {
                Text(card.bankName)
                    .fontSize(16)
                Text(card.cardNumber)
                    .fontSize(14)
                    .opacity(0.6)
            }
            .margin({ left: 12 })
        }
        .width('100%')
        .padding(16)
    }
}
```

### 1.2 数据模型
```typescript
class BankCard {
    id: string;
    bankName: string;
    cardNumber: string;
    bankIcon: Resource;
    isDefault: boolean;

    constructor(data: Partial<BankCard>) {
        Object.assign(this, data);
    }
}
```

## 2. 待办事项列表

### 2.1 组件实现
```typescript
@Component
struct TodoList {
    @State todoItems: TodoItem[] = [];
    private todoController: ListExchangeCtrl<TodoItem> = new ListExchangeCtrl();

    build() {
        Column() {
            ListExchange({
                items: this.todoItems,
                listExchangeCtrl: this.todoController,
                deductionView: this.todoItemBuilder
            })
            .onItemDelete((item: TodoItem) => {
                this.handleDelete(item);
            })
            .onItemMove((from: number, to: number) => {
                this.handlePriorityChange(from, to);
            })
        }
    }

    @Builder
    todoItemBuilder(item: TodoItem) {
        Row() {
            Checkbox()
                .select(item.completed)
                .onChange((value: boolean) => {
                    this.toggleComplete(item, value);
                })
            Text(item.title)
                .decoration({ type: item.completed ? 
                    TextDecorationType.LineThrough : 
                    TextDecorationType.None 
                })
            Text(item.dueDate)
                .fontSize(12)
        }
        .width('100%')
        .padding(16)
    }
}
```

### 2.2 业务逻辑
```typescript
class TodoManager {
    // 切换完成状态
    toggleComplete(item: TodoItem, completed: boolean) {
        item.completed = completed;
        this.updateItem(item);
    }

    // 处理优先级变更
    handlePriorityChange(fromIndex: number, toIndex: number) {
        const priority = this.calculatePriority(toIndex);
        this.todoItems[fromIndex].priority = priority;
        this.sortItems();
    }

    // 计算优先级
    private calculatePriority(index: number): number {
        const step = 100;
        return (index + 1) * step;
    }
}
```

## 3. 音乐播放列表

### 3.1 组件实现
```typescript
@Component
struct MusicPlaylist {
    @State tracks: MusicTrack[] = [];
    private playlistController: ListExchangeCtrl<MusicTrack> = new ListExchangeCtrl();

    build() {
        Column() {
            ListExchange({
                items: this.tracks,
                listExchangeCtrl: this.playlistController,
                deductionView: this.trackItemBuilder
            })
            .onItemMove((from: number, to: number) => {
                this.updatePlayOrder(from, to);
            })
        }
    }

    @Builder
    trackItemBuilder(track: MusicTrack) {
        Row() {
            Image(track.albumCover)
                .width(50)
                .height(50)
                .borderRadius(8)
            Column() {
                Text(track.title)
                    .fontSize(16)
                Text(`${track.artist} · ${track.album}`)
                    .fontSize(14)
                    .opacity(0.6)
            }
            .margin({ left: 12 })
            Image($r('app.media.ic_play'))
                .width(24)
                .height(24)
                .onClick(() => this.playTrack(track))
        }
        .width('100%')
        .padding(16)
    }
}
```

### 3.2 播放控制
```typescript
class PlaylistController {
    private audioPlayer: AudioPlayer = new AudioPlayer();

    // 播放音乐
    async playTrack(track: MusicTrack) {
        await this.audioPlayer.stop();
        await this.audioPlayer.src(track.url);
        await this.audioPlayer.play();
    }

    // 更新播放顺序
    updatePlayOrder(fromIndex: number, toIndex: number) {
        this.savePlaylistOrder();
        this.updateNowPlaying();
    }
}
```

## 4. 照片相册管理

### 4.1 组件实现
```typescript
@Component
struct PhotoAlbum {
    @State photos: PhotoItem[] = [];
    private albumController: ListExchangeCtrl<PhotoItem> = new ListExchangeCtrl();

    build() {
        Column() {
            ListExchange({
                items: this.photos,
                listExchangeCtrl: this.albumController,
                deductionView: this.photoItemBuilder
            })
            .onItemDelete((item: PhotoItem) => {
                this.deletePhoto(item);
            })
        }
    }

    @Builder
    photoItemBuilder(photo: PhotoItem) {
        Stack() {
            Image(photo.url)
                .width('100%')
                .height(200)
                .objectFit(ImageFit.Cover)
            Column() {
                Text(photo.date)
                Text(photo.location)
            }
            .position({ x: 8, y: 8 })
        }
        .width('100%')
    }
}
```

### 4.2 图片处理
```typescript
class PhotoManager {
    // 删除照片
    async deletePhoto(photo: PhotoItem) {
        try {
            await this.deleteFromStorage(photo);
            await this.removeFromAlbum(photo);
            this.updateThumbnails();
        } catch (error) {
            console.error('Failed to delete photo:', error);
        }
    }

    // 优化图片加载
    private optimizeImage(url: string): Promise<string> {
        return ImageOptimizer.process(url, {
            maxWidth: 800,
            quality: 0.8,
            format: 'webp'
        });
    }
}
```

## 5. 性能优化实践

### 5.1 图片优化
```typescript
class ImageOptimizer {
    private static cache: Map<string, string> = new Map();

    static async loadOptimized(url: string): Promise<string> {
        if (this.cache.has(url)) {
            return this.cache.get(url);
        }

        const optimized = await this.processImage(url);
        this.cache.set(url, optimized);
        return optimized;
    }

    static clearCache() {
        this.cache.clear();
    }
}
```

### 5.2 列表优化
```typescript
// 虚拟列表优化
@Component
struct OptimizedList {
    private virtualListController: VirtualListController = new VirtualListController();

    build() {
        List() {
            LazyForEach(this.virtualListController, (item: any) => {
                ListItem() {
                    this.itemBuilder(item)
                }
            })
        }
        .onScrollIndex((first: number) => {
            this.virtualListController.loadMore(first);
        })
    }
}
```

## 6. 最佳实践总结

### 6.1 实现建议
1. 根据业务场景选择合适的交互方式
2. 优化图片和资源加载
3. 实现错误处理和恢复机制
4. 提供良好的用户反馈

### 6.2 性能建议
1. 使用虚拟列表处理大量数据
2. 实现图片懒加载和缓存
3. 优化动画和交互效果
4. 合理管理内存资源

## 7. 小结

本篇教程详细介绍了：
1. 银行卡管理的实现方案
2. 待办事项列表的开发方法
3. 音乐播放列表的实现细节
4. 照片相册的优化策略
5. 实际应用中的最佳实践

这些实战案例将帮助你更好地理解和使用ListExchange组件。
