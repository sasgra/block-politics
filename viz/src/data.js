function rdm (n) {
  return Math.ceil(Math.random() * n) - (n * 0.5)
}

const seed = 200

const initialData = {
  selected: 'C',
  parties: {
    FP: '(FP) Feministiskt partiet?',
    S: '(S) Socialdemokratiska',
    M: '(M) Moderata samlingspartiet',
    MP: '(MP) Miljöpartiet',
    FP: '(FP) Feministiskt partiet?',
    SD: '(SD) Sverigedemokraterna',
    C: '(C) Centerpartiet',
    KD: '(KD) Kristdemokraterna'
  },
  data: {
    FP: {
        keys: ['M', 'SD',  'C',  'V',  'S'],
        values: [rdm(seed), rdm(seed), rdm(seed), rdm(seed), rdm(seed)]
      },
    S: {
      keys: ['SD', 'V', 'KD', 'C', 'MP', 'M'],
      values: [rdm(seed), rdm(seed), rdm(seed), rdm(seed), rdm(seed), rdm(seed)]
    },
    M: {
      keys: ['SD', 'V', 'MP', 'KD'],
      values: [rdm(seed), rdm(seed), rdm(seed), rdm(seed)]
    },
    MP: {
      keys: ['SD', 'V', 'KD'],
      values: [rdm(seed), rdm(seed), rdm(seed)]
    },
    FP: {
      keys: ['KD', 'MP'],
      values: [rdm(seed), rdm(seed)]
    },
    SD: {
      keys: ['KD', 'V'],
      values: [rdm(seed), rdm(seed)]
    },
    C: {
      keys: ['KD', 'M', 'V', 'SD', 'MP'],
      values: [-90, 90, rdm(seed), rdm(seed), rdm(seed)]
    },
    KD: {
      keys: ['V'],
      values: [rdm(seed)]
    }
  },
}

// percent based
initialData.max = (seed * 0.5)
initialData.min = -(seed * 0.5)

export default initialData
