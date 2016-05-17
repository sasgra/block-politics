var path = require('path')
var webpack = require('webpack')

module.exports = {
  entry: './src/boot.jsx',
  output: { path: __dirname, filename: 'build.js' },
  module: {
    loaders: [
      {
        test: /.jsx?$/,
        loader: 'babel',
        exclude: /node_modules/,
        query: {
          presets: ['es2015'],
          plugins: [
            ['transform-react-jsx', { pragma: 'element' }]
          ]
        }
      }
    ]
  }
}
