from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re

# ================== FAKE DATABASE ==================
laptops = [
    {"name": "ASUS Vivobook 15", "price": 15000000, "usage": ["hoc tap", "van phong"]},
    {"name": "Dell Inspiron 14", "price": 18000000, "usage": ["lap trinh", "van phong"]},
    {"name": "Lenovo IdeaPad 3", "price": 12000000, "usage": ["hoc tap"]},
    {"name": "Acer Nitro 5", "price": 22000000, "usage": ["gaming"]},
    {"name": "ASUS TUF Gaming", "price": 25000000, "usage": ["gaming"]},
    {"name": "MacBook Air M1", "price": 23000000, "usage": ["lap trinh", "van phong"]},
]

# ================== HELPER ==================
def extract_price(price_text):
    if not price_text:
        return None

    # tìm số trong text
    numbers = re.findall(r'\d+', price_text)
    if not numbers:
        return None

    price = int(numbers[0])

    # nếu user nói "20 triệu"
    if "triệu" in price_text:
        return price * 1000000

    return price


# ================== ACTION: RECOMMEND ==================
class ActionRecommendLaptop(Action):

    def name(self):
        return "action_recommend_laptop"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):

        price_text = tracker.get_slot("price")
        usage = tracker.get_slot("usage")

        price = extract_price(price_text)

        results = []

        for lap in laptops:
            # lọc theo giá
            if price and lap["price"] > price:
                continue

            # lọc theo nhu cầu
            if usage:
                if not any(u in usage.lower() for u in lap["usage"]):
                    continue

            results.append(lap)

        if not results:
            dispatcher.utter_message(text="😅 Không tìm được máy phù hợp, bạn thử tăng ngân sách hoặc đổi nhu cầu nhé.")
            return []

        msg = "🔥 Gợi ý cho bạn:\n"
        for lap in results:
            msg += f"- {lap['name']} (~{lap['price']:,} VND)\n"

        dispatcher.utter_message(text=msg)
        return []


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
            text="👉 So sánh nhanh:\n- Dell: bền, build tốt\n- ASUS: hiệu năng cao, gaming tốt\n- HP: thiết kế đẹp, văn phòng"
        )

        return []