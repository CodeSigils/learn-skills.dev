---
name: angular-directives
description: "ALWAYS use when working with Angular Directives, custom directives, attribute directives, structural directives, or directive composition in Angular applications."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Directives

**Version:** Angular 21 (2025)
**Tags:** Directives, Components, DOM, Custom Directives

**References:** [Directives Guide](https://angular.dev/guide/directives) • [Attribute Directives](https://angular.dev/guide/directives/attribute-directives) • [Structural Directives](https://angular.dev/guide/directives/structural-directives)

## API Changes

This section documents recent version-specific API changes.

- NEW: Directive composition API — Use `hostDirectives` to compose directives [source](https://angular.dev/guide/directives)

- NEW: Signal inputs in directives — Use `input()` for reactive directive properties

- NEW: Standalone directives — All directives can be standalone

- NEW: Control flow syntax — @if, @for, @switch replace *ngIf, *ngFor

## Best Practices

- Create attribute directives for reusable behavior

```ts
import { Directive, ElementRef, Renderer2, Input } from '@angular/core';

@Directive({
  selector: '[appHighlight]'
})
export class HighlightDirective {
  @Input() set appHighlight(color: string) {
    this.renderer.setStyle(this.el.nativeElement, 'background-color', color || 'yellow');
  }

  constructor(private el: ElementRef, private renderer: Renderer2) {}
}
```

- Use @Input and @Output for directive communication

```ts
@Directive({
  selector: '[appClickTracker]'
})
export class ClickTrackerDirective {
  @Input() trackName = 'default';
  @Output() clicked = new EventEmitter<string>();

  @HostListener('click')
  onClick() {
    this.clicked.emit(this.trackName);
  }
}
```

- Use TemplateRef for structural directives

```ts
import { Directive, Input, TemplateRef, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[appUnless]'
})
export class UnlessDirective {
  @Input() set appUnless(condition: boolean) {
    if (!condition) {
      this.vcRef.createEmbeddedView(this.templateRef);
    } else {
      this.vcRef.clear();
    }
  }

  constructor(
    private templateRef: TemplateRef<any>,
    private vcRef: ViewContainerRef
  ) {}
}
```

- Use ViewContainerRef for complex structural logic

```ts
@Directive({ selector: '[appDynamic]' })
export class DynamicDirective {
  constructor(
    private vcr: ViewContainerRef,
    private templateRef: TemplateRef<any>
  ) {
    this.vcr.createEmbeddedView(this.templateRef);
  }
}
```

- Use hostDirectives for composition

```ts
@Component({
  selector: 'app-card',
  standalone: true,
  imports: [HighlightDirective],
  hostDirectives: [
    {
      directive: HighlightDirective,
      inputs: ['appHighlight: highlight']
    }
  ],
  template: `<ng-content></ng-content>`
})
export class CardComponent {}
```

- Use standalone: true for modern directives

```ts
@Directive({
  selector: '[appStandalone]',
  standalone: true
})
export class StandaloneDirective {}
```

- Use signals in directives

```ts
@Directive({
  selector: '[appSignal]'
})
export class SignalDirective {
  value = input<string>('');
  
  ngOnInit() {
    console.log(this.value());
  }
}
```

- Use @HostBinding for property binding

```ts
@Directive({
  selector: '[appDisable]'
})
export class DisableDirective {
  @Input() set disabled(value: boolean) {
    this.hostBinding.nativeElement.disabled = value;
  }
  
  constructor(private hostBinding: ElementRef) {}
}
```

- Keep directives focused — One responsibility

```ts
// ✅ Good - focused directive
@Directive({ selector: '[appTooltip]' })

// ❌ Bad - too many responsibilities
@Directive({ selector: '[appTooltip][appTooltipMaxWidth][appTooltipTheme]' })
```

- Use descriptive selectors

```ts
// ✅ Good
@Directive({ selector: '[appUserCard]' })

// ❌ Bad
@Directive({ selector: '[appUc]' })
```
