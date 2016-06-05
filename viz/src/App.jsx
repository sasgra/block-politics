import { element } from 'deku'

import { padding, labelWidth, labelBorder, height } from './constants'
import { setCurrent } from './actions'
import { scale } from './utils'
import Stacked from './components/stacked-bars'
import Combo from './components/combo'
import Info from './components/info'

function App ({ context: { index, selected, data, parties, colors, contrast }, dispatch, props, path }) {

  let
    xScale = (v) => v * 100,
    xScale50 = (v) => 50 + v * 50,
    { keys, values, text } = data[selected]

  return (
    <div>
      <Combo
        style={
           `background-color: ${colors[selected]};` +
           `color: ${contrast[selected]};` +
           `border-color: ${contrast[selected]};` +
           `border-opacity: 0.5;`
        }
        index={index}
        data={data}
        selected={selected}
        parties={parties}
        onChange={setCurrent(dispatch)}/>
      <h2 class="title">Röstning sedan valet</h2>
      <Stacked colors={colors} selected={selected} index={index} values={values.after} xScale={xScale50} keys={keys}/>
      <Info info={text}/>
      <h2 class="title">Röstning under förra mandatperioden</h2>
      <Stacked colors={colors} selected={selected} index={index} values={values.before} xScale={xScale50} keys={keys}/>
    </div>
  )
}

export default App
