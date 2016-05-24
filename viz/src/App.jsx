import { element as $ } from 'deku'
// const {
//   div,
//   span,
//   hr,
//   h1,
//   h2
// } = require('hyperscript-helpers')($)

import { padding, labelWidth, labelBorder, height } from './constants.js'
import { setCurrent } from './actions.js'
import { scale } from './utils.js'
import Stacked from './components/stacked-bars.jsx'
import Combo from './components/combo.jsx'

function App ({ context: { min, max, index, selected, data, parties }, dispatch, props, path }) {

  let
    // xScale = scale([min, max], [0, 100]),
    xScale = (v) => v * 100,
    keys = data[selected].keys,
    values = data[selected].values

  return $('div', {},
    [
      $(Combo, { data, selected, index, parties, onChange: setCurrent(dispatch) }),
      $('h1', {}, parties[selected]),
      $('hr'),
      $('h2', {}, 'Before'),
      $(Stacked, { values: values.before, xScale, keys }),
      $('hr'),
      $('h2', {}, 'After'),
      $(Stacked, { values: values.after, xScale, keys }),
    ]
  )
  // return (
  //   <div>
  //     <Combo
  //       data={data}
  //       selected={selected}
  //       parties={parties}
  //       onChange={setCurrent(dispatch)}/>
  //     <h1>{parties[selected]}</h1>
  //     <hr />
  //     <h2>Before</h2>
  //     <Stacked values={data[selected].values.before} xScale={xScale} keys={data[selected].keys}/>
  //     <hr />
  //     <h2>After</h2>
  //     <Stacked values={data[selected].values.after} xScale={xScale} keys={data[selected].keys}/>
  //   </div>
  // )
}

export default App
