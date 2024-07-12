import librosa
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


def setup_model():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = "openai/whisper-small"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True, attn_implementation="sdpa"
    )
    model.to(device)
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
        torch_dtype=torch_dtype,
        device=device
    )
    return pipe


def transcribe_audio(audio_file, pipe):
    audio_file, sr = librosa.load(audio_file)
    if sr != 16000:
        audio_file = librosa.resample(audio_file, orig_sr=sr, target_sr=16000)
    temp_file = "temp_audio.mp3"
    response = pipe(audio_file)
    print(response)
    return response['text']

