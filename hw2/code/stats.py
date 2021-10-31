import matplotlib.pyplot as plt
import pandas as pd
import os
from nltk.tokenize import TreebankWordTokenizer, word_tokenize
import statistics
import numpy as np

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
temp_dw = []
start = 0
for turns in dialogues_turns:
    end = start+turns
    dialogue_turns = " ".join(lines[start:end])
    words_in_dialogue = len(TreebankWordTokenizer().tokenize(dialogue_turns))
    temp_dw.append(words_in_dialogue)
    start = end

# Vocabulary
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

# Vocabulary dictionary to file
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
    writer.write(f"\n> Total Turns: {tot_turns}")
    writer.write(f"\n> Total Words: {len(tokenized_text)}")
    writer.write(f"\n> Total Dialogues: {tot_dialogues}")
    writer.write(f"\n> Vocabulary Size: {len(vocab_dict)}")
    writer.write(f"\n\n> Turns per Dialogue \nStandard Deviation: {statistics.stdev(temp_dt):0.1f}\nMean: {np.mean(temp_dt):0.1f}")
    writer.write(f"\n\n> Words per Turn \nStandard Deviation: {statistics.stdev(temp_tw):0.1f}\nMean: {np.mean(temp_tw):0.1f}")
    writer.write(f"\n\n> Words per Dialogue \nStandard Deviation: {statistics.stdev(temp_dw):0.1f}\nMean: {np.mean(temp_dw):0.1f}")

    writer.write(f"\n\n> Dialogue Turns:")
    for i,d in enumerate(dialogues_turns):
        writer.write(f"\nDialogue no.{i+1}: {d}")

# Plotting
x = [i for i in range(len(temp_dt))]
data_lists = [ temp_dt, temp_tw, temp_dw]

# plt.boxplot(data_lists)
fig,ax = plt.subplots(figsize=(12,50))
bp1 = ax.boxplot(temp_dt, positions=[1], patch_artist=True, boxprops=dict(facecolor="C0"))
bp2 = ax.boxplot(temp_tw, positions=[2], patch_artist=True, boxprops=dict(facecolor="C2"))
bp3 = ax.boxplot(temp_dw, positions=[3], patch_artist=True, boxprops=dict(facecolor="C4"))

y_ticks = [min(min(temp_dt),min(temp_tw), min(temp_dw)), max(max(temp_dt),max(temp_tw), max(temp_dw)), statistics.stdev(temp_dt), np.mean(temp_dt), statistics.stdev(temp_tw), np.mean(temp_tw), statistics.stdev(temp_dw), np.mean(temp_dw)]
y_ticks.sort()
print(y_ticks)
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(['Turns per Dialogue', 'Words per Turn', 'Words per Dialogue'])
ax.set_yticks(y_ticks)

ax.set_ylim([min(min(temp_dt),min(temp_tw)-10, min(temp_dw)), max(max(temp_dt),max(temp_tw), max(temp_dw))+10])
# p1_mean = ax.text(1, np.mean(temp_dt), str(np.mean(temp_dt)) )
ax.annotate("", xy=(1, np.mean(temp_dt)), arrowprops=dict(arrowstyle="->") )
# plt.legend([bp1["boxes"][0], bp2["boxes"][0], bp3["boxes"][0]], ['Turns per Dialogue', 'Words per Turn', 'Words per Dialogue'], loc='upper right')

plot_filepath = ".."+os.sep+"data"+os.sep+"results"+os.sep+"boxplots_dt_tw_dw.png"
plt.savefig(plot_filepath,dpi=300)