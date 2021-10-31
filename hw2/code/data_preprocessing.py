import os
import pandas as pd


dataset_path = ".."+os.sep+"data"+os.sep+"dataset"+os.sep+"dialog-babi-task5-full-dialogs-trn.txt"
with open(dataset_path,"r",encoding="utf-8") as reader:
    data_lines = [ l.strip() for l in reader if l.strip() != "" and "\t" in l]

line_num = len(data_lines)-1
for l in data_lines[::-1]:
    if "<SILENCE>" in l:
        if "\n1 <SILENCE>" in l or line_num==0:
            data_lines.pop(line_num)
        else:
            bot = l.split("\t",maxsplit=1)[-1]
            data_lines[line_num-1] = data_lines[line_num-1]+ " " + bot
            data_lines.pop(line_num)
    line_num-=1

out_lines = ".."+os.sep+"data"+os.sep+"dataset"+os.sep+"clean_dtset.txt"
with open(out_lines,"w",encoding="utf-8") as test_writer:
    for l in data_lines:
        test_writer.write(l+"\n")
        

# DataFrames for results
init_dataset_path = ".."+os.sep+"data"+os.sep+"dataset"+os.sep+"clean_dtset.txt"
data = pd.read_csv(init_dataset_path, header=None, encoding='utf-8',sep="\t")
data = data.rename(columns={0: "User", 1: "Bot"})
data[["Turn","User"]] = data["User"].str.split(' ', n=1, expand=True)

# Dataset Exploration
data["Dialogue"] = 0
dialogue_num = 1
dialogue_col = [1]
prev_turn = 0
turn_counter = 1
turn_col = [1]
for line_num,turn_num in enumerate(data["Turn"][1:]):
    turn_num=int(turn_num)
    if turn_num < prev_turn:
        dialogue_num+=1
        turn_counter = 1
    else:
        turn_counter+=1

    prev_turn = turn_num
    dialogue_col.append(dialogue_num)
    turn_col.append(turn_counter)
    
# Rearrange columns
data["Dialogue"] = dialogue_col
data["Turn"] = turn_col
data = data[["Dialogue","Turn","User","Bot"]]

# print dataframe 

out = ".."+os.sep+"data"+os.sep+"dataset"+os.sep+"dataframe.txt"
data.to_csv(out,header=False,index=False, sep="\t")

out_vis = ".."+os.sep+"data"+os.sep+"dataset"+os.sep+"dataframe_visualization.txt"
data.to_csv(out_vis,header=True,index=False, sep="\t")
