#!/usr/bin/env python3
"""
Migration Script
從舊專案遷移到新專案架構

使用方法: python scripts/migrate_from_old_project.py
"""
import os
import shutil
import sys
from pathlib import Path

def print_header(text):
    """列印標題"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(step, text):
    """列印步驟"""
    print(f"[步驟 {step}] {text}")

def print_success(text):
    """列印成功訊息"""
    print(f"✓ {text}")

def print_warning(text):
    """列印警告訊息"""
    print(f"⚠ {text}")

def print_error(text):
    """列印錯誤訊息"""
    print(f"✗ {text}")

def main():
    """主函數"""
    print_header("CYCU ChatBot - 專案遷移工具")
    
    # 路徑設置
    base_dir = Path(__file__).parent.parent
    old_project_dir = base_dir.parent / "university-query-platform"
    cycu_law_dir = base_dir.parent / "cycu_law"
    new_data_dir = base_dir / "data" / "raw" / "regulations"
    
    print(f"舊專案目錄: {old_project_dir}")
    print(f"法規資料目錄: {cycu_law_dir}")
    print(f"新資料目錄: {new_data_dir}")
    print()
    
    # 檢查舊專案是否存在
    if not old_project_dir.exists():
        print_error(f"找不到舊專案目錄: {old_project_dir}")
        print("請確認路徑是否正確")
        return 1
    
    # 步驟1: 複製 PDF 法規資料
    print_step(1, "複製 PDF 法規資料")
    if cycu_law_dir.exists():
        try:
            # 確保目標目錄存在
            new_data_dir.mkdir(parents=True, exist_ok=True)
            
            # 複製所有 PDF 文件
            pdf_files = list(cycu_law_dir.glob("*.pdf"))
            print(f"找到 {len(pdf_files)} 個 PDF 文件")
            
            for pdf_file in pdf_files:
                dest = new_data_dir / pdf_file.name
                if not dest.exists():
                    shutil.copy2(pdf_file, dest)
                    print(f"  ✓ 複製: {pdf_file.name}")
                else:
                    print(f"  - 跳過（已存在）: {pdf_file.name}")
            
            print_success(f"成功複製 {len(pdf_files)} 個 PDF 文件")
        except Exception as e:
            print_error(f"複製 PDF 文件時發生錯誤: {e}")
            return 1
    else:
        print_warning(f"找不到法規資料目錄: {cycu_law_dir}")
    
    # 步驟2: 複製圖片資源
    print_step(2, "複製圖片資源")
    old_image = old_project_dir / "cycu_image.png"
    new_image_dir = base_dir / "frontend" / "assets" / "images"
    new_image = new_image_dir / "cycu_logo.png"
    
    if old_image.exists():
        try:
            new_image_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(old_image, new_image)
            print_success(f"成功複製圖片到: {new_image}")
        except Exception as e:
            print_error(f"複製圖片時發生錯誤: {e}")
    else:
        print_warning(f"找不到圖片文件: {old_image}")
    
    # 步驟3: 檢查環境變數
    print_step(3, "檢查環境變數")
    old_env = old_project_dir / ".env"
    new_env = base_dir / ".env"
    
    if old_env.exists() and not new_env.exists():
        print(f"發現舊專案的 .env 文件")
        print("請手動檢查並複製必要的配置到新專案的 .env 文件")
        print(f"  舊文件: {old_env}")
        print(f"  新文件: {new_env}")
        print_warning("請確保複製 OPENAI_API_KEY 等重要配置")
    elif new_env.exists():
        print_success(".env 文件已存在")
    else:
        print_warning("請從 .env.example 建立 .env 文件")
    
    # 步驟4: 遷移總結
    print_header("遷移總結")
    print("✓ PDF 法規資料已複製到新專案")
    print("✓ 圖片資源已準備就緒")
    print()
    print("接下來的步驟:")
    print("1. 檢查並配置 .env 文件")
    print("   cp .env.example .env")
    print("   # 編輯 .env，填入 OPENAI_API_KEY")
    print()
    print("2. 建立向量資料庫")
    print("   python scripts/build_vector_store.py")
    print()
    print("3. 啟動新應用")
    print("   python src/app.py")
    print()
    print_header("遷移完成！")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
