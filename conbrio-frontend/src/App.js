import React, {useEffect, useRef, useState} from 'react'
import Module from 'verovio/wasm/verovio-toolkit-wasm-hum.js'
import {VerovioToolkit} from 'verovio'
import {Button, FormControl, FormControlLabel, InputLabel, MenuItem, Select, Switch} from '@mui/material'
import axios from 'axios'
import {WebMidi} from 'webmidi'

function App() {
  const [expectedNote, setExpectedNote] = useState(null)
  const [score, setScore] = useState(null)
  const [toolkit, setToolkit] = useState(null)
  const [chromaticNoteNames, setChromaticNoteNames] = useState([])
  const [maxFlats, setMaxFlats] = useState(7)
  const [maxSharps, setMaxSharps] = useState(7)
  const [minNote, setMinNote] = useState('A0')
  const [maxNote, setMaxNote] = useState('C8')
  const [accidentals, setAccidentals] = useState(true)
  const [midiDevices, setMidiDevices] = useState([])
  const [midiOutputDevices, setMidiOutputDevices] = useState([])
  const [selectedInputDevice, setSelectedInputDevice] = useState('')
  const [selectedOutputDevice, setSelectedOutputDevice] = useState('')
  const [loading, setLoading] = useState(true)
  const expectedNoteRef = useRef(expectedNote)

  function onWebMidiEnabled() {
    console.log(WebMidi.inputs)
    console.log(WebMidi.outputs)
    WebMidi.inputs.forEach(input => console.log(input.manufacturer, input.name))
    setMidiDevices(WebMidi.inputs)
    setMidiOutputDevices(WebMidi.outputs)
  }

  function listenToMidiInput(id) {
    // Remove listener on previous device if applicable
    if (selectedInputDevice) {
      WebMidi.getInputById(selectedInputDevice).removeListener()
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

  function getChromaticNotes() {
    const url = 'http://127.0.0.1:8000/api/chromatic/'
    axios.get(url).then(response => {
      setChromaticNoteNames(response.data.notes.reverse())
      setLoading(false)
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
      toolkit.loadData(data.xml)
      setScore(toolkit.renderToSVG(1, {}))
    })
  }

  useEffect(() => {
    Module().then((VerovioModule) => {
      const verovioToolkit = new VerovioToolkit(VerovioModule)
      setToolkit(verovioToolkit)
      verovioToolkit.setOptions({
        scale: 60,
        font: 'Leipzig',
        staffLineWidth: 0.2,
        stemWidth: 0.3,
        fingeringScale: 0.6,
        header: 'none',
        footer: 'none',
        adjustPageHeight: true,
        adjustPageWidth: true,
      })
      console.log(verovioToolkit.getVersion())
      console.log(verovioToolkit.getOptions())
      WebMidi.enable()
        .then(() => {
          console.log('WebMidi enabled!')
          onWebMidiEnabled()
        })
        .catch((e) => console.log('Error enabling WebMidi:', e))
    })
  }, [])

  useEffect(() => {
    if (!toolkit) return
    getChromaticNotes()
    getExercise()
  }, [toolkit])

  return (
    <div>
      {!loading &&
        <>
          <div style={{display: 'flex', justifyContent: 'center'}}>
            <div dangerouslySetInnerHTML={{__html: score}}></div>
          </div>
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
          <div style={{display: 'flex', justifyContent: 'center'}}>
            <FormControl sx={{m: 1, minWidth: 220}}>
              <InputLabel id="midiDevice-label">Midi Input Device</InputLabel>
              <Select
                labelId="midiDevice-label"
                id="midiDevice"
                value={selectedInputDevice}
                label="Midi Input Device"
                onChange={(e) => {
                  listenToMidiInput(e.target.value)
                  setSelectedInputDevice(e.target.value)
                }}
              >
                {
                  midiDevices.map((device) =>
                    <MenuItem key={device.id} value={device.id}>{device.name}</MenuItem>
                  )
                }
              </Select>
            </FormControl>
            <FormControl sx={{m: 1, minWidth: 220}}>
              <InputLabel id="outputDevice-label">Midi Output Device</InputLabel>
              <Select
                labelId="outputDevice-label"
                id="outputDevice"
                value={selectedOutputDevice}
                label="Midi Output Device"
                onChange={(e) => {
                  setSelectedOutputDevice(e.target.value)
                }}
              >
                {
                  midiOutputDevices.map((device) =>
                    <MenuItem key={device.id} value={device.id}>{device.name}</MenuItem>
                  )
                }
              </Select>
            </FormControl>
          </div>
        </>
      }
    </div>
  )
}

export default App