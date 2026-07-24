import flet as ft
import json
import os
import asyncio
import random
from functools import partial
import datetime

SAVE_FILE = os.path.join(os.path.dirname(__file__), "rpg_progress.json")





# ============ GLOBALS ============
page = None
completed_lessons = []
current_lesson_index = 0
current_theme = "light"
temp_theme = "light"
unlocked_themes = ["light", "dark"]
owned_themes = ["light", "dark"]
xp = 0
level = 1
boss_hp = 100
boss_mode = False
bosses_defeated = 0
lesson_stage = "notes"
current_quiz_index = 0
quiz_score = 0
FORCE_RESET = False
current_player = "Player"
all_players = {}
last_daily_claim = ""
daily_streak = 0
correct_answers_count = 0



def save_data():
    save_progress() # just use the main save function

THEMES = {
    "light": {
        "bg": ft.Colors.WHITE, 
        "card": ft.Colors.GREY_100,
        "accent": ft.Colors.GREEN,
        "text": ft.Colors.BLACK,
        "mode": ft.ThemeMode.LIGHT,
        "price": 0
    },
    "dark": {
        "bg": ft.Colors.BLACK, 
        "card": ft.Colors.GREY_900,
        "accent": ft.Colors.GREEN,
        "text": ft.Colors.WHITE,
        "mode": ft.ThemeMode.DARK,
        "price": 0
    },
    "cyber": {
        "bg": ft.Colors.PURPLE_900, 
        "card": ft.Colors.PURPLE_800,
        "accent": ft.Colors.CYAN_400,
        "text": ft.Colors.CYAN_200,
        "mode": ft.ThemeMode.LIGHT,
        "price": 500
    },
    "ocean": {
        "bg": ft.Colors.BLUE_700, 
        "card": ft.Colors.BLUE_900,
        "accent": ft.Colors.CYAN_400,
        "text": ft.Colors.WHITE,
        "mode": ft.ThemeMode.LIGHT,
        "price": 100
    },
    "forest": {
        "bg": ft.Colors.GREEN_800, 
        "card": ft.Colors.GREEN_900,
        "accent": ft.Colors.LIGHT_GREEN_400,
        "text": ft.Colors.WHITE,
        "mode": ft.ThemeMode.LIGHT,
        "price": 250
    },
}


