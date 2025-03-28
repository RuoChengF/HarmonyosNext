 
> 温馨提示：本篇博客的详细代码已发布到 [git](https://gitcode.com/nutpi/HarmonyosNext) : https://gitcode.com/nutpi/HarmonyosNext 可以下载运行哦！

![](../images/img_fb03dd9d.png)

# HarmonyOS NEXT 网络请求与数据处理：构建可靠的数据层
 

## 1. 网络请求基础

### 1.1 基本概念

| 概念 | 说明 | 使用场景 |
|------|------|----------|
| HTTP请求 | 基本的网络通信 | API调用 |
| WebSocket | 双向实时通信 | 即时消息 |
| 数据序列化 | 数据格式转换 | 请求/响应处理 |

### 1.2 HTTP请求封装

```typescript
class HttpClient {
  private static instance: HttpClient;
  private baseUrl: string;
  
  private constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }
  
  static getInstance(baseUrl: string): HttpClient {
    if (!this.instance) {
      this.instance = new HttpClient(baseUrl);
    }
    return this.instance;
  }
  
  // GET请求
  async get<T>(url: string, params?: object): Promise<T> {
    const queryString = params ? 
      `?${new URLSearchParams(params).toString()}` : '';
    
    const response = await fetch(
      `${this.baseUrl}${url}${queryString}`,
      {
        method: 'GET',
        headers: this.getHeaders()
      }
    );
    
    return this.handleResponse<T>(response);
  }
  
  // POST请求
  async post<T>(url: string, data?: object): Promise<T> {
    const response = await fetch(
      `${this.baseUrl}${url}`,
      {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(data)
      }
    );
    
    return this.handleResponse<T>(response);
  }
  
  private getHeaders(): object {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.getToken()}`
    };
  }
  
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  }
  
  private getToken(): string {
    // 从存储中获取token
    return '';
  }
}
```

## 2. 数据处理机制

### 2.1 数据转换

```typescript
// 数据模型定义
interface UserDTO {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

class User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
  
  constructor(dto: UserDTO) {
    this.id = dto.id;
    this.name = dto.name;
    this.email = dto.email;
    this.createdAt = new Date(dto.created_at);
  }
}

// 数据转换器
class DataTransformer {
  // DTO到模型的转换
  static toModel<T, U>(dto: T, ModelClass: new (dto: T) => U): U {
    return new ModelClass(dto);
  }
  
  // 批量转换
  static toModelList<T, U>(
    dtoList: T[], 
    ModelClass: new (dto: T) => U
  ): U[] {
    return dtoList.map(dto => this.toModel(dto, ModelClass));
  }
}
```

### 2.2 数据验证

```typescript
class DataValidator {
  // 验证规则定义
  private static rules = {
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    phone: /^\d{10}$/,
    required: (value: any) => value !== undefined && value !== null
  };
  
  // 验证单个字段
  static validate(
    value: any, 
    rule: keyof typeof DataValidator.rules
  ): boolean {
    const validator = this.rules[rule];
    if (typeof validator === 'function') {
      return validator(value);
    }
    return validator.test(value);
  }
  
  // 验证对象
  static validateObject(
    obj: object, 
    schema: Record<string, Array<keyof typeof DataValidator.rules>>
  ): boolean {
    for (const [key, rules] of Object.entries(schema)) {
      for (const rule of rules) {
        if (!this.validate(obj[key], rule)) {
          return false;
        }
      }
    }
    return true;
  }
}
```

## 3. 缓存策略

### 3.1 内存缓存

```typescript
class MemoryCache<T> {
  private cache: Map<string, {
    data: T,
    timestamp: number,
    ttl: number
  }> = new Map();
  
  // 设置缓存
  set(key: string, data: T, ttl: number = 60000): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    });
  }
  
  // 获取缓存
  get(key: string): T | null {
    const item = this.cache.get(key);
    if (!item) return null;
    
    if (Date.now() - item.timestamp > item.ttl) {
      this.cache.delete(key);
      return null;
    }
    
    return item.data;
  }
  
  // 清除缓存
  clear(): void {
    this.cache.clear();
  }
}
```

### 3.2 持久化缓存

```typescript
class StorageCache {
  // 写入缓存
  static async set(key: string, data: any): Promise<void> {
    try {
      await localStorage.setItem(
        key,
        JSON.stringify({
          data,
          timestamp: Date.now()
        })
      );
    } catch (error) {
      console.error('Cache write error:', error);
    }
  }
  
