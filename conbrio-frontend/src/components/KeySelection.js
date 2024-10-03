import {FormControl, InputLabel, MenuItem, Select} from "@mui/material";
import React from "react";

export default function KeySelection(props) {
  const scaleOptions = [
    {value: 'major', name: 'Major'},
    {value: 'minor', name: 'Natural Minor'},
    {value: 'melodic', name: 'Melodic Minor'},
    {value: 'harmonic', name: 'Harmonic Minor'},
  ]
  const chordOptions = [
    {value: 'major', name: 'Major'},
    {value: 'minor', name: 'Minor'},
    {value: 'dominant', name: 'Dominant'},
  ]

  return (
    <>
      <FormControl sx={{m: 1, minWidth: 120}}>
        <InputLabel id="tonic-label">Key</InputLabel>
        <Select
          labelId="tonic-label"
          id="tonic"
          value={props.tonic}
          label="Key"
          onChange={(e) => props.setTonic(e.target.value)}
        >
          <MenuItem value={'C'}>C</MenuItem>
          <MenuItem value={'Cs'}>C♯</MenuItem>
          <MenuItem value={'Db'}>D♭</MenuItem>
          <MenuItem value={'D'}>D</MenuItem>
          <MenuItem value={'Eb'}>E♭</MenuItem>
          <MenuItem value={'E'}>E</MenuItem>
          <MenuItem value={'F'}>F</MenuItem>
          <MenuItem value={'Fs'}>F♯</MenuItem>
          <MenuItem value={'Gb'}>G♭</MenuItem>
          <MenuItem value={'G'}>G</MenuItem>
          <MenuItem value={'Gs'}>G♯</MenuItem>
          <MenuItem value={'Ab'}>A♭</MenuItem>
          <MenuItem value={'A'}>A</MenuItem>
          <MenuItem value={'Bb'}>B♭</MenuItem>
          <MenuItem value={'B'}>B</MenuItem>
        </Select>
      </FormControl>
      <FormControl sx={{m: 1, minWidth: 120}}>
        <InputLabel id="quality-label">Quality</InputLabel>
        <Select
          labelId="quality-label"
          id="quality"
          value={props.quality}
          label="Quality"
          onChange={(e) => props.setQuality(e.target.value)}
        >
          {
            props.exercise === 'scales' ?
              scaleOptions.map((option) =>
                <MenuItem key={option.value} value={option.value}>{option.name}</MenuItem>
              )
              :
              chordOptions.map((option) =>
                <MenuItem key={option.value} value={option.value}>{option.name}</MenuItem>
              )
          }
        </Select>
      </FormControl>
    </>
  )
}