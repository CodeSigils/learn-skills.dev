---
name: html-to-pdf
description: 将 HTML 演示文稿（scroll-snap slides）导出为高清 PDF。逐页截图合成，保留动画最终态。当用户说「导出 PDF」「转 PDF」「生成 PDF」「打印」或需要将 HTML slides 分享为静态文件时使用。
---

# HTML Slides → PDF

将基于 scroll-snap 的 HTML 演示文稿导出为高清多页 PDF。

## 原理

浏览器的 `page.pdf()` 无法正确分页 scroll-snap 布局（所有 slide 堆在同一页或只渲染当前可见的）。本方案用 Puppeteer 逐页滚动截图（高 DPI），再用 pdf-lib 合成多页 PDF。

## 依赖

```bash
npm install puppeteer-core pdf-lib
```

系统需要 Chrome/Chromium。支持的路径（脚本会自动检测）：

| 系统 | 路径 |
|------|------|
| Linux | `/usr/bin/google-chrome`, `/usr/bin/chromium-browser`, `/usr/bin/chromium` |
| macOS | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` |
| macOS (Homebrew) | `/opt/homebrew/bin/chromium` |

## 使用流程

### 1. 启动本地 HTTP 服务

```bash
npx -y serve -l 8766 .
```

**不能用 `file://`**。Puppeteer 对本地文件协议有安全限制，字体和部分 CSS 功能也可能失效。

启动后验证：`curl -s http://localhost:8766/ | head -5` 确认有 HTML 输出。

### 2. 运行导出脚本

在 HTML 所在目录创建 `to-pdf.js`（见下方模板），然后执行：

```bash
node to-pdf.js <URL> <OUTPUT_PATH>
```

示例：

```bash
node to-pdf.js http://localhost:8766/qx-xunchang.html ./巡场观察笔记.pdf
```

控制分辨率（默认 2x = 2K）：

```bash
PDF_DPI=1 node to-pdf.js http://localhost:8766/my-slides ./output.pdf   # 标清
PDF_DPI=2 node to-pdf.js http://localhost:8766/my-slides ./output.pdf   # 2K（默认）
PDF_DPI=3 node to-pdf.js http://localhost:8766/my-slides ./output.pdf   # 接近 4K
```

### 3. 脚本模板

创建 `to-pdf.js`：

