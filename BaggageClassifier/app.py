# -------------------------------
# Silence PyTorch / YOLO warnings
# -------------------------------
import warnings
warnings.filterwarnings("ignore")

# -------------------------------
# Imports
# -------------------------------
import streamlit as st
import json
import numpy as np
from PIL import Image
from ultralytics import YOLO

# -------------------------------
# App Config
# -------------------------------
st.set_page_config(page_title="Smart Packing Assistant", layout="centered")
st.title("🧳 Smart Packing Assistant")
st.caption("Upload an image and classify items using airline & IATA rules")

# -------------------------------
# Load YOLO Model
# -------------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8s.pt")  # better recall than nano

model = load_model()

# -------------------------------
# Load Airline / IATA Rules
# -------------------------------
@st.cache_data
def load_rules():
    with open("airline_rules.json", "r") as f:
        return json.load(f)

RULES = load_rules()

# -------------------------------
# Item Normalization
# -------------------------------
def normalize_item(yolo_label: str) -> str:
    mapping = {
        "cell phone": "phone",
        "mobile phone": "phone",
        "scissors": "scissors",
        "knife": "knife",
        "laptop": "laptop",
        "book": "book",
        "backpack": "bag",
        "handbag": "bag"
    }
    return mapping.get(yolo_label, yolo_label)

# -------------------------------
# Rule Engine (Deterministic)
# -------------------------------
def evaluate_item(item: str, airline: str, rules: dict):
    # Airline override first
    airline_rules = rules.get("Airlines", {}).get(airline, {})
    if item in airline_rules:
        override = airline_rules[item]
        return override["decision"], override["reference"]

    # Fall back to IATA
    iata_rules = rules.get("IATA", {}).get(item)
    if iata_rules:
        return iata_rules["decision"], iata_rules["reference"]

    return "⚠️ Uncertain", "No official rule found"

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("✈️ Flight Details")

airline = st.sidebar.selectbox(
    "Select Airline",
    ["IATA", "Indigo", "Emirates", "Lufthansa"]
)

# -------------------------------
# Image Upload
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload an image (camera or gallery)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    inspect_btn = st.button("🔍 Inspect Items")

    if inspect_btn:
        st.info("Detecting items in image...")

        results = model(np.array(image))[0]

        if results.boxes is None or len(results.boxes) == 0:
            st.warning(
                "No recognizable items detected. "
                "Try placing items separately on a clear surface."
            )
        else:
            st.subheader("📦 Detected Items & Packing Rules")

            CONF_THRESHOLD = 0.15

            for box in results.boxes:
                confidence = float(box.conf[0])
                cls_id = int(box.cls[0])

                raw_label = model.names[cls_id].lower()
                item = normalize_item(raw_label)

                decision, reference = evaluate_item(
                    item=item,
                    airline=airline,
                    rules=RULES
                )

                st.markdown(f"### 🧾 Item: **{item.title()}**")
                st.write(f"**Detection confidence:** {round(confidence, 2)}")

                if confidence < CONF_THRESHOLD:
                    st.warning("⚠️ Low confidence detection")

                st.write(f"**Packing decision:** {decision}")
                st.write(f"**Rule reference:** {reference}")
                st.divider()

            st.success("Inspection complete ✅")

# -------------------------------
# Footer
# -------------------------------
st.caption(
    "⚠️ Guidance only. Final authority rests with airline and airport security."
)