THEME_PRICES = [
    {"name": "light", "display": "Light Theme", "cost": 0},
    {"name": "dark", "display": "Dark Theme", "cost": 0},
    {"name": "ocean", "display": "Ocean Theme", "cost": 100},
    {"name": "forest", "display": "Forest Theme", "cost": 250},
    {"name": "cyber", "display": "Cyberpunk Theme", "cost": 500},
]
# 50 LESSONS
LESSONS = [
    {"title": "Lesson 1: Print & Output", 
     "notes": "IN SIMPLE WORDS:\nprint() is how your game talks.\n\nHOW IT WORKS:\n1. Write print(\n2. Put text in \"quotes\"\n3. Close )\n\nWHY IT MATTERS:\nWithout print, players can't see anything happening.", 
     "example": 'print("Hello Hero")\nprint("You have 100 HP")', 
     "quiz": [{"q": "What does print do?", "o": ["A. Saves file", "B. Shows text on screen", "C. Deletes data"], "a": 1}]},

    {"title": "Lesson 2: Variables", 
     "notes": "IN SIMPLE WORDS:\nVariables are boxes with names. You put data inside.\n\nHOW IT WORKS:\nname = \"Aria\"  <- Put text in box called 'name'\nhp = 100      <- Put number in box called 'hp'\n\nWHY IT MATTERS:\nSo you can remember player HP, name, score and change it later.\n\nCOMMON MISTAKE:\nDon't put quotes around numbers: hp = 100 not \"100\"", 
     "example": 'name = "Aria"\nhp = 100\nprint(name, "has", hp, "HP")', 
     "quiz": [{"q": "Which is a variable?", "o": ["A. print", "B. hp", "C. if"], "a": 1}]},

    {"title": "Lesson 3: Data Types", 
     "notes": "IN SIMPLE WORDS:\n4 main types of data in games.\n\nTHE 4 TYPES:\n1. int = whole numbers: 5, 100, -3  <- HP, Score\n2. float = decimals: 3.14, 0.5      <- Damage x1.5\n3. str = text in quotes: \"Sword\"   <- Names\n4. bool = True or False             <- is_alive", 
     "example": 'x = 5       # int\ny = 3.14    # float\nname = "Sword"  # str\nis_alive = True # bool', 
     "quiz": [{"q": "What type is 3.14?", "o": ["A. int", "B. float", "C. str"], "a": 1}]},

    {"title": "Lesson 4: Comments", 
     "notes": "IN SIMPLE WORDS:\n# Comments are notes for YOU. Python ignores them.\n\nHOW IT WORKS:\n# This is a comment\nprint(\"Hi\") # This also works\n\nWHY IT MATTERS:\nSo you remember why you wrote code 2 weeks later. Big games need this.", 
     "example": '# Give player starting HP\nhp = 100', 
     "quiz": [{"q": "How do you comment?", "o": ["A. //", "B. #", "C. /* */"], "a": 1}]},

    {"title": "Lesson 5: Input", 
     "notes": "IN SIMPLE WORDS:\ninput() lets the player type and talk back to your game.\n\nHOW IT WORKS:\nname = input(\"What is your name? \")\n\nIMPORTANT: input() ALWAYS gives you TEXT/str. Even if they type 10.\nTo get a number: age = int(input(\"Age? \"))", 
     "example": 'name = input("Enter hero name: ")\nprint("Welcome", name)', 
     "quiz": [{"q": "input() returns what by default?", "o": ["A. int", "B. str", "C. bool"], "a": 1}]},

    {"title": "Lesson 6: Type Casting", 
     "notes": "IN SIMPLE WORDS:\nChanging data from one type to another.\n\nWHEN YOU NEED IT:\ninput() gives \"10\" as text. But you need number 10 to do math.\n\nTHE 3 CASTS:\nint(\"10\") -> 10\nfloat(\"3.5\") -> 3.5\nstr(100) -> \"100\"", 
     "example": 'age = int(input("Enter age: "))\nage_next_year = age + 1', 
     "quiz": [{"q": "Convert '10' to number?", "o": ["A. str('10')", "B. int('10')", "C. float('10')"], "a": 1}]},

    {"title": "Lesson 7: Math Operators", 
     "notes": "IN SIMPLE WORDS:\nHow to do math in your RPG.\n\nTHE OPERATORS:\n+ add    - subtract    * multiply    / divide\n// floor divide = 7//2 = 3\n% remainder = 7%2 = 1\n** power = 2**3 = 8", 
     "example": 'damage = 10 * 2\nheal = 50 // 2', 
     "quiz": [{"q": "7 // 2 equals?", "o": ["A. 3.5", "B. 3", "C. 4"], "a": 1}]},

    {"title": "Lesson 8: String Methods", 
     "notes": "IN SIMPLE WORDS:\nTools to change text for your game dialogue.\n\nUSEFUL ONES:\n\"hello\".upper() -> \"HELLO\"\n\"HELLO\".lower() -> \"hello\"\nlen(\"sword\") -> 5", 
     "example": 'name = input("Name: ")\nprint(name.upper())', 
     "quiz": [{"q": "'Hello'.lower() gives?", "o": ["A. HELLO", "B. hello", "C. Hello"], "a": 1}]},

    {"title": "Lesson 9: If Statements", 
     "notes": "IN SIMPLE WORDS:\nMake decisions. Run code ONLY if something is True.\n\nHOW IT WORKS:\nif hp > 0:\n    print(\"You are alive\")\n\nINDENTATION MATTERS! Use 4 spaces under if.", 
     "example": 'if hp > 0:\n print("Alive")\nelse:\n print("Game Over")', 
     "quiz": [{"q": "if runs when?", "o": ["A. Always", "B. If condition is True", "C. If False"], "a": 1}]},

    {"title": "Lesson 10: Else & Elif", 
     "notes": "IN SIMPLE WORDS:\nif = check this\nelif = check this other thing\nelse = if nothing above worked\n\nEXAMPLE:\nif score > 90: \"A\"\nelif score > 70: \"B\"\nelse: \"Fail\"", 
     "example": 'if x>10:\n print("Big")\nelif x>5:\n print("Mid")\nelse:\n print("Small")', 
     "quiz": [{"q": "What runs if first if is False but elif is True?", "o": ["A. else", "B. elif", "C. Both"], "a": 1}]},

    {"title": "Lesson 11: While Loops", 
     "notes": "IN SIMPLE WORDS:\nRepeat code WHILE a condition is True. Like combat turns.\n\nHOW IT WORKS:\nwhile hp > 0:\n hp = hp - 10\n print(hp)\n\nWARNING: If condition never becomes False, it loops forever!", 
     "example": 'hp = 50\nwhile hp > 0:\n print("Fighting... HP:", hp)\n hp = hp - 10', 
     "quiz": [{"q": "While stops when?", "o": ["A. Condition is True", "B. Condition is False", "C. Never"], "a": 1}]},

    {"title": "Lesson 12: For Loops", 
     "notes": "IN SIMPLE WORDS:\nLoop over items. Perfect for lists, inventory, or counting.\n\nHOW IT WORKS:\nfor i in range(5):\n print(i)\n\nrange(5) makes: 0, 1, 2, 3, 4", 
     "example": 'for i in range(5):\n print("Enemy", i)\n\ninventory = ["sword", "shield"]\nfor item in inventory:\n print(item)', 
     "quiz": [{"q": "range(3) gives?", "o": ["A. 1,2,3", "B. 0,1,2", "C. 0,1,2,3"], "a": 1}]},

    {"title": "Lesson 13: Break & Continue", 
     "notes": "IN SIMPLE WORDS:\n2 ways to control loops.\n\nbreak = STOP the loop completely. Run away from fight.\ncontinue = SKIP this turn. Go to next item.", 
     "example": 'for i in range(5):\n if i == 2:\n continue # skip 2\n if i == 4:\n break # stop at 4\n print(i)', 
     "quiz": [{"q": "break does what?", "o": ["A. Skip 1 turn", "B. Stop loop completely", "C. Restart loop"], "a": 1}]},

    {"title": "Lesson 14: Lists", 
     "notes": "IN SIMPLE WORDS:\nList = ordered collection. Your inventory or party.\n\nHOW IT WORKS:\ninventory = [\"sword\", \"potion\", \"shield\"]\nPositions start at 0!", 
     "example": 'inventory = ["sword", "potion"]\ninventory.append("shield")\nprint(inventory[0]) # sword', 
     "quiz": [{"q": "Get first item?", "o": ["A. [0]", "B. [1]", "C. [-1]"], "a": 0}]},

    {"title": "Lesson 15: List Methods", 
     "notes": "IN SIMPLE WORDS:\nTools to change lists.\n\nMOST USED:\n.append(x) = add to end\n.pop() = remove last item\nlen(list) = count items\n.remove(x) = remove specific item", 
     "example": 'inventory.append("potion")\ninventory.pop()\nprint(len(inventory))', 
     "quiz": [{"q": "Add item to end?", "o": ["A. append", "B. add", "C. push"], "a": 0}]},

    {"title": "Lesson 16: List Indexing", 
     "notes": "IN SIMPLE WORDS:\nGet items by their position number.\n\nREMEMBER:\n[0] = first item\n[1] = second item\n[-1] = last item", 
     "example": 'party = ["Aria", "Bob", "Chris"]\nprint(party[0]) # Aria\nprint(party[-1]) # Chris', 
     "quiz": [{"q": "Last item index?", "o": ["A. 0", "B. -1", "C. len"], "a": 1}]},

    {"title": "Lesson 17: List Slicing", 
     "notes": "IN SIMPLE WORDS:\nGet part of a list. list[start:stop]\n\nEXAMPLE:\n[0:2] = get item 0 and 1\n[:3] = first 3 items\n[2:] = from item 2 to end", 
     "example": 'inventory = [1,2,3,4,5]\nprint(inventory[1:3]) # [2,3]', 
     "quiz": [{"q": "Get items 0 and 1?", "o": ["A. [0:2]", "B. [0:1]", "C. [1:2]"], "a": 0}]},

    {"title": "Lesson 18: Tuples", 
     "notes": "IN SIMPLE WORDS:\nTuple = list you CANNOT change. Use () instead of []\n\nWHEN TO USE:\nFor fixed data like coordinates (x, y) or colors (r,g,b)", 
     "example": 'pos = (10, 20)\n# pos[0] = 15 <- ERROR! Can not change', 
     "quiz": [{"q": "Can you change tuple?", "o": ["A. Yes", "B. No", "C. Sometimes"], "a": 1}]},

    {"title": "Lesson 19: Dictionaries", 
     "notes": "IN SIMPLE WORDS:\nDict = key:value pairs. Like player stats sheet.\n\nHOW IT WORKS:\nplayer = {\"hp\": 100, \"name\": \"Hero\"}\nTo get: player[\"hp\"]", 
     "example": 'player = {"hp": 100, "name": "Hero"}\nplayer["hp"] = 80\nprint(player["name"])', 
     "quiz": [{"q": "Get hp from player?", "o": ["A. player[0]", "B. player['hp']", "C. player.hp"], "a": 1}]},

    {"title": "Lesson 20: Dict Methods", 
     "notes": "IN SIMPLE WORDS:\nTools for dictionaries.\n\n.keys() = get all keys\n.values() = get all values\n.get(key) = get value safely", 
     "example": 'player.keys() # dict_keys([\'hp\', \'name\'])\nplayer.get("mana", 0)', 
     "quiz": [{"q": "Get all keys?", "o": ["A. keys()", "B. items()", "C. values()"], "a": 0}]},

    {"title": "Lesson 21: Functions def", 
     "notes": "IN SIMPLE WORDS:\ndef = make reusable code. Don't repeat yourself.\n\nHOW IT WORKS:\ndef attack():\n print(\"You hit!\")\n\nThen call it: attack()", 
     "example": 'def heal():\n print("Healed 20 HP")\nheal()\nheal()', 
     "quiz": [{"q": "Keyword to make function?", "o": ["A. func", "B. def", "C. function"], "a": 1}]},

    {"title": "Lesson 22: Parameters & Return", 
     "notes": "IN SIMPLE WORDS:\nParameter = input to function\nreturn = output from function\nEXAMPLE:\ndef add(a, b):\n return a + b", 
     "example": 'def damage(atk, defense):\n return atk - defense\nprint(damage(20, 5))',
     "quiz": [{"q": "What sends value back?", "o": ["A. print", "B. return", "C. def"], "a": 1}]},

    {"title": "Lesson 23: Scope", 
     "notes": "IN SIMPLE WORDS:\nWhere can you use the variable?\n\nlocal = only inside function\n global = everywhere. Use 'global' keyword to change it", 
     "example": 'xp = 0\ndef add_xp():\n global xp\n xp = xp + 10', 
     "quiz": [{"q": "Variable inside function is?", "o": ["A. global", "B. local", "C. both"], "a": 1}]},

    {"title": "Lesson 24: *args and **kwargs", 
     "notes": "IN SIMPLE WORDS:\nLet function take unlimited inputs.\n\n*args = many positional args -> becomes tuple\n**kwargs = many named args -> becomes dict", 
     "example": 'def fight(*enemies):\n for e in enemies:\n print(e)', 
     "quiz": [{"q": "*args collects?", "o": ["A. dict", "B. list", "C. tuple"], "a": 2}]},

    {"title": "Lesson 25: Lambda Functions", 
     "notes": "IN SIMPLE WORDS:\nSmall 1-line function with no name.\n\nUSE: For quick math or sorting\nSYNTAX: lambda x: x * 2", 
     "example": 'double = lambda x: x*2\nprint(double(5))', 
     "quiz": [{"q": "Lambda is for?", "o": ["A. Big functions", "B. Small 1-line functions", "C. Classes"], "a": 1}]},

    {"title": "Lesson 26: Classes & __init__", 
     "notes": "IN SIMPLE WORDS:\nClass = blueprint to make objects. Like \"Player\" blueprint.\n\n__init__ = runs automatically when you create object", 
     "example": 'class Player:\n def __init__(self, hp):\n self.hp = hp\np1 = Player(100)', 
     "quiz": [{"q": "__init__ runs when?", "o": ["A. Delete object", "B. Create object", "C. Loop"], "a": 1}]},

    {"title": "Lesson 27: Methods", 
     "notes": "IN SIMPLE WORDS:\nFunctions inside a class. self = the object itself.\n\nself.hp means \"this object's hp\"", 
     "example": 'def take_damage(self, dmg):\n self.hp -= dmg', 
     "quiz": [{"q": "What is self?", "o": ["A. Nothing", "B. The object", "C. A keyword"], "a": 1}]},

    {"title": "Lesson 28: Inheritance", 
     "notes": "IN SIMPLE WORDS:\nChild class gets all code from Parent class.\n\nEXAMPLE: Boss is a type of Player", 
     "example": 'class Boss(Player):\n pass # Gets all Player methods', 
     "quiz": [{"q": "Inheritance gives?", "o": ["A. Nothing", "B. Parent methods", "C. Errors"], "a": 1}]},

    {"title": "Lesson 29: Encapsulation", 
     "notes": "IN SIMPLE WORDS:\nHide internal details. _variable means \"private, don't touch\"\n\nCONVENTION: _secret = for internal use only", 
     "example": 'class Player:\n def __init__(self):\n self._secret = 5', 
     "quiz": [{"q": "_ means?", "o": ["A. Public", "B. Private convention", "C. Static"], "a": 1}]},

    {"title": "Lesson 30: Objects in Lists", 
     "notes": "IN SIMPLE WORDS:\nStore many objects in 1 list. Like a party of players.\n\nLOOP THROUGH: for p in party:", 
     "example": 'party = [Player(), Player()]\nfor p in party:\n print(p.hp)', 
     "quiz": [{"q": "How loop party?", "o": ["A. for p in party", "B. for party", "C. loop party"], "a": 0}]},

    {"title": "Lesson 31: Try/Except", 
     "notes": "IN SIMPLE WORDS:\nCatch errors so game doesn't crash.\n\nHOW IT WORKS:\ntry: dangerous code\nexcept: run if error happens", 
     "example": 'try:\n x = 10/0\nexcept ZeroDivisionError:\n print("Can not divide by 0")', 
     "quiz": [{"q": "Catch error with?", "o": ["A. catch", "B. except", "C. error"], "a": 1}]},

    {"title": "Lesson 32: Finally", 
     "notes": "IN SIMPLE WORDS:\nfinally ALWAYS runs. Error or no error.\n\nUSE: To close files or save game", 
     "example": 'try:\n...\nfinally:\n print("Game saved")', 
     "quiz": [{"q": "finally runs?", "o": ["A. Only on error", "B. Always", "C. Never"], "a": 1}]},

    {"title": "Lesson 33: Reading Files", 
     "notes": "IN SIMPLE WORDS:\nopen(file, 'r') = read mode\n\nREMEMBER: Always close file after", 
     "example": 'f = open("save.txt", "r")\ndata = f.read()\nf.close()', 
     "quiz": [{"q": "Read mode?", "o": ["A. w", "B. r", "C. a"], "a": 1}]},

    {"title": "Lesson 34: Writing Files", 
     "notes": "IN SIMPLE WORDS:\nopen(file, 'w') = write mode. OVERWRITES file!\n\n'a' = append mode. Adds to end", 
     "example": 'f = open("save.txt", "w")\nf.write("HP:100")\nf.close()', 
     "quiz": [{"q": "Write mode?", "o": ["A. r", "B. w", "C. read"], "a": 1}]},

    {"title": "Lesson 35: JSON", 
     "notes": "IN SIMPLE WORDS:\nJSON = save Python dicts to file. Perfect for save games.\n\njson.dump = save to file\njson.load = load from file", 
     "example": 'import json\njson.dump(player, f)', 
     "quiz": [{"q": "Save dict to file?", "o": ["A. json.load", "B. json.dump", "C. json.save"], "a": 1}]},

    {"title": "Lesson 36: Modules", 
     "notes": "IN SIMPLE WORDS:\nimport = bring code from other files\n\nEXAMPLES: import random, import math", 
     "example": 'import random\nprint(random.randint(1,10))', 
     "quiz": [{"q": "Import keyword?", "o": ["A. include", "B. import", "C. use"], "a": 1}]},

    {"title": "Lesson 37: Pip Packages", 
     "notes": "IN SIMPLE WORDS:\npip = installer for extra libraries\n\nCOMMAND: pip install flet", 
     "example": '# In terminal:\npip install flet', 
     "quiz": [{"q": "Install command?", "o": ["A. pip install", "B. install pip", "C. get pip"], "a": 0}]},

    {"title": "Lesson 38: DateTime", 
     "notes": "IN SIMPLE WORDS:\nWork with dates and time. For daily quests!\n\n.date.today() = today's date", 
     "example": 'import datetime\nprint(datetime.date.today())', 
     "quiz": [{"q": "Get today?", "o": ["A. date.now()", "B. date.today()", "C. today()"], "a": 1}]},

    {"title": "Lesson 39: Random", 
     "notes": "IN SIMPLE WORDS:\nMake random numbers for loot, damage, enemies.\n\nrandint(a,b) = random integer from a to b", 
     "example": 'random.randint(1, 10) # 1 to 10', 
     "quiz": [{"q": "Random 1-10?", "o": ["A. rand(1,10)", "B. randint(1,10)", "C. random(10)"], "a": 1}]},

    {"title": "Lesson 40: Virtual Environments", 
     "notes": "IN SIMPLE WORDS:\nvenv = separate folder for packages. Keeps projects clean.\n\nCOMMAND: python -m venv env", 
     "example": '# Create:\npython -m venv env', 
     "quiz": [{"q": "Create venv?", "o": ["A. venv create", "B. python -m venv", "C. make venv"], "a": 1}]},

    {"title": "Lesson 41: Flet Basics", 
     "notes": "IN SIMPLE WORDS:\nFlet = build apps with Python. No HTML needed.\n\nMain object: ft.Page", 
     "example": 'import flet as ft\ndef main(page: ft.Page):', 
     "quiz": [{"q": "Flet page object?", "o": ["A. ft.Window", "B. ft.Page", "C. ft.App"], "a": 1}]},

    {"title": "Lesson 42: Flet Controls", 
     "notes": "IN SIMPLE WORDS:\nControls = things you see. Buttons, Text, etc.\n\nColumn = stack vertical\nRow = stack horizontal", 
     "example": 'ft.Text("Hello")\nft.Column([btn1, btn2])', 
     "quiz": [{"q": "Stack vertically?", "o": ["A. Row", "B. Column", "C. Stack"], "a": 1}]},

    {"title": "Lesson 43: Flet Events", 
     "notes": "IN SIMPLE WORDS:\non_click = run function when button clicked\nSYNTAX: on_click=function_name", 
     "example": 'ft.Button("Click", on_click=func)', 
     "quiz": [{"q": "Button click event?", "o": ["A. onclick", "B. on_click", "C. click"], "a": 1}]},

    {"title": "Lesson 44: State & Global", 
     "notes": "IN SIMPLE WORDS:\nglobal = let function change variable outside\npage.update() = redraw screen in Flet", 
     "example": 'global xp\nxp += 10\npage.update()', 
     "quiz": [{"q": "Change outside var?", "o": ["A. local", "B. global", "C. static"], "a": 1}]},

    {"title": "Lesson 45: Navigation", 
     "notes": "IN SIMPLE WORDS:\npage.go() = change to different screen/page\n\nUSE: Go from Menu to Lessons", 
     "example": 'page.go("/lessons")', 
     "quiz": [{"q": "Change page?", "o": ["A. page.change", "B. page.go", "C. page.next"], "a": 1}]},

    {"title": "Lesson 46: Themes", 
     "notes": "IN SIMPLE WORDS:\npage.theme_mode = change light/dark\n\nYou can also make custom color themes", 
     "example": 'page.theme_mode = "dark"', 
     "quiz": [{"q": "Dark mode?", "o": ["A. light", "B. dark", "C. night"], "a": 1}]},

    {"title": "Lesson 47: Save System", 
     "notes": "IN SIMPLE WORDS:\nBest way to save = JSON + files\n\nSave dict with all player data", 
     "example": 'json.dump(all_players, f)', 
     "quiz": [{"q": "Best for save data?", "o": ["A. txt", "B. json", "C. csv"], "a": 1}]},

    {"title": "Lesson 48: Animations", 
     "notes": "IN SIMPLE WORDS:\nMake things move/fade in Flet\nanimate_opacity = fade\nanimate_size = grow/shrink", 
     "example": 'ft.Container(animate_opacity=300)', 
     "quiz": [{"q": "Animate fade?", "o": ["A. animate_size", "B. animate_opacity", "C. animate_move"], "a": 1}]},

    {"title": "Lesson 49: Deploy Flet", 
     "notes": "IN SIMPLE WORDS:\nBuild your app so others can play it.\n\nCOMMANDS: flet build apk, flet build exe, flet build web", 
     "example": 'flet build apk', 
     "quiz": [{"q": "Build Android?", "o": ["A. build web", "B. build apk", "C. build exe"], "a": 1}]},

    {"title": "Lesson 50: Capstone Project", 
     "notes": "IN SIMPLE WORDS:\nFINAL PROJECT! Use everything you learned.\n\nBUILD: Full RPG with classes, save system, and Flet UI", 
     "example": 'class Game:\n def __init__(self):\n self.player = Player()', 
     "quiz": [{"q": "Capstone uses?", "o": ["A. Only print", "B. All concepts", "C. Only loops"], "a": 1}]}
]

