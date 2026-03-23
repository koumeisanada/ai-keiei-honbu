import os
import glob
from datetime import datetime, date

BASE_DIR = os.path.expanduser(
    "~/Desktop/AI経営本部/AI活用講義/セールスレター制作"
)
MASTER_FILE = os.path.join(BASE_DIR, "MASTER_セールスレター.md")

FOLDER_ORDER = [
    ("00_ブレインダンプ", "■ ブレインダンプ"),
    ("01_Q_絞り込み", "■ Q：絞り込み"),
    ("02_U_共感", "■ U：共感"),
    ("03_E_教育", "■ E：教育"),
    ("04_S_刺激", "■ S：刺激"),
    ("05_T_行動促進", "■ T：行動促進"),
    ("06_競合分析統合", "■ 競合分析統合"),
    ("07_価格オファー設計", "■ 価格・オファー設計"),
    ("08_初稿", "■ 初稿"),
    ("09_最終完成", "■ 最終完成"),
]

def build_master():
    today = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    content = f"# 最新AI講座 セールスレター MASTER\n"
    content += f"## 制作開始：2026年3月19日\n"
    content += f"## 完成目標：2026年4月19日\n"
    content += f"## 最終更新：{today}\n\n"
    content += "---\n\n"

    total_files = 0

    for folder_name, section_title in FOLDER_ORDER:
        folder_path = os.path.join(BASE_DIR, folder_name)
        if not os.path.exists(folder_path):
            continue

        files = sorted(glob.glob(f"{folder_path}/*.md"))
        if not files:
            continue

        content += f"# {section_title}\n\n"

        for file_path in files:
            file_name = os.path.basename(file_path)
            date_str = file_name[:10] if len(file_name) > 10 else ""

            with open(file_path, "r") as f:
                file_content = f.read()

            content += f"## [{date_str}] {file_name.replace('.md', '')}\n\n"
            content += file_content
            content += "\n\n---\n\n"
            total_files += 1

    content += f"## 制作統計\n"
    content += f"- 総ファイル数：{total_files}個\n"
    content += f"- 最終更新：{today}\n"
    content += f"- 進捗：{total_files}/32ファイル予定\n"

    with open(MASTER_FILE, "w") as f:
        f.write(content)

    print(f"✅ マスターファイル更新完了")
    print(f"✅ 総ファイル数：{total_files}個")
    print(f"✅ 保存先：{MASTER_FILE}")

if __name__ == "__main__":
    build_master()
