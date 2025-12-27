import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


# -------------------------------
# App Config
# -------------------------------
st.set_page_config(page_title="Smart Packing Assistant", layout="centered")
st.title("🧳 Smart Packing Assistant")
st.caption("Upload an image and check cabin vs check-in items")

# -------------------------------
# Load YOLO Model
# -------------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# -------------------------------
# Label Normalization
# -------------------------------
LABEL_NORMALIZATION = {
    "cell phone": "phone",
    "mobile phone": "phone",
    "scissors": "scissors",
    "knife": "knife",
    "laptop": "laptop",
    "book": "book",
    "pen":"pen"
}

# -------------------------------
# Rule Engine
# -------------------------------
CABIN_ALLOWED = {
    "phone", "laptop", "book", "wallet", "keys"
}

CHECKIN_ONLY = {
    "scissors", "knife", "tool", "hammer"
}

NOT_ALLOWED = {
    "gun", "firearm", "explosive"
}

def classify_item(item_name: str):
    if item_name in NOT_ALLOWED:
        return "❌ Not Allowed", "Prohibited item as per aviation safety rules"
    elif item_name in CHECKIN_ONLY:
        return "🧳 Check-in Only", "Restricted or sharp item"
    elif item_name in CABIN_ALLOWED:
        return "✅ Cabin Allowed", "Common personal item"
    else:
        return "⚠️ Uncertain", "Unable to classify safely – check airline rules"

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
        st.info("Detecting items...")

        # Run detection
        results = model(np.array(image))[0]

        if results.boxes is None or len(results.boxes) == 0:
            st.warning("No recognizable items found.")
        else:
            st.subheader("📦 Detected Items & Packing Guidance")

            CONF_THRESHOLD = 0.15

            for box in results.boxes:
                confidence = float(box.conf[0])
                cls_id = int(box.cls[0])

                raw_label = model.names[cls_id].lower()
                item_name = LABEL_NORMALIZATION.get(raw_label, raw_label)

                classification, reason = classify_item(item_name)

                st.markdown(f"### 🧾 Item: **{item_name.title()}**")
                st.write(f"**Detection confidence:** {round(confidence, 2)}")

                if confidence < 0.2:
                    st.warning("⚠️ Low confidence detection")

                st.write(f"**Packing decision:** {classification}")
                st.write(f"**Reason:** {reason}")
                st.divider()

                st.success("Inspection complete ✅")

# -------------------------------
# Footer
# -------------------------------
st.caption(
    "⚠️ Guidance only. Final authority rests with airline and airport security."
)
