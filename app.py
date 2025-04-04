#import necessary modules
import streamlit as st
from pathlib import Path
import google.generativeai as genai

from api_key import api_key

#configure genai with APi key

genai.configure(api_key=api_key)
#setup the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

#define safety settings

safety_settings = [
    {
        "category": "HARM_CATEGORY_DEROGATORY",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_VIOLENCE",
        "threshold": "BLOCK_LOW_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUAL",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_LOW_AND_ABOVE",
    },
]

system_prompt="""

You are a highly skilled medical practitioner and image analysis expert working with a renowned hospital's diagnostics team.

Your primary responsibility is to meticulously examine and interpret a wide range of medical images—including X-rays, CT scans, MRI images, and histopathology slides—to identify any anomalies, diseases, or health risks.

Your evaluations must be:

Clinically accurate and aligned with evidence-based standards

Structured, objective, and clear for integration into radiology/pathology reports

Sensitive to patient context (age, symptoms, history)

Cautious in diagnosis; offer differential interpretations where needed

Cognizant of the limitations of AI and recommend clinical confirmation steps

For each image, you will:

Identify and describe visible abnormalities or unusual patterns

Suggest likely differential diagnoses, including severity and possible implications

Highlight specific regions of interest

Recommend further tests or imaging for clinical confirmation

Generate a report-style summary using radiological or pathological standards

Avoid definitive diagnoses unless image evidence is conclusive. Your role is to assist, not replace, human clinical judgment.


"""



# Set up the Streamlit page
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

st.title("Welcome to the Vital Image Analytics App!") 

st.subheader("An application that can help users to identify medical images")

uploaded_file = st.file_uploader("upload the medical image for analysis", type=["png", "jpg","jpeg"])

submit_button = st.button("Generate the Analysis")

if submit_button:
    #process the uploaded image
    image_data=uploaded_file.getvalue()
    
    #making our image ready
    
    image_parts = [
        {
        "mime_type": "image/jpeg",
        "data": image_data
        }
    ]
    #making our prompt ready
    prompt_parts = [

        image_parts[0],
        system_prompt,
        
    ]
    
    #generate response based on prompt and image
    
    st.image(image_data)
    
    response = model.generate_content(prompt_parts)
    
    st.write(response.text)

