import React, {useState} from 'react'
import {Link} from '@mui/material'
import {useParams, useSearchParams} from "react-router-dom";
import ScaleMenu from "./ScaleMenu";

const ExerciseMenu = (props) => {

  const defaultParams = {
    key: 'C-melodic',
    style: 'ABRSM',
    octaves: 2,
    separation: 'octave'
  }

  const [searchParams, setSearchParams] = useSearchParams(defaultParams)
  const [next_exercise, setNextExercise] = useState({})
  const params = useParams()

  return (
    <>
      <div style={{display: 'flex', justifyContent: 'center'}}>
        {
          <ScaleMenu
            renderScore={props.renderScore}
            searchParams={searchParams}
            setSearchParams={setSearchParams}
            setNextExercise={setNextExercise} />
        }
      </div>
      <div>
        Next: <Link href={next_exercise.url}>{next_exercise.name}</Link> →
      </div>
    </>
  )
}

export default ExerciseMenu
