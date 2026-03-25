---
name: web-components
description: Build reusable, encapsulated UI components using native Web Components APIs — no framework required. Covers Custom Elements, Shadow DOM, HTML Templates, Slots, lifecycle callbacks, and styling with CSS encapsulation. Use this skill whenever the user mentions web components, custom elements, shadow DOM, HTML templates or slots, `customElements.define`, `attachShadow`, `connectedCallback`, or wants to create reusable HTML elements without React, Vue, Angular, or other frameworks. Also triggers on requests for framework-free component architecture, vanilla JS components, or encapsulated UI widgets.
---

# Web Components (No Framework)

Build reusable, encapsulated UI components using only the browser's native APIs.

Web Components consist of three core technologies:

| Technology | Purpose |
|------------|---------|
| **Custom Elements** | Define new HTML tags with custom behavior |
| **Shadow DOM** | Encapsulate markup and styles from the rest of the page |
| **HTML Templates & Slots** | Declare reusable markup structures with composable content |

> **Reference:** [MDN Web Components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components)

---

## Custom Elements

### Anatomy of a Custom Element

Every custom element is a JavaScript class extending `HTMLElement`. The name **must contain a hyphen** (e.g., `my-widget`, `app-header`).

```js
class MyComponent extends HTMLElement {
  // Observed attributes trigger attributeChangedCallback
  static observedAttributes = ["variant", "size"];

  constructor() {
    super();
    // Attach shadow DOM in the constructor or connectedCallback
    this.attachShadow({ mode: "open" });
  }

  connectedCallback() {
    // Element added to DOM — set up rendering, listeners, etc.
    this.render();
  }

  disconnectedCallback() {
    // Clean up: remove listeners, cancel timers, etc.
  }

  adoptedCallback() {
    // Element moved to a new document (rare)
  }

  attributeChangedCallback(name, oldValue, newValue) {
    // Respond to attribute changes — re-render, update state, etc.
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        :host { display: block; }
        .inner { padding: 1rem; }
      </style>
      <div class="inner">
        <slot></slot>
      </div>
    `;
  }
}

customElements.define("my-component", MyComponent);
```

### Registration

```js
// Autonomous custom element
customElements.define("my-component", MyComponent);

// Customized built-in element (limited Safari support)
customElements.define("fancy-button", FancyButton, { extends: "button" });
```

Use autonomous custom elements for broad compatibility. Customized built-in elements (`extends`) are not supported in Safari.

### Lifecycle Callbacks

| Callback | When it fires |
|----------|---------------|
| `constructor()` | Element created. Call `super()` first. Don't inspect attributes or children here. |
| `connectedCallback()` | Added to DOM. Primary setup point — render, attach listeners. |
| `disconnectedCallback()` | Removed from DOM. Tear down listeners, observers, timers. |
| `attributeChangedCallback(name, old, new)` | An observed attribute changed. Only fires for attributes listed in `static observedAttributes`. |
| `adoptedCallback()` | Moved to a new document via `document.adoptNode()`. |
| `connectedMoveCallback()` | Moved via `element.moveBefore()` without disconnect/reconnect cycle. |

### Responding to Attributes

Only attributes listed in `observedAttributes` trigger `attributeChangedCallback`:

```js
class StatusBadge extends HTMLElement {
  static observedAttributes = ["status"];

  attributeChangedCallback(name, oldValue, newValue) {
    if (name === "status") {
      this.shadowRoot.querySelector(".badge").textContent = newValue;
      this.shadowRoot.querySelector(".badge").className = `badge ${newValue}`;
    }
  }
}
```

Reflect properties to attributes for HTML-driven configuration:

```js
get status() {
  return this.getAttribute("status");
}

set status(val) {
  this.setAttribute("status", val);
}
```

---

## Shadow DOM

Shadow DOM provides encapsulation — styles and markup inside the shadow tree don't leak out, and external styles don't leak in.

### Creating a Shadow Root

```js
// Imperative (JavaScript)
const shadow = this.attachShadow({ mode: "open" });

// Declarative (HTML) — useful for SSR
// <my-component>
//   <template shadowrootmode="open">
//     <p>I'm in the shadow DOM</p>
//   </template>
// </my-component>
```

Use `mode: "open"` unless you have a specific reason to use `"closed"` — closed shadow roots are not a security boundary and complicate debugging.

### Encapsulation Rules

| What | Encapsulated? |
|------|---------------|
| CSS selectors | Yes — page styles don't reach in, shadow styles don't leak out |
| `document.querySelector()` | Yes — can't find shadow DOM nodes |
| `element.shadowRoot.querySelector()` | Reaches into open shadow roots |
| JavaScript events | Bubble out by default, but `event.composedPath()` may be truncated for closed roots |
| Inherited CSS properties (`color`, `font-family`, etc.) | No — these inherit through the shadow boundary |

---

## HTML Templates & Slots

### Templates

`<template>` elements hold inert HTML that's cloned at runtime — never rendered until you explicitly insert the content:

```js
const template = document.getElementById("card-template");
const clone = template.content.cloneNode(true);
this.shadowRoot.appendChild(clone);
```

### Slots — Composable Content

Slots let consumers inject their own content into your component's shadow DOM:

```html
<!-- Component template -->
<template id="card-template">
  <style>
    .card { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; }
  </style>
  <div class="card">
    <h2><slot name="title">Default Title</slot></h2>
    <div class="body">
      <slot>Default body content</slot>
    </div>
    <footer>
      <slot name="actions"></slot>
    </footer>
  </div>
