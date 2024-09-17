from copy import deepcopy
from enum import StrEnum, Enum
from typing import Optional

from music21 import key, scale, meter, duration, pitch, note, clef, musicxml, chord, stream, spanner, articulations

from api.utilities import create_grand_staff


class Exercise:
    def __init__(self, tonic='C', quality='major', note_duration=duration.Duration(0.25), octaves=2,
                 key_sig=None, tempo=None, articulation=None, staff='grand'):
        self.tonic = tonic
        self.quality = quality
        self.duration = note_duration
        self.octaves = octaves
        self.key = key_sig
        self.tempo = tempo
        self.articulation = articulation
        self.staff = staff

        if self.staff == 'grand':
            sharps = 0
            if self.key:
                sharps = self.key.sharps
            self.left_hand, self.right_hand, self.grand_staff, self.s = create_grand_staff(
                key.KeySignature(sharps))
        else:
            self.s = stream.PartStaff()
            if self.key:
                self.s.insert(0, key)

        if self.tempo:
            if self.staff == 'grand':
                self.right_hand.insert(0, self.tempo)
            else:
                self.s.insert(0, self.tempo)

    def beam_in_groups(self, group_size, duration='eighth'):
        if self.staff == 'grand':
            stream_list = [self.left_hand, self.right_hand]
        else:
            stream_list = [self.s]

        for s in stream_list:
            beamed_notes = [n for n in s.notes if n.duration == s.notes[0].duration]
            for number, _note in enumerate(beamed_notes):
                _note.beams.beamsList = []
                if number % group_size == 0:
                    _note.beams.fill(duration, type='start')
                elif number % group_size == group_size - 1:
                    _note.beams.fill(duration, type='stop')
                else:
                    _note.beams.fill(duration, type='continue')

            beamed_notes[-1].beams.fill(duration, type='stop')

    def insert_courtesy_clefs(self,
                              new_clef_threshold_asc=pitch.Pitch('F#4'),
                              new_clef_threshold_desc=pitch.Pitch('Bb3'),
                              ottava_threshold=pitch.Pitch('F6'),
                              quantize=1):
        """
        Create courtesy clefs, usually for left hand part.

        Parameters:
            new_clef_threshold_asc (pitch.Pitch): The note above which we will insert a treble clef.
            new_clef_threshold_desc (pitch.Pitch): The note below which we will insert a bass clef.
            ottava_threshold (pitch.Pitch): The note above which we will span notes with an ottava (8va).
            quantize (int or None): The number of beats in a grid where the new clef can be inserted.
        """

        def do_quantize(offset):
            if quantize:
                return (offset // quantize) * quantize

        if not self.staff == 'grand':
            s = self.s
        else:
            s = self.left_hand

        inserted_treble = False
        for n in s.notes:
            if not inserted_treble and n.pitch > new_clef_threshold_asc:
                s.insert(do_quantize(n.offset), clef.TrebleClef())
                inserted_treble = True
            if inserted_treble and n.pitch < new_clef_threshold_desc:
                s.insert(do_quantize(n.offset), clef.BassClef())
                inserted_treble = False

        inserted_ottava = False
        ottava_start = None
        ottava_end = None
        for n in self.right_hand.notes:
            if not inserted_ottava and n.pitch >= ottava_threshold:
                print('Inserting ottava...')
                ottava_start = do_quantize(n.offset)
                inserted_ottava = True
            if inserted_ottava and n.pitch < ottava_threshold:
                print('Terminating ottava...')
                ottava_end = do_quantize(n.offset)
                # If the ottava can end within a beat (i.e. 'and of 2'), extend it to the end of the beat
                if ottava_end > int(n.offset):
                    print('Extending ottava...')
                    print(n.offset, int(n.offset))
                    ottava_end += 1
                print('Ottava start/end: ', ottava_start, ottava_end)
                notes = [n for n in self.right_hand.notes if ottava_start <= n.offset < ottava_end]
                ottava = spanner.Ottava(transposing=False)
                ottava.addSpannedElements(notes)
                self.right_hand.append(ottava)
                inserted_ottava = False
                ottava_start = None
                ottava_end = None

    def get_notes_per_minute(self) -> Optional[int]:
        if not self.tempo or not self.duration:
            return None

        bpm = self.tempo.getQuarterBPM()
        notes_per_beat = 1 / self.duration.quarterLength
        return round(bpm * notes_per_beat)

    def get_ABRSM_level_from_rubric(self, rubric: dict[int, int]) -> int:
        npm = self.get_notes_per_minute()

        if npm >= rubric[8]:
            return 8
        elif npm >= rubric[7]:
            return 7
        elif npm >= rubric[6]:
            return 6
        elif npm >= rubric[5]:
            return 5
        elif npm >= rubric[4]:
            return 4
        elif npm >= rubric[3]:
            return 3
        elif npm >= rubric[2]:
            return 2
        elif npm >= rubric[1]:
            return 1
        else:
            return 0

    def get_tags(self):
        tags = set()

        if self.tonic and self.quality:
            tags.add(f'{self.tonic} {self.quality}')

        if self.octaves:
            tags.add(f'{self.octaves} Octaves')

        if self.articulation:
            tags.add(f'{self.articulation}')

        return tags

    def get_name(self):
        pass

    def get_url(self):
        pass

    def render(self, tags=None):
        if self.staff == 'grand':
            for part in self.left_hand, self.right_hand:
                part.makeNotation(inPlace=True)  # makes measures
        else:
            self.s.makeNotation(inPlace=True)

        parser = musicxml.m21ToXml.GeneralObjectExporter(self.s)
        print('Done generating exercise!')
        if tags:
            print('Tags:')
            print(tags)
        print(self.get_name())
        return parser.parse().decode('utf-8')


class Scale(Exercise):

    class Quality(StrEnum):
        MAJOR = 'major'
        NATURAL_MINOR = 'minor'
        MELODIC_MINOR = 'melodic'
        HARMONIC_MINOR = 'harmonic'

    class Separation(StrEnum):
        OCTAVE = 'octave'
        THIRD = 'third'
        SIXTH = 'sixth'
        TENTH = 'tenth'

    class Articulation(StrEnum):
        LEGATO = 'legato'
        STACCATO = 'staccato'

    class Style(StrEnum):
        ABRSM = 'ABRSM'
        GRAND = 'grand'
        HANON = 'Hanon'
        JONAS = 'Jonas'
        COOKE = 'Cooke'

    class Motion(StrEnum):
        SIMILAR = 'similar'
        CONTRARY = 'contrary'

    def __init__(self, tonic='C', quality='major', note_duration=duration.Duration(0.25), octaves=2,
                 separated_by=Separation.OCTAVE, contrary=False, tempo=None, articulation=Articulation.LEGATO,
                 style=Style.ABRSM):

        self.separated_by = separated_by
        self.contrary = contrary
        self.style = style

        if quality == Scale.Quality.MAJOR:
            key_sig = key.Key(tonic.upper())
            self.scale = key_sig.getScale(quality)
        elif quality == Scale.Quality.NATURAL_MINOR:
            key_sig = key.Key(tonic.lower())
            self.scale = key_sig.getScale(quality)
        elif quality == Scale.Quality.MELODIC_MINOR:
            key_sig = key.Key(tonic.lower())
            self.scale = scale.MelodicMinorScale(tonic)
        elif quality == Scale.Quality.HARMONIC_MINOR:
            key_sig = key.Key(tonic.lower())
            self.scale = scale.HarmonicMinorScale(tonic)
        else:
            raise Exception('Invalid key quality passed to Scale constructor:', quality)

        super().__init__(tonic, quality, note_duration, octaves, key_sig, tempo, articulation,
                         staff='grand')

        if self.style in {Scale.Style.COOKE, Scale.Style.GRAND, Scale.Style.JONAS}:
            time_sig = meter.TimeSignature('7/4')
            time_sig.beamSequence.partition(7)
            time_sig.setDisplay(None)
        elif self.style == Scale.Style.ABRSM:
            time_sig = meter.TimeSignature('15/4')
            time_sig.setDisplay(None)
            self.duration = duration.Duration(0.5)
        else:
            time_sig = meter.TimeSignature('4/4')
        self.left_hand.insert(time_sig)
        self.right_hand.insert(time_sig)

        # Spell scale
        if self.style == Scale.Style.GRAND or self.style == Scale.Style.JONAS:
            lh_notes, rh_notes = self.spell_grand_scale()
        else:
            if self.separated_by == Scale.Separation.SIXTH:
                lh_bottom_note = self.scale.pitchFromDegree(3)
                rh_bottom_note = self.scale.pitchFromDegree(1)
                rh_bottom_note.transpose('p8', inPlace=True)
            elif self.separated_by in {Scale.Separation.THIRD, Scale.Separation.TENTH}:
                lh_bottom_note = self.scale.pitchFromDegree(1)
                rh_bottom_note = self.scale.pitchFromDegree(3)
                if self.separated_by == Scale.Separation.TENTH:
                    rh_bottom_note.transpose('p8', inPlace=True)
            else:
                lh_bottom_note = self.scale.pitchFromDegree(1)
                rh_bottom_note = self.scale.pitchFromDegree(1)
                rh_bottom_note.transpose('p8', inPlace=True)
            if rh_bottom_note >= pitch.Pitch('F4'):
                lh_bottom_note = lh_bottom_note.transpose('-p8')
                rh_bottom_note = rh_bottom_note.transpose('-p8')

            lh_top_note = deepcopy(lh_bottom_note)
            rh_top_note = deepcopy(rh_bottom_note)
            for octave in range(self.octaves):
                lh_top_note.transpose('p8', inPlace=True)
                rh_top_note.transpose('p8', inPlace=True)

            asc = scale.Direction.ASCENDING
            desc = scale.Direction.DESCENDING
            rh_notes = [note.Note(p, duration=self.duration) for p in self.scale.getPitches(rh_bottom_note, rh_top_note, asc)]
            rh_notes.extend(
                [note.Note(p, duration=self.duration) for p in self.scale.getPitches(rh_bottom_note, rh_top_note, desc)][1:])
            rh_notes[-1].duration = duration.Duration(1)

            if not self.contrary:
                if self.separated_by == Scale.Separation.OCTAVE:
                    lh_notes = [deepcopy(n).transpose('-p8') for n in rh_notes]
                else:
                    lh_notes = [note.Note(p, duration=self.duration) for p in
                                self.scale.getPitches(lh_bottom_note, lh_top_note, asc)]
                    lh_notes.extend(
                        [note.Note(p, duration=self.duration) for p in
                         self.scale.getPitches(lh_bottom_note, lh_top_note, desc)][1:])
                    lh_notes[-1].duration = duration.Duration(1)

            else:  # Contrary motion
                lh_top = lh_bottom_note
                lh_bottom = deepcopy(lh_bottom_note)
                for octave in range(self.octaves):
                    lh_bottom.transpose('-p8', inPlace=True)
                lh_notes = [note.Note(p, duration=self.duration) for p in self.scale.getPitches(lh_bottom, lh_top, desc)]
                lh_notes.extend(
                    [note.Note(p, duration=self.duration) for p in self.scale.getPitches(lh_bottom, lh_top, asc)][1:])
                lh_notes[-1].duration = duration.Duration(1)

        if self.articulation == Scale.Articulation.STACCATO:
            for n in lh_notes:
                n.articulations.append(articulations.Staccato())
            for n in rh_notes:
                n.articulations.append(articulations.Staccato())

        self.right_hand.append(rh_notes)
        self.left_hand.append(lh_notes)

    def spell_grand_scale(self):
        bottom_note = self.scale.pitchFromDegree(1)
        # for octave in range(1):
        #     bottom_note.transpose('-p8', inPlace=True)
        if bottom_note >= pitch.Pitch('F2'):
            bottom_note = bottom_note.transpose('-p8')

        top_note = deepcopy(bottom_note)
        for octave in range(4):
            top_note.transpose('p8', inPlace=True)

        middle_note = deepcopy(bottom_note)
        for octave in range(2):
            middle_note.transpose('p8', inPlace=True)

        print('Bottom note:', bottom_note)
        print('Middle note:', middle_note)
        print('Top note:', top_note)

        asc = scale.Direction.ASCENDING
        desc = scale.Direction.DESCENDING

        # Spell RH
        rh_notes = [note.Note(p, duration=self.duration) for p in self.scale.getPitches(bottom_note, top_note, asc)]
        rh_notes.extend(
            [note.Note(p, duration=self.duration) for p in self.scale.getPitches(middle_note, top_note, desc)][1:])
        rh_notes.extend(
            [note.Note(p, duration=self.duration) for p in self.scale.getPitches(middle_note, top_note, asc)][1:])
        rh_notes.extend(
            [note.Note(p, duration=self.duration) for p in self.scale.getPitches(bottom_note, top_note, desc)][1:])

        # Spell LH
        lh_notes = [note.Note(p, duration=self.duration) for p in self.scale.getPitches(bottom_note, middle_note, asc)]
        lh_notes.extend(
            [note.Note(p, duration=self.duration) for p in self.scale.getPitches(bottom_note, middle_note, desc)[1:]])
        lh_notes.extend(
            [note.Note(p, duration=self.duration) for p in self.scale.getPitches(bottom_note, top_note, asc)][1:])
        lh_notes.extend(
            [note.Note(p, duration=self.duration) for p in self.scale.getPitches(bottom_note, top_note, desc)[1:]])

        if self.style == Scale.Style.JONAS:
            # End with the complete 4 octave scale
            four_oct = [note.Note(p, duration=self.duration) for p in
                        self.scale.getPitches(bottom_note, top_note, asc)[1:]] + \
                       [note.Note(p, duration=self.duration) for p in
                        self.scale.getPitches(bottom_note, top_note, desc)[1:]]
            lh_notes.extend(four_oct)
            rh_notes.extend(four_oct)

        lh_notes = [n.transpose('-p8') for n in lh_notes]
        rh_notes[-1].duration = duration.Duration(1)
        lh_notes[-1].duration = duration.Duration(1)

        return lh_notes, rh_notes

    def apply_fingering(self, detail='full'):
        fingering = ScaleFingering(self, detail=detail)
        fingering.apply()

    def get_ABRSM_level(self) -> int:
        # Source: ABRSM 2023-2024 piano syllabus grade 8
        rubric = {
            8: 352,
            7: 320,
            6: 288,
            5: 240,
            4: 200,
            3: 160,
            2: 132,
            1: 120
        }
        return self.get_ABRSM_level_from_rubric(rubric)

    def get_tags(self):
        tags = super().get_tags()

        tags.add('Scale')

        if self.separated_by != self.Separation.OCTAVE:
            tags.add(f'At the {self.separated_by}')

        if self.style:
            tags.add(self.style)

        if self.style in [Scale.Style.JONAS, Scale.Style.GRAND]:
            tags.add('Grand scale')
            tags.add('Contrary motion')
        elif self.contrary:
            tags.add('Contrary motion')

        level = self.get_ABRSM_level()
        if level > 0:
            tags.add(f'ABRSM level {level}')

        return tags

    def get_url(self):
        params = {
            'style': self.style,
        }
        return f'/practice/scales'

    def get_name(self) -> str:
        quality_name = {
            Scale.Quality.MAJOR: 'Major',
            Scale.Quality.MELODIC_MINOR: 'melodic minor',
            Scale.Quality.HARMONIC_MINOR: 'harmonic minor',
            Scale.Quality.NATURAL_MINOR: 'natural minor'
        }
        scale_name = f'{self.style} scale in {self.tonic} {quality_name[self.quality]}'
        if self.contrary:
            scale_name += ', contrary motion'
        if self.separated_by != Scale.Separation.OCTAVE:
            scale_name += f', separated by a {self.separated_by}'

        return scale_name

    def render(self, tags=None):
        quantize = 1
        if self.style == Scale.Style.ABRSM:
            quantize = 2
            self.beam_in_groups(4)
        elif self.style == Scale.Style.COOKE:
            self.beam_in_groups(4, duration='sixteenth')

        self.apply_fingering()
        self.insert_courtesy_clefs(quantize=quantize)
        return super().render(self.get_tags())


class Arpeggio(Exercise):
    
    class Quality(StrEnum):
        MAJOR = 'major'
        MINOR = 'minor'
        DOMINANT = 'dominant'
        DIMINISHED = 'diminished'

    class Inversion(Enum):
        ROOT = 0
        FIRST = 1
        SECOND = 2
        THIRD = 3

    class Style(StrEnum):
        ABRSM = 'ABRSM'
        HANON = 'Hanon'
        JONAS = 'Jonas'
        RACH = 'Rach'

    def __init__(self, tonic='C', quality=Quality.MAJOR, note_duration=duration.Duration(0.5), octaves=2, inversion=0,
                 tempo=None, articulation=None, style=Style.ABRSM, level=None):

        self.inversion = inversion
        self.style = style

        if style == Arpeggio.Style.ABRSM and level is not None:
            if level == 8:
                tempo = tempo.MetronomeMark(number=66, referent=duration.Duration(2))
            elif level == 7:
                tempo = tempo.MetronomeMark(number=56, referent=duration.Duration(2))
            elif level == 6:
                tempo = tempo.MetronomeMark(number=50, referent=duration.Duration(2))
            elif level == 5:
                tempo = tempo.MetronomeMark(number=44, referent=duration.Duration(2))
            elif level == 4:
                tempo = tempo.MetronomeMark(number=80, referent=duration.Duration(1))
            elif level == 3:
                tempo = tempo.MetronomeMark(number=72, referent=duration.Duration(1))
            elif level == 2:
                tempo = tempo.MetronomeMark(number=63, referent=duration.Duration(1))
            elif level == 1:
                tempo = tempo.MetronomeMark(number=58, referent=duration.Duration(1))
            elif level == 0:
                tempo = tempo.MetronomeMark(number=52, referent=duration.Duration(1))
            else:
                raise Exception('Invalid level passed to Arpeggio:', level)

            if level >= 6:
                octaves = 4
            elif level >= 2:
                octaves = 2
            else:
                octaves = 1

        if quality == Arpeggio.Quality.MAJOR:
            key_sig = key.Key(tonic.upper(), mode='major')
        elif quality == Arpeggio.Quality.MINOR:
            key_sig = key.Key(tonic.lower(), mode='minor')
        elif quality == Arpeggio.Quality.DOMINANT:
            key_sig = key.Key(
                key.sharpsToPitch(key.Key(tonic.upper(), mode='major').sharps - 1))  # dominant of the base key
        elif quality == Arpeggio.Quality.DIMINISHED:
            key_sig = None
        else:
            raise ('Invalid key quality passed to Arpeggio constructor:', quality)

        super().__init__(tonic, quality, note_duration, octaves, key_sig, tempo, articulation, staff='grand')

        if quality in [Arpeggio.Quality.MAJOR, Arpeggio.Quality.MINOR]:
            time_sig = meter.TimeSignature('7/4')
        else:
            # Four-note broken chords, more space needed
            time_sig = meter.TimeSignature('9/4')
        time_sig.setDisplay(None)
        self.left_hand.insert(time_sig)
        self.right_hand.insert(time_sig)

        if self.quality == Arpeggio.Quality.MAJOR:
            root = self.key.pitchFromDegree(1)
            notes = [root, root.transpose('M3'), root.transpose('p5')]
        elif self.quality == Arpeggio.Quality.MINOR:
            root = self.key.pitchFromDegree(1)
            notes = [root, root.transpose('m3'), root.transpose('p5')]
        elif self.quality == Arpeggio.Quality.DOMINANT:
            root = self.key.pitchFromDegree(5)
            root.octave = 4
            notes = [root, root.transpose('M3'), root.transpose('p5'), root.transpose('m7')]
        else:
            # Diminished
            root = pitch.Pitch(self.tonic, octave=4)
            notes = [root, root.transpose('m3'), root.transpose('a4'), root.transpose('m6')]

        c = chord.Chord(notes)
        c = c.sortAscending()

        if c[0].pitch >= pitch.Pitch('F4'):
            print('Transposing down...')
            c.transpose('-p8', inPlace=True)

        if self.octaves >= 3:
            for octave in range(self.octaves - 2):
                c.transpose('-p8', inPlace=True)
        if self.inversion != 0:
            c.inversion(self.inversion)

        c = c.sortAscending()

        rh_notes = []

        top_note = deepcopy(c[0])
        top_note.duration = self.duration

        for octave in range(self.octaves):
            top_note = top_note.transpose('p8')

        for octave in range(self.octaves):
            new_notes = [note.Note(p, duration=self.duration) for p in c.pitches]
            c = c.transpose('p8')
            rh_notes.extend(new_notes)

        rh_notes_descending = deepcopy(rh_notes[::-1])
        rh_notes.append(top_note)
        rh_notes.extend(rh_notes_descending)

        if self.quality == Arpeggio.Quality.DOMINANT and self.style == Arpeggio.Style.ABRSM:
            # ABRSM 2022-2023 dominant arpeggios resolve on the tonic
            rh_notes[-1] = rh_notes[-2].transpose('m2')
        rh_notes[-1].duration = duration.Duration(1)  # End with quarter note

        lh_notes = [deepcopy(n).transpose(self.separated_by) for n in rh_notes]

        self.right_hand.append(rh_notes)
        self.left_hand.append(lh_notes)

    def get_ABRSM_level(self) -> int:
        npm = self.get_notes_per_minute()
        # Source: ABRSM 2023-2024 piano syllabus grade 8
        rubric = {
            8: 264,
            7: 224,
            6: 200,
            5: 176,
            4: 160,
            3: 144,
            2: 126,
            1: 106
        }
        return self.get_ABRSM_level_from_rubric(rubric)
    
    def get_tags(self):
        tags = super().get_tags()

        tags.add('Arpeggio')

        if self.style:
            tags.add(self.style)

        if self.quality in [Arpeggio.Quality.DOMINANT, Arpeggio.Quality.DIMINISHED]:
            tags.add(self.quality)

        level = self.get_ABRSM_level()
        if level > 0:
            tags.add(f'Level {level}')

        return tags
    
    def get_name(self):
        inversion_name = {
            1: '1st',
            2: '2nd',
            3: '3rd'
        }
        arpeggio_name = f'{self.style} scale in {self.tonic} {self.quality}'
        if self.inversion != 0:
            arpeggio_name += f', {inversion_name[self.inversion]} inversion'

        return arpeggio_name

    def render(self):
        if self.tonic in ['A', 'Ab']:
            asc_threshold = pitch.Pitch('F4')
        else:
            asc_threshold = pitch.Pitch('G4')
        self.insert_courtesy_clefs(new_clef_threshold_asc=asc_threshold, quantize=2)
        self.beam_in_groups(4)
        return super(Arpeggio, self).render()


class ChordExercise(Exercise):
    def __init__(self, tonic='C', quality='major', note_duration=duration.Duration(0.5), octaves=2, inversion=0,
                 tempo=None, articulation=None, style='simple'):
        super().__init__(tonic, quality, note_duration, octaves, tempo, articulation)
