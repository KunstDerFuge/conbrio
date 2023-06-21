from django.http import JsonResponse

from .exercises import Scale, Arpeggio
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
    style = request.GET.get('style', 'ABRSM')
    print(f'Generating {tonic} {quality} {style} scale...')

    # _scale = Scale(tonic, quality, octaves=2, style=style)
    _scale = Arpeggio(tonic, quality, octaves=2,
                      tempo=tempo.MetronomeMark(number=110, referent=duration.Duration(2)), style=style)

    return JsonResponse({'xml': _scale.render()})


def generate_chord_exercise(request) -> JsonResponse:
    def common_tone_chords_from_note(_note: note.Note) -> [chord.Chord]:
        # Rachmaninoff common tone chord series
        chords = [
            chord.Chord([_note, _note.transpose('M3'), _note.transpose('p5')]),
            chord.Chord([_note, _note.transpose('m3'), _note.transpose('p5')]),
            chord.Chord([_note, _note.transpose('m3'), _note.transpose('m6')]),
            chord.Chord([_note, _note.transpose('M3'), _note.transpose('m6')]),
            chord.Chord([_note, _note.transpose('M3'), _note.transpose('M6')]),
            chord.Chord([_note, _note.transpose('p4'), _note.transpose('M6')]),
            chord.Chord([_note, _note.transpose('p4'), _note.transpose('m6')]),
        ]

        # If G or Ab, transpose down an octave for 7th chord series
        if _note.pitch.name in ['G', 'Ab']:
            _note = _note.transpose('-p8')

        chords += [
            chord.Chord([_note, _note.transpose('M3'), _note.transpose('p5'), _note.transpose('m7')]),
            chord.Chord([_note, _note.transpose('m3'), _note.transpose('d5'), _note.transpose('m6')]),
            chord.Chord([_note, _note.transpose('m3'), _note.transpose('p4'), _note.transpose('M6')]),
            chord.Chord([_note, _note.transpose('M2'), _note.transpose('a4'), _note.transpose('M6')]),
            chord.Chord([_note, _note.transpose('a2'), _note.transpose('a4'), _note.transpose('M6')]),
        ]

        return chords

    def key_from_chord(_chord: chord.Chord) -> key.Key():
        quality = _chord.quality
        if quality == 'augmented':
            quality = 'major'
        elif quality == 'diminished':
            return key.Key(_chord.sortAscending()[0].transpose('p5').name, 'major')
        elif _chord.seventh is not None:
            # Dominant
            return key.Key(_chord.root().transpose('p4'), 'major')

        return key.Key(_chord.root().name, quality)

    def exercise_from_chord(_chord: chord.Chord) -> [chord.Chord]:
        chords = [_chord]
        chord_notes = list(_chord.sortAscending().pitches)
        num_chord_notes = len(_chord)
        for inversion in range(num_chord_notes):
            chord_notes[0] = chord_notes[0].transpose('p8')
            c = chord.Chord(chord_notes)
            chord_notes = list(c.sortAscending().pitches)
            chords.append(c)

        for inversion in range(num_chord_notes, 0, -1):
            chord_notes[-1] = chord_notes[-1].transpose('-p8')
            c = chord.Chord(chord_notes)
            chord_notes = list(c.sortAscending().pitches)
            chords.append(c)

        for c in chords:
            c.duration = duration.Duration(2)
            c.sortAscending(inPlace=True)
            lh_fingering = [
                articulations.Fingering(5),
                articulations.Fingering(3),
                articulations.Fingering(1),
            ]

            rh_fingering = [
                articulations.Fingering(1),
                articulations.Fingering(3),
                articulations.Fingering(5)
            ]

            fingering = lh_fingering
            fingering.extend(rh_fingering)

            for finger in lh_fingering:
                finger.placement = 'below'
                finger.alternate = True

            for finger in rh_fingering:
                finger.placement = 'above'
                finger.substitution = True

            c.articulations.extend(fingering)
        chords[-1].duration = duration.Duration(4)
        return chords

    tonic = request.GET.get('tonic', 'ab')
    # Re-capitalize tonic as major key, i.e. ab -> Ab, g -> G
    key_name = tonic[0].upper() + tonic[1:]
    _key = key.Key(key_name)
    s = stream.Stream()
    s.insert(0, clef.TrebleClef())
    s.insert(0, key.KeySignature(_key.sharps))
    if tonic in ['A', 'B', 'Bb']:
        tonic += '3'
    else:
        tonic += '4'

    for _chord in common_tone_chords_from_note(note.Note(tonic)):
        s.append(key_from_chord(_chord))
        s.append([c for c in exercise_from_chord(_chord)])
        s.append(layout.SystemLayout(isNew=True))

    s.definesExplicitSystemBreaks = True
    s.makeNotation(inPlace=True)

    parser = musicxml.m21ToXml.GeneralObjectExporter(s)
    return JsonResponse({'xml': parser.parse().decode('utf-8')})
