
import { element, createApp } from 'deku'
import { createStore } from 'redux'

import initialState from './data.js'
import App from './app.jsx'
import { log } from './actions.js'
import reducer from './reducers.js'

let store = createStore(reducer, initialState)
let render = createApp(document.querySelector('.chart'), store.dispatch)

function reRender() {
  render(<App />, store.getState())
}

store.subscribe(reRender)
reRender()
