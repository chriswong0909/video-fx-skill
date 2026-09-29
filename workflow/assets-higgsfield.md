# 素材生成（Higgsfield connector）

使用者已連接 Higgsfield（工具名 `mcp__Higgsfield__*`，要先用 ToolSearch 載入）。**只喺素材關卡確認後先生成。**

## 對應
| 需要 | 工具 | 備註 |
|------|------|------|
| 3D 圖示／物件（心臟、腦、藥丸） | `generate_image` → `remove_background` | 提示：glossy 3D render, soft studio light, plain background |
| AI 場景相（花海、診所） | `generate_image` | 9:16 |
| AI B-roll 片段 | `generate_video` | 先 `models_explore(action:'recommend')`；4–5 秒夠用 |
| 圖片轉 3D 模型 | `generate_3d` | 需要 GLB 時先用 |
| 相片補光 | `relight_image` | 只限靜止圖 |
| 放大 | `upscale_image` / `upscale_video` | 推鏡太糊時 |

## 規則
- 開工先 `create_project`（每個影片專案一個），之後所有生成用同一個 `folder_id`。
- 生成前一律 `get_cost:true` 預計 credits，寫入分鏡素材清單。
- 多個素材用 batch 工具 + `jobs_wait`，唔好逐個等。
- 本機檔案要上傳：用 `media_upload_widget`（使用者喺介面揀檔），唔好自己讀 uploads。
- 醫學插圖 AI 生成後要標明「需醫生審核」。
- 生成結果下載後放 `<專案>/assets/`，檔名寫明鏡頭號。

## 其他來源
- Canva connector：`generate-image`、`remove-background`（備用）
- 本機免費：代碼自製（SVG/CSS）、RVM 摳圖
