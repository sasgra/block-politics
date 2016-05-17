import { element } from 'deku'

import { padding, labelWidth, labelBorder, height } from './constants.js'
import { setCurrent } from './actions.js'
import { scale } from './utils.js'
import Bar from './components/bar.jsx'

const EmptyBar = ({ props: { party, percent } }) =>
  <div class="bar bar-invisible" style={`width: 100%; height: ${height}px`}>
    <div class="value" style={`width:0`}></div>
    <div class="label">{party} with {Math.abs(percent)}%</div>
  </div>

/*
<div class="bars bars-negative" style="width:100%">
{ data[selected].values.map((d, i) =>
  d < 0
  ? <Bar party={data[selected].keys[i]} votes={d} index={i} xScale={xScale} />
  : <EmptyBar percent={d} party={data[selected].keys[i]} />
)}
</div>
<div class="bars bars-positive" style="width:100%">
{ data[selected].values.map((d, i) =>
  d > 0
  ? <Bar party={data[selected].keys[i]} votes={d} index={i} xScale={xScale} />
  : <EmptyBar percent={d} party={data[selected].keys[i]} />
)}
</div>
*/

function App ({ context, dispatch, props }) {
  const { values, min, max, selected, data, parties } = context
  const xScale = scale([min, max], [0, 100])
  return (
    <div>
      <select onChange={setCurrent(dispatch)}>{
          Object.keys(data).map(p => <option selected={selected === p} value={p}>{parties[p]}</option>)
        }
      </select>
      <hr />
      <h1>{parties[selected]}</h1>
      <div class="bar-group">
        <div class="bars bars-negative" style="width:100%">
        { data[selected].values.map((d, i) =>
          d < 0
          ? <Bar party={data[selected].keys[i]} align={'right'} type={'value'} votes={d} index={i} xScale={xScale} />
          : <Bar party={data[selected].keys[i]} align={'right'} type={'label'} votes={d} index={i} xScale={xScale} />
        )}
        </div>
        <div class="bars bars-positive" style="width:100%">
        { data[selected].values.map((d, i) =>
          d > 0
          ? <Bar party={data[selected].keys[i]} align={'left'} type={'value'} votes={d} index={i} xScale={xScale} />
          : <Bar party={data[selected].keys[i]} align={'left'} type={'label'} votes={d} index={i} xScale={xScale} />
        )}
        </div>
      </div>
    </div>
  )
}

export default App
