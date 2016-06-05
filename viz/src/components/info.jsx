import { element } from 'deku'
import { padding, labelWidth, labelBorder, height } from '../constants.js'

const Info = ({ context, dispatch, props }) => {
  const { info } = props

  return <div class={`info`}>
      <ul>
      { info.map((d, i) =>
        <li key={i}>{ d }</li>
      )}
      </ul>
    </div>
}

export default Info
