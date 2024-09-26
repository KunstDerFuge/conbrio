import base64

from django.http import JsonResponse

from .exercises import Scale, ChordExercise
from .models import ExerciseScore, Excerpt
from .utilities import *


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

def get_excerpt(request):
    slug = request.path.split('/')[-1]
    excerpt = Excerpt.objects.filter(slug=slug).first()
    if excerpt:
        return JsonResponse(data={'pdf': base64.b64encode(excerpt.pdf.read()).decode('utf-8')})
    return JsonResponse({}, status=404)

def generate_scale(request) -> JsonResponse:
    tonic = request.GET.get('tonic', 'ab').replace('s', '#')
    quality = request.GET.get('quality', Scale.Quality.MAJOR)
    style = request.GET.get('style', Scale.Style.ABRSM)
    octaves = int(request.GET.get('octaves', 2))
    separation = request.GET.get('separation', Scale.Separation.OCTAVE)
    print(f'Generating {tonic} {quality} {style} scale...')

    _scale = Scale(tonic, quality, note_duration=duration.Duration(0.25),
                   tempo=tempo.MetronomeMark(number=80, referent=duration.Duration(1)), octaves=octaves,
                   style=style, separated_by=separation)
    # _scale = Arpeggio(tonic, Arpeggio.Quality.DOMINANT, octaves=4,
    #                   tempo=tempo.MetronomeMark(number=72, referent=duration.Duration(1)), style=style)
    npm = _scale.get_notes_per_minute()
    print('Notes per minute:', npm)
    print('ABRSM level:', _scale.get_ABRSM_level())
    next_name = _scale.get_next().get_name()
    next_url = _scale.get_next().get_url()
    print('Next: ', next_name)

    return JsonResponse({'xml': _scale.render(), 'next_name': next_name, 'next_url': next_url})


def generate_chord_exercise(request) -> JsonResponse:
    tonic = request.GET.get('tonic', 'ab').replace('s', '#')
    quality = request.GET.get('quality', Scale.Quality.MAJOR)
    octaves = int(request.GET.get('octaves', 2))
    _chord_exercise = ChordExercise(tonic, quality, note_duration=duration.Duration(0.25),
                                    tempo=tempo.MetronomeMark(number=80, referent=duration.Duration(1)), octaves=octaves,
                                    style=style)
    return JsonResponse({'xml': _chord_exercise.render(), 'next_name': None, 'next_url': None})

def grade_exercise(request) -> JsonResponse:
    type = request.GET.get('exercise', 'scale')
    key = request.GET.get('key', 'CMaj')
    variant = request.GET.get('variant', None)

    # TODO: actually calculate this
    accuracy = 0.95
    notes_per_minute = 60

    if type == 'scale':
        score = ExerciseScore(
            exercise=Scale(),
            accuracy=accuracy,
            notes_per_minute=notes_per_minute,
        )
        score.save()
        profile = request.user.profile
        profile.exercise_scores.add(score)

    # elif type == 'arpeggio'
