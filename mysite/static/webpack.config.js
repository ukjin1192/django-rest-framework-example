'use strict';

var webpack = require('webpack');
require('es6-promise').polyfill();

var productionMode = JSON.parse(process.env.production_mode || '0');

module.exports = {
  entry: {
    bundle: './index.js',
    vendor: [
      'jquery', 
      'jquery.cookie', 
      'lodash',
      'bootstrap-webpack'
    ]
  },
  output: {
    path: './dist/',
    filename: '[name].js',
    publicPath: '/static/dist/'
  },
  plugins: productionMode ? [
    // Use jquery variable globally
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery"
    }),
    // Separate main file with vendors
    new webpack.optimize.CommonsChunkPlugin(
      'vendor',
      'vendor.bundle.js'
    ),
    // Minify JS files
    new webpack.optimize.UglifyJsPlugin({
      minimize: true
    })
  ] : [
    // Use jquery variable globally
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery"
    }),
    // Separate main file with vendors
    new webpack.optimize.CommonsChunkPlugin(
      'vendor',
      'vendor.bundle.js'
    )
  ],
  resolve: {
    extensions: ['', '.js', '.es6']
  },
  module: {
    loaders: [
      {
        test: /\.scss$/,
        // 1. Convert SCSS to CSS
        // 2. Insert CSS to <style> tag
        loader: "style-loader!css-loader!sass-loader"
      },
      {
        test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/, 
        loader: 'url?limit=10000&mimetype=application/font-woff'
      },
      {
        test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, 
        loader: 'url?limit=10000&mimetype=application/octet-stream'
      },
      {
        test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, 
        loader: 'file'
      },
      {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url?limit=10000&mimetype=image/svg+xml'
      }
    ]
  }
};
