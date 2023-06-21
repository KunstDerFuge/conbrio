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


def create_grand_staff(key_signature: key.KeySignature or None) -> tuple:
    # Create grand staff
    left_hand = stream.PartStaff()
    right_hand = stream.PartStaff()
    grand_staff = layout.StaffGroup([right_hand, left_hand])
    s = stream.Score([right_hand, left_hand, grand_staff])

    left_hand.insert(clef.BassClef())
    right_hand.insert(clef.TrebleClef())

    if key_signature:
        left_hand.insert(0, key_signature)
        right_hand.insert(0, key_signature)

    return left_hand, right_hand, grand_staff, s


def chord_from_key(k: key.Key, *degrees):
    return chord.Chord([k.pitchFromDegree(d) for d in degrees])
