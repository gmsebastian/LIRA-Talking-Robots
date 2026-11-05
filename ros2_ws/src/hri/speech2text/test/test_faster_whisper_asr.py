import types

import numpy
import pytest
import rclpy

from speech2text import faster_whisper_asr


CHUNK = faster_whisper_asr.CHUNK
# One chunk loud enough to trip the power threshold, then silence to end the utterance.
LOUD_CHUNKS = 1
QUIET_CHUNKS = faster_whisper_asr.SILENCE_CHUNKS


class FakeStream:
    """Hands out one loud chunk followed by silence, so exactly one utterance is recorded."""

    def __init__(self):
        loud = (numpy.ones(CHUNK, dtype=numpy.int16) * 20000).tobytes()
        quiet = numpy.zeros(CHUNK, dtype=numpy.int16).tobytes()
        self._pending = [loud] * LOUD_CHUNKS + [quiet] * QUIET_CHUNKS

    def read(self, num_frames, exception_on_overflow=True):
        if self._pending:
            return self._pending.pop(0)
        return numpy.zeros(num_frames, dtype=numpy.int16).tobytes()

    def stop_stream(self):
        pass

    def close(self):
        pass


class FakePyAudio:
    """Stands in for pyaudio.PyAudio so the test never opens a real microphone."""

    paInt16 = 16
    open_kwargs = None

    def open(self, **kwargs):  # noqa: A003 - must mirror pyaudio.PyAudio.open
        FakePyAudio.open_kwargs = kwargs
        return FakeStream()

    def terminate(self):
        pass


class FakeWhisperModel:
    """Records what the node hands to transcribe() instead of running inference."""

    received = None

    def __init__(self, *args, **kwargs):
        pass

    def transcribe(self, audio, beam_size=None, language=None):
        FakeWhisperModel.received = audio
        info = types.SimpleNamespace(language='es', language_probability=1.0)
        return [], info


@pytest.fixture
def node(monkeypatch):
    """Build the node with a stubbed mic and model, and let spin() run one utterance."""
    monkeypatch.setattr(faster_whisper_asr, 'pyaudio',
                        types.SimpleNamespace(PyAudio=FakePyAudio, paInt16=FakePyAudio.paInt16))
    monkeypatch.setattr(faster_whisper_asr, 'WhisperModel', FakeWhisperModel)
    # rclpy.ok() stays true until transcribe() has been called, so the loop exits.
    monkeypatch.setattr(rclpy, 'ok', lambda: FakeWhisperModel.received is None)
    FakeWhisperModel.received = None
    rclpy.init()
    yield faster_whisper_asr.FasterWhisperNode()
    rclpy.shutdown()


def test_transcribe_receives_samples_not_a_file_path(node):
    node.spin()

    audio = FakeWhisperModel.received
    assert isinstance(audio, numpy.ndarray), \
        'a file path makes faster-whisper decode through PyAV, which is broken with av 19'
    assert audio.dtype == numpy.float32
    assert audio.shape == (CHUNK * (LOUD_CHUNKS + QUIET_CHUNKS),)
    assert numpy.abs(audio).max() <= 1.0


def test_capture_format_is_what_whisper_expects(node):
    node.spin()

    # The int16 -> float32 conversion is only valid if the mic captures whisper's own
    # input format; anything else would have to be resampled before transcribe().
    assert faster_whisper_asr.CHANNELS == 1
    assert faster_whisper_asr.RATE == 16000
    assert FakePyAudio.open_kwargs['channels'] == 1
    assert FakePyAudio.open_kwargs['rate'] == 16000
