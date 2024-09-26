import {FormControl, InputLabel, MenuItem, Select} from "@mui/material";
import React, {useEffect, useState} from "react";
import axios from "axios";
import KeySelection from "./KeySelection";

export default function ScaleMenu(props) {
  const [tonic, setTonic] = useState(getTonic(props.searchParams.get('key')))
  const [quality, setQuality] = useState(getQuality(props.searchParams.get('key')))

  const [style, setStyle] = useState(props.searchParams.get('style'))
  const [octaves, setOctaves] = useState(props.searchParams.get('octaves'))
  const [separation, setSeparation] = useState(props.searchParams.get('separation'))

  function getTonic(key) {
    console.log('Got ', key)
    return key.split('-')[0].replace('#', 's')
  }

  function getQuality(key) {
    return key.split('-')[1] || 'major'
  }

  useEffect(() => {
    props.setSearchParams({
      key: tonic + '-' + quality,
      style: style,
      octaves: octaves,
      separation: separation
    })

    function getScale() {
      const url = 'http://127.0.0.1:8000/api/scale'
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
        if ('pdf' in data) {
          console.log('Rendering PDF...')
          props.renderScore(data.pdf, true)
        } else {
          props.renderScore(data.xml)
        }
        if (data.next_name) {
          props.setNextExercise({
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
      <KeySelection tonic={tonic} setTonic={setTonic}
                    quality={quality} setQuality={setQuality}/>
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
    </>
  )
}