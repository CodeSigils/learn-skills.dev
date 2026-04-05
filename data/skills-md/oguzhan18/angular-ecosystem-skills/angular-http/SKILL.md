---
name: angular-http
description: "ALWAYS use when working with Angular HttpClient, HTTP requests, interceptors, error handling, or API communication in Angular applications."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# @angular/common/http

**Version:** Angular 21 (2025)
**Tags:** HTTP, REST, API, Interceptors

**References:** [HttpClient](https://angular.dev/guide/http) • [API](https://angular.io/api/common/http) • [Interceptors](https://angular.dev/guide/http/interceptors)

## API Changes

This section documents recent version-specific API changes.

- NEW: Functional interceptors — Use `provideHttpClient(withInterceptors([...]))` for modern interceptor setup [source](https://dev.to/cristiansifuentes/angular-20-httpclient-interceptors-functional-predictable-and-powerful-kdf)

- NEW: `withFetch` — Use native fetch API with HttpClient [source](https://angular.dev/guide/http)

- NEW: `withInterceptorsFromDi` — Legacy interceptor support with functional approach

- NEW: HttpContext tokens — Per-request metadata using HttpContextToken

- NEW: `AbortSignal` support — Request cancellation with timeout support

- DEPRECATED: Class-based HttpInterceptor — Migrate to functional interceptors

## Best Practices

- Use functional interceptors

```ts
// ✅ Modern functional interceptor
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();
  
  if (token) {
    const authReq = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
    return next(authReq);
  }
  return next(req);
};

// Register
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(withInterceptors([authInterceptor]))
  ]
};
```

- Use interceptors for cross-cutting concerns — Authentication, logging, error handling

```ts
// Error interceptor with retry
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        inject(Router).navigate(['/login']);
      }
      return throwError(() => error);
    })
  );
};
```

- Use retry with backoff for flaky networks

```ts
import { retry, delay, catchError } from 'rxjs/operators';

http.get('/api/data').pipe(
  retry({ count: 3, delay: 1000 })
);
```

- Use HttpContext for per-request flags

```ts
const cacheToken = new HttpContextToken<boolean>(() => false);

export const cacheInterceptor: HttpInterceptorFn = (req, next) => {
  if (req.context.get(cacheToken)) {
    // Check cache
  }
  return next(req);
};

// Usage
http.get('/api/data', {
  context: new HttpContext().set(cacheToken, true)
});
```

- Use proper typing for HTTP responses

```ts
interface User {
  id: number;
  name: string;
}

http.get<User>('/api/user/1').subscribe(user => {
  console.log(user.name); // TypeScript knows the type
});
```

- Use `observe: 'response'` for full HTTP response

```ts
http.get('/api/data', { observe: 'response' }).subscribe(response => {
  console.log(response.headers);
  console.log(response.body);
});
```

- Handle errors globally

```ts
@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  handleError(error: Error) {
    // Log to error tracking service
    console.error(error);
  }
}

// Register
provideErrorHandler(GlobalErrorHandler)
```

- Use `withCredentials` for CORS requests

```ts
http.get('/api/data', { withCredentials: true });
```
