
export function scale (domain, range) {
  return function (n) {
    return ((n - domain[0]) / (domain[1] - domain[0])) * (range[1] - range[0]) + range[0]
  }
}
