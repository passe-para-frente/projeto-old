const path = require('path');

module.exports = {
  entry: './landing/static/js/init.js',
  mode: 'production',
  output: {
    filename: 'main.min.js',
    path: path.resolve(__dirname, 'passe_pra_frente/static/js/')
  }
};
