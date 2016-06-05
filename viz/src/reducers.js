import { combineReducers } from 'redux'
import initialState from './data'

function selectedReducer (state, { type, payload }) {
  switch (type) {
    case 'SELECT_PARTY':
      return payload

    default: return state
  }
}

// receives full state, returns only data
function dataReducer (state, { type, payload }) {
  switch (type) {
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
