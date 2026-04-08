import os

os.environ["COQUI_TOS_AGREED"] = "1"

import io
import numpy as np
import scipy.io.wavfile as wav
import torch
import streamlit as st
from TTS.api import TTS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOICE_PROFILE_DIR = os.path.join(BASE_DIR, "voice_profile")


@st.cache_resource
def load_model():
    """XTTS v2 モデルと事前抽出済み話者特徴量をロード"""
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    model = tts.synthesizer.tts_model

    gpt_cond_latent = torch.load(
        os.path.join(VOICE_PROFILE_DIR, "gpt_cond_latent.pt"),
        map_location="cpu",
    )
    speaker_embedding = torch.load(
        os.path.join(VOICE_PROFILE_DIR, "speaker_embedding.pt"),
        map_location="cpu",
    )

    return model, gpt_cond_latent, speaker_embedding


def split_text(text, max_chars=250):
    """テキストを文単位で分割し、各チャンクが max_chars 以下になるようにする"""
    import re
    sentences = re.split(r'(?<=[.!?。！？])\s*', text)
    chunks = []
    current = ""
    for s in sentences:
        if not s.strip():
            continue
        if current and len(current) + len(s) + 1 > max_chars:
            chunks.append(current.strip())
            current = s
        else:
            current = current + " " + s if current else s
    if current.strip():
        chunks.append(current.strip())
    return chunks if chunks else [text]


def synthesize_speech(text, lang_code, model, gpt_cond_latent, speaker_embedding, speed=1.1):
    """テキストから音声を合成し、WAVバイトを返す。長文は自動分割する。"""
    chunks = split_text(text)
    all_audio = []

    for chunk in chunks:
        out = model.inference(
            text=chunk,
            language=lang_code,
            gpt_cond_latent=gpt_cond_latent,
            speaker_embedding=speaker_embedding,
            speed=speed,
        )
        all_audio.append(np.array(out["wav"]))

    audio_np = np.concatenate(all_audio)
    buf = io.BytesIO()
    wav.write(buf, 24000, (audio_np * 32767).astype(np.int16))
    buf.seek(0)
    return buf.getvalue()


# --- UI ---
st.title("Jason Statham 風 音声合成アプリ")

if not os.path.isdir(VOICE_PROFILE_DIR) or not os.listdir(VOICE_PROFILE_DIR):
    st.error(
        "話者特徴量が見つかりません。先に `uv run python prepare_voice.py` を実行してください。"
    )
    st.stop()

model, gpt_cond_latent, speaker_embedding = load_model()

st.markdown("### データ準備")

input_option = st.selectbox("入力データの選択", ("直接入力", "テキストファイル"))

input_data = None

if input_option == "直接入力":
    input_data = st.text_area(
        "こちらにテキストを入力してください。",
        "If you're going to do something, do it with style.",
    )
else:
    uploaded_file = st.file_uploader("テキストファイルをアップロードしてください。", ["txt"])
    if uploaded_file is not None:
        input_data = uploaded_file.read().decode()

if input_data is not None:
    st.write("入力データ")
    st.write(input_data)

    st.markdown("### パラメータ設定")
    lang = st.selectbox("言語を選択してください", ("英語", "日本語"))

    lang_code_map = {"英語": "en", "日本語": "ja"}
    speed = st.slider("音声スピード", min_value=0.5, max_value=2.0, value=1.1, step=0.1)

    st.markdown("### 音声合成")
    if st.button("音声合成を開始"):
        comment = st.empty()
        comment.write("音声出力を開始します...")
        with st.spinner("生成中..."):
            audio_bytes = synthesize_speech(
                input_data,
                lang_code_map[lang],
                model,
                gpt_cond_latent,
                speaker_embedding,
                speed=speed,
            )
        st.audio(audio_bytes, format="audio/wav")
        comment.write("完了しました")
