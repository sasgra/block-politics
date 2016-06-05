import { element } from 'deku'
import { padding, labelWidth, labelBorder, height } from '../constants.js'

const { abs, round } = Math
const tofixed = (val, n = 1) => parseFloat(val.toFixed(n))
const replaceAll = (target, search, replacement) => target.split(search).join(replacement)
const pathToId = (p) => replaceAll(p, '.', '-')

const render = ({ context, dispatch, props, path }) => {
  const { xScale, index, party, votes, type, align } = props
  const isNull = votes == null
  const nullClass = isNull ? 'bar-empty' : ''
  const isPositive = votes > 0
  const scaledValue = xScale(abs(votes))
  const floatVal = type === 'value' ? align : 'none'
  const width = type === 'value' ? `${scaledValue}%` : '100%'
  const title = type === 'value' ? `${round(scaledValue)} % ${isPositive ? 'med' : 'mot'} ${party} (${votes})` : null
  const id = pathToId(path)

  return <div id={id} class={`bar bar-${type} ${nullClass}`} title={title} key={index} data-value={scaledValue} data-votes={votes} style={
     `float: ${floatVal};` +
     `width: ${width};`
    }>{
      type === 'value'
      ? ''
      : isNull ? ' ' : `${round(scaledValue)} % ${isPositive ? 'med' : 'mot'} ${party}`
    }</div>
}
// : isNull ? ' ' : `${tofixed(scaledValue)} % ${isPositive ? 'med' : 'mot'} ${party}`

function onUpdate ({ path }) {
  const el = document.getElementById(pathToId(path))
  el.classList.add("update")
}

export default {
  render,
  onUpdate
}
