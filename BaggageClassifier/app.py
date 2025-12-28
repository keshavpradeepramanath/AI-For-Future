# -------------------------------
# Silence warnings
# -------------------------------
import warnings
warnings.filterwarnings("ignore")

# -------------------------------
# Imports
# -------------------------------
import streamlit as st
import numpy as np
from PIL import Image
from ultralytics import YOLO

from rule_engine import get_rule   # ✅ DB-backed rule engine

# -------------------------------
# App Config
# -------------------------------
st.set_page_config(
    page_title="Smart Packing Assistant",
    layout="centered"
)

st.title("🧳 Smart Packing Assistant")
st.caption(
    "Upload an image and classify items using airline & IATA rules "
    "(human-approved, deterministic)"
)

# -------------------------------
# Load YOLO Model
# -------------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8s.pt")

model = load_model()

# -------------------------------
# Item Normalization
# -------------------------------
def normalize_item(yolo_label: str) -> str:
    mapping = {
        "cell phone": "phone",
        "mobile phone": "phone",
        "laptop": "laptop",
        "book": "book",
        "scissors": "scissors",
        "knife": "knife",
        "backpack": "bag",
        "handbag": "bag"
    }
    return mapping.get(yolo_label, yolo_label)

# -------------------------------
# Sidebar (Flight Context)
# -------------------------------
st.sidebar.header("✈️ Flight Context")

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
    st.image(image, caption="Uploaded Image", use_column_width=True)

    inspect_btn = st.button("🔍 Inspect Items")

    if inspect_btn:
        st.info("Detecting items...")

        results = model(np.array(image))[0]

        if results.boxes is None or len(results.boxes) == 0:
            st.warning(
                "No recognizable items detected. "
                "Try placing items separately on a clear surface."
            )
        else:
            st.subheader("📦 Detected Items & Packing Guidance")

            CONF_THRESHOLD = 0.15

            for box in results.boxes:
                confidence = float(box.conf[0])
                cls_id = int(box.cls[0])

                raw_label = model.names[cls_id].lower()
                item = normalize_item(raw_label)

                decision, reference = get_rule(
                    item=item,
                    airline=airline
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
    "⚠️ This app provides guidance only. "
    "Final authority rests with airline and airport security."
)
