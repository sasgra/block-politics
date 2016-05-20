import { element } from 'deku'
import { padding, labelWidth, labelBorder, height } from '../constants.js'

// const EmptyBar = ({ props: { party, percent } }) =>
//   <div class="bar bar-invisible" style={`width: 100%; height: ${height}px`}>
//     <div class="value" style={`width:0`}></div>
//     <div class="label">{party} with {Math.abs(percent)}%</div>
//   </div>

const { abs, round } = Math

const Bar = ({ context, dispatch, props }) => {
  const { xScale, index, party, votes, type, align } = props
  const isPositive = votes > 0
  const scaledValue = xScale(Math.abs(votes))
  const floatVal = type === 'value' ? align : 'none'
  const width = type === 'value' ? `calc(${scaledValue}%)` : '100%'

  return <div class={`bar bar-${type}`} key={index} style={
     `float: ${floatVal};` +
     `width: ${width};`
    }>{
      type === 'value'
      ? ''
      : `${round(abs(xScale(votes)))}% ${isPositive ? 'with' : 'against'} ${party}`
    }</div>
}

export default Bar
