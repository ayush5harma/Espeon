LOOK_R = '( )'
LOOK_L = '( )'
LOOK_R_HAPPY = '( )'
LOOK_L_HAPPY = '()'
SLEEP = '()'
AWAKE = '()'
BORED = '()'
INTENSE = '()'  #when eating handshake
COOL = '(⌐■_■)'
HAPPY = '(•‿‿•)'
EXCITED = '(ᵔ◡◡ᵔ)'
MOTIVATED = '(☼‿‿☼)'
DEMOTIVATED = '()'
SMART = '()'
LONELY = '(ಠ_ಠ)'
SAD = '((ಥ﹏ಥ))'
ANGRY = "()"


def load_from_config(config):
    for face_name, face_value in config.items():
        globals()[face_name.upper()] = face_value
