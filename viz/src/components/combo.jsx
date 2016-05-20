import { element } from 'deku'

const Combo = ({ props: { parties, selected, data, onChange } }) =>
  <select onChange={onChange}>{
      Object.keys(data)
        .map(p => <option selected={selected === p} value={p}>{parties[p]}</option>)
    }
  </select>

export default Combo
