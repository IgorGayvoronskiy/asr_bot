import librosa
import torch
import time
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


def setup_model():
    model_id = "KnIgor/whisper-small-ru"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch.float32, low_cpu_mem_usage=True, use_safetensors=True, attn_implementation="sdpa"
    )
    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        generate_kwargs={'language': 'russian', 'task': 'transcribe'},
        torch_dtype=torch.float32,
    )
    return pipe


def transcribe_audio(audio_file, pipe):
    audio_file, sr = librosa.load(audio_file)
    if sr != 16000:
        audio_file = librosa.resample(audio_file, orig_sr=sr, target_sr=16000)
    start_time = time.time()
    response = pipe(audio_file)
    generation_time = time.time() - start_time
    print(f"Текст: {response['text']}, Время работы: {generation_time}")
    return response["text"]
