import torch
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import serial
import wordninja
import time

# Load M2M100 model
model_name = "facebook/m2m100_418M"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print("Device set to use", device)

# Set up UART connection
uart_port = "/dev/serial0"  # Change if needed
baud_rate = 9600
ser = serial.Serial(uart_port, baud_rate, timeout=1)

# Initialize buffer
buffer = ""

def translate_to_chinese(text):
    tokenizer.src_lang = "en"
    encoded = tokenizer(text, return_tensors="pt").to(device)
    generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id("zh"))
    return tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

print("Waiting for ASL input via UART...")

try:
    while True:
        if ser.in_waiting > 0:
            byte = ser.read().decode("utf-8", errors="ignore")
            if byte == "\n":
                asl_input = buffer.strip()
                buffer = ""
                if not asl_input:
                    continue
                english = " ".join(wordninja.split(asl_input.upper()))
                print("English:", english)
                try:
                    chinese = translate_to_chinese(english)
                    print("Chinese:", chinese)
                except Exception as e:
                    print("⚠️ Translation failed:", e)
            else:
                buffer += byte
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    ser.close()
