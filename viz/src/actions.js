

export function setCurrent (dispatch) {
  return event => {
    dispatch({
      type: 'SELECT_PARTY',
      payload: event.target.value
    })
  }
}
