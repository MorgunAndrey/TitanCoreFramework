var path = require('path');

module.exports = {
  mode: 'development', // Режим разработки
  // mode: 'production',
  entry: './components/test/app.js', // Точка входа
  output: {
    path: path.resolve(__dirname, './static/dist'),
    filename: 'test.js'
  },
  module: {
    rules: [
      {
        test: /\.(ts|js)x?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react']
          }
        }
      },
      {
        test: /\.(sass|less|css|scss)$/,
        use: ["style-loader", "css-loader", 'sass-loader'],
      },
    ]
  }
}