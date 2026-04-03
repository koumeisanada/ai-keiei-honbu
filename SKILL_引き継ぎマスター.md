# SKILL_引き継ぎマスター
# 真田孔明 AI経営本部 - 全情報引き継ぎドキュメント
# 最終更新：2026年04月03日

---

## AI経営本部 フォルダ構造（完全版）
## ※新しいChatでClaude Codeが迷わないよう完全なパスで記載

### ルートパス
~/Desktop/AI経営本部/

### 全フォルダ一覧（実際に存在するもの全て）

```
~/Desktop/AI経営本部/
├── AI活用講義/
│   ├── セールスレター制作/
│   │   ├── 00_ブレインダンプ/
│   │   ├── 01_Q_絞り込み/
│   │   ├── 02_U_共感/
│   │   ├── 03_E_教育/
│   │   ├── 04_S_刺激/
│   │   ├── 05_T_行動促進/
│   │   ├── 06_競合分析統合/
│   │   │   ├── AI活用成功事例集/
│   │   │   ├── ライバル徹底調査/
│   │   │   │   ├── 英語圏25校/
│   │   │   │   └── 日本20校/
│   │   │   ├── 他社比較分析/
│   │   │   └── 日本AI講座分析/
│   │   ├── 07_価格オファー設計/
│   │   ├── 08_初稿/
│   │   ├── 09_最終完成/
│   │   └── 毎日の作業ログ/
│   ├── 講義資料/
│   │   ├── 第01回/
│   │   ├── 第02回/
│   │   ├── 第03回/
│   │   ├── 第04回/
│   │   ├── 第05回/
│   │   ├── 第06回/
│   │   ├── 第07回/
│   │   ├── 第08回/
│   │   ├── 第09回/
│   │   ├── 第10回/
│   │   ├── 第11回/
│   │   └── 第12回/
│   ├── 資料/
│   └── 特典/
├── API連携/
│   ├── ChatGPT/
│   ├── Gemini/
│   └── 設定ファイル/
├── スタッフ向けマニュアル/
├── ワンチーム/
│   └── 資料/
├── 競合調査/
│   ├── 最新AI講座/
│   ├── 地下ソサエティ/
│   └── 北の株式投資大学/
├── 集客販売/
│   ├── Instagramストーリー画像/
│   │   └── ゼータ/
│   ├── Instagram動画原稿/
│   │   ├── ゼータ/
│   │   └── 飲食店/
│   ├── LINE原稿/
│   ├── ZOOMセミナー資料/
│   │   ├── ケイタ式物販/
│   │   ├── ロイ式物販/
│   │   ├── ワンチーム/
│   │   ├── 銀行融資/
│   │   ├── 地下ソサエティ/
│   │   └── 北の株式投資大学/
│   ├── クロージングセミナー/
│   │   ├── AI活用講義/
│   │   ├── ケイタ式物販/
│   │   ├── ロイ式物販/
│   │   ├── ワンチーム/
│   │   ├── 銀行融資/
│   │   ├── 地下ソサエティ/
│   │   └── 北の株式投資大学/
│   ├── セールスレター/
│   │   └── マスター文書/
│   ├── メルマガ原稿/
│   │   └── 過去記事/
│   ├── 個別面談案内メール/
│   │   └── 北の株式投資大学/
│   └── 日次成果物/
│       ├── 20260321/
│       ├── 20260322/
│       ├── 20260323/
│       ├── 20260324/
│       ├── 20260325/
│       ├── 20260326/
│       └── AI最新情報アーカイブ/
├── 成功シンドロームOS/
├── 地下ソサエティ/
│   ├── 講義セミナー/
│   │   ├── ゴールド/
│   │   │   └── 資料/
│   │   └── シルバー/
│   │       └── 資料/
│   └── 資料/
│       ├── サラリーマンでお金をもらう/
│       └── セミナー感想/
├── 品質チェック/
│   ├── LINE/
│   ├── セールスレター/
│   ├── メルマガ/
│   └── 講義資料/
├── 物販ビジネス/
│   ├── ケイタ式/
│   │   ├── AI自動化分析/
│   │   ├── リサーチ結果/
│   │   └── 資料/
│   │       └── ケイタ式 メール/
│   │           ├── No1-13/
│   │           ├── No14-27/
│   │           ├── No28-41/
│   │           ├── No42-55/
│   │           ├── No56-69/
│   │           ├── No70-83/
│   │           ├── No84-97/
│   │           ├── No98-111/
│   │           ├── No112-125/
│   │           ├── No126-139/
│   │           ├── No140-153/
│   │           ├── No154-167/
│   │           └── No168-180/
│   ├── ロイ式/
│   │   ├── AI自動化分析/
│   │   └── 資料/
│   └── 共通資料/
└── 北の株式投資大学/
    └── 資料/
        ├── デイリーリサーチ/
        └── 競合比較・リスク分析/
```

