# 聲效混音（sounds/ 聲效庫）

## 1. 聲效庫結構
- `sounds/SFX-###-slug/`：`sound.md`（front matter：id, name, name_en, category, duration, volume, mood, video_types, pace, pairs_with, source, license, learned, used_in, status）、`sound.mp3`、`peaks.json`（網頁波形用）。
- 類別：whoosh 轉場風聲｜pop 彈出｜ui 介面｜ding 提示音｜impact 重擊｜riser 張力｜foley 擬音｜accent 點綴｜music 背景音樂｜ambience 環境聲
- SFX 編號同 FX 分開；移除嘅寫入 `sounds/REMOVED.md`，編號唔重用。
- `registry.json` 嘅 `sounds` 陣列有全部摘要；揀聲效先睇佢，唔使逐個讀 sound.md。

## 2. 入庫
- 內置合成：`python3 tools/sfx.py synth`（已存在會略過；`--force --only SFX-00X` 重做）。
- 外來聲效（Pixabay、Mixkit 等免版稅）：`python3 tools/sfx.py add <檔> <slug> <category> "<中文名>" --start 0.2 --dur 1.0 --source "<網址>" --license "<授權>"`，然後補完 sound.md 嘅 mood、pairs_with、幾時用。**授權唔清楚嘅唔入庫。**
- 唔好由參考片抽聲效（人聲音樂混埋、版權屬原作者）；參考片只記錄「幾時落聲」，寫喺 analysis.md 嘅聲效欄。
- 入庫後 `node scripts/build-registry.mjs && node scripts/build-gallery.mjs`，重新發佈效果目錄。

## 2b. 聲效包（Kenney CC0）
- `sounds/PACKS.md` 列出每個包嘅來源同授權；sound.md 有 `pack`、`curated`、`source_file`、`license`。
- 揀聲效優先次序：精選（curated，有 pairs_with）→ Kenney 擬音（kenney-casino 紙卡、kenney-rpg 翻書／開門、kenney-impact 撞擊）→ 其他。
- Kenney 短音樂（kenney-jingles）只用喺片頭片尾 1–3 秒，唔好當背景音樂 loop。
- 匯入新包：`python3 tools/import_pack.py <資料夾> <pack-slug> --license "..." --source "..."`（授權唔清楚唔匯入）。

## 3. 點樣落聲
- 對準**畫面動作**：接觸格、出現格、推鏡最快嗰格；唔係對準句子開頭。whoosh 嘅聲音中心喺約 40% 位，所以要早 0.3 秒落。riser／suck-in 要喺動作之前開始，完結一刻 = 畫面出現。
- 密度：口播片平均每 3–5 秒最多 1 個；同一個聲效每 60 秒最多 3 次；ding 全片 1–3 次。
- 講者講緊重點字嗰刻唔好落大聲效；放喺停頓位或者字尾。
- 醫療嚴肅題材：避免 error-buzz、glitch、sparkle；用 pop-soft、card-slide、whoosh-soft、ding。

## 4. 混音（原聲音量不變）
1. 分鏡 JSON 每鏡加 `sfx`：`[{"sfx":"SFX-001","t":3.8,"vol":0.35}]`（t 係全片時間）。
2. 草稿階段可以喺 HyperFrames 加 `<audio data-start data-duration data-track-index data-volume src>` 試位。
3. 正式版一律用：
   ```
   python3 tools/sfx.py mix source.mp4 cues.json mix.m4a
   ffmpeg -i render.mp4 -i mix.m4a -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy -shortest out.mp4
   ```
   `mix` 用 amix normalize=0（人聲保持 1.0）+ alimiter 防爆音。**有聲效就唔再係原音軌 md5**，要同使用者講明音軌已加聲效。
4. 建議音量：sound.md 嘅 `volume`（0.3–0.5）；背景音樂 0.08–0.15，人聲講嘢時再壓低。
5. 核對：用手機喇叭同耳機各聽一次；`ffmpeg -i out.mp4 -af volumedetect` 確認 max_volume < -0.5 dB。
