import json

def set_trading_state(enabled: bool):
    with open("state.json", "w") as f:
        json.dump({"trading_enabled": enabled}, f)

def get_trading_state() -> bool:
    try:
        with open("state.json", "r") as f:
            data = json.load(f)
            return data.get("trading_enabled", True)
    except:
        return True  # إذا لم يوجد الملف، نفترض أن التداول مفعل
