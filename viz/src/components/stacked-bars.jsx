import { element } from 'deku'
import Bar from './bar.jsx'

const Stacked = ({ props: { values, keys, xScale } }) =>
  <div class="bar-group">
    <div class="bars bars-negative" style="width:100%">
    { values.map((d, i) =>
      <Bar
        party={keys[i]}
        align={'right'} type={d < 0 ? 'value' : 'label'}
        votes={d} index={i} xScale={xScale} />
    )}
    </div>
    <div class="bars bars-positive" style="width:100%">
    { values.map((d, i) =>
      <Bar
        party={keys[i]}
        align={'left'}
        type={d > 0 ? 'value' : 'label'}
        votes={d} index={i} xScale={xScale} />
    )}
    </div>
  </div>

export default Stacked
