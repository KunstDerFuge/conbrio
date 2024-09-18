import React, {useEffect, useState} from 'react'
import {FormControl, InputLabel, MenuItem, Select} from '@mui/material'
import axios from 'axios'

const Scales = (props) => {
  const [tonic, setTonic] = useState('C')
  const [quality, setQuality] = useState('minor')
  const [style, setStyle] = useState('ABRSM')
  const [octaves, setOctaves] = useState(2)
  const [separation, setSeparation] = useState('octave')


  useEffect(() => {
    function getScale() {
      const url = 'http://127.0.0.1:8000/api/scale/'
      axios.get(url, {
        params: {
          tonic: tonic,
          quality: quality,
          style: style,
          octaves: octaves,
          separation: separation,
        }
      }).then(response => {
        let data = response.data
        console.log(data)
        props.renderScore(data.xml)
      })
    }

    console.log('Rendering', tonic, quality, 'scale...')
    getScale()
  }, [tonic, quality, style, octaves, separation])

  return (
    <div style={{display: 'flex', justifyContent: 'center'}}>
      <FormControl sx={{m: 1, minWidth: 120}}>
        <InputLabel id="tonic-label">Key</InputLabel>
        <Select
          labelId="tonic-label"
          id="tonic"
          value={tonic}
          label="Key"
          onChange={(e) => setTonic(e.target.value)}
        >
          <MenuItem value={'C'}>C</MenuItem>
          <MenuItem value={'C#'}>C♯</MenuItem>
          <MenuItem value={'Db'}>D♭</MenuItem>
          <MenuItem value={'D'}>D</MenuItem>
          <MenuItem value={'Eb'}>E♭</MenuItem>
          <MenuItem value={'E'}>E</MenuItem>
          <MenuItem value={'F'}>F</MenuItem>
          <MenuItem value={'F#'}>F♯</MenuItem>
          <MenuItem value={'G'}>G</MenuItem>
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
          value={quality}
          label="Quality"
          onChange={(e) => setQuality(e.target.value)}
        >
          <MenuItem value={'major'}>Major</MenuItem>
          <MenuItem value={'minor'}>Natural Minor</MenuItem>
          <MenuItem value={'melodic'}>Melodic Minor</MenuItem>
          <MenuItem value={'harmonic'}>Harmonic Minor</MenuItem>
        </Select>
      </FormControl>
      <FormControl sx={{m: 1, minWidth: 120}}>
        <InputLabel id="quality-label">Style</InputLabel>
        <Select
          labelId="style-label"
          id="style"
          value={style}
          label="Style"
          onChange={(e) => setStyle(e.target.value)}
        >
          <MenuItem value={'ABRSM'}>ABRSM</MenuItem>
          <MenuItem value={'grand'}>Grand</MenuItem>
          <MenuItem value={'Hanon'}>Hanon</MenuItem>
          <MenuItem value={'Jonas'}>Alberto Jonas</MenuItem>
          <MenuItem value={'Cooke'}>Cooke</MenuItem>
        </Select>
      </FormControl>
      {
        style !== 'grand' && style !== 'Jonas' &&
        <FormControl sx={{m: 1, minWidth: 120}}>
          <InputLabel id="octaves-label">Octaves</InputLabel>
          <Select
            labelId="octaves-label"
            id="octaves"
            value={octaves}
            label="Octaves"
            onChange={(e) => setOctaves(e.target.value)}
          >
            <MenuItem value={1}>1</MenuItem>
            <MenuItem value={2}>2</MenuItem>
            <MenuItem value={3}>3</MenuItem>
            <MenuItem value={4}>4</MenuItem>
          </Select>
        </FormControl>
      }
      <FormControl sx={{m: 1, minWidth: 120}}>
        <InputLabel id="separation-label">Separated by</InputLabel>
        <Select
          labelId="separation-label"
          id="separation"
          value={separation}
          label="Separated by"
          onChange={(e) => setSeparation(e.target.value)}
        >
          <MenuItem value={'octave'}>Octave</MenuItem>
          <MenuItem value={'third'}>Third</MenuItem>
          <MenuItem value={'tenth'}>Tenth</MenuItem>
          <MenuItem value={'sixth'}>Sixth</MenuItem>
        </Select>
      </FormControl>
    </div>
  )
}

export default Scales
