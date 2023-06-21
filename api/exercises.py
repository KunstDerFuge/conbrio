from copy import deepcopy

from music21 import key, scale, meter, duration, pitch, note, clef, musicxml, interval, chord, stream, articulations

from api.fingering import ScaleFingering
from api.utilities import create_grand_staff


class Exercise:
    def __init__(self, tonic='C', quality='major', note_duration=duration.Duration(0.25), octaves=2,
                 separated_by=interval.Interval('-p8'), key_sig=None, tempo=None, articulation=None, staff='grand'):
        self.tonic = tonic
        self.quality = quality
        self.duration = note_duration
        self.octaves = octaves
        self.separated_by = separated_by
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

    def insert_courtesy_clefs(self, new_clef_threshold_asc=pitch.Pitch('F#4'),
                              new_clef_threshold_desc=pitch.Pitch('Bb3'), quantize=1):
        """
        Create courtesy clefs, usually for left hand part.

        Parameters:
            new_clef_threshold_asc (pitch.Pitch): The note above which we will insert a treble clef.
            new_clef_threshold_desc (pitch.Pitch): The note below which we will insert a bass clef.
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
                break

    def render(self):
        if self.staff == 'grand':
            for part in self.left_hand, self.right_hand:
                part.makeNotation(inPlace=True)  # makes measures
        else:
            self.s.makeNotation(inPlace=True)

        parser = musicxml.m21ToXml.GeneralObjectExporter(self.s)
        print('Done generating scale!')
        return parser.parse().decode('utf-8')


class Scale(Exercise):
    def __init__(self, tonic='C', quality='major', note_duration=duration.Duration(0.25), octaves=2,
                 separated_by=interval.Interval('-p8'), contrary=False, tempo=None, articulation=None,
                 style='ABRSM'):

        self.contrary = contrary
        self.style = style

        if quality == 'major':
            key_sig = key.Key(tonic.upper())
            self.scale = key_sig.getScale('major')
        elif quality == 'minor':
            key_sig = key.Key(tonic.lower())
            self.scale = key_sig.getScale('minor')
        elif quality == 'melodic':
            key_sig = key.Key(tonic.lower())
            self.scale = scale.MelodicMinorScale(tonic)
        elif quality == 'harmonic':
            key_sig = key.Key(tonic.lower())
            self.scale = scale.HarmonicMinorScale(tonic)
        else:
            raise ('Invalid key quality passed to Scale constructor:', quality)

        super().__init__(tonic, quality, note_duration, octaves, separated_by, key_sig, tempo, articulation,
                         staff='grand')

        if self.style == 'Cooke':
            time_sig = meter.TimeSignature('7/4')
            time_sig.beamSequence.partition(7)
            time_sig.setDisplay(None)
        elif self.style == 'ABRSM':
            time_sig = meter.TimeSignature('15/4')
            time_sig.setDisplay(None)
            self.duration = duration.Duration(0.5)
        else:
            time_sig = meter.TimeSignature('4/4')
        self.left_hand.insert(time_sig)
        self.right_hand.insert(time_sig)

        # Spell scale
        bottom_note = self.scale.pitchFromDegree(1)
        if bottom_note >= pitch.Pitch('F4'):
            bottom_note = bottom_note.transpose('-p8')

        top_note = deepcopy(bottom_note)
        for octave in range(self.octaves):
            top_note.transpose('p8', inPlace=True)

        asc = scale.Direction.ASCENDING
        desc = scale.Direction.DESCENDING
        rh_notes = [note.Note(p, duration=self.duration) for p in self.scale.getPitches(bottom_note, top_note, asc)]
        rh_notes.extend(
            [note.Note(p, duration=self.duration) for p in self.scale.getPitches(bottom_note, top_note, desc)][1:])
        rh_notes[-1].duration = duration.Duration(1)

        if not self.contrary:
            lh_notes = [deepcopy(n).transpose(self.separated_by) for n in rh_notes]
        else:
            lh_top = bottom_note
            lh_bottom = deepcopy(bottom_note)
            for octave in range(self.octaves):
                lh_bottom.transpose('-p8', inPlace=True)
            lh_notes = [note.Note(p, duration=self.duration) for p in self.scale.getPitches(lh_bottom, lh_top, desc)]
            lh_notes.extend(
                [note.Note(p, duration=self.duration) for p in self.scale.getPitches(lh_bottom, lh_top, asc)][1:])
            lh_notes[-1].duration = duration.Duration(1)

        if self.articulation:
            for n in lh_notes:
                n.articulations.append(self.articulation)
            for n in rh_notes:
                n.articulations.append(self.articulation)

        self.right_hand.append(rh_notes)
        self.left_hand.append(lh_notes)

    def apply_fingering(self, detail='full'):
        fingering = ScaleFingering(self, detail=detail)
        fingering.apply()

    def render(self):
        quantize = 1
        if self.style == 'ABRSM':
            quantize = 2
            self.beam_in_groups(4)
        elif self.style == 'Cooke':
            self.beam_in_groups(4, duration='sixteenth')

        self.apply_fingering()
        self.insert_courtesy_clefs(quantize=quantize)
        return super().render()


class Arpeggio(Exercise):
    def __init__(self, tonic='C', quality='major', note_duration=duration.Duration(0.5), octaves=2,
                 separated_by=interval.Interval('-p8'), inversion=0, tempo=None, articulation=None,
                 style='ABRSM'):

        self.inversion = inversion
        self.style = style

        if quality == 'major':
            key_sig = key.Key(tonic.upper(), mode='major')
        elif quality == 'minor':
            key_sig = key.Key(tonic.lower(), mode='minor')
        elif quality == 'dominant':
            key_sig = key.Key(
                key.sharpsToPitch(key.Key(tonic.upper(), mode='major').sharps - 1))  # dominant of the base key
        elif quality == 'diminished':
            key_sig = None
        else:
            raise ('Invalid key quality passed to Arpeggio constructor:', quality)

        super().__init__(tonic, quality, note_duration, octaves, separated_by, key_sig, tempo, articulation,
                         staff='grand')

        if quality in ['major', 'minor']:
            time_sig = meter.TimeSignature('7/4')
        else:
            # Four-note broken chords, more space needed
            time_sig = meter.TimeSignature('9/4')
        time_sig.setDisplay(None)
        self.left_hand.insert(time_sig)
        self.right_hand.insert(time_sig)

        if self.quality == 'major':
            root = self.key.pitchFromDegree(1)
            notes = [root, root.transpose('M3'), root.transpose('p5')]
        elif self.quality == 'minor':
            root = self.key.pitchFromDegree(1)
            notes = [root, root.transpose('m3'), root.transpose('p5')]
        elif self.quality == 'dominant':
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

        if self.quality == 'dominant' and self.style == 'ABRSM':
            # ABRSM 2022-2023 dominant arpeggios resolve on the tonic
            rh_notes[-1] = rh_notes[-2].transpose('m2')
        rh_notes[-1].duration = duration.Duration(1)  # End with quarter note

        lh_notes = [deepcopy(n).transpose(self.separated_by) for n in rh_notes]

        self.right_hand.append(rh_notes)
        self.left_hand.append(lh_notes)

    def render(self):
        if self.tonic in ['A', 'Ab']:
            asc_threshold = pitch.Pitch('F4')
        else:
            asc_threshold = pitch.Pitch('G4')
        self.insert_courtesy_clefs(new_clef_threshold_asc=asc_threshold, quantize=2)
        self.beam_in_groups(4)
        return super(Arpeggio, self).render()
