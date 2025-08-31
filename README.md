# 瀑布流图片画廊 (Waterfall Image Gallery)

这是一个响应式的、可筛选的瀑布流图片画廊项目。它能够自动扫描图片目录，生成数据，并通过一个美观的界面进行展示。项目内置了 GitHub Actions 自动化流程，使得图片的更新和数据管理变得非常简单。

![项目截图](image_2b46ba.jpg)

---

## ✨ 主要功能

- **响应式瀑布流布局**: 在不同尺寸的屏幕上都能完美展示图片，优化浏览体验。
- **分类筛选**: 支持根据图片的分类进行筛选，并支持“全部”和“随机”模式。
- **中文分类显示**: 即使目录名是英文，也可以通过配置文件在界面上显示为中文。
- **图片懒加载**: 提升页面加载速度和性能，只有当图片滚动到视口时才进行加载。
- **灯箱效果**: 点击图片可放大查看，支持键盘左右键切换、触摸滑动切换和下载。
- **自动化数据生成**: 使用 Python 脚本自动扫描 `images` 目录，提取图片尺寸等信息并生成 `JSON` 数据文件。
- **GitHub Actions 自动化**: 当你向 `main` 分支推送新的图片时，GitHub Actions 会自动运行 Python 脚本并提交更新后的数据文件，实现完全自动化。

---

## 📂 项目结构

.
├── .github/workflows/
│   └── generate-image-list.yml  # GitHub Actions 配置文件
├── data/
│   └── image-data.json          # 自动生成的图片数据文件
├── images/
│   ├── anime/                   # 图片分类目录 (英文)
│   │   └── ...
│   └── scenery/                 # 图片分类目录 (英文)
│       └── ...
├── category_map.json            # 分类目录名与显示名的映射配置
├── generate_list.py             # 用于生成图片数据的 Python 脚本
├── index.html                   # 主画廊页面
└── README.md                    # 项目说明文件


---

## 🚀 如何使用

### 本地运行

1.  **添加图片**: 将你的图片文件放入 `images/` 目录下。建议按类别分文件夹存放，**文件夹名请使用英文、数字或短横线** (例如 `anime`, `scenery`, `wallpapers`)。
2.  **配置分类名称**: 打开 `category_map.json` 文件，添加你的英文文件夹名与希望显示的中文名称的对应关系。
    ```json
    {
      "anime": "二次元",
      "scenery": "风景"
    }
    ```
3.  **安装依赖**: 运行 Python 脚本需要 `Pillow` 库来读取图片信息。
    ```bash
    pip install Pillow
    ```
4.  **生成数据**: 运行 Python 脚本来更新图片数据。
    ```bash
    python generate_list.py
    ```
    脚本会自动在 `data/` 目录下生成或更新 `image-data.json` 文件。
5.  **查看效果**: 在浏览器中打开 `index.html` 文件即可看到你的图片画廊。（推荐使用 VS Code 的 `Live Server` 插件来运行，以获得最佳体验）。

### 通过 GitHub 自动化 (推荐)

本项目已经配置好了 GitHub Actions，你可以享受更流畅的更新体验：

1.  **添加/删除图片**: 在你的本地 `images` 目录下添加、删除或修改图片。
2.  **更新分类 (如果需要)**: 如果你新增了分类目录，请记得同步更新 `category_map.json` 文件。
3.  **提交与推送**: 将你的改动提交并推送到 GitHub 仓库的 `main` 分支。
    ```bash
    git add .
    git commit -m "feat: add new images"
    git push origin main
    ```
4.  **完成**: 推送完成后，GitHub Actions 会自动在云端运行 `generate_list.py` 脚本，并将更新后的 `data/image-data.json` 文件自动提交回你的仓库。你无需在本地运行 Python 脚本。

---

## 🎨 自定义

所有的样式都写在 `index.html` 文件头部的 `<style>` 标签中。你可以直接修改里面的 CSS 变量或样式规则来调整画廊的外观，例如主题颜色、间距、字体等。
```css
:root {
    --bg-color: #f0fdf4;
    --primary-color: #22c55e;
    /* ... 更多变量 ... */
}
