import { element } from 'deku'
import { padding, labelWidth, labelBorder, height } from '../constants.js'

const { abs, round } = Math
const labels = (label) => label === 'FP' ? 'L' : label
const Axis = ({ context, dispatch, props }) => {
  const { values, keys, selected } = props

  return <div class={`axis`}>
      <ul>
      { values.map((d, i) =>
        <li key={i} class={`${keys[i] === selected ? 'selected' : ''}`}>
          {labels(keys[i])}<span>&nbsp;</span>
        </li>
      )}
      </ul>
    </div>
}

export default Axis
