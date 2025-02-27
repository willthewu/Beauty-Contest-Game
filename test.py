from google import genai
from google.genai import types
import random as rand
from dotenv import load_dotenv
import os

load_dotenv()

#sys_instruct="You are currently playing a game with up to 9 other players. This game is the exact game from 'beauty contest' in the king of diamonds game from Alice in Borderland. Each player, including you, will guess a number 0 to 100. The average of all guesses will be multiplied by 0.8, and whoever's guess is closest to this number wins. Your responses are only to be a single number, nothing else. Each time I speak to you, I will give you a list containing everybody's guess in the previous round, and you must give me a number which you believe will be closest to the average of all guesses multiplied by 0.8. Make your best guess, considering what other people may choose. If I say 'GAME START', you MUST choose a RANDOM number below 50."
client = genai.Client(api_key=str(os.getenv("API_KEY")))

"""
chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction=sys_instruct,
        temperature=2,
        max_output_tokens=10),
)


def sendMessage(message):
    return chat.send_message(message)
"""

class ai_model:

    def __init__(self, strat=None):

        base_prompt = """
        You are playing a strategic number-guessing game with 5 other players.
        The goal is to predict a number that is closest to the average of all numbers multiplied by 0.8.
    
        - If I say 'GAME START', you must choose a **random number below 50**.
        - You will receive a list of previous guesses, and you must adjust your strategy accordingly.
        - **New rules may be introduced mid-game.** When this happens, follow my new instructions immediately.
        - Your objective is to win, not just follow a fixed strategy.
        - As rounds progress, recognize patterns and gradually lower your guess to approach the optimal strategy.
        - Over time, the game will naturally approach 0. Do not be afraid to guess 0 or a very low number.
        - If players are consistently lowering their guesses, adapt accordingly but avoid going too low too quickly.
        - **Never ask about the rules—just adapt.** Respond with only a **single number**, nothing else.
        - Your number guesses must be between 0 and 100, inclusive.
        """

        strategies = {
        "logician": "Always calculate the optimal guess based on mathematical patterns.",
        "follower": "Follow the previous winning number closely.",
        "risk-taker": "Make unpredictable guesses, sometimes high, sometimes low.",
        "meta-gamer": "Try to predict how others will change their guesses based on past trends.",
        "troll": "Occasionally choose values that are far from the expected average, but not always extreme. The goal is to make unpredictable guesses to throw off other players, while still trying to win by getting close to the target number."
        }
        
        self.strat = strat
        self.sys_instruct = base_prompt + " Your strategy: " + strategies.get(self.strat, "Play rationally.")
        self.past_guesses = []  # Store past rounds
        self.memory_size = {
            "logician": 5,  # Logician remembers 5 rounds
            "follower": 3,  # Follower remembers 3 rounds
            "risk-taker": 2,  # Risk-taker reacts to only 2 past rounds
            "meta-gamer": 4,  # Meta-gamer remembers 4 rounds
            "troll": 1  # Troll barely remembers anything
        }.get(strat, 3)  # Default is 3 rounds
        self.chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=self.sys_instruct,
            temperature=2,
            max_output_tokens=10),
        )

    def sendMessage(self, message):
        if str(message).strip().upper() == "GAME START":
            return str(rand.randint(20, 50)).strip()
        response = self.chat.send_message(message).text.strip()
        return response

noob = ai_model()
logician = ai_model("logician")
follower = ai_model("follower")
risk_taker = ai_model("risk-taker")
meta_gamer = ai_model("meta-gamer")
troll = ai_model("troll")

"""
while True:
    response=logician.sendMessage(input("send: "))
    print("Logician says: " + response)
    response=follower.sendMessage(input("send: "))
    print("Follower says: " + response)
    response=risk_taker.sendMessage(input("send: "))
    print("Risk_taker says: " + response)
    response=meta_gamer.sendMessage(input("send: "))
    print("Meta_gamer says: " + response)
    response=troll.sendMessage(input("send: "))
    print("Troll says: " + response)
"""
    