BOSS_LESSONS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
BOSS_REWARDS = {5: {"name": "Boss: Loop Goblin", "xp": 100}, 10: {"name": "Boss: Function Dragon", "xp": 200}, 15: {"name": "Boss: List Hydra", "xp": 300}, 20: {"name": "Boss: Dict Wizard", "xp": 400}, 25: {"name": "Boss: OOP Knight", "xp": 500}, 30: {"name": "Boss: Error Demon", "xp": 600}, 35: {"name": "Boss: File Titan", "xp": 700}, 40: {"name": "Boss: Module Mage", "xp": 800}, 45: {"name": "Boss: Flet Lord", "xp": 900}, 50: {"name": "FINAL BOSS: Python King", "xp": 1000}}

achievements = [
    {"name": "First Steps", "desc": "Complete Lesson 1", "unlocked": False, "icon": "🥇"},
    {"name": "Loop Master", "desc": "Complete Lesson 5", "unlocked": False, "icon": "🔁"},
    {"name": "Function Pro", "desc": "Complete Lesson 10", "unlocked": False, "icon": "⚙️"},
    {"name": "Bug Slayer", "desc": "Get 10 correct answers", "unlocked": False, "icon": "🐛"},
    {"name": "Speed Runner", "desc": "Complete 3 lessons in 1 day", "unlocked": False, "icon": "⚡"},
    {"name": "Collector", "desc": "Unlock 3 themes", "unlocked": False, "icon": "🎨"},
    {"name": "Boss Hunter", "desc": "Defeat 3 Bosses", "unlocked": False, "icon": "👹"},
    {"name": "Perfectionist", "desc": "Get 5/5 in a quiz", "unlocked": False, "icon": "💯"},
    {"name": "Grinder", "desc": "Reach Level 5", "unlocked": False, "icon": "📈"},
    {"name": "Python Graduate", "desc": "Complete all 50 lessons", "unlocked": False, "icon": "🎓"}
]

