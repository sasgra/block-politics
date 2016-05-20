import { element } from 'deku'

import { padding, labelWidth, labelBorder, height } from './constants.js'
import { setCurrent } from './actions.js'
import { scale } from './utils.js'
import Stacked from './components/stacked-bars.jsx'
import Combo from './components/combo.jsx'

function App ({ context, dispatch, props }) {
  const { values, min, max, selected, data, parties } = context
  const xScale = scale([min, max], [0, 100])
  return (
    <div>
      <Combo
        data={data}
        selected={selected}
        parties={parties}
        onChange={setCurrent(dispatch)}/>
      <h1>{parties[selected]}</h1>
      <hr />
      <h2>Before</h2>
      <Stacked values={data[selected].values.before} xScale={xScale} keys={data[selected].keys}/>
      <hr />
      <h2>After</h2>
      <Stacked values={data[selected].values.after} xScale={xScale} keys={data[selected].keys}/>
    </div>
  )
}

export default App
