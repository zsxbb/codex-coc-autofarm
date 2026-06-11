import time
import pyautogui
import cv2
import numpy as np
import random
import threading
import os
from python_imagesearch.imagesearch import *

CODEX_CONFIDENCE = 0.95

# Determine base directory (parent of scripts/) for absolute path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODEX_IMAGE_DIR = os.path.join(BASE_DIR, "images-fix") + os.sep

CODEX_TROOPS = [
    {"image": "rootrider.png", "count": 15},
    {"image": "superwitch.png", "count": 50},
    {"image": "miniwarden.png", "count": 1},
]

CODEX_HEROES = ["dragonduke.png", "queen.png", "royalchampion.png", "warden.png"]

CODEX_HERO_SETTINGS = {
    "dragonduke.png":   {"delay": 10, "active": True},
    "queen.png":          {"delay": 5, "active": True},
    "warden.png":         {"delay": 15, "active": True},
    "royalchampion.png":  {"delay": 15, "active": True},

}

CODEX_FIRST_DETECTION_IMG = "nexticon.png"
CODEX_SPELLS = [
    {
        "image": "hastespell.png",
        #"points": [(0.478, 0.138), (0.543, 0.248), (0.603, 0.325), (0.671, 0.426), (0.72, 0.503)]
        "points": [(0.501, 0.218), (0.433, 0.303), (0.588, 0.313), (0.31, 0.41), (0.491, 0.416), (0.676, 0.412), (0.267, 0.537), (0.413, 0.536), (0.514, 0.524), (0.589, 0.526), (0.674, 0.525)]
    }
]

CODEX_SPAWN_POINTS =[
    (0.897, 0.477), (0.867, 0.446), (0.849, 0.432), (0.827, 0.412), 
(0.809, 0.386), (0.781, 0.357), (0.756, 0.317), (0.735, 0.294), 
(0.714, 0.256), (0.694, 0.226), (0.662, 0.191), (0.643, 0.162), 
(0.609, 0.122), (0.588, 0.096), (0.564, 0.066), (0.559, 0.059), 
(0.448, 0.06), (0.425, 0.1), (0.395, 0.129), (0.354, 0.169), 
(0.349, 0.197), (0.327, 0.22), (0.308, 0.243), (0.293, 0.261),
 (0.276, 0.292), (0.237, 0.335), (0.216, 0.363), (0.196, 0.387),
  (0.183, 0.403), (0.159, 0.442), (0.127, 0.472), (0.143, 0.519), 
  (0.172, 0.567), (0.209, 0.608), (0.228, 0.628), (0.248, 0.653), 
  (0.271, 0.678), (0.297, 0.724), (0.317, 0.736), (0.867, 0.513), 
  (0.843, 0.556), (0.821, 0.58), (0.79, 0.616), (0.751, 0.656), (0.726, 0.699), 
(0.702, 0.722), (0.681, 0.742), (0.673, 0.751)
]

CODEX_JEDA_AWAL_BATTLE  = 1     
CODEX_WAKTU_TUNGGU_BATTLE = 60    
CODEX_JEDA_PULANG_HOME  = 2     


try:
    import pygetwindow as gw
    HAS_GW = True
except ImportError:
    HAS_GW = False

def get_emulator_rect():
    if HAS_GW:
        try:
            windows = gw.getWindowsWithTitle('Clash of Clans')
            if windows:
                win = windows[0]
                if win.isMinimized: win.restore()
                return (win.left, win.top, win.width, win.height)
        except: pass
    return None

def is_image_visible(image_names, custom_confidence=None):
    conf = custom_confidence if custom_confidence else CODEX_CONFIDENCE
    if isinstance(image_names, str): image_names = [image_names]
    rect = get_emulator_rect()
    if not rect: return False
    reg = (rect[0], rect[1], rect[2], rect[3])
    for image_name in image_names:
        image_path = CODEX_IMAGE_DIR + image_name
        try:
            if pyautogui.locateOnScreen(image_path, region=reg, confidence=conf): return True
        except:
            if imagesearcharea(image_path, reg[0], reg[1], reg[0]+reg[2], reg[1]+reg[3], conf)[0] != -1: return True
    return False