### 重要ファイルの完全パス

#### パイプライン・スクリプト（.py）

```
~/Desktop/AI経営本部/generate_ai_lecture.py
~/Desktop/AI経営本部/AI活用講義/ai_cautions_research.py
~/Desktop/AI経営本部/AI活用講義/create_ai_glossary.py
~/Desktop/AI経営本部/AI活用講義/create_manual_v2.py
~/Desktop/AI経営本部/AI活用講義/create_premium_lecture.py
~/Desktop/AI経営本部/AI活用講義/create_project_report.py
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/ai_success_cases_research.py
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/braindump_next.py
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/competitor_comparison.py
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/daily_salesletter.py
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/global_ai_research.py
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/japan_ai_school_research.py
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/movie_ai_research.py
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/rival_deep_research.py
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/rival_research.py
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/salesletter_next.py
~/Desktop/AI経営本部/AI活用講義/講義資料/第01回/generate_premium_docx.py
~/Desktop/AI経営本部/AI活用講義/講義資料/第02回/generate_ai_news_march.py
~/Desktop/AI経営本部/AI活用講義/講義資料/第02回/generate_ai_news_march_v2.py
~/Desktop/AI経営本部/API連携/daily_stock_research.py
~/Desktop/AI経営本部/API連携/enhance_analysis.py
~/Desktop/AI経営本部/API連携/update_master_salesletter.py
~/Desktop/AI経営本部/API連携/Gemini/apply_feedback.py
~/Desktop/AI経営本部/API連携/Gemini/generate_ai_news.py
~/Desktop/AI経営本部/API連携/Gemini/generate_image.py
~/Desktop/AI経営本部/API連携/Gemini/generate_lecture.py
~/Desktop/AI経営本部/API連携/Gemini/generate_line_4days.py
~/Desktop/AI経営本部/API連携/Gemini/generate_line.py
~/Desktop/AI経営本部/API連携/Gemini/generate_merumaga.py
~/Desktop/AI経営本部/API連携/Gemini/generate_reel_zeta.py
~/Desktop/AI経営本部/API連携/Gemini/generate_reel.py
~/Desktop/AI経営本部/API連携/Gemini/generate_supplement.py
~/Desktop/AI経営本部/スタッフ向けマニュアル/generate_manual.py
~/Desktop/AI経営本部/競合調査/ai_competitor_research.py
~/Desktop/AI経営本部/集客販売/generate_keita_event_merumaga.py
~/Desktop/AI経営本部/集客販売/generate_zeta_reel_ai_shacho.py
~/Desktop/AI経営本部/物販ビジネス/ケイタ式/analyze_keitashiki.py
~/Desktop/AI経営本部/北の株式投資大学/資料/create_monthly_report.py
```

#### パイプライン・スクリプト（.sh）

```
~/Desktop/AI経営本部/API連携/auto_commit_salesletter.sh
~/Desktop/AI経営本部/API連携/check_progress.sh
~/Desktop/AI経営本部/API連携/cron_daily.sh
~/Desktop/AI経営本部/API連携/launch_pipeline.sh
~/Desktop/AI経営本部/API連携/pipeline_daily.sh
~/Desktop/AI経営本部/API連携/update_handover.sh
~/Desktop/AI経営本部/API連携/設定ファイル/setup_api.sh
~/Desktop/AI経営本部/競合調査/run_competitor_research.sh
```

#### SKILLファイル

