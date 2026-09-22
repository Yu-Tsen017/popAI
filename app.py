from datetime import datetime, timedelta
import re

class StarlightAgent:
    def __init__(self):
        # 1. 聖地巡禮知識庫 (Footprint RAG)
        self.footprint_db = {
            "咖啡廳": {
                "name_zh": "Cafe Layered 延南店",
                "name_kr": "카페 레이어드 연남점",
                "city": "首爾弘大/延南洞",
                "idol_pick": "安俞真同款",
                "recommended_menu": "原味司康、維多利亞海綿蛋糕",
                "seat_tip": "二樓靠窗靠角落採光最佳座位",
                "status": "營業中（公休日請出發前再次確認）"
            }
        }
        
        # 2. 周邊市價行情資料庫
        self.photocard_prices = {
            "安俞真": {"album_card": (150, 300), "benefit_card": (450, 900)},
            "張員瑛": {"album_card": (200, 400), "benefit_card": (600, 1500)},
            "IVE": {"album_card": (150, 350), "benefit_card": (400, 1000)}
        }
        
        # 3. 防詐騙與敏感字眼過濾
        self.scam_keywords = ["賣貨便簽署協議", "驗證金流", "先匯款", "保證有票", "代搶不連號", "私下交易"]

    def convert_kst_to_tst(self, kst_hour: int, kst_minute: int = 0) -> str:
        """時區轉換：韓國時間 (KST) 比台灣時間 (TST) 快 1 小時"""
        kst_time = datetime(2026, 1, 1, kst_hour, kst_minute)
        tst_time = kst_time - timedelta(hours=1)
        return tst_time.strftime("%H:%M")

    def route_and_respond(self, user_query: str) -> str:
        """第二層與第五層：意圖識別分流、工具調用與結構化回覆"""
        # --- 邊界防禦層：防詐機制檢測 ---
        for kw in self.scam_keywords:
            if kw in user_query:
                return (
                    "⚠️【星軌助手防詐警示】\n"
                    f"偵測到高風險關鍵字：「{kw}」！\n"
                    "• 官方與合法第三方平台絕不會要求簽署「金流驗證保障協議」。\n"
                    "• 請勿私下匯款或點擊陌生連結，二手交易請走正規驗證管道，確保帳號與財物安全。"
                )

        # --- 分支一：跨國日程與時差即時換算 ---
        time_match = re.search(r'(?:韓國(?:時間)?|KST)\s*(\d{1,2})(?:點|時|:)(\d{2})?', user_query)
        if time_match or "直播" in user_query or "時差" in user_query:
            if time_match:
                kst_h = int(time_match.group(1))
                kst_m = int(time_match.group(2)) if time_match.group(2) else 0
                tst_str = self.convert_kst_to_tst(kst_h, kst_m)
                return (
                    "🕒【日程時差換算】\n"
                    f"• 韓國時間 (KST)：{kst_h:02d}:{kst_m:02d}\n"
                    f"• 台灣時間 (TST)：{tst_str}\n"
                    "📌 提示：韓國標準時間比台灣快 1 小時，請準時開啟平台避免錯過即時互動！"
                )

        # --- 分支二：偶像同款聖地巡禮與打卡指南 ---
        if any(w in user_query for w in ["同款", "打卡", "踩點", "咖啡廳", "餐廳", "聖地巡禮"]):
            info = self.footprint_db["咖啡廳"]
            return (
                "📍【同款聖地巡禮指南】\n"
                f"• 地點名稱：{info['name_zh']} ({info['name_kr']})\n"
                f"• 區域分佈：{info['city']}\n"
                f"• 踩點出處：{info['idol_pick']}\n"
                f"• 推薦同款點單：{info['recommended_menu']}\n"
                f"• 拍照打卡座位：{info['seat_tip']}\n"
                f"• 狀態檢驗：{info['status']}\n"
                "⚠️ 提醒：出發前建議透過 Naver Map 再次核對當日公休與營業時間。"
            )

        # --- 分支三：二手周邊行情評估 ---
        if any(w in user_query for w in ["小卡", "周邊", "市價", "行情", "買卡"]):
            price_match = re.search(r'(\d+)\s*(?:元|塊|NT)', user_query)
            if price_match:
                price = int(price_match.group(1))
                low, high = self.photocard_prices["安俞真"]["benefit_card"]
                verdict = "高於常態均價，可能涉及炒價溢價" if price > high else "處於合理行情區間內"
                return (
                    "🏷️【周邊行情評估】\n"
                    f"• 您詢問的價格：NT$ {price}\n"
                    f"• 熱門特典卡參考均價：NT$ {low} ~ NT$ {high}\n"
                    f"• 評估建議：{verdict}。\n"
                    "📌 提醒：二手交易請注意對光影片檢驗假卡，並走正規有保障的賣場管道！"
                )

        # --- 分支四：演唱會搶票規則與觀演指南 ---
        if any(w in user_query for w in ["搶票", "拓元", "小巨蛋", "視線", "座位"]):
            return (
                "🎫【演唱會搶票與觀演指南】\n"
                "1. 售票系統整備：請提前完成拓元 / KKTIX 會員手機實名認證，購票當下切勿重複刷新頁面。\n"
                "2. 視線分析建議：台北小巨蛋黃 2C、紅 2B 區整體舞台視覺完整；世運主場館建議優先考量延伸舞台距離。\n"
                "3. 退票政策須知：依文化部文創法規定，開賣後有手續費級距，切勿購買來源不明的二手讓票。"
            )

        # 預設回覆
        return "✨ 您好！我是星軌助手，可以詢問我：跨國時差換算、偶像同款踩點動線、周邊市價行情或演唱會搶票規則！"

# --- 測試執行區塊 ---
if __name__ == "__main__":
    agent = StarlightAgent()
    print("=" * 60)
    print("星軌助手 (Starlight Agent) 原型已啟動，開始測試四大核心功能：\n")
    
    # 測試情境 1：時差換算
    q1 = "韓國時間晚上 20:00 的直播台灣幾點要看？"
    print(f"用戶：{q1}")
    print(agent.route_and_respond(q1))
    print("-" * 60)
    
    # 測試情境 2：同款踩點
    q2 = "想去首爾弘大找安俞真同款咖啡廳打卡，有推薦嗎？"
    print(f"用戶：{q2}")
    print(agent.route_and_respond(q2))
    print("-" * 60)
    
    # 測試情境 3：行情評估
    q3 = "社群有人這張特典卡賣 800 元合理嗎？"
    print(f"用戶：{q3}")
    print(agent.route_and_respond(q3))
    print("-" * 60)
    
    # 測試情境 4：防詐觸發
    q4 = "賣家叫我加 LINE 點連結驗證金流簽署協議才能寄出"
    print(f"用戶：{q4}")
    print(agent.route_and_respond(q4))
    print("=" * 60)
