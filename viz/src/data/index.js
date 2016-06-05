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
  data: { FP, S, M, MP, SD, C, KD, V },
}
