import matplotlib.pyplot as plt
import pandas as pd
import os
from nltk.tokenize import TreebankWordTokenizer, word_tokenize
import statistics
import numpy as np


def print_results(stats_filepath,tot_turns,tokenized_text,tot_dialogues,vocab_dict,dialogues_turns,temp_tw,temp_dw):
    # stats_filepath = ".."+os.sep+"data"+os.sep+"results"+os.sep+"dataset_stats.txt"
    with open(stats_filepath,"w",encoding="utf-8") as writer:
        writer.write("-> Dataset Statistics <-\n")
        writer.write(f"\n> Total Turns: {tot_turns}")
        writer.write(f"\n> Total Words: {len(tokenized_text)}")
        writer.write(f"\n> Total Dialogues: {tot_dialogues}")
        writer.write(f"\n> Vocabulary Size: {len(vocab_dict)}")
        writer.write(f"\n\n> Turns per Dialogue [{min(dialogues_turns)}, {max(dialogues_turns)}] \nStandard Deviation: {statistics.stdev(dialogues_turns):0.1f}\nMean: {np.mean(dialogues_turns):0.1f}\nMedian: {int(np.median(dialogues_turns))}")
        writer.write(f"\n\n> Words per Turn [{min(temp_tw)}, {max(temp_tw)}] \nStandard Deviation: {statistics.stdev(temp_tw):0.1f}\nMean: {np.mean(temp_tw):0.1f}\nMedian: {int(np.median(temp_tw))}")
        writer.write(f"\n\n> Words per Dialogue [{min(temp_dw)}, {max(temp_dw)}] \nStandard Deviation: {statistics.stdev(temp_dw):0.1f}\nMean: {np.mean(temp_dw):0.1f}\nMedian: {int(np.median(temp_dw))}")

        writer.write(f"\n\n> Dialogue Turns:")
        for i,d in enumerate(dialogues_turns):
            writer.write(f"\nDialogue no.{i+1}: {d}")

def print_vocab(vocab_filepath,vocab_dict):
    with open(vocab_filepath,"w",encoding="utf-8") as voc_writer:
        voc_writer.write(f"Treebank Word Tokenizer\n")
        voc_writer.write(f"Vocabulary size: {len(vocab_dict)}\n")
        voc_writer.write(f"\n> Dictionary:\n")
        for w in vocab_dict.keys():
            voc_writer.write(f"\n{w}: {vocab_dict[w]}")

def words_per_dialogue(dialogues_turns,lines):
    temp_dw = []
    start = 0
    for turns in dialogues_turns:
        end = start+turns
        dialogues_turns = " ".join(lines[start:end])
        words_in_dialogue = len(TreebankWordTokenizer().tokenize(dialogues_turns))
        temp_dw.append(words_in_dialogue)
        start = end

    return temp_dw

def tok_n_vocab(data):
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

    return tokenized_text, vocab_dict

def plotting(dialogues_turns,temp_tw,temp_dw):

    x = [i for i in range(len(dialogues_turns))]
    data_lists = [ dialogues_turns, temp_tw, temp_dw]

    # plt.boxplot(data_lists)
    fig,ax = plt.subplots(figsize=(12,26))
    bp1 = ax.boxplot(dialogues_turns, positions=[1], patch_artist=True, boxprops=dict(facecolor="C0"))
    bp2 = ax.boxplot(temp_tw, positions=[2], patch_artist=True, boxprops=dict(facecolor="C2"))
    bp3 = ax.boxplot(temp_dw, positions=[3], patch_artist=True, boxprops=dict(facecolor="C4"))

    y_ticks = [min(dialogues_turns),min(temp_tw), min(temp_dw), max(dialogues_turns),max(temp_tw), max(temp_dw), np.median(dialogues_turns), np.median(temp_tw), np.median(temp_dw)]
    y_ticks.sort()

    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['Turns per Dialogue', 'Words per Turn', 'Words per Dialogue'])
    ax.set_yticks(y_ticks)

    ax.set_ylim([min(min(dialogues_turns),min(temp_tw)-10, min(temp_dw)), max(max(dialogues_turns),max(temp_tw), max(temp_dw))+10])

    # Annotate mean values
    ax.annotate(f"Mean: {np.mean(dialogues_turns):0.1f}", xy=(1, np.mean(dialogues_turns)), xytext=(1.2, np.mean(dialogues_turns)+2), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='red') )
    ax.annotate(f"Mean: {np.mean(temp_tw):0.1f}", xy=(2, np.mean(temp_tw)), xytext=(2.2, np.mean(temp_tw)+2), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='red') )
    ax.annotate(f"Mean: {np.mean(temp_dw):0.1f}", xy=(3, np.mean(temp_dw)), xytext=(3-0.5, np.mean(temp_dw)+2), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='red') )

    # Annotate median values
    ax.annotate(f"Median: {int(np.median(dialogues_turns))}", xy=(1, np.median(dialogues_turns)), xytext=(1.2, np.median(dialogues_turns)-2), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='blue') )
    ax.annotate(f"Median: {int(np.median(temp_tw))}", xy=(2, np.median(temp_tw)), xytext=(2.2, np.median(temp_tw)-2), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='blue') )
    ax.annotate(f"Median: {int(np.median(temp_dw))}", xy=(3, np.median(temp_dw)), xytext=(3-0.5, np.median(temp_dw)-2), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='blue') )

    # Annotate max values
    ax.annotate(f"Max: {int(max(dialogues_turns))}", xy=(1, max(dialogues_turns)), xytext=(1.2, max(dialogues_turns)+2), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='green') )
    ax.annotate(f"Max: {int(max(temp_tw))}", xy=(2, max(temp_tw)), xytext=(2.2, max(temp_tw)), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='green') )
    ax.annotate(f"Max: {int(max(temp_dw))}", xy=(3, max(temp_dw)), xytext=(3-0.5, max(temp_dw)), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='green') )

    # Annotate min values
    ax.annotate(f"Min: {int(min(dialogues_turns))}", xy=(1, min(dialogues_turns)), xytext=(1.2, min(dialogues_turns)-2), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='purple') )
    ax.annotate(f"Min: {int(min(temp_tw))}", xy=(2, min(temp_tw)), xytext=(2.2, min(temp_tw)), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='purple') )
    ax.annotate(f"Min: {int(min(temp_dw))}", xy=(3, min(temp_dw)), xytext=(3-0.5, min(temp_dw)), ha='left', va='bottom', arrowprops=dict(arrowstyle="->", connectionstyle="arc3, rad=0.1", color='purple') )

    # Save figure
    plot_filepath = ".."+os.sep+"data"+os.sep+"results"+os.sep+"boxplots_dt_tw_dw.png"
    plt.savefig(plot_filepath,dpi=300)

    plot_filepath = ".."+os.sep+"data"+os.sep+"results"+os.sep+"boxplots_dt_tw_dw__small.png"
    plt.savefig(plot_filepath,dpi=100)