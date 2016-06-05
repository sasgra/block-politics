import V from './v'
import S from './s'
import MP from './mp'
import C from './c'
import FP from './fp'
import KD from './kd'
import M from './m'
import SD from './sd'

export default {
  selected: 'C',
  index: ['V', 'S', 'MP', 'C', 'FP', 'KD', 'M', 'SD'],
  parties: {
    V: 'Vänsterpartiet',
    S: 'Socialdemokraterna',
    MP: 'Miljöpartiet',
    C: 'Centerpartiet',
    FP: 'Liberalerna',
    KD: 'Kristdemokraterna',
    M: 'Moderaterna',
    SD: 'Sverigedemokraterna'
  },
  colors: {
    V: '#AF0000',
    S: '#EE2020',
    MP: '#83CF39',
    C: '#009933',
    FP: '#6BB7EC',
    KD: '#231977',
    M: '#1B49DD',
    SD: '#DDDD00'
  },
  contrast: {
    V: 'white',
    S: 'white',
    MP: 'white',
    C: 'white',
    FP: 'white',
    KD: 'white',
    M: 'white',
    SD: 'black'
  },
  data: { FP, S, M, MP, SD, C, KD, V },
}
