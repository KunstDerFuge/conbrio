from music21 import tempo, duration
from api.exercises import Scale, Arpeggio
import random


class ABRSMMockExam:
    def __init__(self, grade):
        self.requirements = []

        if grade == 0:
            scale_tempo = tempo.MetronomeMark(number=54, referent=duration.Duration(1))
            arpeggio_tempo = tempo.MetronomeMark(number=52, referent=duration.Duration(1))
            hs_key_choices_major = {'choices': ['C'], 'choice': 'examiner'}
            hs_key_choices_minor = {'choices': ['D'], 'choice': 'examiner'}
            mode_choices_minor = {'choices': [Scale.Quality.HARMONIC_MINOR, Scale.Quality.MELODIC_MINOR],
                                  'choice': 'candidate'}

            self.requirements = [
                # Hands separately
                {'type': 'scale', 'key': hs_key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 1},
                {'type': 'scale', 'key': hs_key_choices_minor, 'mode': mode_choices_minor, 'tempo': scale_tempo,
                 'octaves': 1},

                # Contrary motion
                # TODO: Five-finger only
                {'type': 'scale', 'key': 'C', 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 1, 'motion': Scale.Motion.CONTRARY},

                # Arpeggios HS
                # TODO: To fifth only
                {'type': 'arpeggio', 'key': hs_key_choices_major, 'mode': Arpeggio.Quality.MAJOR,
                 'tempo': arpeggio_tempo, 'octaves': 1, 'inversion': Arpeggio.Inversion.ROOT},
                {'type': 'arpeggio', 'key': hs_key_choices_minor, 'mode': Arpeggio.Quality.MINOR,
                 'tempo': arpeggio_tempo, 'octaves': 1, 'inversion': Arpeggio.Inversion.ROOT},
            ]

        if grade == 1:
            scale_tempo = tempo.MetronomeMark(number=60, referent=duration.Duration(1))
            arpeggio_tempo = tempo.MetronomeMark(number=58, referent=duration.Duration(1))
            ht_key_choices_major = {'choices': ['C'], 'choice': 'examiner'}
            hs_key_choices_major = {'choices': ['G', 'F'], 'choice': 'examiner'}
            hs_key_choices_minor = {'choices': ['A', 'D'], 'choice': 'examiner'}
            mode_choices_minor = {'choices': [Scale.Quality.HARMONIC_MINOR, Scale.Quality.MELODIC_MINOR],
                                  'choice': 'candidate'}

            self.requirements = [
                # C Major HT
                {'type': 'scale', 'key': ht_key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 1},

                # Hands separately
                {'type': 'scale', 'key': hs_key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2},
                {'type': 'scale', 'key': hs_key_choices_minor, 'mode': mode_choices_minor, 'tempo': scale_tempo,
                 'octaves': 2},

                # Contrary motion
                {'type': 'scale', 'key': 'C', 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 1, 'motion': Scale.Motion.CONTRARY},

                # Arpeggios HS
                {'type': 'arpeggio', 'key': 'G', 'mode': Arpeggio.Quality.MAJOR,
                 'tempo': arpeggio_tempo, 'octaves': 1, 'inversion': Arpeggio.Inversion.ROOT},
                {'type': 'arpeggio', 'key': 'A', 'mode': Arpeggio.Quality.MINOR,
                 'tempo': arpeggio_tempo, 'octaves': 1, 'inversion': Arpeggio.Inversion.ROOT},
            ]

        if grade == 2:
            scale_tempo = tempo.MetronomeMark(number=66, referent=duration.Duration(1))
            arpeggio_tempo = tempo.MetronomeMark(number=63, referent=duration.Duration(1))
            ht_key_choices_major = {'choices': ['G', 'F'], 'choice': 'examiner'}
            ht_key_choices_minor = {'choices': ['A', 'D'], 'choice': 'examiner'}
            hs_key_choices_major = {'choices': ['D', 'A'], 'choice': 'examiner'}
            hs_key_choices_minor = {'choices': ['E', 'G'], 'choice': 'examiner'}
            mode_choices_minor = {'choices': [Scale.Quality.HARMONIC_MINOR, Scale.Quality.MELODIC_MINOR],
                                  'choice': 'candidate'}

            self.requirements = [
                # Major and minor HT
                {'type': 'scale', 'key': ht_key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2},
                {'type': 'scale', 'key': ht_key_choices_minor, 'mode': mode_choices_minor, 'tempo': scale_tempo,
                 'octaves': 2},

                # Hands separately
                {'type': 'scale', 'key': hs_key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2},
                {'type': 'scale', 'key': hs_key_choices_minor, 'mode': mode_choices_minor, 'tempo': scale_tempo,
                 'octaves': 2},

                # Contrary motion
                {'type': 'scale', 'key': 'C', 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY},

                # Chromatic
                # 'tempo': scale_tempo
                # TODO

                # Arpeggios HS
                {'type': 'arpeggio', 'key': hs_key_choices_major, 'mode': Arpeggio.Quality.MAJOR,
                 'tempo': arpeggio_tempo, 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},
                {'type': 'arpeggio', 'key': hs_key_choices_minor, 'mode': Arpeggio.Quality.MINOR,
                 'tempo': arpeggio_tempo, 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},
            ]

        if grade == 3:
            scale_tempo = tempo.MetronomeMark(number=80, referent=duration.Duration(1))
            arpeggio_tempo = tempo.MetronomeMark(number=72, referent=duration.Duration(1))
            ht_key_choices_major = {'choices': ['D', 'A'], 'choice': 'examiner'}
            ht_key_choices_minor = {'choices': ['E', 'G'], 'choice': 'examiner'}
            hs_key_choices_major = {'choices': ['Bb', 'Eb'], 'choice': 'examiner'}
            hs_key_choices_minor = {'choices': ['B', 'C'], 'choice': 'examiner'}
            mode_choices_minor = {'choices': [Scale.Quality.HARMONIC_MINOR, Scale.Quality.MELODIC_MINOR],
                                  'choice': 'candidate'}

            self.requirements = [
                # Major and minor HT
                {'type': 'scale', 'key': ht_key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2},
                {'type': 'scale', 'key': ht_key_choices_minor, 'mode': mode_choices_minor, 'tempo': scale_tempo,
                 'octaves': 2},

                # Hands separately
                {'type': 'scale', 'key': hs_key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2},
                {'type': 'scale', 'key': hs_key_choices_minor, 'mode': mode_choices_minor, 'tempo': scale_tempo,
                 'octaves': 2},

                # Contrary motion
                {'type': 'scale', 'key': 'Eb', 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY},
                {'type': 'scale', 'key': 'C', 'mode': Scale.Quality.HARMONIC_MINOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY},

                # Chromatic contrary motion
                # 'tempo': scale_tempo
                # TODO

                # Arpeggios HT
                {'type': 'arpeggio', 'key': ht_key_choices_major, 'mode': Arpeggio.Quality.MAJOR,
                 'tempo': arpeggio_tempo, 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},
                {'type': 'arpeggio', 'key': ht_key_choices_minor, 'mode': Arpeggio.Quality.MINOR,
                 'tempo': arpeggio_tempo, 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},

                # Arpeggios HS
                {'type': 'arpeggio', 'key': hs_key_choices_major, 'mode': Arpeggio.Quality.MAJOR,
                 'tempo': arpeggio_tempo, 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},
                {'type': 'arpeggio', 'key': hs_key_choices_minor, 'mode': Arpeggio.Quality.MINOR,
                 'tempo': arpeggio_tempo, 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},
            ]

        if grade == 4:
            scale_tempo = tempo.MetronomeMark(number=100, referent=duration.Duration(1))
            arpeggio_tempo = tempo.MetronomeMark(number=80, referent=duration.Duration(1))
            ht_key_choices_major = {'choices': ['Bb', 'Eb'], 'choice': 'examiner'}
            ht_key_choices_minor = {'choices': ['B', 'C'], 'choice': 'examiner'}
            hs_key_choices_major = {'choices': ['B', 'F#', 'Ab'], 'choice': 'examiner'}
            hs_key_choices_minor = {'choices': ['F#', 'F'], 'choice': 'examiner'}
            mode_choices_minor = {'choices': [Scale.Quality.HARMONIC_MINOR, Scale.Quality.MELODIC_MINOR],
                                  'choice': 'candidate'}

            self.requirements = [
                # Major and minor HT
                {'type': 'scale', 'key': ht_key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2},
                {'type': 'scale', 'key': ht_key_choices_minor, 'mode': mode_choices_minor, 'tempo': scale_tempo,
                 'octaves': 2},

                # Hands separately
                {'type': 'scale', 'key': hs_key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2},
                {'type': 'scale', 'key': hs_key_choices_minor, 'mode': mode_choices_minor, 'tempo': scale_tempo,
                 'octaves': 2},

                # Contrary motion
                {'type': 'scale', 'key': 'Eb', 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY},
                {'type': 'scale', 'key': 'C', 'mode': Scale.Quality.HARMONIC_MINOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY},

                # Chromatic
                # 'tempo': scale_tempo
                # TODO

                # Arpeggios HT
                {'type': 'arpeggio', 'key': ht_key_choices_major, 'mode': Arpeggio.Quality.MAJOR,
                 'tempo': arpeggio_tempo, 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},
                {'type': 'arpeggio', 'key': ht_key_choices_minor, 'mode': Arpeggio.Quality.MINOR,
                 'tempo': arpeggio_tempo, 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},

                # Arpeggios HS
                {'type': 'arpeggio', 'key': hs_key_choices_major, 'mode': Arpeggio.Quality.MAJOR,
                 'tempo': arpeggio_tempo, 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},
                {'type': 'arpeggio', 'key': hs_key_choices_minor, 'mode': Arpeggio.Quality.MINOR,
                 'tempo': arpeggio_tempo, 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},
            ]

        if grade == 5:
            scale_tempo = tempo.MetronomeMark(number=60, referent=duration.Duration(2))
            arpeggio_tempo = tempo.MetronomeMark(number=44, referent=duration.Duration(2))
            key_choices_major = {'choices': ['A', 'E', 'B', 'F#', 'Db'], 'choice': 'examiner'}
            key_choices_minor = {'choices': ['F#', 'C#', 'G#', 'Eb', 'Bb'], 'choice': 'examiner'}
            mode_choices_minor = {'choices': [Scale.Quality.HARMONIC_MINOR, Scale.Quality.MELODIC_MINOR],
                                  'choice': 'candidate'}

            self.requirements = [
                # Major and minor
                {'type': 'scale', 'key': key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2},
                {'type': 'scale', 'key': key_choices_minor, 'mode': mode_choices_minor, 'tempo': scale_tempo,
                 'octaves': 2},

                # Staccato scales
                {'type': 'scale', 'key': 'Ab', 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo, 'octaves': 2},
                {'type': 'scale', 'key': 'F', 'mode': mode_choices_minor, 'tempo': scale_tempo, 'octaves': 2},

                # Contrary motion
                {'type': 'scale', 'key': 'Db', 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY},
                {'type': 'scale', 'key': 'C#', 'mode': Scale.Quality.HARMONIC_MINOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY},

                # Chromatic contrary motion
                # 'tempo': scale_tempo
                # TODO

                # Arpeggios
                {'type': 'arpeggio', 'key': key_choices_major, 'mode': Arpeggio.Quality.MAJOR, 'tempo': arpeggio_tempo,
                 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},
                {'type': 'arpeggio', 'key': key_choices_minor, 'mode': Arpeggio.Quality.MINOR, 'tempo': arpeggio_tempo,
                 'octaves': 2, 'inversion': Arpeggio.Inversion.ROOT},

                # Dominant
                {'type': 'arpeggio', 'key': key_choices_major, 'mode': Arpeggio.Quality.DOMINANT,
                 'tempo': arpeggio_tempo, 'octaves': 2},

                # Diminished
                {'type': 'arpeggio', 'key': 'B', 'mode': Arpeggio.Quality.DIMINISHED, 'tempo': arpeggio_tempo,
                 'octaves': 2},
            ]

        if grade == 6:
            scale_tempo = tempo.MetronomeMark(number=72, referent=duration.Duration(2))
            arpeggio_tempo = tempo.MetronomeMark(number=50, referent=duration.Duration(2))
            key_choices_major = {'choices': ['D', 'F', 'Ab', 'B'], 'choice': 'examiner'}
            key_choices_minor = {'choices': ['D', 'F', 'G#', 'B'], 'choice': 'examiner'}
            articulation_choices = {'choices': [Scale.Articulation.LEGATO, Scale.Articulation.STACCATO],
                                    'choice': 'examiner'}

            self.requirements = [
                # Major and minor
                {'type': 'scale', 'key': key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 4, 'articulation': articulation_choices},
                {'type': 'scale', 'key': key_choices_minor,
                 'mode': [Scale.Quality.HARMONIC_MINOR, Scale.Quality.MELODIC_MINOR], 'tempo': scale_tempo,
                 'octaves': 4, 'articulation': articulation_choices},

                # Contrary motion
                {'type': 'scale', 'key': key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY},
                {'type': 'scale', 'key': key_choices_minor, 'mode': Scale.Quality.HARMONIC_MINOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY},

                # Chromatic
                # 'tempo': scale_tempo
                # TODO

                # Arpeggios
                {'type': 'arpeggio', 'key': key_choices_major, 'mode': Arpeggio.Quality.MAJOR, 'tempo': arpeggio_tempo,
                 'octaves': 4, 'inversion': Arpeggio.Inversion.ROOT},
                {'type': 'arpeggio', 'key': key_choices_minor, 'mode': Arpeggio.Quality.MINOR, 'tempo': arpeggio_tempo,
                 'octaves': 4, 'inversion': Arpeggio.Inversion.ROOT},

                # Dominant
                {'type': 'arpeggio', 'key': key_choices_major, 'mode': Arpeggio.Quality.DOMINANT,
                 'tempo': arpeggio_tempo, 'octaves': 4},

                # Diminished
                {'type': 'arpeggio', 'key': 'G#', 'mode': Arpeggio.Quality.DIMINISHED, 'tempo': arpeggio_tempo,
                 'octaves': 4},
                {'type': 'arpeggio', 'key': 'B', 'mode': Arpeggio.Quality.DIMINISHED, 'tempo': arpeggio_tempo,
                 'octaves': 4},
            ]

        if grade == 7:
            scale_tempo = tempo.MetronomeMark(number=80, referent=duration.Duration(2))
            arpeggio_tempo = tempo.MetronomeMark(number=56, referent=duration.Duration(2))
            scales_3rd_apart_tempo = tempo.MetronomeMark(number=60, referent=duration.Duration(2))
            legato_scale_3rds_tempo = tempo.MetronomeMark(number=46, referent=duration.Duration(2))
            staccato_scale_3rds_tempo = tempo.MetronomeMark(number=54, referent=duration.Duration(2))
            key_choices_major = {'choices': ['Db', 'E', 'G', 'Bb'], 'choice': 'examiner'}
            key_choices_minor = {'choices': ['C#', 'E', 'G', 'Bb'], 'choice': 'examiner'}
            articulation_choices = {'choices': [Scale.Articulation.LEGATO, Scale.Articulation.STACCATO],
                                    'choice': 'examiner'}

            self.requirements = [
                # Major and minor
                {'type': 'scale', 'key': key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 4, 'articulation': articulation_choices},
                {'type': 'scale', 'key': key_choices_minor,
                 'mode': [Scale.Quality.HARMONIC_MINOR, Scale.Quality.MELODIC_MINOR], 'tempo': scale_tempo,
                 'octaves': 4, 'articulation': articulation_choices},

                # Separated by a 3rd
                {'type': 'scale', 'key': key_choices_major, 'mode': Scale.Quality.MAJOR,
                 'tempo': scales_3rd_apart_tempo, 'octaves': 4, 'separation': Scale.Separation.THIRD,
                 'articulation': articulation_choices},
                {'type': 'scale', 'key': key_choices_minor, 'mode': Scale.Quality.HARMONIC_MINOR,
                 'tempo': scales_3rd_apart_tempo, 'octaves': 4, 'separation': Scale.Separation.THIRD,
                 'articulation': articulation_choices},

                # Contrary motion
                {'type': 'scale', 'key': key_choices_major, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY, 'articulation': articulation_choices},
                {'type': 'scale', 'key': key_choices_minor, 'mode': Scale.Quality.HARMONIC_MINOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY, 'articulation': articulation_choices},

                # Legato scale in 3rds
                # 'tempo': legato_scale_3rds_tempo
                # TODO

                # Staccato scale in 3rds
                # 'tempo': staccato_scale_3rds_tempo
                # TODO

                # Chromatic contrary motion
                # 'tempo': scale_tempo
                # TODO

                # Arpeggios
                {'type': 'arpeggio', 'key': key_choices_major, 'mode': Arpeggio.Quality.MAJOR, 'tempo': arpeggio_tempo,
                 'octaves': 4, 'inversion': Arpeggio.Inversion.FIRST},
                {'type': 'arpeggio', 'key': key_choices_minor, 'mode': Arpeggio.Quality.MINOR, 'tempo': arpeggio_tempo,
                 'octaves': 4, 'inversion': Arpeggio.Inversion.FIRST},

                # Dominant
                {'type': 'arpeggio', 'key': key_choices_major, 'mode': Arpeggio.Quality.DOMINANT,
                 'tempo': arpeggio_tempo, 'octaves': 4},

                # Diminished
                {'type': 'arpeggio', 'key': 'Bb', 'mode': Arpeggio.Quality.DIMINISHED, 'tempo': arpeggio_tempo,
                 'octaves': 4},
                {'type': 'arpeggio', 'key': 'E', 'mode': Arpeggio.Quality.DIMINISHED, 'tempo': arpeggio_tempo,
                 'octaves': 4},
            ]

        if grade == 8:
            scale_tempo = tempo.MetronomeMark(number=88, referent=duration.Duration(2))
            arpeggio_tempo = tempo.MetronomeMark(number=66, referent=duration.Duration(2))
            scales_6th_apart_tempo = tempo.MetronomeMark(number=60, referent=duration.Duration(2))
            legato_scale_3rds_tempo = tempo.MetronomeMark(number=52, referent=duration.Duration(2))
            staccato_scale_6ths_tempo = tempo.MetronomeMark(number=54, referent=duration.Duration(2))
            key_choices = {'choices': ['C', 'Eb', 'F#', 'A'], 'choice': 'examiner'}
            articulation_choices = {'choices': [Scale.Articulation.LEGATO, Scale.Articulation.STACCATO],
                                    'choice': 'examiner'}

            self.requirements = [
                # Major and minor
                {'type': 'scale', 'key': key_choices, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo, 'octaves': 4,
                 'articulation': articulation_choices},
                {'type': 'scale', 'key': key_choices,
                 'mode': [Scale.Quality.HARMONIC_MINOR, Scale.Quality.MELODIC_MINOR], 'tempo': scale_tempo,
                 'octaves': 4, 'articulation': articulation_choices},

                # Separated by a 6th
                {'type': 'scale', 'key': key_choices, 'mode': Scale.Quality.MAJOR, 'tempo': scales_6th_apart_tempo,
                 'octaves': 4, 'separation': Scale.Separation.SIXTH, 'articulation': articulation_choices},
                {'type': 'scale', 'key': key_choices, 'mode': Scale.Quality.HARMONIC_MINOR,
                 'tempo': scales_6th_apart_tempo, 'octaves': 4, 'separation': Scale.Separation.SIXTH,
                 'articulation': articulation_choices},

                # Contrary motion
                {'type': 'scale', 'key': key_choices, 'mode': Scale.Quality.MAJOR, 'tempo': scale_tempo, 'octaves': 2,
                 'motion': Scale.Motion.CONTRARY, 'articulation': articulation_choices},
                {'type': 'scale', 'key': key_choices, 'mode': Scale.Quality.HARMONIC_MINOR, 'tempo': scale_tempo,
                 'octaves': 2, 'motion': Scale.Motion.CONTRARY, 'articulation': articulation_choices},

                # Legato scale in 3rds
                # 'tempo': legato_scale_3rds_tempo
                # TODO

                # Staccato scale in 6ths
                # 'tempo': staccato_scale_6ths_tempo
                # TODO

                # Chromatic scale a major 6th apart
                # 'tempo': scales_6th_apart_tempo
                # TODO

                # Whole tone scales
                # 'tempo': scale_tempo
                # TODO

                # Arpeggios
                {'type': 'arpeggio', 'key': key_choices, 'mode': Arpeggio.Quality.MAJOR, 'tempo': arpeggio_tempo,
                 'octaves': 4, 'inversion': Arpeggio.Inversion.SECOND},
                {'type': 'arpeggio', 'key': key_choices, 'mode': Arpeggio.Quality.MINOR, 'tempo': arpeggio_tempo,
                 'octaves': 4, 'inversion': Arpeggio.Inversion.SECOND},

                # Dominant
                {'type': 'arpeggio', 'key': key_choices, 'mode': Arpeggio.Quality.DOMINANT, 'tempo': arpeggio_tempo,
                 'octaves': 4},

                # Diminished
                {'type': 'arpeggio', 'key': 'Eb', 'mode': Arpeggio.Quality.DIMINISHED, 'tempo': arpeggio_tempo,
                 'octaves': 4},
                {'type': 'arpeggio', 'key': 'C', 'mode': Arpeggio.Quality.DIMINISHED, 'tempo': arpeggio_tempo,
                 'octaves': 4},
            ]
