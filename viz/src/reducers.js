import { combineReducers } from 'redux'
import initialState from './data.js'

function rdmParty () {
  const parties = Object.keys(initialState.data)
  return parties[Math.floor(Math.random() * parties.length)]
}

function selectedReducer (state, { type, payload }) {
  switch (type) {
    case 'SELECT_PARTY':
      return payload

    case 'CLICKED':
      const sel = rdmParty()
      return sel

    default: return state
  }
}

// receives full state, returns only data
function dataReducer (state, { type, payload }) {
  // console.log(state.data)
  switch (type) {
    // case 'CLICKED':
    //   const selected = state.selected
    //   const data = state.data
    //   const nuState = Object.assign({}, data, { [selected]: data[selected] })
    //   return Object.assign({}, data, { [selected]: data[selected] })

    default: return state.data
  }

  return state.data
}

export default function(state = initialState, action) {
  // prior updates
  const selected = selectedReducer(state.selected, action)
  const updatedState = Object.assign({}, state, { selected })
  // composing result
  return Object.assign({}, state, {
    selected,
    // we need to update with the current selected
    data: dataReducer(updatedState, action)
  })
}
