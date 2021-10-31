import pandas as pd
import os
from nltk.tokenize import TreebankWordTokenizer, word_tokenize


dataset_path = ".."+os.sep+"data"+os.sep+"dataset"+os.sep+"dataframe.txt"
data = pd.read_csv(dataset_path, header=None, encoding='utf-8',sep="\t")
data = data.rename(columns={0: "Dialogue", 1: "Turn", 2: "User", 3: "Bot"})

# Total Turns
tot_turns = len(data)

# Total Dialogues
tot_dialogues = data.iloc[tot_turns-1,data.columns.get_loc("Dialogue")]

# Turn in each dialogue
dialogues_turns = []
temp_dt = data["Turn"].tolist()
dialogues_turns = [ prev_t for prev_t,t in zip(temp_dt[:-1],temp_dt[1:]) if prev_t>t]

# Vocabulary size
list_user = data["User"].tolist()
list_bot = data["Bot"].tolist()
list_user.extend(list_bot)
list_vocab = list_user
text_vocab = " ".join(list_vocab)
tokenized_text = TreebankWordTokenizer().tokenize(text_vocab)

vocab_dict = {} 
for word in tokenized_text: 
    if (word in vocab_dict): 
        vocab_dict[word] += 1
    else: 
        vocab_dict[word] = 1


vocab_filepath = ".."+os.sep+"data"+os.sep+"results"+os.sep+"vocab_dict.txt"
with open(vocab_filepath,"w",encoding="utf-8") as voc_writer:
    voc_writer.write(f"Treebank Word Tokenizer\n")
    voc_writer.write(f"Vocabulary size: {len(vocab_dict)}\n")
    voc_writer.write(f"\n> Dictionary:\n")
    for w in vocab_dict.keys():
        voc_writer.write(f"\n{w}: {vocab_dict[w]}")


# Results to file
stats_filepath = ".."+os.sep+"data"+os.sep+"results"+os.sep+"dataset_stats.txt"
with open(stats_filepath,"w",encoding="utf-8") as writer:
    writer.write("-> Dataset Statistics <-\n")
    writer.write(f"\n> Total turns: {tot_turns}")
    writer.write(f"\n> Vocabulary size: {len(vocab_dict)}")
    writer.write(f"\n> Total dialogues: {tot_dialogues}\n")
    writer.write(f"\n> Dialogue turns:")
    for i,d in enumerate(dialogues_turns):
        writer.write(f"\nDialogue no.{i+1}: {d}")

