import React, {useEffect, useState} from 'react'
import {FormControl, InputLabel, MenuItem, Select} from '@mui/material'
import {Link, useParams, useSearchParams} from "react-router-dom";
import axios from "axios";
import KeySelection from "./KeySelection";

const ExerciseMenu = (props) => {
  function getTonic(key) {
    console.log('Got ', key)
    return key.split('-')[0].replace('#', 's')
  }

  function getQuality(key) {
    return key.split('-')[1] || 'major'
  }

  const defaultChordParams = {
    style: 'ABRSM',
    octaves: 2
  }
  const defaultScaleParams = {
    style: 'ABRSM',
    octaves: 2,
    separation: 'octave'
  }

  const defaultParams = {
    scales: defaultScaleParams,
    chords: defaultChordParams,
    arpeggios: defaultChordParams,
  }

  const octaveOptions = [
    {value: 1, name: '1'},
    {value: 2, name: '2'},
    {value: 3, name: '3'},
    {value: 4, name: '4'},
  ]

  const scaleOptions = [
    {
      optionName: 'style',
      displayName: 'Style',
      minWidth: 120,
      values: [
        {value: 'ABRSM', name: 'ABRSM'},
        {value: 'grand', name: 'Grand'},
        {value: 'Hanon', name: 'Hanon'},
        {value: 'Jonas', name: 'Alberto Jonas'},
        {value: 'Cooke', name: 'Cooke'},
      ]
    },
    {
      optionName: 'octaves',
      displayName: 'Octaves',
      minWidth: 120,
      values: octaveOptions
    },
    {
      optionName: 'separation',
      displayName: 'Separation',
      minWidth: 120,
      values: [
        {value: 'octave', name: 'Octave'},
        {value: 'third', name: 'Third'},
        {value: 'tenth', name: 'Tenth'},
        {value: 'sixth', name: 'Sixth'},
      ]
    }
  ]

  const chordOptions = [
    {
      optionName: 'style',
      displayName: 'Style',
      minWidth: 120,
      values: [
        {value: 'ABRSM', name: 'ABRSM'},
        {value: 'Hanon', name: 'Hanon'},
        {value: 'Jonas', name: 'Alberto Jonas'},
        {value: 'Rachmaninoff', name: 'Rachmaninoff (Common tone series)'},
      ]
    },
    {
      optionName: 'octaves',
      displayName: 'Octaves',
      minWidth: 120,
      values: octaveOptions
    },
  ]

  const options = {
    scales: scaleOptions,
    arpeggios: chordOptions,
    chords: chordOptions,
  }

  const {exercise} = useParams()
  const [searchParams, setSearchParams] = useSearchParams(defaultParams[exercise])
  const [tonic, setTonic] = useState(getTonic(searchParams.get('key')))
  const [quality, setQuality] = useState(getQuality(searchParams.get('key')))
  const [optionsParams, setOptionsParams] = useState(defaultParams[exercise])
  const [nextExercise, setNextExercise] = useState({})
  const {renderScore} = props

  useEffect(() => {
    console.log('Setting search params:', optionsParams)
    setSearchParams({
      key: tonic + '-' + quality,
      ...optionsParams,
    })

    function getExercise() {
      const url = 'http://127.0.0.1:8000/api/' + exercise
      axios.get(url, {
        params: {
          tonic: tonic,
          quality: quality,
          ...optionsParams,
        }
      }).then(response => {
        let data = response.data
        console.log(data)
        if ('pdf' in data) {
          console.log('Rendering PDF...')
          renderScore(data.pdf, true)
        } else {
          renderScore(data.xml)
        }
        if (data.next_name) {
          setNextExercise({
            'name': data.next_name,
            'url': data.next_url,
          })
        }
      })
    }

    console.log('Rendering', exercise, 'exercise in', tonic, quality, '...')
    getExercise()
  }, [tonic, quality, optionsParams, exercise])

  console.log('Exercise:', exercise)
  const exerciseOptions = options[exercise]

  const setOptionsFromUrl = (newUrl) => {
    let newParams = new URLSearchParams(newUrl.split('?')[1])
    console.log('New params: ', newParams)

    console.log('Setting options from URL params:', newParams)
    newParams.forEach((value, key) => {
      if (key === 'key') {
        setTonic(getTonic(value))
        setQuality(getQuality(value))
        newParams['key'] = value
        console.log('Setting key to ', value)
      } else {
        newParams[key] = value
      }
    })
    setOptionsParams(newParams)
  }

  return (
    <>
      <div style={{display: 'flex', justifyContent: 'center'}}>
        <KeySelection tonic={tonic} setTonic={setTonic}
                      quality={quality} setQuality={setQuality} exercise={exercise}/>
        {
          exerciseOptions.map((option) =>
            <FormControl sx={{m: 1, minWidth: option.minWidth}}>
              <InputLabel id={option.optionName + '-label'}>{option.displayName}</InputLabel>
              <Select
                labelId={option.optionName + '-label'}
                id={option.optionName}
                value={optionsParams[option.optionName]}
                label={option.displayName}
                onChange={(e) => {
                  console.log('Setting', option.optionName, 'to', e.target.value)
                  console.log(optionsParams)
                  setOptionsParams({
                    ...optionsParams,
                    [option.optionName]: e.target.value,
                  })
                }}
              >
                {
                  option.values.map((optionValue) =>
                    <MenuItem value={optionValue.value}>{optionValue.name}</MenuItem>
                  )
                }
              </Select>
            </FormControl>
          )}
      </div>
      {
        nextExercise &&
        <div>
          Next: <Link onClick={() => setOptionsFromUrl(nextExercise.url)} to={nextExercise.url}>{nextExercise.name}</Link> →
        </div>
      }
    </>
  )
}

export default ExerciseMenu
