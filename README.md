# RabbitCafe
Simple AI translator backend for local and cloud AI translation

## Problem of existing translation platfroms
* Portability: most of the current product could not be deployed locally
	* or they charge you a lot
* Secrecy: most translations, including the game you play, the document you read, should be kept secret.
* Blurry: the translators are not yours, thus applying lora on it is difficult

## RabbitCafe
** WARNING - lots of rabbits **
the product vision is to create, merge, and serve huge number of loras sitting on base models<br>
🐇 Serious, Percise, Happy, ??? <br>
Pick your selection and start translating <br>
Host very different fused-models and let the a filter decide who to translate what

## Current Progress
* allows using mt5-game model straight from the bin
	* the mt5-small game model is hosted at about 200mb vram, or using cpu (will add onnx support if requested)
* the translation speed is ok, current quality is poor though, nothing leaves your local network
* currently loras are not implemented, will be released soon

## Install

Linux install after cloneing
``` bash
python3 -m venv venv
source venv/bin/activate
pip install -f requirements.txt
```
Linux run
``` bash
python app.py
```