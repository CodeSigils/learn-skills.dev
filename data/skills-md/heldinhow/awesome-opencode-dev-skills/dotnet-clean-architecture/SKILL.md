---
name: dotnet-clean-architecture
description: "Implement Clean Architecture in .NET with proper layer separation for maintainable applications."
---

# .NET Clean Architecture

## Overview
Clean Architecture organizes code into concentric layers with strict dependency rules, ensuring testability and maintainability. This skill should be invoked when building enterprise applications that require long-term maintainability, testability, and separation of concerns.

## Core Principles
- **Dependency Inversion**: Dependencies point inward - domain has no dependencies
- **Layered Structure**: Domain, Application, Infrastructure, Presentation
- **Business Logic in Domain**: Core business rules live in the domain layer
- **Abstractions**: Use interfaces to define boundaries

## Preparation Checklist
- [ ] Plan layer structure (Domain, Application, Infrastructure, Presentation)
- [ ] Define project structure
- [ ] Set up solution with multiple projects
- [ ] Configure dependency injection

## Step-by-Step Process
1. **Domain**: Create Domain project with entities and interfaces
2. **Application**: Build Application project with use cases and DTOs
3. **Infrastructure**: Implement Infrastructure for databases, external APIs
4. **Presentation**: Create API endpoints in Presentation layer
5. **Wire Up**: Configure DI with interface implementations
6. **Test**: Write unit tests for domain and application layers

## Do's and Don'ts
- ✅ **Do** keep domain layer free of external dependencies
- ✅ **Do** use interfaces for all external dependencies
- ✅ **Do** put business logic in application/domain layers
- ❌ **Don't** reference Infrastructure from Domain
- ❌ **Don't** mix concerns across layers
- ❌ **Don't** skip the abstraction layer

## Anti-Patterns
- **The Anemic Domain**: Domain entities with no behavior
- **Infrastructure Leak**: Infrastructure code in domain layer
- **Circular Dependencies**: Breaking layer dependency rules
- **Skipped Abstractions**: Direct dependencies on concrete implementations
