import { element } from 'deku'
import Bar from './bar'
import Axis from './axis'

const Stacked = ({ props: { selected, values, keys, xScale, colors } }) =>
  <div class="bar-group">
    <Axis selected={selected} values={values} keys={keys} />
    <div class="bars bars-negative" style="width:100%">
    { values.map((d, i) =>
      <Bar
        color={colors[keys[i]]}
        party={keys[i]}
        align={'right'} type={d < 0 ? 'value' : 'label'}
        votes={d} index={i} xScale={xScale} />
    )}
    </div>
    <div class="bars bars-positive" style="width:100%">
    { values.map((d, i) =>
      <Bar
        color={colors[keys[i]]}
        party={keys[i]}
        align={'left'}
        type={d > 0 ? 'value' : 'label'}
        votes={d} index={i} xScale={xScale} />
    )}
    </div>
  </div>

export default Stacked
