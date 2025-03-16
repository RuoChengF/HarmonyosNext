 
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](https://files.mdnice.com/user/47561/126db997-6496-421f-ae3f-38e29f3b7649.png)

# HarmonyOS NEXT 组件通信与状态共享：构建高效的组件协作机制

 

## 1. 组件通信基础

### 1.1 通信方式概述

| 通信方式 | 使用场景 | 优点 | 缺点 |
|---------|----------|------|------|
| 属性传递 | 父子组件 | 简单直接 | 层级限制 |
| 事件机制 | 子到父通信 | 解耦合 | 单向流动 |
| 状态管理 | 全局状态 | 统一管理 | 复杂度高 |
| 依赖注入 | 跨组件共享 | 高度解耦 | 配置繁琐 |

### 1.2 基本属性传递

```typescript
// 子组件
@Component
struct ChildComponent {
  @Prop title: string;  // 接收父组件传递的属性
  @State private count: number = 0;
  
  build() {
    Column() {
      Text(this.title)
      Button(`Count: ${this.count}`)
        .onClick(() => {
          this.count++;
        })
    }
  }
}

// 父组件
@Component
struct ParentComponent {
  @State private pageTitle: string = 'Hello';
  
  build() {
    Column() {
      ChildComponent({
        title: this.pageTitle
      })
    }
  }
}
```

## 2. 状态共享机制

### 2.1 状态管理器

```typescript
// 全局状态定义
class AppState {
  @Observed
  class UserState {
    isLoggedIn: boolean = false;
    username: string = '';
    preferences: Map<string, any> = new Map();
  }
  
  @Observed
  class ThemeState {
    isDark: boolean = false;
    primaryColor: string = '#000000';
    fontSize: number = 14;
  }
  
  user: UserState = new UserState();
  theme: ThemeState = new ThemeState();
}

// 状态管理器
class StateManager {
  private static instance: StateManager;
  private state: AppState = new AppState();
  
  static getInstance(): StateManager {
    if (!this.instance) {
      this.instance = new StateManager();
    }
    return this.instance;
  }
  
  getState(): AppState {
    return this.state;
  }
  
  // 更新用户状态
  updateUserState(updates: Partial<AppState['user']>) {
    Object.assign(this.state.user, updates);
  }
  
  // 更新主题状态
  updateThemeState(updates: Partial<AppState['theme']>) {
    Object.assign(this.state.theme, updates);
  }
}
```

### 2.2 状态注入与使用

```typescript
@Component
struct ThemeAwareComponent {
  @ObjectLink themeState: AppState['theme'];
  
  build() {
    Column() {
      Text('Current Theme')
        .fontSize(this.themeState.fontSize)
        .fontColor(this.themeState.primaryColor)
      
      Toggle({ type: ToggleType.Switch, isOn: this.themeState.isDark })
        .onChange((isOn: boolean) => {
          this.themeState.isDark = isOn;
        })
    }
  }
}
```

## 3. 事件总线实现

### 3.1 事件总线定义

```typescript
type EventCallback = (...args: any[]) => void;

class EventBus {
  private static instance: EventBus;
  private events: Map<string, Set<EventCallback>> = new Map();
  
  static getInstance(): EventBus {
    if (!this.instance) {
      this.instance = new EventBus();
    }
    return this.instance;
  }
  
  // 订阅事件
  on(event: string, callback: EventCallback): void {
    if (!this.events.has(event)) {
      this.events.set(event, new Set());
    }
    this.events.get(event).add(callback);
  }
  
  // 取消订阅
  off(event: string, callback: EventCallback): void {
    if (this.events.has(event)) {
      this.events.get(event).delete(callback);
    }
  }
  
  // 触发事件
  emit(event: string, ...args: any[]): void {
    if (this.events.has(event)) {
      this.events.get(event).forEach(callback => {
        callback(...args);
      });
    }
  }
}
```

### 3.2 事件总线使用

```typescript
@Component
struct EventComponent {
  private eventBus = EventBus.getInstance();
  @State private message: string = '';
  
  aboutToAppear() {
    // 订阅事件
    this.eventBus.on('updateMessage', (msg: string) => {
      this.message = msg;
    });
  }
  
  aboutToDisappear() {
    // 取消订阅
    this.eventBus.off('updateMessage', this.handleMessage);
  }
  
  build() {
    Column() {
      Text(this.message)
      Button('Send Message')
        .onClick(() => {
          this.eventBus.emit('updateMessage', 'Hello from EventBus!');
        })
    }
  }
}
```

## 4. 依赖注入

### 4.1 服务定义

```typescript
interface UserService {
  getCurrentUser(): Promise<User>;
  updateProfile(data: Partial<User>): Promise<void>;
}

@Injectable
class UserServiceImpl implements UserService {
  async getCurrentUser(): Promise<User> {
    // 实现获取用户信息的逻辑
    return null;
  }
  
  async updateProfile(data: Partial<User>): Promise<void> {
    // 实现更新用户信息的逻辑
  }
}

// 依赖注入容器
class Container {
  private static instance: Container;
  private services: Map<string, any> = new Map();
  
  static getInstance(): Container {
    if (!this.instance) {
      this.instance = new Container();
    }
    return this.instance;
  }
  
  // 注册服务
  register<T>(token: string, implementation: T): void {
    this.services.set(token, implementation);
  }
  
  // 获取服务
  resolve<T>(token: string): T {
    if (!this.services.has(token)) {
      throw new Error(`Service ${token} not found`);
    }
    return this.services.get(token);
  }
}
```

### 4.2 服务使用

```typescript
@Component
struct UserProfileComponent {
  @Inject('UserService') userService: UserService;
  @State private user: User = null;
  
  async aboutToAppear() {
    try {
      this.user = await this.userService.getCurrentUser();
    } catch (error) {
      console.error('Failed to load user:', error);
    }
  }
  
  build() {
    Column() {
      if (this.user) {
        Text(this.user.name)
        Button('Update Profile')
          .onClick(async () => {
            await this.userService.updateProfile({
              name: 'New Name'
            });
          })
      }
    }
  }
}
```

## 5. 实战案例

### 5.1 购物车状态管理

```typescript
// 购物车状态
@Observed
class CartState {
  items: Map<string, CartItem> = new Map();
  total: number = 0;
  
  addItem(item: Product, quantity: number = 1) {
    const cartItem = this.items.get(item.id) || {
      product: item,
      quantity: 0
    };
    cartItem.quantity += quantity;
    this.items.set(item.id, cartItem);
    this.calculateTotal();
  }
  
  removeItem(itemId: string) {
    this.items.delete(itemId);
    this.calculateTotal();
  }
  
  private calculateTotal() {
    this.total = Array.from(this.items.values())
      .reduce((sum, item) => 
        sum + item.product.price * item.quantity, 0);
  }
}

// 购物车组件
@Component
struct CartComponent {
  @ObjectLink cartState: CartState;
  
  build() {
    Column() {
      // 购物车列表
      List() {
        ForEach(Array.from(this.cartState.items.values()), 
          (item: CartItem) => {
          ListItem() {
            CartItemComponent({ item })
          }
        })
      }
      
      // 总计
      Row() {
        Text(`Total: $${this.cartState.total.toFixed(2)}`)
        Button('Checkout')
          .onClick(() => {
            // 处理结算逻辑
          })
      }
    }
  }
}
```

### 5.2 主题切换实现

```typescript
// 主题定义
interface Theme {
  primaryColor: string;
  backgroundColor: string;
  textColor: string;
  fontSize: {
    small: number;
    medium: number;
    large: number;
  };
}

// 主题服务
@Injectable
class ThemeService {
  private currentTheme: Theme;
  private eventBus = EventBus.getInstance();
  
  setTheme(theme: Theme) {
    this.currentTheme = theme;
    this.eventBus.emit('themeChanged', theme);
  }
  
  getTheme(): Theme {
    return this.currentTheme;
  }
}

// 主题感知组件
@Component
struct ThemeAwareButton {
  @Inject('ThemeService') themeService: ThemeService;
  private text: string;
  @State private theme: Theme;
  
  aboutToAppear() {
    this.theme = this.themeService.getTheme();
    EventBus.getInstance().on('themeChanged', 
      (newTheme: Theme) => {
        this.theme = newTheme;
      });
  }
  
  build() {
    Button(this.text)
      .backgroundColor(this.theme.primaryColor)
      .fontColor(this.theme.textColor)
      .fontSize(this.theme.fontSize.medium)
  }
}
```

### 5.3 表单状态管理

```typescript
// 表单状态
@Observed
class FormState {
  values: Map<string, any> = new Map();
  errors: Map<string, string> = new Map();
  isDirty: boolean = false;
  
  setValue(field: string, value: any) {
    this.values.set(field, value);
    this.isDirty = true;
    this.validate(field);
  }
  
  setError(field: string, error: string) {
    this.errors.set(field, error);
  }
  
  validate(field: string) {
    // 实现字段验证逻辑
  }
  
  isValid(): boolean {
    return this.errors.size === 0;
  }
}

// 表单组件
@Component
struct FormComponent {
  @ObjectLink formState: FormState;
  
  build() {
    Column() {
      TextInput({
        placeholder: 'Username'
      })
      .onChange((value: string) => {
        this.formState.setValue('username', value);
      })
      
      if (this.formState.errors.has('username')) {
        Text(this.formState.errors.get('username'))
          .fontColor(Color.Red)
      }
      
      Button('Submit')
        .enabled(this.formState.isValid())
        .onClick(() => {
          // 处理表单提交
        })
    }
  }
}
```

### 5.4 最佳实践建议

1. **状态管理**
   - 合理划分状态范围
   - 避免状态重复
   - 实现状态同步机制

2. **组件通信**
   - 选择合适的通信方式
   - 保持单向数据流
   - 避免过度耦合

3. **依赖注入**
   - 合理使用服务抽象
   - 实现依赖的解耦
   - 便于单元测试

4. **性能优化**
   - 避免不必要的状态更新
   - 合理使用事件解绑
   - 优化组件重渲染

通过合理使用组件通信和状态共享机制，可以构建出结构清晰、易于维护的应用。在实际开发中，要根据具体需求选择合适的通信方式，并注意性能优化和代码质量。
