
# ASL Translator with ESP32-S3 and Raspberry Pi

This project enables real-time American Sign Language (ASL) gesture recognition using an ESP32-S3 board with a camera, and translates the recognized gestures into English and Chinese using a Raspberry Pi running a transformer model.

---

##  Components

- **ESP32-S3 (XIAO)**: Captures hand gesture images using onboard camera, classifies the gesture using a deployed Edge Impulse model, and sends results via UART.
- **Raspberry Pi**: Receives gesture names from UART, converts them into English phrases using WordNinja, and translates to Chinese using `facebook/m2m100_418M` model.

---

## File Structure

### 1. `ESP32_Live_Detection.ino`
- Arduino sketch to run on the XIAO ESP32-S3.
- Initializes camera and UART.
- Captures image and performs inference using Edge Impulse SDK.
- Sends final gesture prediction over UART to Raspberry Pi.

### 2. `asl_translator.py`
- Python script to run on Raspberry Pi.
- Receives ASL letter strings over UART.
- Uses `wordninja` to split letters into valid English words.
- Translates result using the `facebook/m2m100_418M` model via Hugging Face Transformers.

---

##  Installation and Setup

### Raspberry Pi
```bash
sudo apt update
sudo apt install python3-pip
pip install torch transformers wordninja sentencepiece pyserial
```

### ESP32-S3
1. Flash the `ESP32_Live_Detection.ino` using Arduino IDE.
2. Make sure camera pins are set for XIAO ESP32-S3.
3. Open Serial Monitor to debug.

---

## UART Communication
- ESP32-S3 sends final classified gesture result over UART (9600 baud).
- Raspberry Pi listens on `/dev/serial0` or similar.
- Match TX/RX pins correctly between boards.

---

##  Example Flow

1. ESP32 detects gesture: `ILOVEYOU`
2. Sends via UART: `ILOVEYOU`
3. Raspberry Pi processes:
   ```
   English: I LOVE YOU
   Chinese: 我爱你
   ```

---

## Notes

- You can modify Python script to auto-run on boot for continuous operation.
- M2M100 model supports multilingual translation with good accuracy and runs on CPU.
