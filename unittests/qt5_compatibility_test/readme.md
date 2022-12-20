# How to test

1.  Set environment variable `QT_API`:

    ```shell
    export QT_API=pyqt5
    # or: export QT_API=pyside2
    ```

2.  Run script:

    ```shell
    # A.
    py unittests/qt5_compatibility_test/<xxx.py>
    # B.
    py -m qmlease run unittests/qt5_compatibility_test/<xxx.qml>
    ```
