import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def analyze_document(file_bytes: bytes, file_extension: str) -> str:
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
    
    ext = file_extension.lower()
    if ext == 'pdf':
        mime_type = 'application/pdf'
    elif ext == 'png':
        mime_type = 'image/png'
    elif ext in ['jpg', 'jpeg']:
        mime_type = 'image/jpeg'
    else:
        mime_type = 'application/octet-stream'

    b64_data = base64.b64encode(file_bytes).decode()
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Extract the Total Amount, Date, and Service Provider from this document. Return the result as a clear summary."},
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{b64_data}"}
            }
        ]
    )
    
    response = llm.invoke([message])
    return response.content
