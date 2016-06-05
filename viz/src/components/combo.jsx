import { element } from 'deku'

const Combo = ({ props: { style, parties, index, selected, data, onChange } }) =>
  <div class="combo" style={style}>
    Select one party:
    <select style={style} onChange={onChange}>{
        index
          .map(p => <option selected={selected === p} value={p}>{parties[p]}</option>)
      }
    </select>
  </div>

export default Combo
