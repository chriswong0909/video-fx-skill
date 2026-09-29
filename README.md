# video-fx-skill

會學習嘅剪片 skill（Claude + HyperFrames）。每次剪片都會將新學到嘅效果寫入效果庫，下次自動建議、組合使用。

## 結構
| 路徑 | 內容 |
|------|------|
| `skills/video-fx/SKILL.md` | 說明書：Claude 點問、點分析、點揀效果、點入庫 |
| `workflow/` | 開工問卷、拆解參考片、建議組合、新效果入庫 |
| `effects/FX-###-*/` | 每個效果：`effect.md`（資料）、`snippet.html`（代碼）、`preview.jpg` |
| `effects/INDEX.md`、`registry.json` | 自動生成嘅目錄（`node scripts/build-registry.mjs`） |
| `brands/` | 品牌檔（顏色、字體、禁忌） |
| `refs/` | 參考片分析同縮圖（**唔放原片**） |
| `lessons/` | 技術坑同環境設定 |
| `scripts/` | analyze-ref.sh、new-effect.mjs、build-registry.mjs |
| `tools/` | asr.py（廣東話轉錄）、relight.py（人像補光） |

## 目前效果
- 網頁目錄（有動態預覽）：https://claude.ai/artifact/S4J778bzGTX56umuae9ZAQ
- 本機版：`gallery/index.html`
- 文字版：[effects/INDEX.md](effects/INDEX.md)

## 使用方法
- **Cowork**：安裝呢個 repo 做 plugin，或者對 Claude 講「用 video-fx 幫我剪片」。Claude 會讀 `~/Documents/GitHub/video-fx-skill` 入面最新嘅效果庫。
- **Claude Code**：`ln -s ~/Documents/GitHub/video-fx-skill/skills/video-fx ~/.claude/skills/video-fx`

## 同步
Claude 改完檔案 → 你喺 GitHub Desktop 睇改動 → Commit → Push。

## 注意
`refs/` 有第三方影片縮圖，只作內部學習，repo 請保持私人。
