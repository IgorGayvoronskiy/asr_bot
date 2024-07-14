import librosa
import torch
import time
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


def setup_model():
    # device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id_s = "Maks545curve/whisper-small-ru2-pl-a"
    model_s = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id_s, torch_dtype=torch.float32, low_cpu_mem_usage=True, use_safetensors=True, attn_implementation="sdpa"
    )
    # model_s.to(device)
    processor_s = AutoProcessor.from_pretrained(model_id_s)

    model_id_q = "openai/whisper-large-v3"
    model_q = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id_q, torch_dtype=torch.float32, low_cpu_mem_usage=True, use_safetensors=True, attn_implementation="sdpa"
    )
    # model_q.to(device)
    processor_q = AutoProcessor.from_pretrained(model_id_q)

    pipe_s = pipeline(
        "automatic-speech-recognition",
        model=model_s,
        tokenizer=processor_s.tokenizer,
        feature_extractor=processor_s.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        generate_kwargs={'language': 'russian', 'task': 'transcribe'},
        torch_dtype=torch.float32,
        # device=device
    )

    pipe_q = pipeline(
        "automatic-speech-recognition",
        model=model_q,
        tokenizer=processor_q.tokenizer,
        feature_extractor=processor_q.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        generate_kwargs={'language': 'russian', 'task': 'transcribe'},
        torch_dtype=torch.float32,
        # device=device
    )
    return pipe_s, pipe_q


def transcribe_audio(audio_file, pipe):
    audio_file, sr = librosa.load(audio_file)
    if sr != 16000:
        audio_file = librosa.resample(audio_file, orig_sr=sr, target_sr=16000)
    start_time = time.time()
    response = pipe(audio_file)
    generation_time = time.time() - start_time
    print(f"Текст: {response['text']}, Время работы: {generation_time}")
    return response["text"]
