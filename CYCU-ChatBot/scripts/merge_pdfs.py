#!/usr/bin/env python3
"""
Merge PDFs Script
合併 PDF 文件腳本

此腳本將多個 PDF 文件合併為一個
使用方法: python scripts/merge_pdfs.py
"""
import sys
from pathlib import Path
from PyPDF2 import PdfMerger
import logging

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def merge_pdfs(input_dir: Path, output_file: Path):
    """
    合併目錄下的所有 PDF 文件
    
    Args:
        input_dir: 輸入目錄
        output_file: 輸出文件路徑
    """
    try:
        # 查找所有 PDF 文件
        pdf_files = sorted(input_dir.rglob("*.pdf"))
        
        if not pdf_files:
            logger.error(f"在 {input_dir} 中找不到任何 PDF 文件")
            return False
        
        logger.info(f"找到 {len(pdf_files)} 個 PDF 文件")
        
        # 建立 PDF 合併器
        merger = PdfMerger()
        
        # 逐個添加 PDF
        for i, pdf_file in enumerate(pdf_files, 1):
            try:
                logger.info(f"[{i}/{len(pdf_files)}] 正在處理: {pdf_file.name}")
                merger.append(str(pdf_file))
            except Exception as e:
                logger.warning(f"無法處理 {pdf_file.name}: {e}")
                continue
        
        # 確保輸出目錄存在
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 寫入合併後的 PDF
        logger.info(f"正在寫入合併後的 PDF: {output_file}")
        merger.write(str(output_file))
        merger.close()
        
        logger.info(f"成功！合併後的 PDF 已儲存至: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"合併 PDF 時發生錯誤: {e}", exc_info=True)
        return False


def main():
    """主函數"""
    # 設定路徑
    base_dir = Path(__file__).parent.parent
    input_dir = base_dir / "data" / "raw" / "regulations"
    output_file = base_dir / "data" / "processed" / "cycu_merged.pdf"
    
    logger.info("=" * 60)
    logger.info("PDF 文件合併工具")
    logger.info("=" * 60)
    logger.info(f"輸入目錄: {input_dir}")
    logger.info(f"輸出文件: {output_file}")
    logger.info("")
    
    # 檢查輸入目錄
    if not input_dir.exists():
        logger.error(f"輸入目錄不存在: {input_dir}")
        return 1
    
    # 執行合併
    success = merge_pdfs(input_dir, output_file)
    
    if success:
        logger.info("=" * 60)
        logger.info("合併完成！")
        logger.info("=" * 60)
        return 0
    else:
        logger.error("合併失敗")
        return 1


if __name__ == '__main__':
    sys.exit(main())