def set_defaults():
    global xp, level, boss_hp, unlocked_themes, current_theme, completed_lessons, current_lesson_index, correct_answers_count, bosses_defeated, daily_streak, last_daily_claim
    xp = 0; level = 1; boss_hp = 100; bosses_defeated = 0; daily_streak = 0; last_daily_claim = ""
    unlocked_themes = ["light", "dark"]; current_theme = "light"; completed_lessons = []; current_lesson_index = 0; correct_answers_count = 0
    for a in achievements: a["unlocked"] = False

def save_progress():
    if FORCE_RESET: return
    global all_players
    all_players[current_player] = {
        "xp": xp, "level": level, "boss_hp": boss_hp, "bosses_defeated": bosses_defeated,
        "unlocked_themes": unlocked_themes, 
        "owned_themes": owned_themes, # ADD THIS LINE
        "current_theme": current_theme,
        "completed_lessons": list(completed_lessons), "current_lesson_index": current_lesson_index,
        "achievements": [a["unlocked"] for a in achievements], "correct_answers_count": correct_answers_count,
        "daily_streak": daily_streak, "last_daily_claim": last_daily_claim
    }
    with open(SAVE_FILE, "w") as f: json.dump(all_players, f)

def show_snackbar(page: ft.Page, message: str):
    if page:
        page.snack_bar = ft.SnackBar(
            ft.Text(message, size=16), # NO ICON
            bgcolor=THEMES[current_theme]["accent"]
        )
        page.snack_bar.open = True
        page.update()

def check_daily_quest(page):
    global xp,last_daily_claim, daily_streak
    today = str(datetime.date.today())
    if last_daily_claim!= today:
        xp += 50; daily_streak += 1; last_daily_claim = today
        show_snackbar(page, f"Daily Quest Complete! +50 XP | Streak: {daily_streak} 🔥")
        save_progress()
    if daily_streak == 3 and last_daily_claim == today: # ADD check so it only fires once
        xp += 100; show_snackbar(page, "3 Day Streak! +100 XP")
    if daily_streak == 7 and "ocean" not in unlocked_themes:
        unlocked_themes.append("ocean"); show_snackbar(page, "7 Day Streak! Free Theme Unlocked")
    save_progress() # ADD THIS so streak 3/7 saves

def load_progress():
    global xp, level, boss_hp, unlocked_themes, owned_themes, current_theme, completed_lessons, current_lesson_index, correct_answers_count, all_players, current_player, daily_streak, last_daily_claim, bosses_defeated # ADD owned_themes
    if FORCE_RESET:
        return

    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                all_players = json.load(f)

            # FIX 1: Handle old save format where data was saved without player name
            if "xp" in all_players:
                all_players = {"Player1": all_players}

            # FIX 2: If file is empty {} or corrupted, reset
            if not all_players:
                all_players = {}
                set_defaults()
                return

            # FIX 3: Pick current player. If not set, pick first one
            if current_player not in all_players:
                current_player = list(all_players.keys())[0]

            data = all_players[current_player]

            # Load data into globals
            xp = data.get("xp", 0)
            level = data.get("level", 1)
            boss_hp = data.get("boss_hp", 100)
            bosses_defeated = data.get("bosses_defeated", 0)
            unlocked_themes = data.get("unlocked_themes", ["light", "dark"])
            owned_themes = data.get("owned_themes", ["light", "dark"])
            current_theme = data.get("current_theme", "light")
            completed_lessons = data.get("completed_lessons", [])
            current_lesson_index = data.get("current_lesson_index", 0)

            saved_achs = data.get("achievements", [])
            for i, val in enumerate(saved_achs):
                if i < len(achievements):
                    achievements[i]["unlocked"] = val

            correct_answers_count = data.get("correct_answers_count", 0)
            daily_streak = data.get("daily_streak", 0)
            last_daily_claim = data.get("last_daily_claim", "")

        except Exception as e:
            print("LOAD ERROR:", e)
            all_players = {}
            set_defaults()
    else:
        # No save file exists yet
        all_players = {}

def update_xp(amount):
    global xp, level
    xp += amount
    if xp >= level * 100:
        level += 1; xp = 0
        show_snackbar(page, f"LEVEL UP! Level {level}")
    save_progress(); page.update()

