import pyautogui
import time
import os

try:
    import pygetwindow as gw
    from pynput import mouse
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

CODEX_RECORDED_POINTS = []
CODEX_LAST_PERC = (0, 0)
CODEX_IS_INSIDE_COC = False

def detector():
    global CODEX_IS_INSIDE_COC, CODEX_LAST_PERC
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    if not HAS_LIBS:
        print("[CODEX-ERROR] Library 'pynput' or 'pygetwindow' not found.")
        print("[CODEX-ERROR] Install with: pip install pynput pygetwindow\n")
        return

    sw, sh = pyautogui.size()
    
    print("====================================================")
    print(f"      CODEX COC FARM - SPAWN POINT RECORDER        ")
    print("====================================================")
    print(f" MONITOR : {sw}x{sh}")
    
    windows = gw.getWindowsWithTitle('Clash of Clans')
    if windows:
        win = windows[0]
        print(f" COC ENV : {win.width}x{win.height} at ({win.left}, {win.top})")
    else:
        print(" [CODEX-WARN] 'Clash of Clans' window not found!")

    print("\n [ INSTRUCTIONS ]")
    print(" 1. Left Click inside CoC Window to SAVE coordinates.")
    print(" 2. Press Ctrl+C to STOP and COPY the list.")
    print("-" * 65)

    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.left and windows:
            win = windows[0]
            if win.left <= x <= win.right and win.top <= y <= win.bottom:
                rel_x = x - win.left
                rel_y = y - win.top
                px = round(rel_x / win.width, 3)
                py = round(rel_y / win.height, 3)
                
                CODEX_RECORDED_POINTS.append((px, py))
                print(f"\n [CODEX-SAVED] ({px}, {py}) | Total: {len(CODEX_RECORDED_POINTS)} points")

    listener = mouse.Listener(on_click=on_click)
    listener.start()

    try:
        while True:
            x, y = pyautogui.position()
            if windows:
                win = windows[0]
                CODEX_IS_INSIDE_COC = (win.left <= x <= win.right) and (win.top <= y <= win.bottom)
                
                if CODEX_IS_INSIDE_COC:
                    rel_x = x - win.left
                    rel_y = y - win.top
                    px = round(rel_x / win.width, 3)
                    py = round(rel_y / win.height, 3)
                    CODEX_LAST_PERC = (px, py)
                    print(f" [CODEX] MOUSE AT {CODEX_LAST_PERC} (Click to Save)      ", end="\r")
                else:
                    print(" [CODEX] Cursor outside CoC window...              ", end="\r")
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        listener.stop()
        print("\n\n" + "="*50)
        print(" CODEX RECORDING RESULTS (Copy to autoattack.py):")
        print("="*50)
        if CODEX_RECORDED_POINTS:
            print(f"points = {CODEX_RECORDED_POINTS}\n")
        else:
            print("\n No coordinates recorded.")
        print("="*50)

if __name__ == "__main__":
    detector()