def wait_for_image(image_names, timeout=15, sub_region=None, confidence=None):
    if isinstance(image_names, str): image_names = [image_names]
    rect = get_emulator_rect()
    if not rect: return None
    search_reg = sub_region if sub_region else (rect[0], rect[1], rect[2], rect[3])
    conf = confidence if confidence else CODEX_CONFIDENCE
    start_time = time.time()
    while time.time() - start_time < timeout:
        for image_name in image_names:
            image_path = CODEX_IMAGE_DIR + image_name
            try:
                pos = pyautogui.locateCenterOnScreen(image_path, region=search_reg, confidence=conf)
                if pos:
                    return pos, image_name
            except:
                pos = imagesearcharea(image_path, search_reg[0], search_reg[1], search_reg[0]+search_reg[2], search_reg[1]+search_reg[3], conf)
                if pos[0] != -1:
                    img = cv2.imread(image_path)
                    if img is not None:
                        h, w = img.shape[:2]
                        real_pos = (pos[0] + search_reg[0] + (w // 2), pos[1] + search_reg[1] + (h // 2))
                        return real_pos, image_name
        time.sleep(0.5)
    return None

def wait_and_click(image_names, timeout=15, sub_region=None):
    res = wait_for_image(image_names, timeout, sub_region)
    if res:
        pos, name = res
        pyautogui.click(pos)
        print(f"[CODEX-OK] {name} clicked at {pos}!")
        return pos
    return None

def deploy_all_troops():
    rect = get_emulator_rect()
    if not rect: return
    ox, oy, win_w, win_h = rect
    unit_reg = (rect[0], rect[1] + int(rect[3]*0.65), rect[2], int(rect[3]*0.35))
    for troop in CODEX_TROOPS:
        if wait_and_click(troop["image"], timeout=10, sub_region=unit_reg):
            print(f"[CODEX-TROOP] Deploying {troop['image']} ({troop['count']}x)...")
            count = 0
            while count < int(troop["count"]):
                rx, ry = random.choice(CODEX_SPAWN_POINTS)
                rx_rand = rx + random.uniform(-0.008, 0.008)
                ry_rand = ry + random.uniform(-0.008, 0.008)
                pyautogui.click(int(ox + (win_w * rx_rand)), int(oy + (win_h * ry_rand)))
                time.sleep(random.uniform(0.02, 0.04))
                count += 1

def deploy_all_heroes():
    deployed_heroes = []
    rect = get_emulator_rect()
    if not rect: return []
    ox, oy, win_w, win_h = rect
    unit_reg = (rect[0], rect[1] + int(rect[3]*0.65), rect[2], int(rect[3]*0.35))
    for hero in CODEX_HEROES:
        pos = wait_and_click(hero, timeout=3, sub_region=unit_reg)
        if pos:
            if hero in CODEX_HERO_SETTINGS and CODEX_HERO_SETTINGS[hero]["active"]:
                deployed_heroes.append({
                    "name": hero,
                    "time": time.time(),
                    "pos": pos,
                    "delay": CODEX_HERO_SETTINGS[hero]["delay"],
                    "done": False
                })
                print(f"[CODEX-HERO] {hero} deployed! Skill delay: {CODEX_HERO_SETTINGS[hero]['delay']}s")
            rx, ry = random.choice(CODEX_SPAWN_POINTS)
            rx_rand = rx + random.uniform(-0.005, 0.005)
            ry_rand = ry + random.uniform(-0.005, 0.005)
            pyautogui.click(int(ox + (win_w * rx_rand)), int(oy + (win_h * ry_rand)))
            time.sleep(random.uniform(0.1, 0.2))
    return deployed_heroes

def deploy_all_spells():
    rect = get_emulator_rect()
    if not rect: return
    ox, oy, win_w, win_h = rect
    unit_reg = (rect[0], rect[1] + int(rect[3]*0.65), rect[2], int(rect[3]*0.35))
    for spell in CODEX_SPELLS:
        if wait_and_click(spell["image"], timeout=5, sub_region=unit_reg):
            print(f"[CODEX-SPELL] Activating {spell['image']}...")
            for rx, ry in spell["points"]:
                pyautogui.click(int(ox + (win_w * rx)), int(oy + (win_h * ry)))
                time.sleep(0.1)

def battle_and_ability_management(deployed_heroes):
    start_battle = time.time()
    while time.time() - start_battle < CODEX_WAKTU_TUNGGU_BATTLE:
        if not is_image_visible(["EndBattle.png", "Surrender.png"], custom_confidence=0.8):
            time.sleep(2) 
            if not is_image_visible(["EndBattle.png", "Surrender.png"], custom_confidence=0.8):
                print("[CODEX-BATTLE] Done naturally.")
                return "NATURAL"
        for hero in deployed_heroes:
            if not hero["done"] and (time.time() - hero["time"] >= hero["delay"]):
                print(f"[CODEX-SKILL] ACTIVATING {hero['name'].upper()} POWER!")
                pyautogui.click(hero["pos"])
                hero["done"] = True
        time.sleep(0.5)
    
    if is_image_visible(["EndBattle.png", "Surrender.png"], custom_confidence=0.8):
        print(f"[CODEX-TIMEOUT] Time limit reached ({CODEX_WAKTU_TUNGGU_BATTLE}s). Clicking End...")
        wait_and_click(["EndBattle.png", "Surrender.png"], timeout=5)
    return "TIMEOUT"

def main_sequence():
    print("========================================")
    print(f"           CODEX COC FARM              ")
    print("========================================")

    while True:
        # Recovery check: are we already in a battle?
        if is_image_visible(CODEX_FIRST_DETECTION_IMG):
            print(f"[CODEX-RECOVERY] Already in battle ({CODEX_FIRST_DETECTION_IMG} detected).")
        else:
            print("\n[CODEX-SEARCH] Looking for Attack_Map.png...")
            if not wait_and_click("Attack_Map.png", timeout=60): continue
            time.sleep(0.5)
            if not wait_and_click("FindAMatch.png", timeout=20): continue
            time.sleep(0.5)
            if not wait_and_click("Attack_Green.png", timeout=30): continue

        time.sleep(CODEX_JEDA_AWAL_BATTLE)
        print(f"[CODEX-WAIT] Waiting for battle UI ({CODEX_FIRST_DETECTION_IMG})...")
        if not wait_for_image(CODEX_FIRST_DETECTION_IMG, timeout=45):
            print(f"[CODEX-SKIP] Failed to detect {CODEX_FIRST_DETECTION_IMG}, skipping this cycle.")
            continue
        
        time.sleep(1.5) 
        
        deploy_all_troops()
        deployed_heroes = deploy_all_heroes()
        deploy_all_spells()
        
        status_battle = battle_and_ability_management(deployed_heroes)
        print(f"[CODEX-INFO] Cleanup process ({status_battle})...")
        if status_battle == "TIMEOUT":
            wait_and_click("Okay.png", timeout=2)
        time.sleep(CODEX_JEDA_PULANG_HOME)
        print("[CODEX-INFO] Returning Home...")
        wait_and_click("ReturnHome.png", timeout=15)
        
        print("\n[CODEX-SUCCESS] Attack Cycle Complete. Starting next cycle...\n")
        time.sleep(3)

if __name__ == "__main__":
    try:
        main_sequence()
    except KeyboardInterrupt:
        print("\nBot dimatikan.")
