from transformers import pipeline
from transformers.pipelines.pt_utils import KeyDataset
import re
import copy
from datetime import datetime
from tqdm.auto import tqdm
from datasets import Dataset

#model_path="iryneko571/mt5-translation-ja_zh-game-small"
'''
setup pipeline for translation
'''
pipe=None
def pipeinit(config):
    global pipe
    then = datetime.now()
    print(then,"initiate model")
    pipe = pipeline("translation",
                    model=config["model_path"],
                    tokenizer=config["model_path"],
                    repetition_penalty=config["repetition_penalty"], # just avoid repeating in a cheap way
                    batch_size=config["batch_size"], # just a reference don't set it too high
                    max_length=config["max_length"])
    now = datetime.now()
    print(now,"init time",now-then)

'''
text preprocess and post process
switch between different types of breaks
will add different stuff such as \t later
'''
# preprocess translatables
def preprocess(batch):
    samples=[None] * len(batch)
    for i in range(len(batch)):
        if "\r\n" in batch[i]:
            samples[i]=(batch[i].replace("\r\n","\\n"),"rn") # rn for old type
            continue
        if "\\n" in batch[i]:
            samples[i]=(batch[i],"nn") # nn for two slash
            continue
        if "\n" in batch[i]:
            samples[i]=(batch[i].replace("\n","\\n"),"n") # n for one slash
            continue
        else:
            samples[i]=(batch[i],"s") # s for safe
    return samples
    
# process translated back to original format
def postprocess(samples):
    batch=[None] * len(samples)
    for i in range(len(samples)):
        t, a = samples[i]
        if a=="rn":
            batch[i]=t.replace("\\n","\r\n")
            continue
        if a=="nn":
            batch[i]=t
            continue
        if a=="n":
            batch[i]=t.replace("\\n","\n")
            continue
        if a=="s":
            batch[i]=t
            continue
        else:
            print(f"error determine the type of {t}")
    return batch

'''
initial batch translation
will combine the batch and do the translation
'''
def liststream(list):
    for i in range(len(list)):
        yield i
def translate_batch(batch,lang='<-ja2zh->'): # batch is an array of string
    # preprocess
    samples=preprocess(batch)
    # format translist
    trans_list=[None] * len(batch)
    for i in range(len(batch)):
        t,a = samples[i]
        trans_list[i]=f'{lang} {batch[i]}'
    # now translate
    global pipe
    transdict={
        "text":trans_list
    }
    datalist=Dataset.from_dict(transdict)
    translated=[]
    for out in tqdm(pipe(KeyDataset(datalist, "text")),total=len(datalist)):
        #print(out)
        for o in out:
            translated.append(o)
    #translated={"test":"test"}
    #pipe(dataset, batch_size=batch_size), )
    # format result
    resultlist=[None] * len(translated)
    for i in range(len(translated)):
        resultlist[i]=(translated[i]['translation_text'],samples[i][1])
    # postprocess
    result=postprocess(resultlist)
    # return results
    return result

