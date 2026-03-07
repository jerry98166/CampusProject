#!/bin/bash

# CYCU ChatBot - 快速開始腳本
# 自動化專案設置流程

set -e  # 遇到錯誤立即退出

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函數：列印標題
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# 函數：列印成功訊息
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# 函數：列印警告訊息
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 函數：列印錯誤訊息
print_error() {
    echo -e "${RED}✗${NC} $1"
}

# 函數：列印步驟
print_step() {
    echo -e "\n${BLUE}[步驟 $1]${NC} $2"
}

# 檢查 Python 版本
check_python() {
    print_step 1 "檢查 Python 版本"
    
    if ! command -v python3 &> /dev/null; then
        print_error "找不到 Python3，請先安裝 Python 3.8 或以上版本"
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    required_version="3.8"
    
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
        print_success "Python 版本: $(python3 --version)"
    else
        print_error "需要 Python 3.8 或以上版本，當前版本: $(python3 --version)"
        exit 1
    fi
}

# 建立虛擬環境
setup_venv() {
    print_step 2 "建立虛擬環境"
    
    if [ -d "venv" ]; then
        print_warning "虛擬環境已存在，跳過建立"
    else
        python3 -m venv venv
        print_success "虛擬環境建立完成"
    fi
    
    # 啟動虛擬環境
    source venv/bin/activate
    print_success "虛擬環境已啟動"
}

# 安裝依賴
install_dependencies() {
    print_step 3 "安裝依賴套件"
    
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    
    print_success "依賴套件安裝完成"
}

# 配置環境變數
setup_env() {
    print_step 4 "配置環境變數"
    
    if [ -f ".env" ]; then
        print_warning ".env 文件已存在"
        read -p "是否要覆蓋現有的 .env 文件？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_success "保留現有的 .env 文件"
            return
        fi
    fi
    
    cp .env.example .env
    print_success ".env 文件已建立"
    
    # 提示用戶輸入 API Key
    echo -e "\n${YELLOW}請輸入您的 OpenAI API Key:${NC}"
    read -s openai_key
    
    if [ -n "$openai_key" ]; then
        # macOS 和 Linux 的 sed 語法不同
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/your_openai_api_key_here/$openai_key/" .env
        else
            sed -i "s/your_openai_api_key_here/$openai_key/" .env
        fi
        print_success "OpenAI API Key 已設置"
    else
        print_warning "未設置 OpenAI API Key，請手動編輯 .env 文件"
    fi
}

# 檢查 PDF 文件
check_pdf_files() {
    print_step 5 "檢查 PDF 資料文件"
    
    pdf_count=$(find data/raw/regulations -name "*.pdf" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$pdf_count" -gt 0 ]; then
        print_success "找到 $pdf_count 個 PDF 文件"
    else
        print_warning "未找到 PDF 文件"
        echo "請將 PDF 文件放置到 data/raw/regulations/ 目錄"
        echo "或運行遷移腳本: python scripts/migrate_from_old_project.py"
    fi
}

# 建立向量資料庫
build_vector_store() {
    print_step 6 "建立向量資料庫"
    
    if [ -d "data/vector_store" ] && [ "$(ls -A data/vector_store)" ]; then
        print_warning "向量資料庫已存在"
        read -p "是否要重新建立向量資料庫？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_success "保留現有的向量資料庫"
            return
        fi
    fi
    
    pdf_count=$(find data/raw/regulations -name "*.pdf" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$pdf_count" -eq 0 ]; then
        print_warning "沒有 PDF 文件，跳過向量資料庫建立"
        return
    fi
    
    echo "正在建立向量資料庫（這可能需要幾分鐘）..."
    python scripts/build_vector_store.py
    
    if [ $? -eq 0 ]; then
        print_success "向量資料庫建立完成"
    else
        print_error "向量資料庫建立失敗"
        exit 1
    fi
}

# 運行測試
run_tests() {
    print_step 7 "運行測試（可選）"
    
    read -p "是否要運行測試？(y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pytest tests/ -v
        print_success "測試完成"
    else
        print_success "跳過測試"
    fi
}

# 完成提示
finish() {
    print_header "設置完成！"
    
    echo -e "${GREEN}✓${NC} 專案設置成功完成"
    echo ""
    echo "下一步操作："
    echo ""
    echo "1. 啟動應用："
    echo "   ${BLUE}source venv/bin/activate${NC}  # 啟動虛擬環境"
    echo "   ${BLUE}python src/app.py${NC}          # 啟動應用"
    echo ""
    echo "2. 訪問應用："
    echo "   ${BLUE}http://localhost:8080${NC}"
    echo ""
    echo "3. 查看文檔："
    echo "   - README.md - 專案說明"
    echo "   - docs/API.md - API 文檔"
    echo "   - docs/DEPLOYMENT.md - 部署指南"
    echo "   - docs/DEVELOPMENT.md - 開發指南"
    echo ""
}

# 主流程
main() {
    print_header "CYCU ChatBot - 自動設置"
    
    echo "此腳本將協助您完成以下設置："
    echo "1. 檢查 Python 版本"
    echo "2. 建立虛擬環境"
    echo "3. 安裝依賴套件"
    echo "4. 配置環境變數"
    echo "5. 檢查資料文件"
    echo "6. 建立向量資料庫"
    echo "7. 運行測試（可選）"
    echo ""
    
    read -p "按 Enter 開始..." -s
    echo ""
    
    check_python
    setup_venv
    install_dependencies
    setup_env
    check_pdf_files
    build_vector_store
    run_tests
    finish
}

# 執行主流程
main
