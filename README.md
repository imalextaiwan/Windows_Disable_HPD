==============================================================================
HPD Presence Sensing Auto-Disable Tool
Human Presence Detection 自動關閉工具
==============================================================================
版本：1.2.0
作者：Alex Huang
日期：2026-03-09

[ 程式用途 ]
本工具旨在自動開啟 Windows 的「存在感應 (Presence Sensing)」設定頁面，
並自動將相關的偵測開關切換為關閉狀態。包含以下功能：
- 取消「我離開時關閉螢幕」
- 取消「接近時喚醒此裝置」
- 取消「轉移視線時將螢幕調暗」
- 取消「偵測其他人查看我的螢幕的時間」

[ 執行方式 ]
1. 雙擊執行「Disable_HPD_20260309_1.exe」。
2. 程式啟動後，畫面中央會跳出「檢查設定中，請勿移動鍵盤或滑鼠」的提示。
3. 程式會自動開啟設定頁面並進行關閉動作。
4. 執行完畢後，會彈出「成功」或「失敗」的對話框，點擊確認即可。

[ ⚠️ 注意事項 ]
本程式使用介面自動化（UI Automation）技術模擬滑鼠點擊。
執行期間（約 3~5 秒內），請務必遵守以下原則，以免干擾程式運作：
- 請勿移動滑鼠
- 請勿敲擊鍵盤
- 請勿切換其他視窗

[ 日誌與除錯 ]
程式每次執行，皆會在工具所在目錄下自動建立「logs」資料夾，
並產生記錄檔（例如：hpd_v1.2.0_日期_時間_主機_pid.log）。
若遇到執行失敗，請開啟最新的 log 檔查看具體錯誤原因。

[ 錯誤碼說明 (Exit Codes) ]
若您將本程式加入批次檔 (Batch) 自動執行，可透過以下回傳碼判斷結果：
   0 : 執行成功
  10 : 無法開啟設定頁面
  20 : 找不到任何設定開關
  30 : 開關關閉失敗 (部分或全部)
  99 : 發生未預期的系統錯誤


==============================================================================
[ 授權條款 (MIT License) ]

Copyright (c) 2026 Alex Huang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

------------------------------------------------------------------------------
[ 中文翻譯參考 (僅供參考，法律效力以英文原文為準) ]

版權所有 (c) 2026 Alex Huang

特此免費授予任何獲得本軟體及相關文件檔案（「軟體」）副本之人，
無限制地處理本軟體的權利，包括但不限於使用、複製、修改、合併、發佈、散佈、
再授權及/或販售本軟體副本的權利，並允許獲提供本軟體之人為之，
但須符合以下條件：

上述版權聲明及本許可聲明應包含於本軟體的所有副本或實質部分中。

本軟體是「按原樣」提供，不附帶任何明示或暗示的保證，包含但不限於
對適銷性、特定用途適用性及不侵權的保證。在任何情況下，作者或版權持有人
均不對因本軟體或本軟體的使用或其他交易而產生、引起或與之相關的
任何索賠、損害或其他責任負責，無論是合約、侵權或其他形式的訴訟。
==============================================================================
