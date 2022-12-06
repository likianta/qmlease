# 操作流程

下载 pyside6-essentials 到指定目录:

```shell
cd <sidework/pyside_package_tailor>
pip install pyside6-essentials -t venv/qt_for_python
```

此时将得到 `venv/qt_for_python/PySide6`. 将这个文件夹拷贝到 `dist/PySide6`.

**裁剪**

运行我们的裁剪程序:

```python
# 获取帮助
py -m pptailor -h
# 裁剪
py -m pptailor tailor dist/PySide6
```

它将会生成:

```
dist
|= PySide6  # 在这个目录下, 一些文件已经被 "删除" 了. 它的体积有了明显的下降.
|= deleted  # 所有被 "删除" 的文件, 会放在这里. 
   |# 它们在这里是平铺的结构, 多级路径被转换为 "--" 连接的顶层路径.
   |= examples
   |= plugins--sqldrivers
   |= resources
   |= translations
   |- opengl32sw.dll
   |- ...
```

**恢复**

如果要恢复, 即把 "deleted" 中的文件放回原处, 请运行:

```shell
py -m pptailor restore dist/PySide6
```

# 如何使用

将 `dist` 目录加入到 `sys.path` 中:

```python
import sys
sys.path.insert(0, '~/dist/')

# test
import PySide6
print(PySide6.__path__)
```

# 体积降低了多少?

以 6.4.1 为例观察:

- 原始体积
  - whl 文件: 77mb
  - 解压后: 195mb
- 裁剪后
  - 压缩前: 102mb
  - 普通压缩后: 34.5mb
  - 极限压缩后: 21mb

# 测试

- 在 `depsland/build/setup_wizard` 中测试通过.
- 在 `(private_project)/eye_diagram` 中测试通过.
