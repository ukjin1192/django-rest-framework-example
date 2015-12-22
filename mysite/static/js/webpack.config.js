'use strict';

var webpack = require('webpack');

module.exports = {
    entry: {
      bundle: './index.js',
      vendor: ['jquery', 'jquery.cookie', 'lodash'],
    },
    output: {
      path: './dist/',
      filename: '[name].js',
    },
    plugins: [
      new webpack.optimize.CommonsChunkPlugin(
        'vendor',
        'vendor.bundle.js'
      )
    ],
    resolve: {
      extensions: ['', '.js', '.es6']
    },
};
