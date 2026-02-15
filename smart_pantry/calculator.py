from .models import UserProfile, ActivityLevel

def calculate_bmr(user: UserProfile) -> float:
    """
    Calculates Basal Metabolic Rate (BMR) using the Mifflin-St Jeor Equation.
    """
    bmr = (10 * user.weight_kg) + (6.25 * user.height_cm) - (5 * user.age)

    if user.gender.lower() == 'male':
        bmr += 5
    elif user.gender.lower() == 'female':
        bmr -= 161
    else:
        # Fallback for other gender identities, using an average or default to female (safer lower bound)
        bmr -= 161

    return bmr

def calculate_tdee(user: UserProfile) -> float:
    """
    Calculates Total Daily Energy Expenditure (TDEE).
    """
    bmr = calculate_bmr(user)
    return bmr * user.activity_level.value