```
~/Desktop/AI経営本部/SKILL_引き継ぎマスター.md（本ファイル）
~/Desktop/AI経営本部/AI活用講義/SKILL_講義セミナー執筆.md
~/Desktop/AI経営本部/AI活用講義/SKILL_講義資料Word生成.md
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/SKILL_セールスレター表現技法.md
~/Desktop/AI経営本部/API連携/SKILL_毎日のルーティン指示.md
~/Desktop/AI経営本部/API連携/Gemini/SKILL_画像生成プロンプト.md
~/Desktop/AI経営本部/競合調査/SKILL_競合調査.md
~/Desktop/AI経営本部/集客販売/Instagram動画原稿/SKILL_リール動画原稿.md
~/Desktop/AI経営本部/集客販売/Instagram動画原稿/ゼータ/SKILL_ゼータリール専用.md
~/Desktop/AI経営本部/集客販売/Instagram動画原稿/飲食店/SKILL_焼肉店リール専用.md
~/Desktop/AI経営本部/集客販売/LINE原稿/SKILL_LINE自動生成.md
~/Desktop/AI経営本部/集客販売/セールスレター/SKILL_セールスレター最重要ノウハウ.md
~/Desktop/AI経営本部/集客販売/メルマガ原稿/SKILL_メルマガ自動生成.md
~/Desktop/AI経営本部/集客販売/メルマガ原稿/SKILL_改善履歴.md
~/Desktop/AI経営本部/集客販売/メルマガ原稿/SKILL_真田孔明学習メモ.md
~/Desktop/AI経営本部/集客販売/メルマガ原稿/SKILL_文章表現最上位原則.md
~/Desktop/AI経営本部/成功シンドロームOS/SKILL_成功シンドロームOS最重要.md
~/Desktop/AI経営本部/成功シンドロームOS/SKILL_提供商品一覧.md
~/Desktop/AI経営本部/品質チェック/SKILL_品質チェック.md
~/Desktop/AI経営本部/北の株式投資大学/資料/デイリーリサーチ/SKILL_考察資料強化.md
```

#### CLAUDE.mdファイル

```
~/Desktop/AI経営本部/CLAUDE.md
~/Desktop/AI経営本部/AI活用講義/CLAUDE.md
~/Desktop/AI経営本部/ワンチーム/CLAUDE.md
~/Desktop/AI経営本部/集客販売/CLAUDE.md
~/Desktop/AI経営本部/地下ソサエティ/CLAUDE.md
~/Desktop/AI経営本部/物販ビジネス/CLAUDE.md
~/Desktop/AI経営本部/北の株式投資大学/CLAUDE.md
```

#### Wordファイル（.docx）

```
~/Desktop/AI経営本部/AI_news_lecture_20260322.docx
~/Desktop/AI経営本部/AI活用講義/講義資料/第01回/【受講生用】AI経営本部_独自構造カスタマイズマニュアル.docx
~/Desktop/AI経営本部/AI活用講義/講義資料/第01回/【受講生用】Level5_AI経営本部_導入マニュアル_v2.docx
~/Desktop/AI経営本部/AI活用講義/講義資料/第01回/【受講生用】Level5_AI経営本部_導入マニュアル.docx
~/Desktop/AI経営本部/AI活用講義/講義資料/第01回/第01回_②Level講義資料_完成版.docx
~/Desktop/AI経営本部/AI活用講義/講義資料/第01回/第01回_講義資料_AIと向き合う前に知っておくべきこと.docx
~/Desktop/AI経営本部/AI活用講義/講義資料/第01回/第01回_講義資料_最高品質版.docx
~/Desktop/AI経営本部/AI活用講義/講義資料/第02回/第02回_①AI最新情報_2026年3月まとめ.docx
~/Desktop/AI経営本部/AI活用講義/特典/【特典】AI用語集_完全版.docx
~/Desktop/AI経営本部/AI活用講義/【報告書】最新AI活用講座プロジェクト_2026年03月22日.docx
~/Desktop/AI経営本部/スタッフ向けマニュアル/AI経営本部_構築マニュアル_汎用版.docx
~/Desktop/AI経営本部/北の株式投資大学/資料/20260324_米国テクノロジー企業_最新動向レポート_2026年3月号.docx
~/Desktop/AI経営本部/北の株式投資大学/資料/20260325_米国テクノロジー企業_最新動向レポート_2026年3月号.docx
~/Desktop/AI経営本部/北の株式投資大学/資料/chika_society_AI_news_20260322.docx
~/Desktop/AI経営本部/北の株式投資大学/資料/NVIDIA_GTC基調講演_完全版_20260318.docx
~/Desktop/AI経営本部/北の株式投資大学/資料/NVIDIA考察資料_20260318.docx
~/Desktop/AI経営本部/北の株式投資大学/資料/NVIDIA考察資料_完全版_20260318.docx
```

