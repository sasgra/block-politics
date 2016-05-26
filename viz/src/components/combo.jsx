import { element } from 'deku'

const Combo = ({ props: { parties, index, selected, data, onChange } }) =>
  <select onChange={onChange}>{
      index
        .map(p => <option selected={selected === p} value={p}>{parties[p]}</option>)
    }
  </select>

export default Combo
