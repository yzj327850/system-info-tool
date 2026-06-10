#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 将 Python 脚本打包成 .exe
"""

import subprocess
import sys
import os


def install_requirements():
    """安装必要的依赖"""
    print("正在安装依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "openpyxl", "-q"])
    print("依赖安装完成")


def build_exe():
    """打包成 exe"""
    print("\n开始打包...")
    
    # 清理旧的构建文件
    import shutil
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"清理 {dir_name} 目录...")
            try:
                shutil.rmtree(dir_name, onerror=lambda f, p, e: None)
            except:
                pass
    # 清理 .pyc 文件
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))
        for dir in dirs:
            if dir == '__pycache__':
                shutil.rmtree(os.path.join(root, dir))
    print("清理完成")
    
    # 获取 pyinstaller 路径
    pyinstaller_path = os.path.expanduser("~\\AppData\\Local\\Python\\pythoncore-3.14-64\\Scripts\\pyinstaller.exe")
    if not os.path.exists(pyinstaller_path):
        # 尝试使用 pip 安装的 pyinstaller
        pyinstaller_path = "pyinstaller"
    
    # PyInstaller 参数
    args = [
        pyinstaller_path,
        "--onefile",           # 打包成单个文件
        "--console",           # 显示控制台窗口
        "--noconfirm",         # 覆盖输出目录
        "--clean",             # 清理临时文件
        "--add-data", "template.xlsx;.",  # 嵌入模板文件
        "--name", "SystemInfo",  # 输出文件名
        "system_info.py"
    ]
    
    result = subprocess.run(args, capture_output=True, text=True, shell=True)
    
    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("打包成功!")
        print("=" * 50)
        print("\n输出文件位置: dist/SystemInfo.exe")
        print("\n使用方法:")
        print("  直接双击运行 dist/SystemInfo.exe")
        print("=" * 50)
    else:
        print("打包失败:")
        print(result.stderr)
        return False
    
    return True


def main():
    print("=" * 50)
    print("    电脑信息获取工具 - 打包脚本")
    print("=" * 50)
    
    # 检查 Python 版本
    if sys.version_info < (3, 6):
        print("错误: 需要 Python 3.6 或更高版本")
        sys.exit(1)
    
    # 安装依赖
    try:
        import PyInstaller
        import openpyxl
        print("依赖已安装")
    except ImportError:
        install_requirements()
    
    # 打包
    if build_exe():
        print("\n打包完成!")
    else:
        print("\n打包失败，请检查错误信息")
    
    input("\n按回车键退出...")


if __name__ == "__main__":
    main()