def check_achievements(page: ft.Page, lesson_num: int):
    global correct_answers_count, bosses_defeated
    newly_unlocked = []
    if lesson_num == 1 and not achievements[0]["unlocked"]: achievements[0]["unlocked"] = True; newly_unlocked.append(achievements[0])
    if lesson_num == 5 and not achievements[1]["unlocked"]: achievements[1]["unlocked"] = True; newly_unlocked.append(achievements[1])
    if lesson_num == 10 and not achievements[2]["unlocked"]: achievements[2]["unlocked"] = True; newly_unlocked.append(achievements[2])
    if correct_answers_count >= 10 and not achievements[3]["unlocked"]: achievements[3]["unlocked"] = True; newly_unlocked.append(achievements[3])
    if len(completed_lessons) >= 3 and not achievements[4]["unlocked"]: achievements[4]["unlocked"] = True; newly_unlocked.append(achievements[4])
    if len(unlocked_themes) >= 3 and not achievements[5]["unlocked"]: achievements[5]["unlocked"] = True; newly_unlocked.append(achievements[5])
    if bosses_defeated >= 3 and not achievements[6]["unlocked"]: achievements[6]["unlocked"] = True; newly_unlocked.append(achievements[6])
    if quiz_score == len(LESSONS[current_lesson_index]["quiz"]) and not achievements[7]["unlocked"]: achievements[7]["unlocked"] = True; newly_unlocked.append(achievements[7])
    if level >= 5 and not achievements[8]["unlocked"]: achievements[8]["unlocked"] = True; newly_unlocked.append(achievements[8])
    if lesson_num == 50 and not achievements[9]["unlocked"]: achievements[9]["unlocked"] = True; newly_unlocked.append(achievements[9])
    for ach in newly_unlocked: show_snackbar(page, f"{ach['icon']} Achievement Unlocked: {ach['name']}!")
    save_progress()

def start_boss_quiz(): # REMOVED e parameter
    global lesson_stage, current_quiz_index, boss_hp, boss_mode, quiz_score
    lesson_stage = "quiz"; current_quiz_index = 0; quiz_score = 0; boss_hp = 3; boss_mode = True
    random.shuffle(LESSONS[current_lesson_index]["quiz"])
    show_snackbar(page, "BOSS FIGHT! Get 3 right in a row!")
    show_lesson_screen()
def start_quiz(e):
    global lesson_stage, current_quiz_index, quiz_score, boss_mode
    lesson_stage = "quiz"
    current_quiz_index = 0
    quiz_score = 0
    
    if (current_lesson_index + 1) in BOSS_REWARDS:
        boss_mode = True
        boss_hp = 3
        show_snackbar(page, "BOSS FIGHT! Get 3 right in a row!")
    else:
        boss_mode = False
    
    random.shuffle(LESSONS[current_lesson_index]["quiz"])
    show_lesson_screen()
def open_notes(index):
    global current_lesson_index, lesson_stage, current_quiz_index, quiz_score

    current_lesson_index = index
    lesson_stage = "notes" # Always start with notes
    current_quiz_index = 0
    quiz_score = 0
    
    show_lesson_screen() # Show notes first
def show_lessons():
    global xp
    page.clean()
    t = THEMES[current_theme]
    
    lesson_cards = []
    for i, lesson in enumerate(LESSONS):
        xp_needed = i * 10  # Lesson 1=0, Lesson 2=10, Lesson 3=20
        is_unlocked = xp >= xp_needed
        is_completed = i in completed_lessons
        is_boss = (i + 1) in BOSS_REWARDS

        if is_completed:
            status = "✅ COMPLETED"
            color = "#00FF00"
        elif is_unlocked:
            status = "🔓 UNLOCKED" if not is_boss else "👹 BOSS"
            color = t["accent"]
        else:
            status = "🔒 LOCKED"
            color = "#555"

        btn_text = f"{status} Lesson {i+1}: {lesson['title']}\nNeed: {xp_needed} XP"

        lesson_cards.append(
            ft.ElevatedButton(
                content=ft.Text(btn_text, color="#000", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, size=16), # FORCE BLACK TEXT
                on_click=lambda e, idx=i: open_notes(idx),
                disabled=not is_unlocked,
                width=750,
                height=80,
                bgcolor=t["accent"], # USE ACCENT AS BUTTON BG INSTEAD
            )
        )

    page.add(
        ft.Column([
            ft.Text("📚 PYTHON RPG - 50 LESSONS", size=28, weight=ft.FontWeight.BOLD, color=t["text"]),
            ft.Text(f"Total XP: {xp}", size=18, color=t["accent"]),
            ft.Divider(),
            ft.Container(
                content=ft.Column(lesson_cards, scroll=ft.ScrollMode.AUTO, spacing=10),
                height=500
            ),
            ft.ElevatedButton(
                content=ft.Text("⬅️ Back to Menu", color="#000"), # FIX THIS ONE TOO
                on_click=lambda e: show_menu(), 
                bgcolor=t["accent"]
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )
    page.update()
def check_quiz_answer(e):
    global current_quiz_index, quiz_score, correct_answers_count, boss_hp, boss_mode, bosses_defeated
    
    lesson = LESSONS[current_lesson_index]
    q = lesson["quiz"][current_quiz_index]
    selected = e.control.data
    
    if selected == q["a"]:
        quiz_score += 1
        correct_answers_count += 1
        update_xp(10)
        show_snackbar(page, "✅ Correct! +10 XP")
        save_data()
        if boss_mode: 
            boss_hp -= 1
            show_snackbar(page, f"👹 Boss HP: {boss_hp}/3")
    else:
        show_snackbar(page, f"❌ Wrong! Correct: {q['o'][q['a']]}")
        save_data()
        if boss_mode: 
            boss_hp = 3
            show_snackbar(page, "👹 Boss HP Reset to 3!")
    
    current_quiz_index += 1
    
    if boss_mode and boss_hp <= 0:
        boss_mode = False
        bosses_defeated += 1 # <- YOU WERE MISSING THIS
        boss_reward = BOSS_REWARDS[current_lesson_index + 1]
        update_xp(boss_reward["xp"])
        show_snackbar(page, f"🎉 BOSS DEFEATED! +{boss_reward['xp']} XP")
        if current_lesson_index not in completed_lessons:
            completed_lessons.append(current_lesson_index)
        check_achievements(page, current_lesson_index + 1)
        save_progress()
        show_lessons()
        
    elif current_quiz_index >= len(lesson["quiz"]):
        if not boss_mode:
            if current_lesson_index not in completed_lessons:
                completed_lessons.append(current_lesson_index)
                update_xp(20) # completion bonus
            check_achievements(page, current_lesson_index + 1)
            show_snackbar(page, "🎉 Lesson Complete!")
            save_progress()
        show_lessons()
    else:
        show_lesson_screen()
def show_lesson_screen():
    lesson = LESSONS[current_lesson_index]
    page.clean()
    t = THEMES[current_theme]
    
    header = ft.Row([
        ft.ElevatedButton(
            content=ft.Text("← Back to Lessons", color="#000"), # FIXED
            on_click=lambda e: show_lessons(), 
            bgcolor=t["accent"]
        ),
        ft.Text(lesson["title"], size=26, weight=ft.FontWeight.BOLD, color=t["text"])
    ])

    notes_card = ft.Container(
        content=ft.Column([
            ft.Text("📝 NOTES", size=24, weight=ft.FontWeight.BOLD, color=t["accent"]),
            ft.Text(lesson["notes"], size=20, color=t["text"], weight=ft.FontWeight.W_500),
            ft.Divider(color=t["accent"]),
            ft.Text("💻 EXAMPLE:", size=22, weight=ft.FontWeight.BOLD, color=t["accent"]),
            ft.Container(
                content=ft.Text(lesson.get("example", ""), size=18, color="#00FF00", font_family="monospace", weight=ft.FontWeight.BOLD), 
                bgcolor="#000", padding=15, border_radius=10
            ),
            ft.ElevatedButton("START QUIZ →", on_click=start_quiz, bgcolor="#00FF00", color="#000", width=700, height=60) # NEW BUTTON
        ]), 
        padding=20, bgcolor=t["card"], border_radius=15, margin=15, width=800
    )

    # Only show quiz if stage is quiz
    page_content = [header, notes_card]
    
    if lesson_stage == "quiz":
        q = lesson["quiz"][current_quiz_index]
        quiz_card = ft.Container(
            content=ft.Column([
                ft.Text(f"Q {current_quiz_index + 1}/{len(lesson['quiz'])}", size=18, color=t["accent"]),
                ft.Text(q["q"], weight=ft.FontWeight.BOLD, size=20, color=t["text"]),
                *[ft.ElevatedButton(

                    content=ft.Text(opt), # FIXED
                    data=i, 
                    on_click=check_quiz_answer, 
                    width=700, 
                    height=50
                ) for i, opt in enumerate(q["o"])]
            ], spacing=15),
            padding=20, bgcolor=t["card"], border_radius=15, margin=15
        )
        if boss_mode:
            quiz_card.content.controls.insert(0, ft.Text(f"👹 BOSS HP: {boss_hp}/3", color="#FF0000", size=22, weight=ft.FontWeight.BOLD))
        page_content.append(quiz_card)

    page.add(*page_content)
    page.update()



def preview_theme(e):
    global current_theme, temp_theme
    name = e.control.data
    temp_theme = current_theme
    current_theme = name
    apply_theme()
    asyncio.create_task(revert_theme())

async def revert_theme():
    global current_theme
    await asyncio.sleep(3)
    current_theme = temp_theme
    apply_theme()

def show_shop():
    page.clean()
    t = THEMES[current_theme]
    
    boosts = [
        {"name": "2x XP Boost", "desc": "Next lesson gives 2x XP", "cost": 50, "type": "boost"},
        {"name": "Skip Question", "desc": "Skip 1 hard quiz question", "cost": 30, "type": "boost"},
    ]
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.ElevatedButton("← Back", on_click=lambda e: show_menu(), bgcolor=t["accent"], color="#000"),
                    ft.Text("SHOP", size=28, weight=ft.FontWeight.BOLD, color=t["text"]),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Text(f"Your XP: {xp}", size=20, color=t["text"]),
                ft.Divider(),
                
                ft.Text("BOOSTS", size=18, weight=ft.FontWeight.BOLD, color=t["text"]),
                ft.Column([
                    ft.Card(content=ft.ListTile(
                        title=ft.Text(b["name"], weight=ft.FontWeight.BOLD, color=t["text"]),
                        subtitle=ft.Text(b["desc"], color=t["text"]),
                        trailing=ft.ElevatedButton(
                            f"{b['cost']} XP",
                            on_click=lambda e, c=b["cost"], t=b["type"], n=b["name"]: buy_item(c, t, n),
                            disabled=xp < b["cost"]
                        ),
                    )) for b in boosts
                ]),
                
                ft.Divider(),
                
                ft.Text("THEMES", size=18, weight=ft.FontWeight.BOLD, color=t["text"]),
                ft.Column([
                    ft.Card(content=ft.ListTile(
                        title=ft.Text(tp["display"], weight=ft.FontWeight.BOLD, color=t["text"]),
                        subtitle=ft.Text("Free" if tp["cost"] == 0 else "Unlocks new colors", color=t["text"]),
                        trailing=ft.ElevatedButton(
                            "EQUIPPED" if current_theme == tp["name"] else f"{tp['cost']} XP",
                            on_click=lambda e, c=tp["cost"], tpe="theme", n=tp["name"]: buy_item(c, tpe, n),
                            disabled=xp < tp["cost"] or current_theme == tp["name"]
                        ),
                    )) for tp in THEME_PRICES
                ]),
                
            ], scroll=ft.ScrollMode.AUTO, spacing=10), padding=15, expand=True
        )
    )
    page.update()

