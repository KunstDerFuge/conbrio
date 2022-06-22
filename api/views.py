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


def generate_scale(request) -> JsonResponse:
    tonic = request.GET.get('tonic', 'ab')
    quality = request.GET.get('quality', 'melodic')
    print(f'Generating {tonic} {quality} scale...')

    if quality == 'major':
        k = key.Key(tonic.upper())
        scl = k.getScale('major')
    elif quality == 'minor':
        k = key.Key(tonic.lower())
        scl = k.getScale('minor')
    elif quality == 'melodic':
        k = key.Key(tonic.lower())
        scl = scale.MelodicMinorScale(tonic)
    elif quality == 'harmonic':
        k = key.Key(tonic.lower())
        scl = scale.HarmonicMinorScale(tonic)
    else:
        raise ('Invalid key quality passed to generate_scale:', quality)

    left_hand, right_hand, grand_staff, s = create_grand_staff(key.KeySignature(k.sharps))
    time_sig = meter.TimeSignature('7/4')
    time_sig.beamSequence.partition(7)
    left_hand.insert(time_sig)
    right_hand.insert(time_sig)
    sixteenth = duration.Duration(0.25)

    # Spell scale
    bottom_note = scl.pitchFromDegree(1)
    if bottom_note >= pitch.Pitch('F4'):
        bottom_note = bottom_note.transpose('-p8')
    top_note = bottom_note.transpose('p8').transpose('p8')
    asc = scale.DIRECTION_ASCENDING
    desc = scale.DIRECTION_DESCENDING
    rh_notes = [note.Note(p, duration=sixteenth) for p in scl.getPitches(bottom_note, top_note, asc)]
    rh_notes.extend(
        [note.Note(p, duration=sixteenth) for p in scl.getPitches(bottom_note, top_note, desc)][1:])
    rh_notes[-1].duration = duration.Duration(1)
    lh_notes = [n.transpose('-p8') for n in rh_notes]
    right_hand.append(rh_notes)
    left_hand.append(lh_notes)
    p = bottom_note

    new_clef_threshold_asc = pitch.Pitch('F4')
    new_clef_threshold_desc = pitch.Pitch('Bb3')
    inserted_treble = False
    for n in left_hand.notes:
        if not inserted_treble and n.pitch > new_clef_threshold_asc:
            left_hand.insert(int(n.offset), clef.TrebleClef())
            inserted_treble = True
        if inserted_treble and n.pitch < new_clef_threshold_desc:
            left_hand.insert(int(n.offset), clef.BassClef())
            break

    for part in left_hand, right_hand:
        part.makeNotation(inPlace=True)  # makes measures

    parser = musicxml.m21ToXml.GeneralObjectExporter(s)
    print('Done generating scale!')
    return JsonResponse({'xml': parser.parse().decode('utf-8')})