#### セールスレター（09_最終完成）

```
~/Desktop/AI経営本部/AI活用講義/セールスレター制作/09_最終完成/
├── SL_FINAL_最終品質チェック・完成.md
├── セールスレター_完全版_v1.md
├── セールスレター_完全版_v2.md
├── セールスレター_完全版_v3.md
├── セールスレター_完全版_v4.md
├── セールスレター_完全版_v5.md
├── セールスレター_完全版_v6.md
├── セールスレター_完全版_v8.md
├── セールスレター_完全版_v9.md
├── セールスレター_完全版_v10.md
├── セールスレター_完全版_v11.md
└── セールスレター_完全版_v12.md（最新版）
```

#### 日次成果物の保存先

```
~/Desktop/AI経営本部/集客販売/日次成果物/YYYYMMDD/
・メルマガ.txt
・LINE4日分.txt
・リール動画原稿.txt
・AI最新情報.txt
・品質チェック結果.txt
```

#### 米国企業リサーチの保存先

```
~/Desktop/AI経営本部/北の株式投資大学/資料/デイリーリサーチ/
ファイル名：YYYYMMDD_米国企業リサーチ.md
```

#### AI最新情報アーカイブ

```
~/Desktop/AI経営本部/集客販売/日次成果物/AI最新情報アーカイブ/
ファイル名：YYYYMMDD_AI最新情報.md
```

---

### Claude Codeでよく使うコマンド集

#### パイプライン実行
```bash
bash ~/Desktop/AI経営本部/API連携/pipeline_daily.sh
```

#### 米国企業リサーチ単体実行
```bash
python3 ~/Desktop/AI経営本部/API連携/daily_stock_research.py
```

#### AI最新情報単体実行
```bash
python3 ~/Desktop/AI経営本部/API連携/Gemini/generate_ai_news.py
```

#### メルマガ単体実行
```bash
python3 ~/Desktop/AI経営本部/API連携/Gemini/generate_merumaga.py
```

#### LINE原稿単体実行
```bash
python3 ~/Desktop/AI経営本部/API連携/Gemini/generate_line_4days.py
```

#### リール動画原稿単体実行
```bash
python3 ~/Desktop/AI経営本部/API連携/Gemini/generate_reel.py
```

#### ゼータリール単体実行
```bash
python3 ~/Desktop/AI経営本部/API連携/Gemini/generate_reel_zeta.py
```

#### ケイタ式分析実行
```bash
python3 ~/Desktop/AI経営本部/物販ビジネス/ケイタ式/analyze_keitashiki.py
```

#### 競合調査実行
```bash
python3 ~/Desktop/AI経営本部/競合調査/ai_competitor_research.py
```

#### 引き継ぎマスター確認
```bash
cat ~/Desktop/AI経営本部/SKILL_引き継ぎマスター.md
```

#### GitHubプッシュ（main）
```bash
cd ~/Desktop/AI経営本部 && git add . && git commit -m "更新内容" && git push origin main
```

#### GitHubプッシュ（セールスレター）
```bash
cd ~/Desktop/AI経営本部 && git add . && git commit -m "更新内容" && git push origin salesletter-development
```

#### 今日の成果物確認
```bash
ls ~/Desktop/AI経営本部/集客販売/日次成果物/$(date +%Y%m%d)/
```

#### APIキー確認
```bash
echo $GEMINI_API_KEY | cut -c1-10
echo $OPENAI_API_KEY | cut -c1-10
echo $ANTHROPIC_API_KEY | cut -c1-10
```

---

### 新しいChatを開いた時の最初のコマンド

以下をClaude Codeに入力する：
```bash
cat ~/Desktop/AI経営本部/SKILL_引き継ぎマスター.md
```

これで全フォルダ・全ファイルの場所が把握できる。
