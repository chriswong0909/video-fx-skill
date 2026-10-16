# #29 Odometer 測試卡（2026-10-16，text-motion-40 程式碼做起點）

卡：`styles/kallaway/cards-9x16/kallaway.x.ext29.html`（未驗證）。文字「65歲以上女性 25%」，Healthy Days 淺色品牌色，背景係 `test10s_v2.mp4` 嘅一格（講者）。

重做步驟（本機 VM，`source ~/hf/env.sh`）：
```
python3 tools/cards.py adapt --ext 29 --freeze 1.6            # 已做；之後人手換字（見卡內 effect 註解）
python3 tools/ext_effects.py brandfont --project ~/hf/ext29 --text "65歲以上女性25%"   # 「歲」兩款原作字體都缺
python3 tools/cards.py use kallaway.x.ext29 --project ~/hf/ext29 --name b29 --dur 4 \
  --slots '{"num":"25","unit":"%","label":"65歲以上女性"}' --cues 0.3 --brand healthy-days
# 對比專案：--dur 6.4 --loops 3，npx hyperframes snapshot --at 0.05,0.8,1.55,2.3,3.05,3.8,4.55,5.3 --no-end
```
- `card_once.jpg`：實際用法（單次播放，凍結），8 格。
- `compare_strip_vs_card.jpg`：上排 strips 原作分格圖，下排我哋嘅卡（loops 3，同樣 0.75 秒間隔）。
- `full_card_1.5s.png`：完整 9:16 一格（講者上面 chest 位）。
圖片唔入 git（二進制）。
