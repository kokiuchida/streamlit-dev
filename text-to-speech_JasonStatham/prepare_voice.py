"""
音声ファイルから話者特徴量を事前抽出し、voice_profile/ に保存するスクリプト。
Streamlit起動前に一度だけ実行する。
"""

import os
import torch
from TTS.api import TTS

AUDIO_DIR = "audio"
OUTPUT_DIR = "voice_profile"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("モデルをロード中...")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

    model = tts.synthesizer.tts_model

    # 音声ファイル一覧（MP3のみ）
    audio_files = sorted(
        os.path.join(AUDIO_DIR, f)
        for f in os.listdir(AUDIO_DIR)
        if f.endswith(".mp3")
    )
    print(f"音声ファイル: {audio_files}")

    # 話者特徴量を抽出
    print("話者特徴量を抽出中...")
    gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(
        audio_path=audio_files
    )

    # 保存
    torch.save(gpt_cond_latent, os.path.join(OUTPUT_DIR, "gpt_cond_latent.pt"))
    torch.save(speaker_embedding, os.path.join(OUTPUT_DIR, "speaker_embedding.pt"))
    print(f"話者特徴量を {OUTPUT_DIR}/ に保存しました。")


if __name__ == "__main__":
    main()
