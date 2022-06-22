import React, {useEffect, useRef, useState} from 'react'
import {Button, FormControl, FormControlLabel, InputLabel, MenuItem, Select, Switch} from '@mui/material'
import axios from 'axios'
import {WebMidi} from 'webmidi'

function ReadingRandomNote(props) {
  const [expectedNote, setExpectedNote] = useState(null)
  const [chromaticNoteNames, setChromaticNoteNames] = useState([])
  const [maxFlats, setMaxFlats] = useState(7)
  const [maxSharps, setMaxSharps] = useState(7)
  const [minNote, setMinNote] = useState('A0')
  const [maxNote, setMaxNote] = useState('C8')
  const [accidentals, setAccidentals] = useState(true)
  const expectedNoteRef = useRef(expectedNote)

  useEffect(() => {
    getExercise()
    getChromaticNotes()
  }, [])

  function getChromaticNotes() {
    const url = 'http://127.0.0.1:8000/api/chromatic/'
    axios.get(url).then(response => {
      setChromaticNoteNames(response.data.notes.reverse())
    })
  }

  function getExercise() {
    const url = 'http://127.0.0.1:8000/api/exercise/'
    axios.get(url, {
      params: {
        max_flats: maxFlats,
        max_sharps: maxSharps,
        min_note: minNote,
        max_note: maxNote,
        accidentals: accidentals
      }
    }).then(response => {
      let data = response.data
      setExpectedNote(data.note)
      expectedNoteRef.current = data.note
      props.renderScore(data.xml)
    })
  }

  function listenToMidiInput(id) {
    // Remove listener on previous device if applicable
    if (props.selectedInputDevice) {
      WebMidi.getInputById(props.selectedInputDevice).removeListener()
    }
    console.log('Listening to input on device at ID', id)
    WebMidi.getInputById(id).addListener('noteon', e => {
      const playedNote = e.note.number
      if (expectedNoteRef.current === playedNote) {
        console.log('Correct note played')
        getExercise()
      } else {
        console.log('Incorrect note played')
        console.log('Expected', expectedNoteRef.current, 'got', playedNote)
      }
    })
  }

  useEffect(() => {
    if (props.selectedInputDevice) {
      listenToMidiInput(props.selectedInputDevice.id)
    }
  }, [props.selectedInputDevice])

  return (
    <>
      <div style={{display: 'flex', justifyContent: 'center'}}>
        <Button variant="contained" sx={{m: 1}} onClick={getExercise}>New Exercise</Button>
      </div>
      <div style={{display: 'flex', justifyContent: 'center'}}>
        <FormControl sx={{m: 1, minWidth: 120}}>
          <InputLabel id="maxFlats-label">Max Flats</InputLabel>
          <Select
            labelId="maxFlats-label"
            id="maxFlats"
            value={maxFlats}
            label="Max Flats"
            onChange={(e) => setMaxFlats(e.target.value)}
          >
            <MenuItem value={0}>0</MenuItem>
            <MenuItem value={1}>1</MenuItem>
            <MenuItem value={2}>2</MenuItem>
            <MenuItem value={3}>3</MenuItem>
            <MenuItem value={4}>4</MenuItem>
            <MenuItem value={5}>5</MenuItem>
            <MenuItem value={6}>6</MenuItem>
            <MenuItem value={7}>7</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{m: 1, minWidth: 120}}>
          <InputLabel id="maxSharps-label">Max Sharps</InputLabel>
          <Select
            labelId="maxSharps-label"
            id="maxSharps"
            value={maxSharps}
            label="Max Sharps"
            onChange={(e) => setMaxSharps(e.target.value)}
          >
            <MenuItem value={0}>0</MenuItem>
            <MenuItem value={1}>1</MenuItem>
            <MenuItem value={2}>2</MenuItem>
            <MenuItem value={3}>3</MenuItem>
            <MenuItem value={4}>4</MenuItem>
            <MenuItem value={5}>5</MenuItem>
            <MenuItem value={6}>6</MenuItem>
            <MenuItem value={7}>7</MenuItem>
          </Select>
        </FormControl>
        <FormControl sx={{m: 1, minWidth: 120}}>
          <InputLabel id="minNote-label">Min Note</InputLabel>
          <Select
            labelId="minNote-label"
            id="minNote"
            value={minNote}
            label="Min Note"
            onChange={(e) => setMinNote(e.target.value)}
          >
            {
              chromaticNoteNames.map((note) =>
                <MenuItem key={note} value={note}>{note}</MenuItem>
              )
            }
          </Select>
        </FormControl>
        <FormControl sx={{m: 1, minWidth: 120}}>
          <InputLabel id="maxNote-label">Max Note</InputLabel>
          <Select
            labelId="maxNote-label"
            id="maxNote"
            value={maxNote}
            label="Max Note"
            onChange={(e) => setMaxNote(e.target.value)}
          >
            {
              chromaticNoteNames.map((note) =>
                <MenuItem key={note} value={note}>{note}</MenuItem>
              )
            }
          </Select>
        </FormControl>
        <FormControlLabel
          control={<Switch checked={accidentals} onChange={(e) => setAccidentals(e.target.checked)}/>}
          label="Accidentals"/>
      </div>
    </>
  )
}

export default ReadingRandomNote
