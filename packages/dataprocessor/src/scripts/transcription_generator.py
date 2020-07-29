from .extract_transcription import extract_transcription
from .save_transcription import save_transcription, save_transcriptions


def create_transcriptions(google_speech_client, wav_file_path, output_path, api_response_file):
    response = google_speech_client.call_speech_to_text(wav_file_path, True, output_path, api_response_file)
    transcriptions = extract_transcription(response)
    save_transcriptions(output_path, transcriptions, 'chunk')
    return transcriptions


def create_azure_transcription(azure_client, language, wav_file_path, punctuation=False):
    result = azure_client.speech_to_text(wav_file_path, language)
    transcription_file_path = wav_file_path.replace('.wav', '.txt')
    transcription = result.text if punctuation else remove_punctation(result.text)
    # TODO handle API failures
    save_transcription(transcription, transcription_file_path)
    return transcription


def create_google_transcription(google_client, wav_file_path):
    content = google_client.call_speech_to_text(wav_file_path, False)
    transcription_file_path = wav_file_path.replace('.wav', '.txt')
    transcriptions = list(map(lambda c: c.alternatives[0].transcript, content.results))
    complete_transcription = ' '.join(transcriptions)
    save_transcription(complete_transcription, transcription_file_path)
    return complete_transcription

def remove_punctation(data_string):
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~।'
    table = str.maketrans(dict.fromkeys(punctuation))
    return data_string.translate(table)