</template>
```

```html
<!-- Usage -->
<my-card>
  <span slot="title">Product Name</span>
  <p>This goes in the default (unnamed) slot.</p>
  <button slot="actions">Buy Now</button>
</my-card>
```

| Slot type | Behavior |
|-----------|----------|
| Named (`<slot name="x">`) | Filled by children with `slot="x"` attribute |
| Default / unnamed (`<slot>`) | Catches all children without a `slot` attribute |
| Fallback content | Text inside `<slot>` shown when no content is provided |

### Listening for Slot Changes

```js
this.shadowRoot.querySelector("slot").addEventListener("slotchange", (e) => {
  const assigned = e.target.assignedNodes({ flatten: true });
  console.log("Slot content changed:", assigned);
});
```

---

## Styling

### CSS Encapsulation Overview

Shadow DOM scopes styles automatically. Use these selectors to style from inside and outside:

| Selector | Where it's used | What it does |
|----------|----------------|--------------|
| `:host` | Inside shadow DOM | Styles the host element itself |
| `:host(.active)` | Inside shadow DOM | Styles the host when it matches a selector |
| `:host-context(.dark)` | Inside shadow DOM | Styles the host when an ancestor matches |
| `::slotted(span)` | Inside shadow DOM | Styles slotted (light DOM) elements (top-level only) |
| `::part(label)` | Outside shadow DOM | Styles shadow DOM elements with `part="label"` |

### :host and :host-context

```css
/* Inside shadow DOM */
:host {
  display: block;
  font-family: system-ui, sans-serif;
}

:host([size="large"]) {
  font-size: 1.5rem;
}

:host-context(.dark-theme) {
  background: #1a1a1a;
  color: #f0f0f0;
}
```

### CSS Parts — Styling from Outside

Expose internal elements for external styling:

```js
// Inside shadow DOM template
`<button part="trigger">Click me</button>
 <div part="panel">Panel content</div>`
```

```css
/* Consumer's stylesheet */
my-dropdown::part(trigger) {
  background: navy;
  color: white;
}
```

### Constructable Stylesheets

Share styles across multiple components efficiently:

```js
const shared = new CSSStyleSheet();
shared.replaceSync(`
  :host { display: block; box-sizing: border-box; }
  *, *::before, *::after { box-sizing: inherit; }
`);

class MyComponent extends HTMLElement {
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: "open" });
    shadow.adoptedStyleSheets = [shared, componentStyles];
  }
}
```

---

## Accessibility

Web components require explicit accessibility work because shadow DOM can obscure semantic information from assistive technology.

### ARIA and Shadow DOM

ARIA attribute references (`aria-labelledby`, `aria-describedby`, `aria-controls`) **do not cross shadow boundaries** by default. Use these strategies:

```js
connectedCallback() {
  const shadow = this.attachShadow({ mode: "open" });

  // Strategy 1: Set ARIA on the host element (in light DOM)
  this.setAttribute("role", "tablist");
  this.setAttribute("aria-label", "Navigation tabs");

  // Strategy 2: Use ElementInternals for form-associated components
  // this._internals = this.attachInternals();
}
```

### Focus Management

Use `delegatesFocus` to automatically forward focus into the shadow tree:

```js
this.attachShadow({ mode: "open", delegatesFocus: true });
```

Ensure interactive elements inside the shadow DOM are keyboard-navigable:

```html
<!-- Inside shadow template -->
<button part="close" aria-label="Close dialog">×</button>
```

### Form-Associated Custom Elements

Make custom elements work with `<form>`, validation, and `FormData`:

```js
class MyInput extends HTMLElement {
  static formAssociated = true;

  constructor() {
    super();
    this._internals = this.attachInternals();
    this.attachShadow({ mode: "open" });
  }

  connectedCallback() {
    this.shadowRoot.innerHTML = `
      <label><slot></slot></label>
      <input type="text">
    `;
    const input = this.shadowRoot.querySelector("input");
    input.addEventListener("input", () => {
      this._internals.setFormValue(input.value);
    });
  }

  // Participate in form validation
  get validity() { return this._internals.validity; }
  get validationMessage() { return this._internals.validationMessage; }
  checkValidity() { return this._internals.checkValidity(); }
  reportValidity() { return this._internals.reportValidity(); }
}

