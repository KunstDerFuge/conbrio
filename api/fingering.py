from dataclasses import dataclass

from music21 import note, articulations


class ChordFingering:
    pass


class ScaleFingering:
    def __init__(self, scale, detail='full'):
        self.scale = scale
        self.detail = detail
        self.group = 1

    def fingering_for_scale(self):
        group = 1
        scale_name = f'{self.scale.tonic} {self.scale.quality}'
        if scale_name in ['Cb major', 'B major', 'B minor', 'F# major', 'F# minor',
                          'Gb major', 'C# major', 'C# minor', 'Db major']:
            group = 2
        elif scale_name in ['Ab major', 'Ab minor', 'Bb major', 'Bb minor', 'D# minor', 'Eb major', 'Eb minor',
                            'G# minor', 'A# minor', 'F major', 'F minor']:
            group = 3

    def fingering_for_note(self, _note: note.Note, hand: str, last_note: note.Note or None,
                           last_finger: int) -> int or None:
        degree = self.scale.key.getScaleDegreeFromPitch(_note.pitch)

        if hand == 'left':
            top_note = max(self.scale.left_hand.notes)
            bottom_note = min(self.scale.left_hand.notes)
        else:
            top_note = max(self.scale.right_hand.notes)
            bottom_note = min(self.scale.right_hand.notes)

        ascending = True
        if last_note is None:
            if hand == 'left' and self.scale.contrary:
                ascending = False
        else:
            if _note < last_note or _note == top_note:
                ascending = False

        # return self.fingering[self.scale.tonic][self.scale.quality][degree]
        return "345"

    def apply_fingering_for_hand(self, notes, hand: str):
        last_note = None
        last_finger = None
        for n in notes:
            finger = self.fingering_for_note(n, hand, last_note, last_finger)
            last_finger = finger
            last_note = n
            if finger:
                n.articulations.append(articulations.Fingering(finger))

    def apply(self):
        if not self.scale.left_hand:
            raise 'Cannot apply fingering without separate hand information.'

        for hand, notes in zip(('left', 'right'), (self.scale.left_hand.notes, self.scale.right_hand.notes)):
            self.apply_fingering_for_hand(notes, hand)
