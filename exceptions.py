class SpeechError(Exception):
    pass


class EmptySpeechError(SpeechError):
    pass


class SpeechRecognizeError(SpeechError):
    pass
