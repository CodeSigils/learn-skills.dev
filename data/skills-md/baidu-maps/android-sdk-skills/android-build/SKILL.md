---
name: android-build
description: Compiles Android projects via Gradle (gradlew). Use when building Android apps, running Gradle tasks, compiling Android projects, CI/CD for Android, or when the user mentions Android 编译、构建、build、gradle.
---

# Android 工程编译

通过 Gradle 命令行（`gradlew`）编译 Android 工程，适用于本地构建、脚本、CI/CD。

## 前置条件

- 已安装 **JDK**（Android 开发通常需 JDK 11 或 17，与项目 `compileSdk`/AGP 匹配）
- 工程根目录存在 **gradlew**（或可生成 Gradle Wrapper）
- 已配置 **ANDROID_HOME**（或 `sdk.dir` 在 `local.properties` 中）

## 基本命令

```bash
# 进入工程根目录（含 build.gradle / build.gradle.kts 的目录）
cd /path/to/YourAndroidProject

# 调试包（APK）
./gradlew assembleDebug

# 发布包（APK，需配置 signing）
./gradlew assembleRelease

# 全量构建（含测试）
./gradlew build
```

Windows 使用 `gradlew.bat`，例如：`gradlew.bat assembleDebug`。

## 常用任务

| 任务 | 说明 |
|------|------|
| `assembleDebug` | 打 Debug APK |
| `assembleRelease` | 打 Release APK |
| `build` | 编译 + 跑测试，产出 Debug/Release |
| `clean` | 清理 build 输出 |
| `installDebug` | 安装 Debug 到已连接设备/模拟器 |
| `bundleRelease` | 打 AAB（Google Play 上架用） |

## 清理后构建

```bash
./gradlew clean assembleDebug
# 或
./gradlew clean build
```

## 查看所有任务

```bash
./gradlew tasks
# 仅看应用相关
./gradlew tasks --group=build
```

## 常见问题

- **找不到 gradlew**：在工程根目录执行 `gradle wrapper` 生成（需本机已装 Gradle），或从其他 Android 项目复制 `gradlew`、`gradlew.bat`、`gradle/wrapper/`。
- **sdk.dir 未配置**：在工程根目录创建 `local.properties`，内容：`sdk.dir=/path/to/Android/sdk`（或设环境变量 ANDROID_HOME）。
- **JDK 版本不匹配**：用 `./gradlew -version` 查看所用 JVM；需与项目/AGP 要求一致（如 JDK 17）。
- **依赖下载失败**：检查网络与仓库配置（`repositories` 含 `google()`、`mavenCentral()` 等）。
- **CI 无交互**：可加 `-no-daemon`、`--no-build-cache` 等，避免守护进程与缓存导致环境差异。

## 更多参考

- 签名配置、AAB、多渠道与 CI 建议见 [reference.md](reference.md)
