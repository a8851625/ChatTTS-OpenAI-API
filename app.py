import torch
import ChatTTS
from fastapi.responses import StreamingResponse, Response
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import hashlib
# 加载声学统计数据
import datetime
import uvicorn
import re
import argparse
from loguru import logger
import soundfile as sf

# 初始化Flask应用
app = FastAPI()
chat = ChatTTS.Chat() 
p = '/app/ChatTTS/assest/spk_stat.pt'
std, mean = torch.load(p).chunk(2)

# 推理参数
rand_spk = torch.randn(768) * std + mean

def generate_speech(input_text, voice, speed=1.0,prompt='', temperature=0.3, top_p=0.8, top_k=20):
    # 生成随机说话者嵌入
    
    params_infer_code = {
        'spk_emb': rand_spk,
        'temperature': temperature,
        'top_P': top_p,
        'top_K': top_k,
    }
    
    # 文本生成细化参数
    params_refine_text = {
        #'prompt': '[oral_2][laugh_0][break_6]'
        'prompt': prompt
    }
    torch.manual_seed(voice)
    # 生成语音
    wavs = chat.infer([input_text], use_decoder=True,params_infer_code=params_infer_code ,params_refine_text= params_refine_text)

    return wavs

voice_mapping = {
    "alloy": "4099",
    "echo": "2222",
    "fable": "6653",
    "onyx": "7869",
    "nova": "5099",
    "shimmer": "4099"
}

def replace_non_alphanumeric(text):
    return re.sub(r'[^\w\s]', ' ', text)

class SpeechRequest(BaseModel):
    model: str
    input: str
    voice: str = 'alloy'
    response_format: str = 'wav'
    speed: float = 1.0
    temperature: float = 0.3
    prompt: str = '[oral_2][laugh_0][break_6]'

@app.post("/v1/audio/speech")
async def create_speech(request: SpeechRequest):
    if not request.model or not request.input or not request.voice:
        raise HTTPException(status_code=400, detail="Missing required parameters")
    
    try:
        # 生成语音
        input_text = replace_non_alphanumeric(request.input)
        speed = float(request.speed)
        temperature = request.temperature
        voice = request.voice # man 7869 2222 6653 women 4099 5099
        voice = voice_mapping.get(voice, '4099')
        prompt = request.prompt
        logger.info(f"[tts]{input_text=}\n{voice=},{speed=}\n")
        wavs = generate_speech(input_text, voice, temperature=temperature,prompt=prompt)
        # 将音频保存到内存中的文件
        
        md5_hash = hashlib.md5()
        md5_hash.update(f"{input_text}-{voice}-{speed}".encode('utf-8'))
        datename=datetime.datetime.now().strftime('%Y%m%d-%H_%M_%S')
        filename = datename+'-'+md5_hash.hexdigest() + f".{request.response_format}"

        wav_file_path=f'/tmp/{filename}'
        sf.write(wav_file_path, wavs[0][0], samplerate=22000)
        return FileResponse(wav_file_path, media_type=f'audio/{request.response_format}')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5001)
    args = parser.parse_args()

    chat.load_models()
    generate_speech("hi!","2222")
    uvicorn.run(app, host=args.host, port=args.port)
