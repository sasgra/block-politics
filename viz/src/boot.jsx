
import { element, createApp } from 'deku'
import { createStore } from 'redux'

import initialState from './data'
import App from './app'
import { log } from './actions'
import reducer from './reducers'

let store = createStore(reducer, initialState)
let render = createApp(document.querySelector('.chart'), store.dispatch)

function reRender() {
  render(<App />, store.getState())
}

store.subscribe(reRender)
reRender()
