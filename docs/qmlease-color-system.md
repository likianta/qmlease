# QmlEase 配色系统

## 设计理论

挑选一个具有高辨识度的颜色作为颜色种子, 我们可以生产以下类型的颜色:

- surface: 界面背景色, 非常浅的颜色
- panel: ...
- on_surface: 对界面背景色对抗的前景色, 通常用于直接书写在界面上的文字内容.
- container: 容器背景色, 较界面背景色更深一些.
- on_container: 与容器背景色对抗的前景色, 通常用于直接书写在容器上的文字内容.
- outline: 边框色.
- primary: 主色调.
- secondary: 次色调, 稍弱于主色调.
- tertiary: 次次色调, 更弱于次色调.
- burst: 激发色调, 在主色调的基础上拉高亮度和饱和, 可能刺激眼睛, 需要谨慎使用.
- inverse: 反色.

我们会用一个检查器来判断用户选取的强调色是否符合要求. 通常来说, 具有辨识度的颜色会被接受.

除了主色调外, 我们另外准备了其他颜色种子来生成其所对应的系列:

- 红色种子: 表示错误.
- 绿色种子: 表示成功.
- 黄色种子: 表示警告.
- 蓝色种子: 表示信息.
- 紫色种子: 表示负面信息或引人关注的严肃内容.
- 灰色种子: 用于生成中性色.

默认配色中, 这些种子由我根据个人喜好选取, 我不使用标准色 (例如 `#FF0000`) 作为种子色, 而是使用观感舒适的颜色.

## 相对颜色变体

- alt
- var
- higher
- lower
- neutral
- tint

## 颜色生成器

...

---

[## HCT]

HCT 指 Hue, Chroma, Tone, 分别代表色相 (什么颜色), 色度 (颜色浓度), 明度 (颜色亮度).

[## Role]

格式: [<type>_<part>_<variant>]

示例: [
    main
    main_container
    main_border
    main_text

    error
    error_container
    error_border
    error_text
    info...
    success...
    warning...
    comment...

    text_primary
    text_secondary
    text_tertiary
    text_error
    text_info
    ...

    surface
    surface_higher
    surface_highest

    main_border
    main_border_higher
    main_border_highest
]

补充说明: [
    - [*_higher] 和 [*_lighter] 表达相同的含义
        [
            info_container_higher
            info_container_lighter
        ]
    - [*_lower] 和 [*_darker] 表达相同的含义
        [
            info_container_lower
            info_container_darker
        ]
]

[## 问答]

[
    Q: 如果已有的色彩不够用, 怎么创建新的颜色?
    A: ...
]

[## 其他]

[### 关于 Material You Colors 的意见]

目前遇到的一些痛点: [
    = [~~ 输入框的容器背景色找不到合适的低对比度的灰色 (如下图所示)]
]
