FIELD_LABELS = {
    "Age (yrs)": "Age (years)",
    "Weight (Kg)": "Weight (kg)",
    "Height(Cm)": "Height (cm)",
    "BMI": "Body Mass Index (BMI)",
    "Blood Group": "Blood group",
    "Pulse rate(bpm) ": "Pulse rate (beats per minute)",
    "RR (breaths/min)": "Respiratory rate (breaths per minute)",
    "Hb(g/dl)": "Haemoglobin (g/dL)",

    "Cycle(R/I)": "Menstrual cycle regularity",
    "Period length(days)": "Period length (days)",
    "Marraige Status (Yrs)": "Years married",
    "Pregnant(Y/N)": "Currently pregnant",
    "No. of aborptions": "Number of abortions",

    "I beta-HCG(mIU/mL)": "Beta human chorionic gonadotropin I (mIU/mL)",
    "II beta-HCG(mIU/mL)": "Beta human chorionic gonadotropin II (mIU/mL)",
    "FSH(mIU/mL)": "Follicle-stimulating hormone (FSH) (mIU/mL)",
    "LH(mIU/mL)": "Luteinizing hormone (LH) (mIU/mL)",
    "FSH/LH": "FSH to LH ratio",
    "TSH (mIU/L)": "Thyroid-stimulating hormone (TSH) (mIU/L)",
    "AMH(ng/mL)": "Anti-Müllerian hormone (AMH) (ng/mL)",
    "PRL(ng/mL)": "Prolactin (PRL) (ng/mL)",
    "Vit D3 (ng/mL)": "Vitamin D3 (ng/mL)",
    "PRG(ng/mL)": "Progesterone (PRG) (ng/mL)",
    "RBS(mg/dl)": "Random blood sugar (RBS) (mg/dL)",

    "Hip(inch)": "Hip circumference (inch)",
    "Waist(inch)": "Waist circumference (inch)",
    "Waist:Hip Ratio": "Waist-to-hip ratio",

    "Weight gain(Y/N)": "Weight gain",
    "hair growth(Y/N)": "Excess hair growth",
    "Skin darkening (Y/N)": "Skin darkening",
    "Hair loss(Y/N)": "Hair loss",
    "Pimples(Y/N)": "Pimples or acne",
    "Fast food (Y/N)": "Frequent fast food intake",
    "Reg.Exercise(Y/N)": "Regular exercise",

    "BP _Systolic (mmHg)": "Systolic blood pressure (mmHg)",
    "BP _Diastolic (mmHg)": "Diastolic blood pressure (mmHg)",

    "Follicle No. (L)": "Number of follicles (left ovary)",
    "Follicle No. (R)": "Number of follicles (right ovary)",
    "Avg. F size (L) (mm)": "Average follicle size, left ovary (mm)",
    "Avg. F size (R) (mm)": "Average follicle size, right ovary (mm)",
    "Endometrium (mm)": "Endometrium thickness (mm)",
}

BLOOD_GROUP_MAP = {
    "11": "O+",
    "12": "A+",
    "13": "B+",
    "14": "AB+",
    "15": "O-",
    "16": "A-",
    "17": "B-",
    "18": "AB-",
    11: "O+",
    12: "A+",
    13: "B+",
    14: "AB+",
    15: "O-",
    16: "A-",
    17: "B-",
    18: "AB-",
}

YES_NO_MAP = {
    "0": "No",
    "1": "Yes",
    0: "No",
    1: "Yes",
}

CYCLE_MAP = {
    "R": "Regular",
    "I": "Irregular",
    "2": "Regular",
    "4": "Irregular",
    2: "Regular",
    4: "Irregular",
    "0": "Regular",
    "1": "Irregular",
    0: "Regular",
    1: "Irregular",
}

BINARY_FEATURES = [
    "Pregnant(Y/N)",
    "Weight gain(Y/N)",
    "hair growth(Y/N)",
    "Skin darkening (Y/N)",
    "Hair loss(Y/N)",
    "Pimples(Y/N)",
    "Fast food (Y/N)",
    "Reg.Exercise(Y/N)",
]

SECTION_ORDER = [
    "Personal Information",
    "Cycle and Reproductive History",
    "Symptoms and Lifestyle",
    "Vital Signs and Body Measures",
    "Hormonal and Laboratory Values",
    "Ultrasound Findings",
    "Other Inputs",
]

def normalize_feature_name(feature: str) -> str:
    feature = feature.strip()
    if feature in ["Cycle length(days)", "Cycle length", "Cycle length(days) "]:
        return "Period length(days)"
    return feature


def get_display_label(feature: str) -> str:
    feature = normalize_feature_name(feature)
    return FIELD_LABELS.get(feature, feature)


def is_binary_feature(feature: str) -> bool:
    return feature in BINARY_FEATURES


def is_cycle_feature(feature: str) -> bool:
    return feature == "Cycle(R/I)"


def get_binary_options():
    return [0, 1]


def format_category_value(feature: str, value):
    if feature == "Blood Group":
        return BLOOD_GROUP_MAP.get(value, str(value))

    if feature == "Cycle(R/I)":
        return CYCLE_MAP.get(value, str(value))

    if is_binary_feature(feature):
        return YES_NO_MAP.get(value, str(value))

    return str(value)


def get_section(feature: str) -> str:
    feature = normalize_feature_name(feature)

    if feature in ["Age (yrs)", "Blood Group"]:
        return "Personal Information"

    if feature in [
        "Cycle(R/I)",
        "Period length(days)",
        "Marraige Status (Yrs)",
        "Pregnant(Y/N)",
        "No. of aborptions",
        "I beta-HCG(mIU/mL)",
        "II beta-HCG(mIU/mL)",
    ]:
        return "Cycle and Reproductive History"

    if feature in [
        "Weight gain(Y/N)",
        "hair growth(Y/N)",
        "Skin darkening (Y/N)",
        "Hair loss(Y/N)",
        "Pimples(Y/N)",
        "Fast food (Y/N)",
        "Reg.Exercise(Y/N)",
    ]:
        return "Symptoms and Lifestyle"

    if feature in [
        "Weight (Kg)",
        "Height(Cm)",
        "BMI",
        "Pulse rate(bpm) ",
        "RR (breaths/min)",
        "Hb(g/dl)",
        "Hip(inch)",
        "Waist(inch)",
        "Waist:Hip Ratio",
        "BP _Systolic (mmHg)",
        "BP _Diastolic (mmHg)",
    ]:
        return "Vital Signs and Body Measures"

    if feature in [
        "FSH(mIU/mL)",
        "LH(mIU/mL)",
        "FSH/LH",
        "TSH (mIU/L)",
        "AMH(ng/mL)",
        "PRL(ng/mL)",
        "Vit D3 (ng/mL)",
        "PRG(ng/mL)",
        "RBS(mg/dl)",
    ]:
        return "Hormonal and Laboratory Values"

    if feature in [
        "Follicle No. (L)",
        "Follicle No. (R)",
        "Avg. F size (L) (mm)",
        "Avg. F size (R) (mm)",
        "Endometrium (mm)",
    ]:
        return "Ultrasound Findings"

    return "Other Inputs"


def get_numeric_step(feature: str) -> float:
    if "Age" in feature or "No." in feature or "Pulse" in feature or "RR" in feature or "BP" in feature:
        return 1.0
    return 0.1

