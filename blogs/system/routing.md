 
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](../images/img_dc63209e.png)

# HarmonyOS NEXT 路由导航与页面管理：构建清晰的应用架构
 

## 1. 路由系统基础

### 1.1 基本概念

| 概念 | 说明 | 使用场景 |
|------|------|----------|
| 页面路由 | 页面间跳转管理 | 应用内导航 |
| 路由栈 | 页面访问历史记录 | 返回管理 |
| 路由参数 | 页面间数据传递 | 信息共享 |

### 1.2 路由配置

```typescript
// pages.json
{
  "pages": [
    {
      "path": "pages/index",
      "component": "Index"
    },
    {
      "path": "pages/detail",
      "component": "Detail"
    }
  ]
}

// 路由管理类
class RouterManager {
  // 路由配置
  private static routes = new Map<string, any>();
  
  // 注册路由
  static register(path: string, component: any) {
    this.routes.set(path, component);
  }
  
  // 获取路由组件
  static getComponent(path: string) {
    return this.routes.get(path);
  }
}
```

## 2. 页面管理机制

### 2.1 页面生命周期

```typescript
@Entry
@Component
struct PageLifecycleDemo {
  @State message: string = 'Hello';
  
  // 页面显示时触发
  onPageShow() {
    console.log('Page is shown');
  }
  
  // 页面隐藏时触发
  onPageHide() {
    console.log('Page is hidden');
  }
  
  // 页面销毁时触发
  onBackPress() {
    console.log('Back pressed');
    return false;
  }
  
  build() {
    Column() {
      Text(this.message)
    }
  }
}
```

### 2.2 页面栈管理

```typescript
class PageStackManager {
  private static pageStack: Array<string> = [];
  
  // 添加页面到栈
  static push(path: string) {
    this.pageStack.push(path);
  }
  
  // 从栈中移除页面
  static pop() {
    return this.pageStack.pop();
  }
  
  // 获取当前页面
  static getCurrentPage() {
    return this.pageStack[this.pageStack.length - 1];
  }
  
  // 清空页面栈
  static clear() {
    this.pageStack = [];
  }
}
```

## 3. 导航模式实现

### 3.1 基本导航

```typescript
@Component
struct NavigationDemo {
  // 页面跳转
  navigateToDetail() {
    router.push({
      url: 'pages/detail',
      params: {
        id: '123'
      }
    });
  }
  
  // 返回上一页
  goBack() {
    router.back();
  }
  
  build() {
    Column() {
      Button('Go to Detail')
        .onClick(() => this.navigateToDetail())
      
      Button('Go Back')
        .onClick(() => this.goBack())
    }
  }
}
```

### 3.2 高级导航功能

```typescript
class NavigationService {
  // 替换当前页面
  static replace(url: string, params?: object) {
    router.replace({
      url,
      params
    });
  }
  
  // 清空栈并跳转
  static relaunch(url: string) {
    router.clear();
    router.push({
      url
    });
  }
  
  // 返回到指定页面
  static backTo(url: string) {
    while (PageStackManager.getCurrentPage() !== url) {
      if (PageStackManager.pageStack.length <= 1) {
        break;
      }
      router.back();
    }
  }
}
```

## 4. 参数传递与处理

### 4.1 参数传递方式

```typescript
@Component
struct ParameterDemo {
  // 1. URL参数传递
  navigateWithQuery() {
    router.push({
      url: 'pages/detail?id=123&type=product'
    });
  }
  
  // 2. 对象参数传递
  navigateWithParams() {
    router.push({
      url: 'pages/detail',
      params: {
        id: '123',
        type: 'product'
      }
    });
  }
}

// 参数接收页面
@Entry
@Component
struct DetailPage {
  @State private params: any = router.getParams();
  
  build() {
    Column() {
      Text(`ID: ${this.params.id}`)
      Text(`Type: ${this.params.type}`)
    }
  }
}
```

### 4.2 参数管理器

```typescript
class ParameterManager {
  private static params = new Map<string, any>();
  
  // 设置页面参数
  static setPageParams(pageId: string, params: any) {
    this.params.set(pageId, params);
  }
  
  // 获取页面参数
  static getPageParams(pageId: string) {
    return this.params.get(pageId);
  }
  
  // 清理页面参数
  static clearPageParams(pageId: string) {
    this.params.delete(pageId);
  }
}
```

## 5. 实战案例

### 5.1 电商应用导航实现

```typescript
@Component
struct ECommerceNavigation {
  // 商品列表页
  navigateToProducts() {
    router.push({
      url: 'pages/products',
      params: {
        category: 'electronics'
      }
    });
  }
  
  // 商品详情页
  navigateToProductDetail(productId: string) {
    router.push({
      url: 'pages/product/detail',
      params: {
        id: productId
      }
    });
  }
  
  // 购物车页面
  navigateToCart() {
    router.push({
      url: 'pages/cart'
    });
  }
  
  // 结算页面
  navigateToCheckout() {
    router.push({
      url: 'pages/checkout',
      params: {
        from: 'cart'
      }
    });
  }
  
  build() {
    Column() {
      // 导航栏实现
      Row() {
        Button('Products')
          .onClick(() => this.navigateToProducts())
        Button('Cart')
          .onClick(() => this.navigateToCart())
      }
    }
  }
}
```

### 5.2 路由守卫实现

```typescript
class RouterGuard {
  // 前置守卫
  static async beforeEach(to: string, from: string) {
    // 检查用户登录状态
    if (needsAuth(to) && !isLoggedIn()) {
      // 重定向到登录页
      router.push({
        url: 'pages/login',
        params: {
          redirect: to
        }
      });
      return false;
    }
    return true;
  }
  
  // 后置守卫
  static afterEach(to: string, from: string) {
    // 记录路由历史
    console.log(`Navigation: ${from} -> ${to}`);
  }
}

// 路由守卫使用
class NavigationWithGuard {
  static async navigate(url: string) {
    const currentPage = PageStackManager.getCurrentPage();
    
    // 执行前置守卫
    const canProceed = await RouterGuard.beforeEach(url, currentPage);
    if (!canProceed) {
      return;
    }
    
    // 执行导航
    router.push({
      url
    });
    
    // 执行后置守卫
    RouterGuard.afterEach(url, currentPage);
  }
}
```

### 5.3 最佳实践建议

1. **路由组织**
   - 使用清晰的路由结构
   - 实现路由守卫机制
   - 管理路由参数传递

2. **页面管理**
   - 合理控制页面栈深度
   - 及时清理不需要的页面
   - 优化页面切换性能

3. **参数处理**
   - 规范参数传递格式
   - 实现参数验证
   - 处理参数丢失情况

4. **性能优化**
   - 预加载关键页面
   - 实现页面缓存
   - 优化转场动画

通过合理的路由导航和页面管理，可以构建出结构清晰、导航流畅的应用。在实际开发中，要注意平衡用户体验和性能消耗，确保应用的整体表现良好。
