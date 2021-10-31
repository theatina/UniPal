import matplotlib.pyplot as plt
import pandas as pd
import os
from nltk.tokenize import TreebankWordTokenizer, word_tokenize
import statistics
import numpy as np
import my_funlib

dataset_path = ".."+os.sep+"data"+os.sep+"dataset"+os.sep+"dataframe.txt"
data = pd.read_csv(dataset_path, header=None, encoding='utf-8',sep="\t")
data = data.rename(columns={0: "Dialogue", 1: "Turn", 2: "User", 3: "Bot"})

# Total Turns
tot_turns = len(data)

# Total Dialogues
tot_dialogues = data.iloc[tot_turns-1,data.columns.get_loc("Dialogue")]

# Turns per dialogue
dialogues_turns = []
temp_dt = data["Turn"].tolist()
dialogues_turns = [ prev_t for prev_t,t in zip(temp_dt[:-1],temp_dt[1:]) if prev_t>t]

# Words per turn
with open(dataset_path,"r",encoding="utf-8") as r:
    lines = r.read().split("\n")

lines = [" ".join(l.split("\t")[2:]) for l in lines if l!=""]
temp_tw = [len(TreebankWordTokenizer().tokenize(l)) for l in lines]

# Words per dialogue
temp_dw = my_funlib.words_per_dialogue(dialogues_turns,lines)

# Vocabulary
tokenized_text,vocab_dict = my_funlib.tok_n_vocab(data)

# Vocabulary dictionary to file
vocab_filepath = ".."+os.sep+"data"+os.sep+"results"+os.sep+"vocab_dict.txt"
my_funlib.print_vocab(vocab_filepath,vocab_dict)

# Results to file
stats_filepath = ".."+os.sep+"data"+os.sep+"results"+os.sep+"dataset_stats.txt"
my_funlib.print_results(stats_filepath,tot_turns,tokenized_text,tot_dialogues,vocab_dict,temp_dt,temp_tw,temp_dw,dialogues_turns)

# Plot results
my_funlib.plotting(temp_dt,temp_tw,temp_dw)