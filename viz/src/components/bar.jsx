import { element } from 'deku'
import { padding, labelWidth, labelBorder, height } from '../constants.js'

// const EmptyBar = ({ props: { party, percent } }) =>
//   <div class="bar bar-invisible" style={`width: 100%; height: ${height}px`}>
//     <div class="value" style={`width:0`}></div>
//     <div class="label">{party} with {Math.abs(percent)}%</div>
//   </div>

const Bar = ({ context, dispatch, props }) => {
  const { xScale, index, party, votes, visible } = props
  const isPositive = votes > 0
  const isVisible = visible ? 'visible' : 'invisible'
  const scaledValue = xScale(Math.abs(votes))
  const floatVal = isPositive ? 'left' : 'right'
  const width = visible ? `calc(${scaledValue}%)` : 0

  return <div class={`bar bar-${isVisible}`} style={
      `float: ${floatVal};` +
      // `margin-bottom: ${padding}px;` +
      // `top: ${(height * index)}px;` +
      `width: 100%;`
    }>
    { visible
      ? <div class="label"></div>
      : <div class="label">{party} with {Math.abs(votes)}%</div>
    }
    <div class="value" title={votes} key={index} style={
     `float: ${floatVal};` +
     `width: ${width};` +
     `height: ${height}px`
    //  `padding: ${padding}px;`
   }></div>
  </div>
}

export default Bar
