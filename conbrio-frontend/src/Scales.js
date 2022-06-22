import React, {useEffect, useState} from 'react'
import {FormControl, InputLabel, MenuItem, Select} from '@mui/material'
import axios from 'axios'

function Scales(props) {
  const [tonic, setTonic] = useState('C')
  const [quality, setQuality] = useState('minor')


  useEffect(() => {
    function getScale() {
      const url = 'http://127.0.0.1:8000/api/scale/'
      axios.get(url, {
        params: {
          tonic: tonic,
          quality: quality
        }
      }).then(response => {
        let data = response.data
        console.log(data)
        props.renderScore(data.xml)
      })
    }

    console.log('Rendering', tonic, quality, 'scale...')
    getScale()
  }, [tonic, quality])

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
    </div>
  )
}

export default Scales