customElements.define("my-input", MyInput);
```

### Accessibility Checklist

- [ ] Assign appropriate `role` on the host or internal elements
- [ ] Provide `aria-label` or `aria-labelledby` for non-obvious components
- [ ] Ensure all interactive elements are keyboard-reachable
- [ ] Use `delegatesFocus: true` when the component wraps a single focusable element
- [ ] Use `ElementInternals` for form-associated components
- [ ] Test with a screen reader (VoiceOver, NVDA, JAWS)
- [ ] Ensure focus is visible (never suppress `:focus-visible` without a replacement)

---

## Complete Example

A fully encapsulated `<alert-banner>` component demonstrating all three technologies:

```js
// alert-banner.js
const template = document.createElement("template");
template.innerHTML = `
  <style>
    :host {
      display: block;
      font-family: system-ui, sans-serif;
    }

    .banner {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem 1rem;
      border-radius: 6px;
      border: 1px solid;
    }

    :host([variant="info"]) .banner {
      background: #e8f4fd;
      border-color: #b3d9f2;
      color: #0c5a97;
    }

    :host([variant="warning"]) .banner {
      background: #fff8e1;
      border-color: #ffe082;
      color: #8d6e00;
    }

    :host([variant="error"]) .banner {
      background: #fdecea;
      border-color: #f5c6cb;
      color: #a71d2a;
    }

    .icon { flex-shrink: 0; }
    .content { flex: 1; }

    button {
      background: none;
      border: none;
      cursor: pointer;
      font-size: 1.25rem;
      line-height: 1;
      padding: 0.25rem;
      color: inherit;
      opacity: 0.7;
    }

    button:hover,
    button:focus-visible {
      opacity: 1;
    }
  </style>

  <div class="banner" role="alert">
    <span class="icon" aria-hidden="true">
      <slot name="icon">ℹ️</slot>
    </span>
    <div class="content">
      <slot></slot>
    </div>
    <button part="close" aria-label="Dismiss">×</button>
  </div>
`;

class AlertBanner extends HTMLElement {
  static observedAttributes = ["variant"];

  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.shadowRoot.appendChild(template.content.cloneNode(true));
  }

  connectedCallback() {
    if (!this.hasAttribute("variant")) {
      this.setAttribute("variant", "info");
    }

    this.shadowRoot.querySelector("button").addEventListener("click", () => {
      this.dispatchEvent(new CustomEvent("dismiss", { bubbles: true }));
      this.remove();
    });
  }

  attributeChangedCallback(name, oldValue, newValue) {
    // Variant styles are handled via :host([variant]) CSS selectors
  }
}

customElements.define("alert-banner", AlertBanner);
```

```html
<!-- Usage -->
<alert-banner variant="warning">
  <span slot="icon">⚠️</span>
  Your session will expire in 5 minutes.
</alert-banner>
```

---

## Common Patterns

### Lazy Rendering

Defer heavy rendering until the element is visible:

```js
connectedCallback() {
  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      this.render();
      observer.disconnect();
    }
  });
  observer.observe(this);
}
```

### Custom Events

Communicate up the DOM tree with `CustomEvent`:

```js
this.dispatchEvent(new CustomEvent("item-selected", {
  bubbles: true,
  composed: true,  // crosses shadow boundary
  detail: { id: this.dataset.id }
}));
```

Set `composed: true` when events need to be heard outside the shadow root.

### Custom States

Expose internal states for CSS via `CustomStateSet`:

```js
class ToggleSwitch extends HTMLElement {
  constructor() {
    super();
    this._internals = this.attachInternals();
  }

  get checked() {
    return this._internals.states.has("checked");
  }

  set checked(flag) {
    flag ? this._internals.states.add("checked")
         : this._internals.states.delete("checked");
  }
}
```

```css
/* Style from outside */
toggle-switch:state(checked) {
  --track-color: green;
}
```

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Use `innerHTML` in the constructor | Render in `connectedCallback()` |
| Inspect attributes/children in constructor | Defer to `connectedCallback()` |
| Use `tabindex > 0` | Let natural DOM order manage focus |
| Skip `super()` in the constructor | Always call `super()` first |
| Forget to clean up in `disconnectedCallback` | Remove listeners, cancel timers, disconnect observers |
| Use closed shadow DOM for "security" | Use `mode: "open"` — closed is not a security boundary |
| Put ARIA id-references across shadow boundaries | Put ARIA on the host or use `ElementInternals` |

---

## Browser Support

All evergreen browsers support the full Web Components API:

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Custom Elements v1 | 54+ | 63+ | 10.1+ | 79+ |
| Shadow DOM v1 | 53+ | 63+ | 10+ | 79+ |
| HTML Templates | 26+ | 22+ | 8+ | 13+ |
| Slots | 53+ | 63+ | 10+ | 79+ |
| Constructable Stylesheets | 73+ | 101+ | 16.4+ | 79+ |
| Form-associated custom elements | 77+ | 98+ | 16.4+ | 79+ |
| Declarative Shadow DOM | 111+ | 123+ | 16.4+ | 111+ |
| Customized built-in elements | 54+ | 63+ | **No** | 79+ |
