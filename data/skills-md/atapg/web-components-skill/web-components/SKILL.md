---
name: web-components
description: Manage web components - create, style, and use custom HTML elements with shadow DOM and encapsulation. Triggered when user asks about creating custom elements, using shadow DOM, handling events, or integrating web components.
license: MIT
metadata:
  author: atapg
---

# Web Component Skills

Web components allow developers to create reusable, encapsulated HTML elements that can be used across different web applications. They provide a way to extend HTML with custom elements, shadow DOM, and templates, enabling better modularity and maintainability.

## Principles

1. **Encapsulation First** - Use shadow DOM to isolate component styles and markup
2. **Custom Elements** - Extend `HTMLElement` and register with `customElements.define()`
3. **Slots for Composition** - Use `<slot>` for content projection
4. **Events for Communication** - Dispatch custom events for parent-child communication
5. **Attributes for Configuration** - Use attributes for component props
6. **No Framework Lock-in** - Web components work with any framework or vanilla JS

### Creation & Basics → [creation.md](./rules/creation.md)

- **Use `customElements.define()` for registering custom elements.**
- **Invoke `attachShadow()` for creating shadow DOM.**
- **Create `template` element for defining component structure.**
- **Set `cloneNode(true)` for cloning template content.**
- **Set `mode: 'open'` for shadow root to make it accessible from outside.**

### Lifecycle & State Management → [lifecycle.md](./rules/lifecycle.md)

- **Use `connectedCallback()` for initialization and setup.**
- **Use `disconnectedCallback()` for cleanup and resource management.**
- **Use `attributeChangedCallback()` for observing attribute changes.**
- **Use `adoptedCallback()` for handling document adoption.**
- **Create getters and setters for property synchronization.**
- **Set `requestAnimationFrame()` for DOM updates in callbacks.**
- **Debounce expensive operations to avoid performance issues.**

### Events & Communication → [events.md](./rules/events.md)

- **Use `dispatchEvent()` for dispatching custom events.**
- **Use `addEventListener()` for listening to events.**
- **Always use `removeEventListener()` for removing event listeners on disconnect.**
- **Use `CustomEvent` for creating custom events with data.**
- **Use `detail` property for passing event data.**
- **Set `bubbles: true` for bubbling events up the DOM tree.**
- **Set `composed: true` for crossing shadow DOM boundaries.**
- **Use `preventDefault()` for preventing default browser behavior.**
- **Use `stopPropagation()` for stopping event propagation.**
- **Use `stopImmediatePropagation()` for stopping other listeners on the same element.**

### Slots and content projection → [slots.md](./rules/slots.md)

- **Use `<slot>` element for content projection.**
- **Add `name` attribute for named slots.**
- **Add `default` slot for fallback content.**
- **Use `assignedElements()` for accessing projected content.**
- **Use `assignedNodes()` for accessing projected nodes.**
- **Use `slotchange` event for detecting slot changes.**

### Performance optimization → [performance.md](./rules/performance.md)

- **Use `requestAnimationFrame()` for DOM updates in callbacks.**
- **Debounce expensive operations to avoid performance issues.**
- **Set `loading="lazy"` for lazy loading web components.**
- **Set `loading="eager"` for eager loading web components.**
- **Set `loading="auto"` for automatic loading web components.**
- **Use document fragments for batch updates.**

## Key Patterns

### Basic Component Structure

Basic component structure for scalable web components (Use this approach for all web components if user asks for clean, maintainable code or doesn't specify a particular approach)

**Note:** Install `jenkey2011.string-highlight` or relevant extension for syntax highlighting in the template.

```typescript
const template = `
  <div>
    Hello World!
  </div>

  <style>

  </style>
`;

class WebComponent extends HTMLElement {
	private template: HTMLTemplateElement;

	constructor() {
		super();
		this.attachShadow({ mode: 'open' });
		this.template = document.createElement('template');
		this.template.innerHTML = template;
		this.render();
	}

	private render() {
		const fragment = document.createDocumentFragment();
		fragment.appendChild(this.template.content.cloneNode(true));
		this.shadowRoot && this.shadowRoot.appendChild(fragment);
	}

	static get observedAttributes() {
		return [
			/** attribute names */
		];
	}

	private connectedCallback() {}

	private disconnectedCallback() {}

	private attributeChangedCallback(
		name: string,
		oldValue: string,
		newValue: string,
	) {
		if (oldValue === newValue) return;

		switch (name) {
			default:
				break;
		}
	}
}

customElements.define('web-component', WebComponent);
```

## Framework Integration

Web components can be integrated with various frameworks:

- **React**: Use `@lit/react` wrapper to use web components as React components
- **Vue**: Use `vue-web-component-wrapper` to wrap web components
- **Angular**: Use `@angular/elements` to convert components to web components
- **Svelte**: Use `svelte-web-components` to create web components

## Detailed References

- [Creation](./rules/creation.md) - Basic component structure and registration
- [Lifecycle & State Management](./rules/lifecycle.md) - Component lifecycle methods and state management
- [Events & Communication](./rules/events.md) - Event handling and communication patterns
- [Slots and content projection](./rules/slots.md) - Content projection and slot management
- [Performance optimization](./rules/performance.md) - Performance optimization techniques
