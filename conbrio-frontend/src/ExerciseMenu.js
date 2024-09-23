import React, {useEffect, useState} from 'react'
import {FormControl, InputLabel, Link, MenuItem, Select} from '@mui/material'
import axios from 'axios'
import {useParams, useSearchParams} from "react-router-dom";

const Scales = (props) => {

  const defaultParams = {
    key: 'C-minor',
    style: 'ABRSM',
    octaves: 2
  }

  const [searchParams, setSearchParams] = useSearchParams(defaultParams)
  const [tonic, setTonic] = useState(getTonic(searchParams.get('key')))
  const [quality, setQuality] = useState(getQuality(searchParams.get('key')))
  const [style, setStyle] = useState(searchParams.get('style'))
  const [octaves, setOctaves] = useState(searchParams.get('octaves'))
  const [separation, setSeparation] = useState(searchParams.get('separation'))
  const [next_exercise, setNextExercise] = useState({})
  const params = useParams()

  function getTonic(key) {
    console.log('Got ', key)
    return key.split('-')[0].replace('#', 's')
  }

  function getQuality(key) {
    return key.split('-')[1] || 'major'
  }

  useEffect(() => {
    setSearchParams({
      key: tonic + '-' + quality,
      style: style,
      octaves: octaves,
      separation: separation
    })

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
        if (data.next_name) {
          setNextExercise({
            'name': data.next_name,
            'url': data.next_url,
          })
        }
      })
    }

    console.log('Rendering', tonic, quality, 'scale...')
    getScale()
  }, [tonic, quality, style, octaves, separation])

  return (
    <>
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
      <div>
        Next: <Link href={next_exercise.url}>{next_exercise.name}</Link> →
      </div>
    </>
  )
}

export default Scales
