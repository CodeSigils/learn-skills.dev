---
name: angular-di
description: "ALWAYS use when working with Angular Dependency Injection, providers, services, inject tokens, or hierarchical injection in Angular applications."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Dependency Injection

**Version:** Angular 21 (2025)
**Tags:** DI, Services, Providers, Tokens, inject()

**References:** [DI Guide](https://angular.dev/guide/di) • [API](https://angular.io/api/core) • [inject()](https://angular.io/api/core/inject)

## API Changes

This section documents recent version-specific API changes.

- NEW: Functional injection with inject() — Preferred over constructor injection in modern Angular [source](https://medium.com/tenantcloud-engineering/understanding-dependency-injection-in-angular-constructor-injection-vs-5c75f0226f70)

- NEW: inject() with Optional decorator — `inject(Service, { optional: true })`

- NEW: inject() with SkipSelf — `inject(Service, { skipSelf: true })`

- NEW: Tree-shakable InjectionToken — `new InjectionToken<T>(desc, { providedIn: 'root' })`

## Best Practices

- Use providedIn: 'root' for singleton services

```ts
@Injectable({ providedIn: 'root' })
export class LoggerService {
  log(message: string) { console.log(message); }
}
```

- Use inject() function for cleaner code

```ts
@Component({})
export class MyComponent {
  private service = inject(MyService);
  private router = inject(Router);
}
```

- Use InjectionToken for non-class dependencies

```ts
export const API_URL = new InjectionToken<string>('apiUrl');

providers: [
  { provide: API_URL, useValue: 'https://api.example.com' }
]

constructor(@Inject(API_URL) private apiUrl: string) {}
```

- Use factory providers for complex instantiation

```ts
providers: [
  {
    provide: AuthService,
    useFactory: (http: HttpClient, config: AppConfig) => {
      return new AuthService(http, config.apiUrl);
    },
    deps: [HttpClient, APP_CONFIG]
  }
]
```

- Use multi providers for multiple implementations

```ts
providers: [
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
  { provide: HTTP_INTERCEPTORS, useClass: LogInterceptor, multi: true }
]
```

- Use @Optional for optional dependencies

```ts
constructor(@Optional() private logger: LoggerService) {
  this.logger?.log('Optional dependency');
}
```

- Use @SkipSelf to avoid self-injection

```ts
constructor(@SkipSelf() @Optional() private parent: ParentService) {}
```

- Use forwardRef for circular dependencies

```ts
constructor(@Inject(forwardRef(() => ParentService)) private parent: ParentService) {}
```

- Use hierarchical injectors for scoping

```ts
// Component-level provider
@Component({
  providers: [MyService]
})
export class MyComponent {}

// Lazy-loaded module provider
@Injectable({ providedIn: MyModule })
export class MyService {}
```

- Use interface injection pattern

```ts
export interface CacheInterface {
  get(key: string): any;
}

export const CACHE_TOKEN = new InjectionToken<CacheInterface>('cache');
```

- Use providedIn: 'any' for lazy-loaded services

```ts
@Injectable({ providedIn: 'any' })
export class LazyService {}
```