```javascript
const puppeteer = require('puppeteer-core');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');
const path = require('path');

const url = process.argv[2] || 'http://localhost:8766';
const output = process.argv[3] || 'output.pdf';
const DPI = parseInt(process.env.PDF_DPI || '2', 10);

function findChrome() {
  const candidates = [
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/opt/homebrew/bin/chromium',
  ];
  const found = candidates.find(p => fs.existsSync(p));
  if (!found) {
    console.error('Chrome/Chromium not found. Searched:', candidates.join(', '));
    process.exit(1);
  }
  return found;
}

(async () => {
  const startTime = Date.now();
  const chrome = findChrome();
  console.log(`Chrome: ${chrome}`);

  const browser = await puppeteer.launch({
    executablePath: chrome,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
    headless: 'new',
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: DPI });

  console.log(`Loading: ${url}`);
  try {
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
  } catch (err) {
    console.error(`Failed to load ${url}:`, err.message);
    console.error('Is the local HTTP server running? Try: npx -y serve -l 8766 .');
    await browser.close();
    process.exit(1);
  }

  // 等待字体加载完成
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));

  // 注入样式：隐藏导航 UI、禁用 scroll-snap、强制所有动画到完成态
  await page.evaluate(() => {
    // 隐藏导航元素（但不误伤 <section> 等内容标签）
    document.querySelectorAll('.nav-dots, .progress-bar, [class*="nav"]')
      .forEach(el => { if (el.tagName !== 'SECTION') el.style.display = 'none'; });

    // 强制所有 slide 标记为 visible
    document.querySelectorAll('.slide, section[data-slide]')
      .forEach(s => s.classList.add('visible'));

    const style = document.createElement('style');
    style.textContent = `
      /* 禁用 scroll-snap，防止截图时滚动偏移 */
      html { scroll-snap-type: none !important; scroll-behavior: auto !important; }
      .slide, section[data-slide] { scroll-snap-align: unset !important; }

      /* 强制所有 reveal 动画到完成态 */
      .reveal, .reveal-left, .reveal-scale, .reveal-blur,
      [class*="reveal"] {
        opacity: 1 !important; transform: none !important;
        filter: none !important; transition: none !important;
      }

      /* 条形图、区间图等数据可视化 */
      .bar-value { width: var(--w) !important; transition: none !important; }
      .range-bar, [class*="bar"] { opacity: 1 !important; transition: none !important; }
      [class*="gap-bar"] { opacity: 0.85 !important; animation: none !important; }
    `;
    document.head.appendChild(style);
  });
  await new Promise(r => setTimeout(r, 1000));

  const slides = await page.$$('.slide, section[data-slide]');
  const slideCount = slides.length;

  if (slideCount === 0) {
    console.error('No slides found. Check that your HTML uses .slide or section[data-slide] elements.');
    await browser.close();
    process.exit(1);
  }

  console.log(`Found ${slideCount} slides, DPI=${DPI}x (${1920 * DPI}×${1080 * DPI}px)`);

  const pdfDoc = await PDFDocument.create();
  const title = await page.title();
  if (title) pdfDoc.setTitle(title);

  for (let i = 0; i < slideCount; i++) {
    await page.evaluate(idx => {
      document.querySelectorAll('.slide, section[data-slide]')[idx]
        .scrollIntoView({ behavior: 'instant' });
    }, i);
    await new Promise(r => setTimeout(r, 600));

    const pngBuf = await page.screenshot({ type: 'png' });
    const img = await pdfDoc.embedPng(pngBuf);
    const p = pdfDoc.addPage([1920, 1080]);
    p.drawImage(img, { x: 0, y: 0, width: 1920, height: 1080 });
    console.log(`  Slide ${i + 1}/${slideCount} ✓`);
  }

  const pdfBytes = await pdfDoc.save();
  const outputDir = path.dirname(output);
  if (outputDir && !fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  fs.writeFileSync(output, pdfBytes);

  const sizeMB = (pdfBytes.length / 1024 / 1024).toFixed(1);
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`\nPDF saved: ${output}`);
  console.log(`  ${slideCount} pages, ${sizeMB} MB, ${elapsed}s`);

  await browser.close();
})();
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `deviceScaleFactor` | 渲染倍率。`1`=标清(1920×1080), `2`=2K/Retina(3840×2160), `3`=接近4K |
| `PDF_DPI` 环境变量 | 同上，可通过 `PDF_DPI=3 node to-pdf.js ...` 设置 |
| viewport `width/height` | PDF 页面尺寸（点），16:9 用 1920×1080 |

## 注意事项

- **HTTP 必须** — HTML 必须通过 HTTP 服务，不能用 `file://`，否则字体加载和部分 CSS 功能会失效
- **每页 100vh** — 每个 slide 的高度应为 `100vh`，截图按视口大小裁切
- **字体需联网** — Google Fonts 等需联网加载。离线环境需提前缓存或改用本地字体
- **scroll-snap 必须禁用** — 脚本注入的 CSS 会自动禁用 scroll-snap，否则 `scrollIntoView` 可能偏移到相邻 slide
- **`--font-render-hinting=none`** — Chrome 启动参数，确保字体渲染在无显示器的服务器上也清晰，避免 hinting 导致的锯齿
- **生成时间** — 约 1-2 秒/页，12 页约 20 秒。DPI 越高图片越大，生成越慢
- **data 可视化** — 脚本会强制 `.bar-value`、`.range-bar` 等动画元素到完成态。如有自定义动画类名，需在注入 CSS 中补充