def change_theme(theme_name):
    global current_theme
    current_theme = theme_name
    apply_theme()
    show_settings()

def show_reset_page():
    page.clean()
    t = THEMES[current_theme]

    def do_reset(e):
        global FORCE_RESET
        FORCE_RESET = True
        set_defaults()
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        show_snackbar(page, "Progress WIPED!")
        apply_theme()
        show_menu()
        FORCE_RESET = False

    page.add(
        ft.Column([
            ft.Text("🗑️ RESET PROGRESS", size=32, weight=ft.FontWeight.BOLD, color="#FF0000"),
            ft.Container(
                content=ft.Column([
                    ft.Text("⚠️ WARNING", size=24, weight=ft.FontWeight.BOLD, color="#FF0000"),
                    ft.Text("This will DELETE all 50 lessons, XP, Levels, Bosses, Achievements", size=16, color=t["text"]),
                    ft.Text("This cannot be undone!", size=16, color=t["text"]),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=20, bgcolor="#2A0000", border_radius=15, width=700
            ),
            ft.Row([
                ft.ElevatedButton("← CANCEL", on_click=lambda e: show_menu(), bgcolor=t["accent"], color="#000", width=340, height=60),
                ft.ElevatedButton("YES WIPE EVERYTHING", on_click=do_reset, bgcolor="#FF0000", color="#000", width=340, height=60),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30)
    )
    page.update()
    
    
def show_export_page():
    page.clean()
    t = THEMES[current_theme]
    
    filename = f"RPG_Progress_{current_player}_{datetime.date.today()}.txt"
    data = all_players[current_player]
    completed = data.get('completed_lessons') or []
    unlocked = data.get('unlocked_themes') or []
    achs = data.get('achievements') or []

    content = f"""🐍 RPG PYTHON LEARNER - PROGRESS REPORT
Player: {current_player}
Date: {datetime.date.today()}

Level: {data.get('level', 1)}
XP: {data.get('xp', 0)}
Lessons Completed: {len(completed)}/50
Bosses Defeated: {data.get('bosses_defeated', 0)}
Themes Unlocked: {len(unlocked)}
Achievements: {sum(1 for a in achs if a)}/{len(achievements)}

Keep Grinding!
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    page.add(
        ft.Column([
            ft.Text("📤 EXPORT COMPLETE", size=32, weight=ft.FontWeight.BOLD, color=t["accent"]),
            ft.Container(
                content=ft.Column([
                    ft.Text("Your progress has been saved!", size=18, color=t["text"]),
                    ft.Text(f"File: {filename}", size=14, color="#00FF00", weight="bold"),
                    ft.Divider(),
                    ft.Text(content, size=14, color=t["text"], font_family="monospace"),
                ], scroll=ft.ScrollMode.AUTO),
                padding=20, bgcolor=t["card"], border_radius=15, width=750, height=400
            ),
            ft.ElevatedButton("← BACK TO MENU", on_click=lambda e: show_menu(), bgcolor=t["accent"], color="#000", width=700, height=60)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )
    page.update()

def show_settings():
    page.controls.clear()
    t = THEMES[current_theme]
    
    # BUILD THEME BUTTONS
    theme_buttons = []
    for name, data in THEMES.items():
        is_owned = name in owned_themes
        is_current = name == current_theme
        
        if is_current:
            btn_text = f"✅ {name.upper()} - EQUIPPED"
            btn_color = "#00FF00"
            on_click_func = None
        elif is_owned:
            btn_text = f"✓ {name.upper()} - EQUIP"
            btn_color = data["accent"]
            on_click_func = lambda e, n=name: equip_theme(n)
        else:
            btn_text = f"🔒 {name.upper()} - {data['price']} XP"
            btn_color = "#555"
            on_click_func = lambda e, n=name: buy_theme(n)
            
        theme_buttons.append(
            ft.ElevatedButton(
                btn_text,
                on_click=on_click_func,
                bgcolor=btn_color,
                color="#000",
                width=700,
                height=60,
                disabled = is_current
            )
        )

    page.add(
        ft.Column([
            ft.Text("⚙️ THEME SHOP", size=32, weight=ft.FontWeight.BOLD, color=t["text"]),
            ft.Text(f"Your XP: {xp}", size=20, color=t["accent"]),
            ft.Divider(),
            ft.Text("Unlock new themes with XP!", color=t["text"]),
            
            ft.Column(theme_buttons, spacing=10, scroll=ft.ScrollMode.AUTO),
            
            ft.Divider(),
            ft.ElevatedButton(
                "⬅️ BACK TO MENU",
                on_click=lambda e: show_menu(),
                bgcolor=t["accent"],
                color="#000"
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    )
    page.update()

def equip_theme(name):
    global current_theme
    current_theme = name
    save_data()
    show_settings()

def buy_theme(name):
    global xp, owned_themes
    price = THEMES[name]["price"]
    if name in owned_themes:
        equip_theme(name)
    elif xp >= price:
        xp -= price
        owned_themes.append(name) # ADD THIS
        unlocked_themes.append(name) # ADD THIS TOO
        equip_theme(name)
        save_progress() # ADD THIS
    else:
        show_snackbar(page, "Not enough XP!")

def close_dlg(e=None):
    page.dialog.open = False
    page.update()

def show_achievements_ui():
    page.clean() # <- SAME AS "50 LESSONS"
    t = THEMES[current_theme]
    achievement_rows = []
    
    for ach in achievements:
        if ach["unlocked"]:
            icon_color = "#00FF00"; text_color = t["text"]; bg_color = t["card"]; status = "UNLOCKED"
        else:
            icon_color = "#555"; text_color = "#555"; bg_color = "#1A1A1A"; status = "LOCKED"

        achievement_rows.append(
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Text(ach["icon"], size=35),
                    title=ft.Text(ach["name"], weight=ft.FontWeight.BOLD, color=text_color, size=16),
                    subtitle=ft.Text(ach["desc"], color=text_color, size=13),
                    trailing=ft.Text(status, color=icon_color, weight=ft.FontWeight.BOLD, size=12),
                ),
                bgcolor=bg_color, border_radius=10, padding=5, margin=2
            )
        )

    unlocked_count = sum(1 for a in achievements if a["unlocked"])

    page.add( # <- SAME AS "50 LESSONS"
        ft.Column([
            ft.Row([
                ft.ElevatedButton("← Back to Menu", on_click=lambda e: show_menu(), bgcolor=t["accent"], color="#000"),
                ft.Text("🏆 ACHIEVEMENTS", size=28, weight=ft.FontWeight.BOLD, color=t["text"]),
                ft.Container(content=ft.Text(f"{unlocked_count}/{len(achievements)}", color="#000", weight="bold"), bgcolor=t["accent"], padding=10, border_radius=20)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Container(
                content=ft.Column(achievement_rows, scroll=ft.ScrollMode.AUTO, spacing=10),
                height=500
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    )
    page.update()



def ask_name_popup():
    tf = ft.TextField(label="Enter your name", autofocus=True)

    def create_and_start(e):
        global current_player
        name = tf.value.strip()
        if name == "":
            tf.error_text = "Enter a name"
            page.update()
            return
        if name not in all_players:
            all_players[name] = {
                "xp": 0, "level": 1, "boss_hp": 100, "bosses_defeated": 0,
                "unlocked_themes": ["light", "dark"], "current_theme": "light",
                "completed_lessons": [], "current_lesson_index": 0,
                "achievements": [False] * len(achievements), "correct_answers_count": 0,
                "daily_streak": 0, "last_daily_claim": ""
            }
        current_player = name
        save_progress()
        page.dialog.open = False
        check_daily_quest(page)
        show_menu()
        page.update()

    page.dialog = ft.AlertDialog(
        title=ft.Text("🐍 Welcome to Python RPG!"),
        content=tf,
        actions=[ft.ElevatedButton("Start", on_click=create_and_start)],
        modal=True,
        on_dismiss=lambda e: None
    )
    page.dialog.open = True
    page.update()

def show_menu():
    page.controls.clear()
    t = THEMES[current_theme]
    player_btns = [ft.ElevatedButton(name, data=name, on_click=switch_player) for name in all_players.keys()]

    xp_needed_for_next = level * 100
    xp_progress = xp / xp_needed_for_next if xp_needed_for_next > 0 else 0

    page.add(
        ft.Column([
            ft.Text("🐍 RPG Python Learner", size=32, weight=ft.FontWeight.BOLD, color=t["text"]),
            
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"👤 {current_player}", size=20, weight="bold", color=t["text"]),
                        ft.Container(content=ft.Text(f"LVL {level}", size=18, weight="bold", color="#000"), bgcolor=t["accent"], padding=10, border_radius=20)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"{xp} / {xp_needed_for_next} XP", size=14, color=t["text"]),
                    ft.ProgressBar(value=xp_progress, color=t["accent"], bgcolor="#000", height=12, border_radius=10),
                    ft.Text(f"🔥 {daily_streak} Day Streak", size=16, color="#FF8C42", weight="bold"),
                ]), 
                padding=20, bgcolor=t["card"], border_radius=15, width=750
            ),
            
            ft.Text(f"📚 Lessons: {len(completed_lessons)}/50", color=t["text"]),
            ft.Divider(),

            ft.ElevatedButton("📚 50 LESSONS", on_click=lambda e: show_lessons(), bgcolor=t["accent"], color="#000", width=700, height=60),
            ft.ElevatedButton("⚔️ PRACTICE ARENA", on_click=lambda e: show_practice_arena(), bgcolor="#FF8C42", color="#000", width=700, height=60),
            ft.ElevatedButton("🏆 LEADERBOARD", on_click=lambda e: show_leaderboard(), bgcolor=t["accent"], color="#000", width=700, height=60),
            ft.ElevatedButton("⚙️ THEME SHOP", on_click=lambda e: show_settings(), bgcolor=t["accent"], color="#000", width=700, height=60),
            
            ft.Divider(),

            # ===== NEW BUTTONS WITH CONTENT =====
            ft.Row([
                ft.ElevatedButton(
                    content=ft.Row([ft.Text("🏆"), ft.Text("ACHIEVEMENTS")], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    on_click=lambda e: show_achievements_ui(), 
                    bgcolor="#FFD700",
                    color="#000", 
                    width=340, height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25))
                ),
                ft.ElevatedButton(
                    content=ft.Row([ft.Text("📤"), ft.Text("EXPORT")], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                    on_click=lambda e: show_export_page(),  
                    bgcolor="#00F5FF",
                    color="#000", 
                    width=340, height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25))
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),

            ft.ElevatedButton(
                content=ft.Row([ft.Text("🗑️"), ft.Text("RESET PROGRESS")], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                on_click=lambda e: show_reset_page(), 
                bgcolor="#FF0000",
                color="#000", 
                width=700, height=55,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25))
            ),

            ft.Divider(),
            ft.Text("Switch Player:", color=t["text"]),
            ft.Row(player_btns, wrap=True, alignment=ft.MainAxisAlignment.CENTER),

        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
    )
    page.update()

def show_leaderboard():
    page.controls.clear()
    t = THEMES[current_theme]
    rows = []
    sorted_players = sorted(all_players.items(), key=lambda item: item[1].get('xp', 0), reverse=True)
    for i, (name, data) in enumerate(sorted_players):
        lvl = data.get('level', 1)
        xp_val = data.get('xp', 0)
        lessons = len(data.get('completed_lessons', []))
        if i == 0: color = "#FFD700"
        elif i == 1: color = "#C0C0C0"
        elif i == 2: color = "#CD7F32"
        else: color = t["accent"]
        rows.append(ft.Text(f"{i+1}. {name} - Lvl {lvl} | {xp_val} XP | {lessons} Lessons", color=color, size=16, weight=ft.FontWeight.BOLD))

    page.add(
        ft.Column([
            ft.Text("🏆 Leaderboard", size=28, weight=ft.FontWeight.BOLD, color=t["text"]),
            ft.Container(content=ft.Column(rows, spacing=10), padding=20, bgcolor=t["card"], border_radius=10, width=500),
            ft.ElevatedButton("Back", on_click=lambda e: show_menu(), bgcolor=t["accent"], color="#000")
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )
    page.update()

def switch_player(e):
    global current_player
    current_player = e.control.data
    load_progress()
    show_menu()

def apply_theme(theme_name=None): # <- add =None
    global current_theme
    if theme_name: # <- if we passed one, use it
        current_theme = theme_name
    
    t = THEMES[current_theme]
    page.theme_mode = t["mode"]
    page.bgcolor = t["bg"]
    
    save_progress()
    page.update()
def show_practice_arena():
    page.controls.clear()
    t = THEMES[current_theme]
    
    page.add(
        ft.Column([
            ft.Text("⚔️ PRACTICE ARENA", size=32, weight=ft.FontWeight.BOLD, color=t["text"]),
            ft.Text(f"Current XP: {xp} | Grind without losing progress", size=16, color=t["accent"]),
            ft.Divider(),
            
            ft.ElevatedButton(
                content=ft.Text("🎯 RANDOM QUIZ - +5 XP per correct", color="#000", weight=ft.FontWeight.BOLD),
                on_click=lambda e: start_practice_quiz(),
                bgcolor="#00F5FF",
                width=700,
                height=80
            ),
            
            ft.ElevatedButton(
                content=ft.Text("👹 BOSS RUSH - +20 XP per correct", color="#000", weight=ft.FontWeight.BOLD),
                on_click=lambda e: start_boss_rush(),
                bgcolor="#FF0000",
                width=700,
                height=80
            ),
            ft.ElevatedButton(
                content=ft.Text("💻 FREE PRACTICE - Type & Run Python", color="#000", weight=ft.FontWeight.BOLD),
                on_click=lambda e: show_free_practice(),
                bgcolor="#00FF00",
                width=700,
                height=80
            ),
            ft.ElevatedButton(
                content=ft.Text("⬅️ BACK TO MENU", color="#000"),
                on_click=lambda e: show_menu(),
                bgcolor=t["accent"]
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )
    page.update()


practice_questions = []
practice_index = 0
practice_score = 0
practice_mode = "normal" # "normal" or "boss"

def start_practice_quiz():
    global practice_questions, practice_index, practice_score, practice_mode
    practice_mode = "normal"
    practice_index = 0
    practice_score = 0
    # Grab 10 random questions from all lessons
    all_q = []
    for lesson in LESSONS:
        for q in lesson["quiz"]:
            all_q.append(q)
    random.shuffle(all_q)
    practice_questions = all_q[:10]
    show_practice_question()

def start_boss_rush():
    global practice_questions, practice_index, practice_score, practice_mode, boss_hp
    practice_mode = "boss"
    practice_index = 0
    practice_score = 0
    boss_hp = 5 # Boss has 5 HP
    all_q = []
    for lesson in LESSONS:
        for q in lesson["quiz"]:
            all_q.append(q)
    random.shuffle(all_q)
    practice_questions = all_q[:15]
    show_snackbar(page, "👹 BOSS RUSH! Get 5 right before you lose!")
    show_practice_question()

def show_practice_question():
    page.clean()
    t = THEMES[current_theme]
    q = practice_questions[practice_index]
    
    header_text = f"Question {practice_index + 1}/{len(practice_questions)}"
    if practice_mode == "boss":
        header_text = f"👹 BOSS HP: {boss_hp}/5 | Q {practice_index + 1}/{len(practice_questions)}"
    
    page.add(
        ft.Column([
            ft.Text(header_text, size=20, color=t["accent"]),
            ft.Text(q["q"], weight=ft.FontWeight.BOLD, size=22, color=t["text"]),
            *[ft.ElevatedButton(
                content=ft.Text(opt),
                data=i,
                on_click=check_practice_answer,
                width=700,
                height=60
            ) for i, opt in enumerate(q["o"])],
            ft.ElevatedButton(
                content=ft.Text("⬅️ Exit Arena", color="#000"),
                on_click=lambda e: show_practice_arena(),
                bgcolor="#555"
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    )
    page.update()

def check_practice_answer(e):
    global practice_index, practice_score, xp, boss_hp
    selected = e.control.data
    correct = practice_questions[practice_index]["a"]
    xp_gain = 20 if practice_mode == "boss" else 5
    
    if selected == correct:
        practice_score += 1
        update_xp(xp_gain)
        show_snackbar(page, f"✅ Correct! +{xp_gain} XP")
        if practice_mode == "boss":
            boss_hp -= 1
    else:
        show_snackbar(page, f"❌ Wrong! Correct: {practice_questions[practice_index]['o'][correct]}")
        if practice_mode == "boss":
            boss_hp = 5 # Reset boss
            show_snackbar(page, "👹 Boss HP Reset!")
    
    practice_index += 1
    
    # Check win/lose conditions
    if practice_mode == "boss" and boss_hp <= 0:
        show_snackbar(page, f"🎉 BOSS DEFEATED! Final Score: {practice_score}")
        update_xp(100) # Bonus
        show_practice_arena()
    elif practice_index >= len(practice_questions):
        show_snackbar(page, f"🏁 Practice Complete! Score: {practice_score}/{len(practice_questions)}")
        show_practice_arena()
    else:
        show_practice_question()

def show_free_practice():
    t = THEMES[current_theme]
    code_input = ft.TextField(
        label="Type Python Code Here",
        multiline=True,
        min_lines=8,
        max_lines=15,
        width=800,
        bgcolor="#000",
        color="#00FF00",
        text_style=ft.TextStyle(font_family="monospace", size=16)
    )
    output = ft.Text("", size=16, color="#FFFFFF", font_family="monospace")

    def run_code(e):
        # DISABLED FOR ANDROID SAFETY
        output.value = ">>> CODE EXECUTION DISABLED IN APK\n>>> Use this only on PC"
        page.update()

    page.clean()
    page.add(
        ft.Column([
            ft.Text("💻 FREE PRACTICE ARENA", size=28, weight=ft.FontWeight.BOLD, color=t["text"]),
            ft.Text("⚠️ Disabled on Mobile | +1 XP for trying", size=14, color="#FF8C42"),
            code_input,
            ft.ElevatedButton(
                content=ft.Text("▶️ RUN CODE", weight=ft.FontWeight.BOLD),
                on_click=run_code,
                bgcolor="#00FF00",
                color="#000",
                width=800,
                height=60
            ),
            ft.Container(
                content=ft.Column([output], scroll=ft.ScrollMode.AUTO),
                bgcolor="#1A1A1A",
                padding=15,
                border_radius=10,
                width=800,
                height=250
            ),
            ft.ElevatedButton(
                content=ft.Text("⬅️ Back to Arena", color="#000"),
                on_click=lambda e: show_practice_arena(),
                bgcolor=t["accent"]
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, scroll=ft.ScrollMode.AUTO)
    )
    page.update()


def buy_item(cost, item_type, item_name):
    global xp
    
    # 1. CHECK IF PLAYER HAS ENOUGH XP
    if xp < cost:
        page.snack_bar = ft.SnackBar(ft.Text(f"Not enough XP! Need {cost} XP"))
        page.snack_bar.open = True
        page.update()
        return
    
    # 2. TAKE THE XP
    xp -= cost
    
    # 3. APPLY THE ITEM EFFECT
    if item_type == "boost":
        page.snack_bar = ft.SnackBar(ft.Text(f"Bought {item_name}! -{cost} XP"))
        # TODO: add boost logic later. Ex: set a flag for 2x XP
        
    elif item_type == "theme":
        apply_theme(item_name) # this will also call save_data()
        page.snack_bar = ft.SnackBar(ft.Text(f"Theme changed to {item_name}! -{cost} XP"))
    
    # 4. SAVE AND REFRESH
    if item_type != "theme": # theme already saves inside apply_theme
        save_data()
        
    page.snack_bar.open = True
    show_shop() # refresh shop to update XP and button states


def show_stats():
    page.clean()
    page.add(
        ft.Column([
            ft.ElevatedButton("← Back", on_click=lambda e: show_menu()),
            ft.Text(f"Total XP: {xp}", size=24),
            ft.Text(f"Lessons Done: {len(completed_lessons)}/{len(LESSONS)}", size=20)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
    )
    page.update()
def main(page_param: ft.Page):
    global page, current_player, all_players, current_theme, xp, level, boss_hp, bosses_defeated, unlocked_themes, completed_lessons, current_lesson_index, correct_answers_count, daily_streak, last_daily_claim
    
    page = page_param
    page.title = "RPG Python Master - 50 Lessons"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    load_progress() # 1. LOAD FIRST
    

    page.theme = ft.Theme()
    apply_theme(current_theme) # 3. APPLY THEME AFTER PAGE EXISTS

    if not all_players:
        ask_name_popup()
        return

    if current_player not in all_players:
        current_player = list(all_players.keys())[0]
        data = all_players[current_player]
        xp = data.get("xp", 0); level = data.get("level", 1); boss_hp = data.get("boss_hp", 100)
        bosses_defeated = data.get("bosses_defeated", 0); unlocked_themes = data.get("unlocked_themes", ["light", "dark"])
        current_theme = data.get("current_theme", "light"); completed_lessons = data.get("completed_lessons", [])
        current_lesson_index = data.get("current_lesson_index", 0); correct_answers_count = data.get("correct_answers_count", 0)
        daily_streak = data.get("daily_streak", 0); last_daily_claim = data.get("last_daily_claim", "")
        apply_theme(current_theme) # re-apply after loading player

    try:
        check_daily_quest(page)
    except:
        pass

    show_menu()
    page.update()


ft.app(target=main, assets_dir="assets")
