from flask import Flask, request, send_file
import main
from datetime import datetime
import json
import redis

app=Flask(__name__)
'''
configueration phase
'''
# load config
configfile=None
with open("config.json","r") as f:
    configfile=json.loads(f.read())
# model pipeline config
main.pipeinit(configfile["Model"])
# redis config
redis_enabled=False
r=None
cache_prefix=None
try:
    r=redis.Redis(host=configfile["Redis"]["address"], 
                  port=configfile["Redis"]["port"], 
                  password=configfile["Redis"]["password"], 
                  decode_responses=True
                 )
    cache_prefix=configfile["Redis"]["prefix"]
    r.set('foo', 'bar')
    r.get('foo')
    type(r.get('ne'))
    print("redis initiated")
except:
    print("redis not connected")
# application port config
port="9900"
if configfile["Application"]["port"] !="":
    port=configfile["Application"]["port"]
# application from and to are not applicable here

# basic Translation
def translate_one(data):
    result=main.translate_batch([data])[0]
        #print(result)
    return result
'''
controllers
'''
# this works for the xunity autotranslator, the normal bunch
@app.route("/translate",methods=["GET"])
def auto_translate():
    data=request.args.get('text')
    print(data)
    # Check Redis config
    if redis_enabled==True:
        rd=r.get(cache_prefix+data)
        if rd!=None:
            print("cache hit",data,"=>",rd)
            return rd
        else:
            print("cache miss")
            time=datetime.now()
            result=translate_one(data)
            print("time:",datetime.now()-time)
            if r.set(cache_prefix+data,result):
                print("cache in",data,"=>",result)
            return result
    else:
        time=datetime.now()
        result=translate_one(data)
        print("time:",datetime.now()-time)
        print(result)
        return result
# this opens the upload interface
@app.route("/translate/upload",methods=["GET"])
def show_upload():
    with open("interface.html","r") as f:
        return f.read()
# this translates json
# this is not async should be a problem, but capacity wise i don't have enough machines
@app.route("/translate/json",methods=["POST"])
def json_translate():
    result={}
    k=list(request.json.keys())
    r=main.translate_batch(k)
    for i in range(len(k)):
        result[k[i]]=r[i]
    filename=datetime.now().strftime("%y%m%d%H%M%S")
    with open(f"tmp/{filename}.json","w") as f:
        json.dump(result,f,indent=2,ensure_ascii=False)
    return send_file(f"tmp/{filename}.json")
'''
start up application
'''
if __name__=='__main__':
    app.run(host="0.0.0.0", port=port)