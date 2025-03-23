import random

def generate_random_suffix():
   words = [
      "crab", "tiger", "wolf", "eagle", "koala", "otter", "lynx", "gecko",
      "puma", "panda", "raven", "shark", "zebra", "hawk", "bat", "snail",
      "elephant", "leopard", "deer", "sparrow", "lion", "fox", "rabbit", "whale",
      "giraffe", "peacock", "coyote", "kangaroo", "platypus", "otter", "beetle",
      "mongoose", "falcon", "seagull", "crow", "owl", "bison", "panther", "goose",
      "caterpillar", "jackal", "walrus", "komodo", "toucan", "hippopotamus", "penguin",
      "skunk", "gorilla", "starling", "dolphin", "bat", "parrot", "quail", "dingo",
      "kitty", "slug", "tardigrade", "baboon", "badger", "camel", "dragonfly",
      "eel", "gazelle", "gnat", "heron", "hornet", "hyena", "ibex", "jaguar", "jellyfish",
      "lark", "lemur", "lobster", "locust", "louse", "manatee", "mammoth", "mink",
      "mosquito", "narwhal", "octopus", "oyster", "partridge", "pelican", "porcupine",
      "raccoon", "ram", "salamander", "sardine", "sloth", "spider", "boa", "squid"
   ]
   return f"{random.choice(words)}-{random.randint(100, 999)}"