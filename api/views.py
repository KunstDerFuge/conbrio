import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .utilities import *
from music21 import stream, layout, note, key, clef, pitch, musicxml


def get_random_note(request):
    max_sharps = int(request.GET.get('max_sharps', 7))
    max_flats = int(request.GET.get('max_flats', 7))
    min_note = replace_fancy_accidentals(request.GET.get('min_note', 'A0'))
    max_note = replace_fancy_accidentals(request.GET.get('max_note', 'C8'))
    accidentals = request.GET.get('accidentals', 'true') == 'true'

    # Choose random key signature, hand, and note
    key_sig = key.KeySignature(random.randint(max_flats * -1, max_sharps))
    hand = random.randint(0, 1)
    left_hand, right_hand, grand_staff, s = create_grand_staff(key_sig)

    random_note = generate_random_note(min_note, max_note, accidentals, key_sig)

    print(random_note)

    if random_note < pitch.Pitch('Ab3'):
        hand = 0
    elif random_note > pitch.Pitch('F#4'):
        hand = 1

    if hand == 0:
        left_hand.insert(note.Note(random_note))
    else:
        right_hand.insert(note.Note(random_note))

    for part in left_hand, right_hand:
        part.makeNotation(inPlace=True)  # makes measures

    parser = musicxml.m21ToXml.GeneralObjectExporter(s)
    return JsonResponse({'note': random_note.midi, 'xml': parser.parse().decode('utf-8')})


def get_all_chromatic_notes(request):
    return JsonResponse(
        {'notes': [n.unicodeNameWithOctave for n in scale.ChromaticScale('C').getPitches('A0', 'C8')]})


def generate_scale(scale: str) -> JsonResponse:
    scale.Scale


# Create your views here.
