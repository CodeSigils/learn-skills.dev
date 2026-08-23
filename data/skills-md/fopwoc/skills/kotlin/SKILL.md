---
name: kotlin
description: >
  General Kotlin engineering conventions. Use for all Kotlin code.
---

# General

- Prefer idiomatic Kotlin over Java-style code. Embrace Kotlin syntax sugar and expressive language features to write elegant code.
- Keep the file's `package` declaration consistent with its actual path within the module.
- Do not add command-line properties, system properties, or Gradle property passthrough for application startup unless I explicitly ask for it.
- Always verify that your changes compile without errors. Use `./gradlew`.

# Multiplatform

Backend projects are JVM-only by default unless I explicitly ask otherwise.

Android apps, including Jetpack Compose apps, should always use a Kotlin Multiplatform project structure, even when Android is currently the only target.

- For platform-specific functionality, define the API in common code and keep platform details behind it. Platform code should provide an implementation of the common API. Design the boundary so adding another platform does not require changing common consumers.

# KSP

When KSP is used, prefer compile-time type relationships over names, strings, configuration keys, or conventions.

- Never identify Kotlin types by string classpaths when the relationship can be expressed through Kotlin types, annotations, inheritance, generics, or KSP symbols.
- Design annotations and user-facing APIs so referenced types are supplied as actual Kotlin types and can be resolved by KSP from the annotated symbol.
- Prefer marker interfaces, base types, generic constraints, typed annotations, and inheritance when they let KSP discover relationships statically.
- Let KSP derive names and types from symbols instead of requiring developers to repeat information as strings.
- Use KotlinPoet `ClassName`, `TypeName`, and symbol-derived type information. Do not construct type references from hardcoded qualified names when they can be obtained from declarations.

## KSP module structure

For reusable KSP-based functionality, separate responsibilities into three modules:

- **Library/runtime module:** public APIs, interfaces, base types, helpers, and runtime functionality used by generated and consumer code.
- **Annotations module:** lightweight annotations and annotation-facing types required by consumer source code.
- **Processor module:** KSP processor and code generation implementation.

Keep the processor an implementation detail. Consumer/runtime code must not depend on it.

Keep annotations lightweight and independent from processor implementation.

Generated code should integrate through the typed APIs provided by the library/runtime module rather than duplicating runtime behavior.
