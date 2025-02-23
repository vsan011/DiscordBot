
import os
import time
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk

import setting


class TTS:

    speak_count = 0
    VOICE_NAME = "en-US-AshleyNeural"
    pitch_percentage = '+25%'
    speech_config = speechsdk.SpeechConfig(subscription=setting.SPEECH_KEY, region=setting.SPEECH_REGION)
    # Set output to mp3
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # pre-connect
    connection = speechsdk.Connection.from_speech_synthesizer(speech_synthesizer)
    connection.open(True)

    @staticmethod
    def check_and_delete_wav(folder_path, max_files=10):
        """
            檢查文件夾中的 .wav 檔案數量，若超過 max_files 則全數刪除
            :param folder_path: 目標文件夾路徑
            :param max_files: 允許的最大檔案數量
            :return: 無
            """
        try:
            target_folder = Path(folder_path)

            # 檢查路徑是否存在且為文件夾
            if not target_folder.exists():
                print(f"錯誤：路徑 {target_folder} 不存在。")
                return
            if not target_folder.is_dir():
                print(f"錯誤：{target_folder} 不是文件夾。")
                return

            # 獲取所有 .wav 文件（不區分大小寫）
            wav_files = [
                f for f in target_folder.glob("*")
                if f.is_file() and f.suffix.lower() == ".wav"
            ]
            # 統計數量
            num_wav = len(wav_files)

            # 判斷是否超過限制
            if num_wav > max_files:
                print(f"文件數量超過 {max_files}，開始刪除...")
                deleted_count = 0
                # 逐個刪除文件（避免權限問題中斷）
                for wav_file in wav_files:
                    try:
                        os.remove(wav_file)
                        deleted_count += 1
                        print(f"已刪除：{wav_file.name}")
                    except Exception as e:
                        print(f"刪除 {wav_file.name} 失敗：{str(e)}")

                print(f"操作完成，共刪除 {deleted_count}/{num_wav} 個文件")
            else:
                print(f"文件數量未超過 {max_files}，無需刪除")
        except Exception as e:
            print(f"發生未預期的錯誤：{str(e)}")

    if speak_count % 10 == 0 or speak_count == 0: check_and_delete_wav(setting.AUDIO_DIR)

    @staticmethod
    def speak(text):
        TTS.speak_count += 1
        start_time = time.time()
        #filename
        first_word = text.split(' ')
        output_filename = f"{setting.AUDIO_DIR}/output_{time.strftime('%Y%m%d-%H%M%S')}_{first_word[0]}.wav"

        ssml = f"""
                <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
                    <voice name='{TTS.VOICE_NAME}'>
                        <prosody pitch='{TTS.pitch_percentage}'>
                            {text}
                        </prosody>
                    </voice>
                </speak>
                """

        # Synthesize speech
        result = TTS.speech_synthesizer.speak_ssml_async(ssml).get()

        if os.path.exists(output_filename):
            os.remove(output_filename)

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # 流式讀取音頻
            audio_stream = speechsdk.AudioDataStream(result)
            audio_stream.save_to_wav_file(output_filename)
            audio_stream.position = 0
            audio_buffer = bytes(1600)  # 1600 bytes ≈ 50ms 音頻
            filled_size = audio_stream.read_data(audio_buffer)

            #calculate file size
            total_size = 0
            while filled_size > 0:
                print("{} bytes received.".format(filled_size))
                total_size += filled_size
                filled_size = audio_stream.read_data(audio_buffer)

            print(f"生成全新文件 {output_filename}, 大小: {total_size} bytes")
            print('Time taken: {:0.2f}s'.format(time.time() - start_time))
            return output_filename

        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))


if __name__ == "__main__":
    print(TTS.speak("test subject 2"))