  // 读取缓存
  static async get(key: string): Promise<any> {
    try {
      const cached = await localStorage.getItem(key);
      if (!cached) return null;
      
      const { data, timestamp } = JSON.parse(cached);
      return data;
    } catch (error) {
      console.error('Cache read error:', error);
      return null;
    }
  }
}
```

## 4. 错误处理

### 4.1 错误类型定义

```typescript
class NetworkError extends Error {
  constructor(
    public status: number,
    public message: string
  ) {
    super(message);
    this.name = 'NetworkError';
  }
}

class ValidationError extends Error {
  constructor(
    public field: string,
    public message: string
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}
```

### 4.2 错误处理器

```typescript
class ErrorHandler {
  // 处理网络错误
  static handleNetworkError(error: NetworkError): void {
    switch (error.status) {
      case 401:
        // 处理未授权
        this.handleUnauthorized();
        break;
      case 404:
        // 处理未找到
        this.handleNotFound();
        break;
      default:
        // 处理其他错误
        this.handleGenericError(error);
    }
  }
  
  // 处理验证错误
  static handleValidationError(error: ValidationError): void {
    // 显示错误信息
    console.error(`Validation error in ${error.field}: ${error.message}`);
  }
  
  private static handleUnauthorized(): void {
    // 重定向到登录页
    router.push({
      url: 'pages/login'
    });
  }
  
  private static handleNotFound(): void {
    // 显示404页面
    router.push({
      url: 'pages/404'
    });
  }
  
  private static handleGenericError(error: Error): void {
    // 显示通用错误提示
    console.error('An error occurred:', error);
  }
}
```

## 5. 实战案例

### 5.1 数据服务实现

```typescript
class UserService {
  private http = HttpClient.getInstance('https://api.example.com');
  private cache = new MemoryCache<User>();
  
  // 获取用户信息
  async getUser(id: string): Promise<User> {
    // 检查缓存
    const cached = this.cache.get(`user_${id}`);
    if (cached) return cached;
    
    try {
      // 发起请求
      const dto = await this.http.get<UserDTO>(`/users/${id}`);
      
      // 转换数据
      const user = DataTransformer.toModel(dto, User);
      
      // 缓存结果
      this.cache.set(`user_${id}`, user);
      
      return user;
    } catch (error) {
      if (error instanceof NetworkError) {
        ErrorHandler.handleNetworkError(error);
      }
      throw error;
    }
  }
  
  // 更新用户信息
  async updateUser(id: string, data: Partial<User>): Promise<User> {
    try {
      // 验证数据
      if (!DataValidator.validateObject(data, {
        email: ['email'],
        phone: ['phone']
      })) {
        throw new ValidationError('user', 'Invalid user data');
      }
      
      // 发起请求
      const dto = await this.http.put<UserDTO>(`/users/${id}`, data);
      
      // 转换并更新缓存
      const user = DataTransformer.toModel(dto, User);
      this.cache.set(`user_${id}`, user);
      
      return user;
    } catch (error) {
      if (error instanceof ValidationError) {
        ErrorHandler.handleValidationError(error);
      }
      throw error;
    }
  }
}
```

### 5.2 使用示例

```typescript
@Component
struct UserProfile {
  @State private user: User | null = null;
  private userService = new UserService();
  
  async aboutToAppear() {
    try {
      this.user = await this.userService.getUser('123');
    } catch (error) {
      console.error('Failed to load user:', error);
    }
  }
  
  build() {
    Column() {
      if (this.user) {
        Text(this.user.name)
        Text(this.user.email)
        Text(this.user.createdAt.toLocaleDateString())
      } else {
        LoadingComponent()
      }
    }
  }
}
```

### 5.3 最佳实践建议

1. **网络请求**
   - 统一封装请求客户端
   - 实现请求拦截器
   - 处理请求超时

2. **数据处理**
   - 规范数据转换流程
   - 实现数据验证
   - 处理数据一致性

3. **缓存策略**
   - 合理使用多级缓存
   - 实现缓存失效机制
   - 处理缓存同步

4. **错误处理**
   - 统一错误处理机制
   - 实现错误重试
   - 提供友好的错误提示

通过合理的网络请求和数据处理策略，可以构建出可靠、高效的数据层。在实际开发中，要注意平衡性能和可维护性，确保应用的数据处理流程清晰可控。
