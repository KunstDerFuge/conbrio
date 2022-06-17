import random

from music21 import *


def generate_random_note(min_note: str, max_note: str, accidentals: bool,
                         scale_key: key.KeySignature or None) -> pitch.Pitch:
    if scale_key:
        pitches = scale_key.getScale().getPitches(min_note, max_note)
    else:
        pitches = scale.ChromaticScale('C').getPitches(min_note, max_note)

    print(f'Generating random pitch in {scale_key} between {min_note} and {max_note}...')
    random_pitch = random.choice(pitches)

    if accidentals:
        random_pitch.accidental = random.randint(-2, 2)

    return random_pitch


def replace_fancy_accidentals(fancy: str) -> str:
    return fancy.replace('♭', 'b').replace('♯', '#')
