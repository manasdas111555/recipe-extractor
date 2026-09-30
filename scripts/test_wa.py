import time
import subprocess
import pyautogui
import urllib.parse
import webbrowser
from pathlib import Path

def send_txt_file_to_whatsapp(phone_number: str, txt_file_path: str):
    txt_path = Path(txt_file_path).resolve()
    if not txt_path.exists():
        print(f"File not found: {txt_path}")
        return False

    phone = phone_number.strip().replace(" ", "").replace("-", "").replace("+", "")
    
    # 1. Open WhatsApp Web chat window
    wa_url = f"https://web.whatsapp.com/send?phone={phone}"
    print(f"Opening WhatsApp Web for phone: {phone}...")
    webbrowser.open(wa_url)

    # 2. Wait for WhatsApp Web chat interface to load fully
    print("Waiting 12 seconds for WhatsApp Web to load...")
    time.sleep(12)

    # 3. Copy the .txt file directly to Windows Clipboard as File object
    print(f"Copying file {txt_path} to Windows Clipboard...")
    ps_cmd = f"Set-Clipboard -Path '{txt_path}'"
    subprocess.run(["powershell", "-command", ps_cmd], check=True)

    # 4. Focus browser and Paste (Ctrl + V)
    print("Pasting file into WhatsApp Web...")
    pyautogui.hotkey('ctrl', 'v')
    
    # 5. Wait for attachment preview window to appear in WhatsApp Web
    time.sleep(2)

    # 6. Press Enter to SEND the document file
    print("Pressing Enter to send the file...")
    pyautogui.press('enter')
    
    time.sleep(2)
    print("Sent file successfully!")
    return True

if __name__ == "__main__":
    # Test with dummy file
    test_file = Path(r"C:\Users\admin\Downloads\Reciepe\test_recipe.txt")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("Sample Recipe Content\n- 1 cup flour\n- 2 eggs")
    
    print("Created test file.")
