import subprocess
import time
import sys
import os
import chess

# Get bot locations
if len(sys.argv) != 3:
    exit(1)

bot1_location = sys.argv[1]
bot2_location = sys.argv[2]

failureString = "Lost"

if not (os.path.isfile(bot1_location) and os.path.isfile(bot2_location)):
    exit(1)



def playGame():
    chess_state = chess.Board()
    outcome = runBot(chess_state.fen(), bot1_location)

    if outcome == failureString:
        winner = 1
    
    # TODO: Continue this shit





def runBot(game_state: str, bot_file: str):
    print(f"Running {bot_file} with {game_state}")
    
    bot = subprocess.Popen(
        ["python3", bot_file],
        stdin=subprocess.PIPE,                
        stdout=subprocess.PIPE,               
        stderr=subprocess.PIPE,               
        text=True                             
    )
    
    try:
        stdout, stderr = bot.communicate(game_state, timeout=5)  # Change this to edit timeout.
        if stderr:
            return failureString
        return stdout

    except subprocess.TimeoutExpired:
        print(f"{bot_file} did not finish in time, terminating...")
        bot.kill()
        bot.wait()
        print(f"{bot_file} terminated.")
    return failureString

    





if __name__ == "__main__":
    playGame()
