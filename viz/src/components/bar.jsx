import { element } from 'deku'
import { padding, labelWidth, labelBorder, height } from '../constants.js'

const { abs, round } = Math
const tofixed = (val, n = 1) => parseFloat(val.toFixed(n))

const Bar = ({ context, dispatch, props }) => {
  const { xScale, index, party, votes, type, align } = props
  const isNull = votes == null
  const nullClass = isNull ? 'bar-empty' : ''
  const isPositive = votes > 0
  const scaledValue = xScale(abs(votes))
  const floatVal = type === 'value' ? align : 'none'
  const width = type === 'value' ? `${scaledValue}%` : '100%'
  const title = type === 'value' ? `${round(scaledValue)} % ${isPositive ? 'med' : 'mot'} ${party} (${votes})` : null

  return <div class={`bar bar-${type} ${nullClass}`} key={index} title={title} data-value={scaledValue} data-votes={votes} style={
     `float: ${floatVal};` +
     `width: ${width};`
    }>{
      type === 'value'
      ? ''
      : isNull ? '…' : `${tofixed(scaledValue)} % ${isPositive ? 'med' : 'mot'} ${party}`
    }</div>
}

export default Bar
