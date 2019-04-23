const webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var path = require("path");


module.exports = env => {
  return {
    entry: {
      //upload: './src/upload.js',
      projectPage: './src/projectPage.jsx',
      indexPage: './src/indexPage.jsx',
      loginPage: './src/loginPage.jsx',
      signupPage: './src/signupPage.jsx',
      uploadPage: './src/uploadPage.jsx',
      //profilePage: './src/profilePage.jsx'
    },
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: [
            {
              loader: 'babel-loader',
              options: {
                presets: ['@babel/react']
              }
            }
          ]
        },
        {
          test: /\.css$/,
          use: ["style-loader", "css-loader"]
        },
        {
          test: /\.(gif|png|jpe?g|svg)$/i,
          use: [
            'file-loader',
            {
              loader: 'image-webpack-loader',
              options: {
                disable: true, // webpack@2.x and newer
              },
            },
          ],
        }
      ]
    },
    resolve: {
      extensions: ['*', '.js', '.jsx']
    },
    output: {
      path: path.resolve('../static/bundles/'),
      publicPath: '../static/bundles/',
      filename: '[name].bundle.js'
    },
    plugins: [
      //new webpack.HotModuleReplacementPlugin(),
      new webpack.DefinePlugin({
        'process.env': {
          API_URL: JSON.stringify(env.API_URL)
        }
      }),
      new BundleTracker({filename: '../../webpack-stats.json'}),
      // new webpack.DefinePlugin({
      //   API_URL: JSON.stringify(process.env.API_URL)
      // })
    ]
  };
  // devServer: {
  //   contentBase: './dist'
  // }
};
