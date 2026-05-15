from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re

# ================== FAKE DATABASE ==================
laptops = [
    {"name": "ASUS Vivobook 15", "price": 15000000, "usage": ["hoc tap", "van phong"]},
    {"name": "Dell Inspiron 14", "price": 18000000, "usage": ["lap trinh", "van phong"]},
    {"name": "Lenovo IdeaPad 3", "price": 12000000, "usage": ["hoc tap"]},
    {"name": "Acer Nitro 5", "price": 22000000, "usage": ["gaming"]},
    {"name": "ASUS TUF Gaming", "price": 25000000, "usage": ["gaming"]},
    {"name": "MacBook Air M1", "price": 23000000, "usage": ["lap trinh", "van phong"]},
    {"name": "MSI GF63", "price": 20000000, "usage": ["gaming"]},
    {"name": "Gigabyte G5", "price": 21000000, "usage": ["gaming"]},
    {"name": "HP Pavilion 15", "price": 14000000, "usage": ["hoc tap", "van phong"]},
    {"name": "Acer Swift 3", "price": 17000000, "usage": ["hoc tap", "lap trinh"]},
    {"name": "Lenovo Legion 5", "price": 30000000, "usage": ["gaming"]},
    {"name": "Razer Blade 14", "price": 45000000, "usage": ["gaming"]},
    {"name": "Dell XPS 13", "price": 32000000, "usage": ["lap trinh", "do hoa"]},
    {"name": "MacBook Pro 14", "price": 52000000, "usage": ["do hoa", "lap trinh"]},
    {"name": "Asus ROG Strix G", "price": 28000000, "usage": ["gaming"]},
    {"name": "HP ZBook Firefly", "price": 40000000, "usage": ["do hoa"]},
    {"name": "Acer Aspire 5", "price": 11000000, "usage": ["hoc tap", "van phong"]},
    {"name": "Lenovo ThinkPad T14", "price": 26000000, "usage": ["van phong", "lap trinh"]},
    {"name": "MSI Stealth 15M", "price": 35000000, "usage": ["gaming", "lap trinh"]},
    {"name": "HP Omen 16", "price": 27000000, "usage": ["gaming"]},
    {"name": "Asus ZenBook 14", "price": 19000000, "usage": ["hoc tap", "lap trinh"]},
    {"name": "Acer Predator Helios", "price": 38000000, "usage": ["gaming"]},
    {"name": "Lenovo Yoga Slim 7", "price": 21000000, "usage": ["hoc tap", "lap trinh"]},
    {"name": "Dell G15", "price": 24000000, "usage": ["gaming"]},
    {"name": "Huawei MateBook D 15", "price": 16000000, "usage": ["hoc tap", "van phong"]},
    {"name": "Microsoft Surface Laptop 4", "price": 29000000, "usage": ["hoc tap", "do hoa"]},
    {"name": "Asus ProArt Studiobook", "price": 60000000, "usage": ["do hoa"]},
]

# ================== HELPER ==================
def extract_price(price_text):
    if not price_text:
        return None

    # tìm số trong text
    numbers = re.findall(r'\d+', price_text)
    if not numbers:
        return None

    if len(numbers) > 1 and ("-" in price_text or "đến" in price_text or "toi" in price_text):
        price = int(numbers[-1])
    else:
        price = int(numbers[0])

    # nếu user nói "20 triệu"
    if "triệu" in price_text:
        return price * 1000000

    return price


def infer_usage(usage_text):
    if not usage_text:
        return None

    normalized_text = usage_text.lower()

    if any(keyword in normalized_text for keyword in ["game", "gaming", "chơi", "choi", "valorant", "pubg", "lol", "cs2"]):
        return "gaming"
    if any(keyword in normalized_text for keyword in ["văn phòng", "van phong", "office", "kế toán", "ke toan"]):
        return "van phong"
    if any(keyword in normalized_text for keyword in ["lập trình", "lap trinh", "code", "developer", "dev"]):
        return "lap trinh"
    if any(keyword in normalized_text for keyword in ["đồ họa", "do hoa", "edit", "render", "thiết kế", "thiet ke"]):
        return "do hoa"
    if any(keyword in normalized_text for keyword in ["học tập", "hoc tap", "sinh viên", "sinh vien", "study"]):
        return "hoc tap"

    return None


# ================== ACTION: RECOMMEND ==================
class ActionRecommendLaptop(Action):

    def name(self):
        return "action_recommend_laptop"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):

        latest_text = tracker.latest_message.get("text", "")
        current_price_text = tracker.get_slot("price")
        current_usage = tracker.get_slot("usage")

        inferred_usage = current_usage or infer_usage(latest_text)
        inferred_price_text = current_price_text or latest_text
        price = extract_price(inferred_price_text)

        events = []
        if inferred_usage and not current_usage:
            events.append(SlotSet("usage", inferred_usage))
        if price and not current_price_text:
            events.append(SlotSet("price", inferred_price_text))

        if not inferred_usage and not price:
            dispatcher.utter_message(
                text="Bạn muốn máy dùng để chơi game, văn phòng hay đồ họa? Cho mình thêm mức ngân sách nữa là mình lọc ngay cho bạn nhé."
            )
            return events

        if not inferred_usage:
            dispatcher.utter_message(
                text="Bạn cho mình biết nhu cầu sử dụng chính trước nhé: chơi game, văn phòng, đồ họa hay lập trình?"
            )
            return events

        if not price:
            dispatcher.utter_message(
                text="Bạn dự định mua laptop trong tầm giá khoảng bao nhiêu tiền ạ?"
            )
            return events

        results = []

        for lap in laptops:
            # lọc theo giá
            if price and lap["price"] > price:
                continue

            # lọc theo nhu cầu
            if inferred_usage:
                if inferred_usage not in lap["usage"]:
                    continue

            results.append(lap)

        if not results:
            dispatcher.utter_message(
                text=(
                    f"Hiện chưa có laptop phù hợp với nhu cầu '{inferred_usage}' trong tầm giá này. "
                    "Bạn thử tăng ngân sách hoặc đổi nhu cầu một chút, mình sẽ lọc lại ngay cho bạn."
                )
            )
            return events

        msg = "Gợi ý cho bạn:\n"
        for lap in results:
            msg += f"- {lap['name']} (~{lap['price']:,} VND)\n"

        dispatcher.utter_message(text=msg)
        return events


# ================== ACTION: CHECK PRICE ==================
class ActionCheckPrice(Action):

    def name(self):
        return "action_check_price"

    def run(self, dispatcher, tracker, domain):

        brand = tracker.get_slot("brand")

        if brand:
            dispatcher.utter_message(text=f"Dòng {brand} có giá từ 12 - 30 triệu tùy cấu hình.")
        else:
            dispatcher.utter_message(text="Laptop bên mình có giá từ 10 triệu đến 30 triệu nhé!")

        return []


# ================== ACTION: COMPARE ==================
class ActionCompareLaptop(Action):

    def name(self):
        return "action_compare_laptop"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message(
            text="So sánh nhanh:\n- Dell: bền, build tốt\n- ASUS: hiệu năng cao, gaming tốt\n- HP: thiết kế đẹp, văn phòng"
        )

        return []


# ================== ACTION: CONFIRM PURCHASE ==================
class ActionConfirmPurchase(Action):

    def name(self):
        return "action_confirm_purchase"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message(
            text="Cảm ơn bạn! Đơn hàng của bạn đã được tiếp nhận. Chúng tôi sẽ liên hệ với bạn trong 1-2 giờ để xác nhận chi tiết và thời gian giao hàng. Bạn có cần hỗ trợ gì thêm không?"
        )

        return []