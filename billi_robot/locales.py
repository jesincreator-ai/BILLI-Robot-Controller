"""Offline status text used by the voice layer."""

MESSAGES = {
    "en": {"stopped": "Movement stopped", "guardian_veto": "Safety system blocked movement",
           "low_battery": "Battery is low"},
    "ta": {"stopped": "இயக்கம் நிறுத்தப்பட்டது", "guardian_veto": "பாதுகாப்பு அமைப்பு இயக்கத்தைத் தடுத்தது",
           "low_battery": "மின்கலம் குறைவாக உள்ளது"},
    "si": {"stopped": "චලනය නතර කළා", "guardian_veto": "ආරක්ෂක පද්ධතිය චලනය නතර කළා",
           "low_battery": "බැටරිය අඩුයි"},
}


def message(key, language="en"):
    table = MESSAGES.get(language, MESSAGES["en"])
    return table.get(key, MESSAGES["en"].get(key, key))
