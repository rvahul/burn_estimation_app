import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
from rembg import remove
from utils.segmentation import segment_burn
from utils.preprocessing import enhance_image
import io

st.title("AI-Based Burn Percentage & Fluid Estimation")

# Step 1: Fill in the basic details
with st.form("patient_details"):
    patient_name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    weight = st.number_input("Weight (kg)", min_value=1)
    injury_time = st.time_input("Time of Injury")
    submitted = st.form_submit_button("Continue")

if submitted:
    st.success("Details submitted! Please upload the burn image.")

# Step 2: Upload the Image
uploaded_file = st.file_uploader("Upload Burn Image", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Uploaded Image", use_column_width=True)

    # Step 3: Remove Background
    result_img_bytes = remove(uploaded_file.read())
    cleaned_image = Image.open(io.BytesIO(result_img_bytes))
    st.image(cleaned_image, caption="Image after Background Removal")

    # Step 4: Enhance the Features
    enhanced_image = enhance_image(cleaned_image)
    st.image(enhanced_image, caption="Enhanced Image for Segmentation")

    # Step 5: Segment Burn Region
    mask, mask_overlay = segment_burn(enhanced_image)
    st.image(mask_overlay, caption="Segmented Burn Area (Overlay)")

    # Step 6: Calculate TBSA and Fluid Requirement
    burn_pct = np.round((np.sum(mask) / mask.size) * 100, 2)  # Example calculation
    fluid_24hr = 4 * weight * burn_pct
    fluid_8hr = fluid_24hr / 2
    fluid_16hr = fluid_24hr / 2

    # Step 7: Generate the Report
    st.markdown(f"""
    ### Automated Burn Analysis Report
    - **Name:** {patient_name}
    - **Age:** {age}
    - **Weight:** {weight} kg
    - **Burn TBSA (estimated):** {burn_pct:.2f}%
    - **Fluid Requirement [Last 24h] (Parkland formula):** {fluid_24hr:.0f} mL
      - First 8h: {fluid_8hr:.0f} mL
      - Next 16h: {fluid_16hr:.0f} mL
    """)
    st.image(mask_overlay, caption="Burn Segmentation Visualization (for report)")

