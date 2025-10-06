

def calculate_calories(age, gender, height_cm, weight_kg, activity_level, temperature_c):

    # 1️⃣ Base BMR using Mifflin–St Jeor
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender.lower() == "female":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    # 2️⃣ Activity multiplier
    activity_multipliers = {
        1: 1.2,
        2: 1.375,
        3: 1.55,
        4: 1.725,
        5: 1.9
    }

    if activity_level not in activity_multipliers:
        raise ValueError("Activity level must be between 1 and 5")

    tdee = bmr * activity_multipliers[activity_level]

    # 3️⃣ Temperature adjustment
    if temperature_c < 15:
        tdee *= 1.05  # 5% higher in cold
    elif temperature_c > 30:
        tdee *= 0.95  # 5% lower in heat

    return round(tdee, 2)