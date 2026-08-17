---
name: lime-echart
description: Provides comprehensive guidance for Lime ECharts including chart creation, configuration, data visualization, and interactive charts. Use when the user asks about Lime ECharts, needs to create charts, visualize data, or work with ECharts features.
license: Complete terms in LICENSE.txt
---

## When to use this skill

Use this skill whenever the user wants to:
- Create ECharts charts in UniApp or UniAppX projects
- Display data visualizations (line charts, bar charts, pie charts, etc.) in H5, mini-programs, or App
- Configure and customize ECharts charts for cross-platform compatibility
- Integrate ECharts into UniApp/UniAppX applications
- Handle chart events and interactions in UniApp/UniAppX
- Optimize chart performance in mobile environments
- Use advanced ECharts features in UniApp/UniAppX

## How to use this skill

To use lime-echart in UniApp/UniAppX projects:

1. **Install and configure** lime-echart:
   - Load `examples/getting-started/installation.md` for installation instructions
   - Load `examples/getting-started/basic-usage.md` for basic setup and configuration
   - Load `examples/getting-started/configuration.md` for detailed configuration options

2. **Choose the chart type** based on the user's requirements:
   - Line chart/折线图 → `examples/charts/line-chart.md`
   - Bar chart/柱状图 → `examples/charts/bar-chart.md`
   - Pie chart/饼图 → `examples/charts/pie-chart.md`
   - Scatter chart/散点图 → `examples/charts/scatter-chart.md`
   - Radar chart/雷达图 → `examples/charts/radar-chart.md`
   - Gauge chart/仪表盘 → `examples/charts/gauge-chart.md`
   - Funnel chart/漏斗图 → `examples/charts/funnel-chart.md`
   - Heatmap/热力图 → `examples/charts/heatmap.md`
   - Tree chart/树图 → `examples/charts/tree-chart.md`
   - Map chart/地图 → `examples/charts/map-chart.md`
   - Candlestick chart/K线图 → `examples/charts/candlestick-chart.md`
   - Boxplot chart/箱线图 → `examples/charts/boxplot-chart.md`

3. **Load the appropriate example file** from the `examples/` directory:
   - `examples/getting-started/installation.md` - Installation and setup
   - `examples/getting-started/basic-usage.md` - Basic usage examples
   - `examples/getting-started/configuration.md` - Configuration options
   - `examples/charts/line-chart.md` - Line chart examples
   - `examples/charts/bar-chart.md` - Bar chart examples
   - `examples/charts/pie-chart.md` - Pie chart examples
   - `examples/charts/scatter-chart.md` - Scatter chart examples
   - `examples/charts/radar-chart.md` - Radar chart examples
   - `examples/charts/gauge-chart.md` - Gauge chart examples
   - `examples/charts/funnel-chart.md` - Funnel chart examples
   - `examples/charts/heatmap.md` - Heatmap examples
   - `examples/charts/tree-chart.md` - Tree chart examples
   - `examples/charts/map-chart.md` - Map chart examples
   - `examples/charts/candlestick-chart.md` - Candlestick chart examples
   - `examples/charts/boxplot-chart.md` - Boxplot chart examples
   - `examples/advanced/dynamic-data.md` - Dynamic data updates
   - `examples/advanced/event-handling.md` - Chart event handling
   - `examples/advanced/custom-theme.md` - Custom theme configuration
   - `examples/advanced/multiple-charts.md` - Multiple charts on one page
   - `examples/advanced/responsive-charts.md` - Responsive chart design
   - `examples/advanced/performance-optimization.md` - Performance optimization

4. **Follow the specific instructions** in that example file for syntax, structure, and best practices

5. **Reference the API documentation** when needed:
   - `api/component-api.md` - Component API reference
   - `api/methods-api.md` - Methods API reference
   - `api/events-api.md` - Events API reference
   - `api/options-api.md` - Options API reference

6. **Use templates** for quick start:
   - `templates/basic-chart.md` - Basic chart template
   - `templates/advanced-chart.md` - Advanced chart template
   - `templates/chart-with-data.md` - Chart with data binding template


### Doc mapping (one-to-one with official documentation)

- See examples and API files → https://ext.dcloud.net.cn/plugin?id=4899

## Examples and Templates

This skill includes detailed examples organized to match the official documentation structure. All examples are in the `examples/` directory (see mapping above).

**To use examples:**
- Identify the topic from the user's request
- Load the appropriate example file from the mapping above
- Follow the instructions, syntax, and best practices in that file
- Adapt the code examples to your specific use case

**To use templates:**
- Reference templates in `templates/` directory for common scaffolding
- Adapt templates to your specific needs and coding style

## API Reference

- **Component API**: `api/component-api.md` - lime-echart component properties and attributes
- **Methods API**: `api/methods-api.md` - Available methods for chart manipulation
- **Events API**: `api/events-api.md` - Chart events and event handling
- **Options API**: `api/options-api.md` - ECharts options configuration reference

## Best Practices

1. **Platform Compatibility**: Test charts on all target platforms (H5, mini-programs, App)
2. **Performance**: Use lazy loading for charts and optimize data volume
3. **Responsive Design**: Ensure charts adapt to different screen sizes
4. **Data Format**: Validate and format data before passing to charts
5. **Error Handling**: Implement proper error handling for chart initialization and data loading
6. **Memory Management**: Dispose charts properly when components are destroyed
7. **Theme Consistency**: Use consistent themes across your application
8. **Accessibility**: Consider accessibility when designing charts

## Resources

- **Official Plugin**: https://ext.dcloud.net.cn/plugin?id=4899
- **ECharts Official Documentation**: https://echarts.apache.org/
- **UniApp Documentation**: https://uniapp.dcloud.net.cn/
- **UniAppX Documentation**: https://uniapp.dcloud.net.cn/uni-app-x/

## Keywords

lime-echart, echart, echarts, uniapp, uniappx, chart, visualization, line chart, bar chart, pie chart, scatter chart, radar chart, gauge chart, funnel chart, heatmap, tree chart, map chart, candlestick chart, boxplot chart, 图表, 折线图, 柱状图, 饼图, 散点图, 雷达图, 仪表盘, 漏斗图, 热力图, 树图, 地图, K线图, 箱线图

## 能力边界

### ✅ 适用场景
- 当你需要使用此技能对应的技术栈时
- 当项目需要遵循最佳实践时
- 当需要快速上手或深入理解核心概念时

### ⚠️ 需要注意
- 复杂业务逻辑需要结合具体场景调整
- 性能优化需要根据实际数据量评估

### ❌ 不适用场景
- 不相关的技术栈或框架
- 需要完全自定义的特殊场景

## 常见陷阱 (Gotchas)

1. **版本兼容性**：注意框架版本与依赖库的兼容性，不同版本 API 可能有差异
2. **配置文件格式**：配置文件格式错误是最常见的问题，建议使用编辑器的语法检查
3. **环境变量**：确保所有必要的环境变量已正确设置，敏感信息不要硬编码
4. **依赖冲突**：多版本共存时注意依赖冲突，使用 lock 文件锁定版本
5. **性能陷阱**：大数据量场景下注意性能优化，避免 N+1 查询等常见问题

## 使用流程

### Step 1: 环境准备
确保开发环境已安装必要的依赖和工具。

### Step 2: 配置初始化
根据项目需求进行基础配置。

### Step 3: 核心功能使用
按照示例代码实现核心功能。

### Step 4: 测试验证
运行测试确保功能正常。

### Step 5: 部署上线
完成开发后进行部署和监控。
