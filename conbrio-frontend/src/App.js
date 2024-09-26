import React, {useEffect, useState} from 'react'
import Module from 'verovio/wasm/verovio-toolkit-wasm-hum.js'
import {VerovioToolkit} from 'verovio'
import {WebMidi} from 'webmidi'
import {FormControl, InputLabel, MenuItem, Select} from '@mui/material'
import ExerciseMenu from './components/ExerciseMenu'
import PDFReader from "./components/PDFReader";
import {Document, Page} from "@react-pdf/renderer";

function App() {
  const [score, setScore] = useState('')
  const [pdfData, setPdfData] = useState('')
  const [toolkit, setToolkit] = useState(null)
  const [midiDevices, setMidiDevices] = useState([])
  const [midiOutputDevices, setMidiOutputDevices] = useState([])
  const [selectedInputDevice, setSelectedInputDevice] = useState('')
  const [selectedOutputDevice, setSelectedOutputDevice] = useState('')
  const [loading, setLoading] = useState(true)
  const [exercise, setExercise] = useState('scales')

  function renderScore(scoreData, isPdf = false) {
    if (isPdf) {
      console.log('Received PDF data...')
      setPdfData(scoreData)
    } else {
      toolkit.loadData(scoreData)
      setScore(toolkit.renderToSVG(1, {}))
    }
  }

  function onWebMidiEnabled() {
    console.log(WebMidi.inputs)
    console.log(WebMidi.outputs)
    WebMidi.inputs.forEach(input => console.log(input.manufacturer, input.name))
    setMidiDevices(WebMidi.inputs)
    setMidiOutputDevices(WebMidi.outputs)
  }

  useEffect(() => {
    Module().then((VerovioModule) => {
      const verovioToolkit = new VerovioToolkit(VerovioModule)
      setToolkit(verovioToolkit)
      verovioToolkit.setOptions({
        scale: 50,
        font: 'Leipzig',
        staffLineWidth: 0.2,
        stemWidth: 0.3,
        fingeringScale: 0.6,
        header: 'none',
        footer: 'none',
        landscape: false,
        adjustPageHeight: true,
        adjustPageWidth: true,
        breaks: 'encoded',
      })
      console.log(verovioToolkit.getVersion())
      console.log(verovioToolkit.getOptions())
      !WebMidi.isEnabled &&
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
    setLoading(false)
  }, [toolkit])

  return (
    <div>
      {!loading &&
        <>
          <div style={{display: 'flex', justifyContent: 'center'}}>
            <div>
              <Select
                variant='standard'
                labelId="exercise-label"
                id="exercise"
                value={exercise}
                label="Exercise"
                onChange={(e) => setExercise(e.target.value)}
              >
                <MenuItem value={'scales'}>Scales</MenuItem>
                <MenuItem value={'arpeggios'}>Arpeggios</MenuItem>
                <MenuItem value={'chords'}>Chords</MenuItem>
              </Select>
            </div>
            <br/>
            <div dangerouslySetInnerHTML={{__html: score}}></div>
            {/*<PDFReader pdf={pdfData} />*/}
          </div>
          {/*<ReadingRandomNote renderScore={renderScore} selectedInputDevice={selectedInputDevice} />*/}
          {
            <ExerciseMenu renderScore={renderScore}/>
          }
          <div style={{display: 'flex', justifyContent: 'center'}}>
            <FormControl sx={{m: 1, minWidth: 220}}>
              <InputLabel id="midiDevice-label">Midi Input Device</InputLabel>
              <Select
                labelId="midiDevice-label"
                id="midiDevice"
                value={selectedInputDevice}
                label="Midi Input Device"
                onChange={(e) => {
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
